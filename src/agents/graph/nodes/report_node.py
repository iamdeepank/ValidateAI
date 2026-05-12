from datetime import datetime
from pathlib import Path
import json
from src.schemas import AgentState
from src.schemas import FinalReport


def report_node(state: AgentState) -> AgentState:

    comparison = state.comparison_result

    # -----------------------------------
    # Safety Check
    # -----------------------------------
    if comparison is None:
        return AgentState(
            user_input=state.user_input,
            parsed_input=state.parsed_input,
            execution_plan=state.execution_plan,
            validation_error={
                "validation_error": (
                    "Comparison result missing"
                )
            },
            raw_llm_output=state.raw_llm_output,
            ui_data=state.ui_data,
            generated_sql=state.generated_sql,
            db_data=state.db_data,
            comparison_result=state.comparison_result,
        )

    # -----------------------------------
    # Build Typed Report
    # -----------------------------------
    report = FinalReport(

        timestamp=str(datetime.utcnow()),
        status=comparison.status,
        dashboard=state.parsed_input.dashboard,
        environment=(
            state.parsed_input.environment
        ),
        screen_name=(
            state.parsed_input.screen_name
        ),
        summary=comparison.summary,

        failed_metrics=[
            metric
            for metric in comparison.metric_results
            if metric.status == "FAIL"
        ],
        passed_metrics=[
            metric
            for metric in comparison.metric_results
            if metric.status == "PASS"
        ],

        generated_sql=state.generated_sql
    )

    # -----------------------------------
    # Return Updated State
    # -----------------------------------
    artifact_dir = Path(
        state.artifact_dir
    )

    with open(
            artifact_dir / "report_node.json",
            "w"
    ) as f:
        json.dump(
            report.model_dump(),
            f,
            indent=2
        )

    return AgentState(
        user_input=state.user_input,
        parsed_input=state.parsed_input,
        execution_plan=state.execution_plan,
        validation_error=None,
        raw_llm_output=state.raw_llm_output,
        ui_data=state.ui_data,
        generated_sql=state.generated_sql,
        db_data=state.db_data,
        comparison_result=state.comparison_result,
        final_report=report
    )
