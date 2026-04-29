from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.schemas.input_schema import ValidationRequest
from app.schemas.plan_schema import ExecutionPlan


class AgentState(BaseModel):
    user_input: str
    parsed_input: Optional[ValidationRequest] = None
    execution_plan: Optional[ExecutionPlan] = None
    validation_error: Optional[str] = None
    # raw debug info (important for observability)
    raw_llm_output: Optional[str] = None

