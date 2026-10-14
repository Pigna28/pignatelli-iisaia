from datetime import datetime, timezone
from typing import Annotated, Literal
from urllib.parse import urlsplit

from pydantic import Field, field_validator, model_validator

from .schemas import Input, Text

Status = Literal["in_progress", "passed", "failed"]
Notes = Annotated[str, Field(strict=True, max_length=10000)]


class ThreadInput(Input):
    title: Text
    description: Notes = ""


class StepInput(Input):
    title: Text
    notes: Notes = ""
    status: Status = "in_progress"
    metric: Text | None = None
    measured_value: Annotated[float, Field(strict=True, allow_inf_nan=False)] | None = None
    unit: Text | None = None
    measured_at: datetime | None = None

    @field_validator("measured_at", mode="before")
    @classmethod
    def date_string(cls, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Usar fecha ISO 8601 con zona horaria")
        return value

    @field_validator("measured_at")
    @classmethod
    def utc(cls, value):
        if value is not None:
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError("La fecha requiere zona horaria")
            return value.astimezone(timezone.utc)
        return value

    @model_validator(mode="after")
    def measurement_complete(self):
        fields = (self.metric, self.measured_value, self.unit)
        if any(value is not None for value in fields) and not all(
            value is not None for value in fields
        ):
            raise ValueError("La medición requiere métrica, valor y unidad juntos")
        return self


class LinkInput(Input):
    name: Text
    url: Annotated[str, Field(strict=True, max_length=2048)]

    @field_validator("url")
    @classmethod
    def safe_url(cls, value):
        parsed = urlsplit(value)
        if (
            parsed.scheme not in {"https", "http"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or any(ord(c) <= 32 for c in value)
        ):
            raise ValueError(
                "Usar un enlace HT../pignatelli-iisaia/tp_final/HTTPS sin credenciales ni espacios"
            )
        return value
