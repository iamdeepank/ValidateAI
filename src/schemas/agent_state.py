from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from src.schemas import ValidationRequest
from src.schemas import ExecutionPlan
from .comparison_schema import ComparisonResult
from .report_schema import FinalReport



class AgentState(BaseModel):
    user_input: str
    parsed_input: Optional[ValidationRequest] = None
    execution_plan: Optional[ExecutionPlan] = None
    validation_error: Optional[str] = None
    raw_llm_output: Optional[str] = None
    ui_data: Optional[List[Dict[str, Any]]] = None
    generated_sql: Optional[str] = None
    db_data: Optional[Any] = None
    comparison_result: Optional[Any] = None
    final_report: Optional[Any] = None
    comparison_result: Optional[ComparisonResult] = None
    final_report: Optional[FinalReport] = None

