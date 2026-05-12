from typing import Dict, Any
from src.schemas import ValidationRequest
from src.schemas import AgentState
from pathlib import Path
import json


def validator_node(state: AgentState) -> AgentState:
    parsed_input = state.parsed_input
    artifact_dir = Path(
        state.artifact_dir
    )

    if parsed_input is None:
        with open(
                artifact_dir / "validator_node.txt",
                "w"
        ) as f:
            f.write("Parsed input is missing")
        AgentState(
            user_input=state.user_input,
            parsed_input=state.parsed_input,
            execution_plan=state.execution_plan,
            validation_error="Parsed input is missing",
            raw_llm_output = state.raw_llm_output,
            artifact_dir=str(state.artifact_dir)
        )

    try:
        # Handle both dict and model
        if isinstance(parsed_input, dict):
            validated = ValidationRequest(**parsed_input)
        elif isinstance(parsed_input, ValidationRequest):
            validated = parsed_input
        else:
            raise ValueError("Invalid parsed_input type")



        with open(
                artifact_dir / "validator_node.json",
                "w"
        ) as f:
            json.dump(
                validated.model_dump(),
                f,
                indent=2
            )

        return AgentState(
            user_input=state.user_input,
            parsed_input=validated,
            execution_plan=state.execution_plan,
            raw_llm_output=state.raw_llm_output,
            validation_error=None,
            artifact_dir=str(state.artifact_dir)
        )

    except Exception as e:
        with open(
                artifact_dir / "validator_node.txt",
                "w"
        ) as f:
            f.write(str(e))
        return AgentState(
            user_input=state.user_input,
            parsed_input=None,
            execution_plan=state.execution_plan,
            raw_llm_output=state.raw_llm_output,
            validation_error=str(e),
            artifact_dir=str(state.artifact_dir)
        )
