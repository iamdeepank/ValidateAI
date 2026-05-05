from pydantic import BaseModel
from typing import Optional,Dict,Any,List


class UIData(BaseModel):
    role: str
    name: str
    team: str
    t_target: str
    ct_target: Optional[str] = None


class RunAgentRequest(BaseModel):
    user_input: str


class RunAgentResponse(BaseModel):
    parsed_input: dict | None
    execution_plan: dict | None
    validation_error: str | None
    raw_llm_output: str | None
    ui_data: Optional[List[UIData]] = None
