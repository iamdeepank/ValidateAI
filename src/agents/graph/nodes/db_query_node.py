from sqlalchemy import text
from pathlib import Path
from src.schemas import AgentState
from src.utils import refine_demo_sql
from src.tools import execute_query
from src.db import engine
import json

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

        # ---------------------------------
        # Execute Query
        # ---------------------------------

        rows = execute_query(refined_query)

        artifact_dir = Path(
            state.artifact_dir
        )

        with open(
                artifact_dir / "db_data.json",
                "w"
        ) as f:

            json.dump(
                rows,
                f,
                indent=2
            )

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
            db_data=rows,
            artifact_dir=str(state.artifact_dir)

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