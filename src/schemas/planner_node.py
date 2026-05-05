from pydantic import BaseModel, Field
from typing import List, Literal


AllowedStep = Literal[
    "extract_ui_data",
    "generate_sql",
    "execute_query",
    "compare_results"
]


class ExecutionPlan(BaseModel):
    steps: List[AllowedStep] = Field(..., min_items=1)

    class Config:
        extra = "forbid"
        validate_assignment = True
