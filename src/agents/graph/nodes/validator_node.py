from typing import Dict, Any
from src.schemas import ValidationRequest
from src.schemas import AgentState



def validator_node(state: AgentState) -> AgentState:
    parsed_input = state.parsed_input

    if parsed_input is None:
        AgentState(
            user_input=state.user_input,
            parsed_input=state.parsed_input,
            execution_plan=state.execution_plan,
            validation_error="Parsed input is missing",
            raw_llm_output = state.raw_llm_output,
        )

    try:
        # Handle both dict and model
        if isinstance(parsed_input, dict):
            validated = ValidationRequest(**parsed_input)
        elif isinstance(parsed_input, ValidationRequest):
            validated = parsed_input
        else:
            raise ValueError("Invalid parsed_input type")

        return AgentState(
            user_input=state.user_input,
            parsed_input=validated,
            execution_plan=state.execution_plan,
            raw_llm_output=state.raw_llm_output,
            validation_error=None
        )

    except Exception as e:
        return AgentState(
            user_input=state.user_input,
            parsed_input=None,
            execution_plan=state.execution_plan,
            raw_llm_output=state.raw_llm_output,
            validation_error=str(e)
        )
