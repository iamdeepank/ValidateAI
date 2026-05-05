from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date


class Filters(BaseModel):
    country: Optional[str] = Field(default=None)
    date_from: Optional[date] = Field(default=None)
    date_to: Optional[date] = Field(default=None)

    # @field_validator("date_to")
    # def validate_date_range(cls, v, values):
    #     if v and values.get("date_from") and v < values["date_from"]:
    #         raise ValueError("date_to must be >= date_from")
    #     return v


class ValidationRequest(BaseModel):
    filters: Filters
    metrics: List[str] = Field(..., min_items=1)
    validation_type: str = Field(...)

    class Config:
        extra = "forbid"              # prevent hallucinated fields
        validate_assignment = True   # enforce runtime safety