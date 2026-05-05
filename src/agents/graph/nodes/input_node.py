from langchain_core.messages import HumanMessage, SystemMessage
from src.llm import llm
from src.schemas import ValidationRequest
import json
import re
from src.schemas import AgentState


PROMPT1 = """
Convert user input into STRICT JSON.

Schema:
{
  "filters": {
    "country": "string | null",
    "team": "string | null",
    "role": "string | null"
  },
}

ONLY return JSON.
"""

PROMPT="""
You are a JSON extraction system.

Task:
Extract filters from user input.

Rules:
- Return ONLY valid JSON
- Do NOT write code
- Do NOT explain anything
- Do NOT include markdown

Schema:
{
  "filters": {
    "country": "string | null",
    "team": "string | null",
    "role": "string | null"
    
  },
    "metrics": [
    "string | null",
    "string | null"
  ],
  "environments": [
    "string | null",
    "string | null"
  ],
  "dashboard": "string | null",
  "screen_name": "string | null"
}

"""



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

    return AgentState(
            user_input=state.user_input,
            parsed_input=validated,
            execution_plan=state.execution_plan,
            validation_error=None,
            raw_llm_output = raw_content
        )