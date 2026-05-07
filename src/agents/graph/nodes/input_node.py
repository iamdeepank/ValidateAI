from langchain_core.messages import HumanMessage, SystemMessage
from src.llm import llm
from src.schemas import ValidationRequest
import json
import re
from src.schemas import AgentState

SYSTEM_PROMPT = """
You are an enterprise dashboard validation input parser.

Your responsibility is to convert a user's natural language request into a STRICT structured validation request.

You are validating dashboard UI data against backend database data.

Return ONLY valid JSON.
Do NOT explain.
Do NOT add markdown.
Do NOT add comments.

-----------------------------------
VALIDATION REQUEST SCHEMA
-----------------------------------

{
  "dashboard": "string",

  "screen_name": "string",

  "environment": "string",

  "entity_filters": {
    "country": "string | null",
    "team": "string | null",
    "role": "string | null",
    "player_name": "string | null"
  },

  "metric_filters": [
    "string | None"
  ],

  "validation_config": {
    "comparison_type": "row_level",
    "tolerance": 0.05
  }
}

-----------------------------------
FIELD RULES
-----------------------------------

1. dashboard
- Name of dashboard platform
- Example:
  - Tableau
  - MicroStrategy
  - PowerBI

2. screen_name
- Dashboard page/screen name

3. environment
- Must be ONE value only
- Examples:
  - Preprod
  - Prod
  - Staging
  - QA
  - Dev

4. entity_filters
- Used for dashboard filtering
- If user does not provide a value:
  use null

5. metric_filters
- Must contain VALID metric names only

Allowed metric names:
- t_target_last12
- ct_target_last12
- ct_last12_delta
- t_last12_delta
- hltv_wr
- age

6. validation_config
- comparison_type default:
  row_level

- tolerance default:
  0.05

-----------------------------------
IMPORTANT BUSINESS RULES
-----------------------------------

1. NEVER invent filters

2. NEVER invent metrics

3. NEVER generate SQL

4. NEVER generate explanations

5. If a filter is not provided:
   set value to null

6. Metric names MUST be normalized to snake_case

Example:
"T Target Last12"
becomes:
"t_target_last12"

7. If dashboard not provided:
   default to "Tableau"

8. If environment not provided:
   default to "Preprod"

9. If screen_name not provided:
   default to "Overall"

-----------------------------------
EXAMPLE INPUT
-----------------------------------

Validate AWPer players from Canada for
T Target Last12 and CT Target Last12
on Tableau Overall dashboard in Preprod

-----------------------------------
EXAMPLE OUTPUT
-----------------------------------

{
  "dashboard": "Tableau",
  "screen_name": "Overall",
  "environment": "Preprod",
  "entity_filters": {
    "country": "Canada",
    "team": null,
    "role": "AWPer",
    "player_name": null
  },
  "metric_filters": [
    "string | None",
    "sting | None"
  ],
  "validation_config": {
    "comparison_type": "row_level",
    "tolerance": 0.05
  }
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
        SystemMessage(content=SYSTEM_PROMPT),
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