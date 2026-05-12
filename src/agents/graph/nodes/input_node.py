from langchain_core.messages import HumanMessage, SystemMessage
from src.llm import llm
from src.schemas import ValidationRequest
import json
import re
from src.schemas import AgentState
from src.utils import load_prompt,ArtifactManager

PROMPT = load_prompt(
    "v1/input_node.txt"
)

def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Invalid JSON from LLM: {text}")


def input_node(state:AgentState)->AgentState:
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(content=state.user_input)
    ]

    response = llm.invoke(messages)

    raw_content = response.content
    parsed_dict = extract_json(raw_content)

    validated = ValidationRequest(**parsed_dict)

    # setup Artifact
    artifact_manager = ArtifactManager()

    artifact_manager.save_text(
        "raw_llm_output.txt",
        state.user_input
    )

    artifact_manager.save_json(
        "parsed_input.json",
        validated.model_dump()
    )

    return AgentState(
            user_input=state.user_input,
            parsed_input=validated,
            execution_plan=state.execution_plan,
            validation_error=None,
            raw_llm_output = raw_content,
            artifact_dir= str(
            artifact_manager.run_dir
    )
        )
