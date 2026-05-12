from langchain_core.messages import HumanMessage, SystemMessage
from src.schemas import AgentState
from pathlib import Path
import json
from src.schemas import ExecutionPlan,ExecutionStep


def planner_node(state: AgentState) -> AgentState:

    plan = ExecutionPlan(

        workflow_id="validation_workflow_v1",

        execution_strategy="sequential",

        steps=[

            ExecutionStep(
                step_id=1,
                step_name="extract_ui_data",
                node_name="ui_node",
                depends_on=[],
                critical=True
            ),
            ExecutionStep(
                step_id=2,
                step_name="generate_sql",
                node_name="sql_generation_node",
                depends_on=[1],
                critical=True
            ),

            ExecutionStep(
                step_id=3,
                step_name="execute_query",
                node_name="db_query_node",
                depends_on=[2],
                critical=True
            ),

            ExecutionStep(
                step_id=4,
                step_name="compare_results",
                node_name="comparison_node",
                depends_on=[1, 3],
                critical=True
            ),

            ExecutionStep(
                step_id=5,
                step_name="generate_report",
                node_name="report_node",
                depends_on=[4],
                critical=True
            )
        ]
    )

    # ----------------------------------------
    # Reuse existing artifact folder
    # ----------------------------------------

    print(" state.artifact_dir===", state.artifact_dir)
    print(" state.artifact_dir===", type(state.artifact_dir))
    artifact_dir = Path(
        state.artifact_dir
    )

    # ----------------------------------------
    # Save execution plan
    # ----------------------------------------

    with open(
            artifact_dir / "execution_plan.json",
            "w"
    ) as f:
        json.dump(
            plan.model_dump(),
            f,
            indent=2
        )

    return AgentState(
            user_input=state.user_input,
            parsed_input=state.parsed_input,
            execution_plan=plan,
            validation_error=state.validation_error,
            raw_llm_output=state.raw_llm_output,
            artifact_dir=state.artifact_dir
        )