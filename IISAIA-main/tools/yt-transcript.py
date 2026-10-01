"""Extract the full transcript of a YouTube video.

Usage:
    python tools/yt-transcript.py <youtube_url_or_id> [options]

Options:
    -o, --output FILE    Write transcript to file instead of stdout
    -l, --lang LANG      Preferred language code (default: es, fallback: en, then any)
    --timestamps         Include timestamps in output
    --fmt FORMAT         Output format: text (default), json, srt
"""

import argparse
import json
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter, TextFormatter, JSONFormatter


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from a YouTube URL or return as-is if already an ID."""
    patterns = [
        r"(?:v=|\/v\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    print(f"Error: could not extract video ID from '{url_or_id}'", file=sys.stderr)
    sys.exit(1)


def fetch_transcript(video_id: str, lang: str) -> list[dict]:
    """Fetch transcript, trying preferred language first, then fallbacks."""
    ytt_api = YouTubeTranscriptApi()

    # Build language priority list
    langs = [lang]
    if lang != "en":
        langs.append("en")

    try:
        transcript = ytt_api.fetch(video_id, languages=langs)
        return transcript.snippets
    except Exception:
        pass

    # Fallback: list available transcripts and pick the first one
    try:
        transcript_list = ytt_api.list(video_id)
        available = list(transcript_list)
        if not available:
            print("Error: no transcripts available for this video.", file=sys.stderr)
            sys.exit(1)
        print(
            f"Preferred language '{lang}' not found. "
            f"Using '{available[0].language}' ({available[0].language_code}).",
            file=sys.stderr,
        )
        transcript = ytt_api.fetch(video_id, languages=[available[0].language_code])
        return transcript.snippets
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_output(snippets: list, fmt: str, timestamps: bool) -> str:
    """Format transcript snippets into the requested output format."""
    if fmt == "json":
        data = [{"text": s.text, "start": s.start, "duration": s.duration} for s in snippets]
        return json.dumps(data, ensure_ascii=False, indent=2)

    if fmt == "srt":
        formatter = SRTFormatter()
        return formatter.format_transcript(snippets)

    # Plain text
    if timestamps:
        lines = [f"[{format_timestamp(s.start)}] {s.text}" for s in snippets]
        return "\n".join(lines)

    return "\n".join(s.text for s in snippets)


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video transcript")
    parser.add_argument("video", help="YouTube URL or video ID")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-l", "--lang", default="es", help="Preferred language (default: es)")
    parser.add_argument("--timestamps", action="store_true", help="Include timestamps")
    parser.add_argument(
        "--fmt",
        choices=["text", "json", "srt"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    print(f"Fetching transcript for video: {video_id}", file=sys.stderr)

    snippets = fetch_transcript(video_id, args.lang)
    output = format_output(snippets, args.fmt, args.timestamps)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Transcript saved to {args.output}", file=sys.stderr)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
