import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from src.schemas import AgentState
from src.llm import llm
from src.schemas import ExecutionPlan



PROMPT1 = """
You are a planning engine for a data validation system.

Your task:
Generate an execution plan based on the input.

Allowed steps ONLY:
- extract_ui_data
- generate_sql
- execute_query
- compare_results

Rules:
- Do NOT invent new steps
- Do NOT skip required steps
- Always return steps in logical order
- Output MUST be valid JSON
- Do NOT include explanations or text outside JSON

Required Output Format:
{
  "steps": ["extract_ui_data", "generate_sql", "execute_query", "compare_results"]
}

Input:
{input}
"""

PROMPT2 = """
You are an intelligent planner.

Based on the input, decide which steps are required to validate report data.

Available steps:
1. extract_ui_data → fetch data from UI
2. generate_sql → create query for backend
3. execute_query → run query on database
4. compare_results → compare UI and DB data

Rules:
- Include only necessary steps
- Maintain correct order
- Always include compare_results at the end
- Output ONLY JSON

Output:
{
  "steps": ["step1", "step2"]
}

Input:
{input}
"""


PROMPT = """
Create execution plan from input.

Allowed steps:
- extract_ui_data
- generate_sql
- execute_query
- compare_results

Return STRICT JSON only:
{
  "steps": ["step1", "step2"]
}
"""


# PLANNER_PROMPT = """
# You are a planning engine.
#
# Create an execution plan for validating dashboard data.
#
# Return only structured output.
#
# Rules:
# - Always include these steps in order:
#   1. extract_ui_data
#   2. generate_sql
#   3. execute_query
#   4. compare_results
# """

PLANNER_PROMPT = """
You are a planning engine.

Return ONLY the following JSON structure:

{
  "steps": ["extract_ui_data", "generate_sql", "execute_query", "compare_results"]
}

STRICT RULES:
- ONLY return "steps"
- DO NOT include filters, metrics, or any other fields
- DO NOT explain anything
- DO NOT add extra keys

Always return exactly 4 steps in order.
"""

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return json.loads(match.group())


def planner_node(state: AgentState) -> AgentState:

    plan = ExecutionPlan(
        steps=[
            "extract_ui_data",
            "generate_sql",
            "execute_query",
            "compare_results"
        ]
    )

    return AgentState(
        user_input=state.user_input,
        parsed_input=state.parsed_input,
        execution_plan=plan,
        validation_error=state.validation_error,
        raw_llm_output=state.raw_llm_output
    )