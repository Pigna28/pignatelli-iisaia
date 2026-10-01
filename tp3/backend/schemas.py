from datetime import date, datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator

Macro = Literal["Tx", "Rx", "PLL"]
Text = Annotated[str, Field(strict=True, min_length=1, max_length=120)]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ChipInput(Input):
    part_number: Text
    board: Text
    assembled_at: date | None = None

    @field_validator("assembled_at", mode="before")
    @classmethod
    def date_only(cls, value):
        if value is None:
            raise ValueError("Omitir assembled_at si no se conoce la fecha")
        if not isinstance(value, str) or len(value) != 10:
            raise ValueError("Usar fecha YYYY-MM-DD")
        return value


class TestInput(Input):
    metric: Text
    measured_value: Annotated[float, Field(strict=True, allow_inf_nan=False)]
    unit: Text
    passed: StrictBool
    measured_at: datetime | None = None

    @field_validator("measured_at", mode="before")
    @classmethod
    def timestamp_string(cls, value):
        if not isinstance(value, str):
            raise ValueError("Usar timestamp ISO 8601 con zona horaria u omitir el campo")
        return value

    @field_validator("measured_at")
    @classmethod
    def with_timezone(cls, value):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("measured_at requiere zona horaria")
        return value.astimezone(timezone.utc)
