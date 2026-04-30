from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.schemas import ValidationRequest
from src.schemas import ExecutionPlan


class AgentState(BaseModel):
    user_input: str
    parsed_input: Optional[ValidationRequest] = None
    execution_plan: Optional[ExecutionPlan] = None
    validation_error: Optional[str] = None
    # raw debug info (important for observability)
    raw_llm_output: Optional[str] = None

