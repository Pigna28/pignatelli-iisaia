# Tokenizacion

Before we plug text into neural networks we have to decide how we're going to represent this text and how we're going to feed it in. The way our technology works for these neural nets is that they expect a one-dimensional sequence of symbols and they want a finite set of symbols that are possible. So we have to decide what are the symbols and then we have to represent our data as a one-dimensional sequence of those symbols.

Right now what we have is a one-dimensional sequence of text. It starts here and it goes here and then it comes here, etc. So this is a one-dimensional sequence even though on my monitor of course it's laid out in a two-dimensional way, but it goes from left to right and top to bottom. So it's a one-dimensional sequence of text.

Now this being computers, of course there's an underlying representation here. So if I do what's called UTF-8 encode this text then I can get the raw bits that correspond to this text in the computer. It turns out that for example this very first bar here is the first eight bits as an example.

So what is this thing? This is a representation that we are looking for in a certain sense. We have exactly two possible symbols, zero and one, and we have a very long sequence of it. Now as it turns out, this sequence length is actually going to be a very finite and precious resource in our neural network and we actually don't want extremely long sequences of just two symbols. Instead what we want is we want to trade off this symbol size of this vocabulary as we call it and the resulting sequence length. So we don't want just two symbols and extremely long sequences; we're going to want more symbols and shorter sequences.

## De bits a bytes

One naive way of compressing or decreasing the length of our sequence here is to basically consider some group of consecutive bits, for example eight bits, and group them into a single what's called byte. Because these bits are either on or off, if we take a group of eight of them there turns out to be only 256 possible combinations of how these bits could be on or off. Therefore we can re-represent this sequence into a sequence of bytes instead. This sequence of bytes will be eight times shorter but now we have 256 possible symbols. So every number here goes from 0 to 255. I really encourage you to think of these not as numbers but as unique IDs or like unique symbols.

## Byte Pair Encoding

In production for state-of-the-art language models you actually want to go even beyond this. You want to continue to shrink the length of the sequence because again it is a precious resource, in return for more symbols in your vocabulary. The way this is done is by running what's called the Byte Pair Encoding algorithm. The way this works is we're basically looking for consecutive bytes or symbols that are very common. For example it turns out that the sequence 116 followed by 32 is quite common and occurs very frequently. So what we're going to do is we're going to group this pair into a new symbol. We're going to mint a symbol with an ID 256 and we're going to rewrite every single pair 116, 32 with this new symbol. Then we can iterate this algorithm as many times as we wish and each time when we mint a new symbol we're decreasing the length and we're increasing the symbol size.

In practice it turns out that a pretty good setting of the vocabulary size turns out to be about 100,000 possible symbols. In particular GPT-4 uses 100,277 symbols.

This process of converting from raw text into these symbols, or as we call them tokens, is the process called tokenization.

## Tik Tokenizer

Let's now take a look at how GPT-4 performs tokenization, going from text to tokens and from tokens back to text and what this actually looks like. One website I like to use to explore these token representations is called Tik Tokenizer. Come here to the dropdown and select CL100K base which is the GPT-4 base model tokenizer. Here on the left you can put in text and it shows you the tokenization of that text.

For example, "hello world" turns out to be exactly two tokens: the token "hello" which is the token with ID 15339, and the token " world" that is the token 11917. So "hello space world" -- now if I was to join these two for example, I'm going to get again two tokens but it's the token "h" followed by the token "lloworld" without the "h". If I put in two spaces here between hello and world, it's again a different tokenization. There's a new token 220 here.

You can play with this and see what happens here. Also keep in mind this is case sensitive, so if this is a capital H it is something else, or if it's "Hello World" then actually this ends up being three tokens instead of just two tokens.

So you can play with this and get an intuitive sense of what these tokens work like. We're actually going to loop around to tokenization a bit later in the video. For now I just wanted to show you the website and I wanted to show you that this text basically at the end of the day, for example if I take one line here, this is what GPT-4 will see it as. This text will be a sequence of length 62. This is the sequence here and this is how the chunks of text correspond to these symbols. Again there's 100,277 possible symbols and we now have one-dimensional sequences of those symbols.

So what I've done now is I've taken this sequence of text that we have here in the data set and I have re-represented it using our tokenizer into a sequence of tokens. For example when we go back to the FineWeb data set they mentioned that not only is this 44 terabytes of disk space, but this is about a 15 trillion token sequence in this data set. Again keep in mind that all of these represent little text chunks, they're all just like atoms of these sequences, and the numbers here don't make any sense, they're just unique IDs.
