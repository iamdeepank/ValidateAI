from email.policy import default

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date


class Filters(BaseModel):
    country: Optional[str] = Field(default=None)
    team: Optional[str] = Field(default=None)
    role: Optional[str] = Field(default=None)

class ValidationRequest(BaseModel):
    filters: Filters =Field(description="filters of the report.",default="No Filter")
    metrics: List[str] =Field(description="metrics of the report.",default=None)
    dashboard: str =Field(description="Name of the dashboard.",default=None)
    screen_name: str =Field(description="Name of the dashboard screen.",default=None)
    environments: List[str] =Field(description="environment of dashboard",default=None)

    class Config:
        extra = "forbid"              # prevent hallucinated fields
        validate_assignment = True   # enforce runtime safety