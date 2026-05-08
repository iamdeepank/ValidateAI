from sqlalchemy import text

from src.schemas import AgentState
from src.utils import refine_demo_sql
from src.tools import execute_query
from src.db import engine


def db_query_node(state: AgentState) -> AgentState:

    try:

        # ---------------------------------
        # Validate Input Query
        # ---------------------------------
        if not state.generated_sql:
            raise ValueError("generated_sql is empty")

        # ---------------------------------
        # Refine Query
        # ---------------------------------
        refined_query = refine_demo_sql(
            state
        )
        # ---------------------------------
        # Allow ONLY SELECT
        # ---------------------------------
        if not refined_query.upper().startswith("SELECT"):
            raise ValueError(
                "Only SELECT queries are allowed"
            )

        print("\n[DB QUERY NODE]")
        print("Refined SQL:")
        print(refined_query)

        # ---------------------------------
        # Execute Query
        # ---------------------------------

        rows = execute_query(refined_query)

        print("Fetched Rows:", len(rows))

        # ---------------------------------
        # Return Updated State
        # ---------------------------------
        return AgentState(
            user_input=state.user_input,
            parsed_input=state.parsed_input,
            execution_plan=state.execution_plan,
            validation_error=None,
            raw_llm_output=state.raw_llm_output,
            ui_data=state.ui_data,
            generated_sql=state.generated_sql,
            db_data=rows

        )

    except Exception as e:

        print("\n[DB QUERY ERROR]")
        print(str(e))

        return AgentState(
            user_input=state.user_input,
            parsed_input=state.parsed_input,
            execution_plan=state.execution_plan,
            validation_error=f"Error on db_query_node, {str(e)}",
            raw_llm_output=state.raw_llm_output,
            ui_data=state.ui_data,
            generated_sql=state.generated_sql,
        )