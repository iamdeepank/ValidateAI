from langchain_core.messages import HumanMessage, SystemMessage
from app.llm.groq_client import call_groq
from app.schemas.plan_schema import ExecutionPlan
import json
import re



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


def safe_extract_json(text: str):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Invalid JSON from LLM: {text}")


def planner_node(state):
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(content=state["parsed_input"].model_dump_json())
    ]

    response = call_groq(messages)

    plan_dict = safe_extract_json(response)

    validated_plan = ExecutionPlan(**plan_dict)

    return {
        **state,
        "execution_plan": validated_plan,
        "raw_llm_output": response
    }