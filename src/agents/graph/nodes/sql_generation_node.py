from langchain_core.messages import HumanMessage, SystemMessage
from src.llm import llm
from src.schemas import AgentState
from src.utils import load_prompt

PROMPT = load_prompt(
    "v1/sql_generation.txt"
)
print("ooppppppppppppppp",PROMPT)

def sql_generation_node(state:AgentState)->AgentState:

    result = llm.invoke([
        SystemMessage(content=PROMPT),
        HumanMessage(content=str(state.parsed_input))
    ])

    return AgentState(
        user_input=state.user_input,
        parsed_input=state.parsed_input,
        execution_plan=state.execution_plan,
        validation_error=None,
        raw_llm_output=state.raw_llm_output,
        ui_data=state.ui_data,
        generated_sql=str(result.content)

    )