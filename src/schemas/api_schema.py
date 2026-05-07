
from pydantic import BaseModel
from typing import Optional,Dict,Any,List

class UIData(BaseModel):
    role: str
    player_name: str
    team: str
    t_target_last12: str
    ct_target_last12: Optional[str] = None


class RunAgentRequest(BaseModel):
    user_input: str


class RunAgentResponse(BaseModel):
    parsed_input: dict | None
    execution_plan: dict | None
    validation_error: str | None
    raw_llm_output: str | None
    ui_data: Optional[List[UIData]] = None
    sql_generation:str | None
    db_data: Optional[Any] = None
    comparison_result: Optional[Any] = None
    final_report: Optional[Any] = None




