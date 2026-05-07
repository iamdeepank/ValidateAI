from pydantic import BaseModel
from typing import List

class ExecutionStep(BaseModel):

    step_id: int
    step_name: str
    node_name: str
    depends_on: List[int]
    critical: bool = True


class ExecutionPlan(BaseModel):

    workflow_id: str
    execution_strategy: str
    steps: List[ExecutionStep]