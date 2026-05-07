from src.schemas import AgentState
from src.utils import NormalizationUtils
from src.schemas.comparison_schema import (
    ComparisonResult,
    ComparisonSummary,
    MetricComparisonResult
)
from src.utils import VALID_METRICS


def comparison_node(state: AgentState) -> AgentState:

    ui_data = state.ui_data or []
    db_data = state.db_data or []

    tolerance = (
        state.parsed_input
        .validation_config
        .tolerance
    )

    metric_results: list[MetricComparisonResult] = []

    matched_rows = 0
    failed_rows = 0

    # -----------------------------------
    # Iterate UI Rows
    # -----------------------------------
    for ui_row in ui_data:

        ui_player = (
            NormalizationUtils.normalize_string(
                ui_row.get("player_name")
            )
        )

        matched_db = None

        # -----------------------------------
        # Find Matching DB Row
        # -----------------------------------
        for db_row in db_data:

            db_player = (
                NormalizationUtils.normalize_string(
                    db_row.get("player_name")
                )
            )

            if ui_player == db_player:
                matched_db = db_row
                break

        # -----------------------------------
        # Missing DB Match
        # -----------------------------------
        if not matched_db:

            failed_rows += 1

            metric_results.append(
                MetricComparisonResult(
                    player_name=ui_player,
                    status="FAIL",
                    reason="Player not found in DB"
                )
            )

            continue

        matched_rows += 1

        # -----------------------------------
        # Metric Mapping
        # -----------------------------------

        requested_metrics = [
            metric
            for metric in (
                state.parsed_input.metric_filters
            )

            if metric in VALID_METRICS
        ]

        if not requested_metrics:
            AgentState(
                user_input=state.user_input,
                parsed_input=state.parsed_input,
                execution_plan=state.execution_plan,
                validation_error="No valid metrics requested",
                raw_llm_output=state.raw_llm_output,
                ui_data=state.ui_data,
                generated_sql=state.generated_sql,
                db_data=state.db_data,

            )

        # -----------------------------------
        # Dynamic Metric Mapping
        # -----------------------------------
        metrics = [
            (metric, metric)
            for metric in requested_metrics
        ]

        print("metricssss",metrics)
        print("metricssss typee",type(metrics))
        # -----------------------------------
        # Compare Metrics
        # -----------------------------------
        for ui_metric, db_metric in metrics:

            ui_value = (
                NormalizationUtils.safe_float(
                    ui_row.get(ui_metric)
                )
            )

            db_value = (
                NormalizationUtils.safe_float(
                    matched_db.get(db_metric)
                )
            )

            # -----------------------------------
            # Invalid Conversion
            # -----------------------------------
            if ui_value is None or db_value is None:

                failed_rows += 1

                metric_results.append(
                    MetricComparisonResult(
                        player_name=ui_player,
                        metric=db_metric,
                        ui_value=ui_value,
                        db_value=db_value,
                        status="FAIL",
                        reason="Invalid numeric conversion"
                    )
                )

                continue

            # -----------------------------------
            # Difference Calculation
            # -----------------------------------
            difference = abs(ui_value - db_value)

            passed = difference <= tolerance

            if not passed:
                failed_rows += 1

            metric_results.append(
                MetricComparisonResult(
                    player_name=ui_player,
                    metric=db_metric,
                    ui_value=ui_value,
                    db_value=db_value,
                    difference=difference,
                    tolerance=tolerance,
                    status=(
                        "PASS"
                        if passed
                        else "FAIL"
                    ),
                    reason=(
                        None
                        if passed
                        else (
                            f"Difference "
                            f"{difference} exceeded "
                            f"tolerance {tolerance}"
                        )
                    )
                )
            )

    # -----------------------------------
    # Final Status
    # -----------------------------------
    final_status = (
        "PASS"
        if failed_rows == 0
        else "FAIL"
    )

    # -----------------------------------
    # Typed Comparison Result
    # -----------------------------------
    comparison_result = ComparisonResult(

        status=final_status,

        summary=ComparisonSummary(
            total_ui_rows=len(ui_data),
            total_db_rows=len(db_data),
            matched_rows=matched_rows,
            failed_rows=failed_rows
        ),

        metric_results=metric_results
    )

    # -----------------------------------
    # Return Updated State
    # -----------------------------------
    return AgentState(
        user_input=state.user_input,
        parsed_input=state.parsed_input,
        execution_plan=state.execution_plan,
        validation_error=None,
        raw_llm_output=state.raw_llm_output,
        ui_data=state.ui_data,
        generated_sql=state.generated_sql,
        db_data=state.db_data,
        comparison_result=comparison_result

    )
