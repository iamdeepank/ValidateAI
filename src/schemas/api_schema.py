from pydantic import BaseModel


class RunAgentRequest(BaseModel):
    user_input: str


class RunAgentResponse(BaseModel):
    parsed_input: dict | None
    execution_plan: dict | None
    validation_error: str | None