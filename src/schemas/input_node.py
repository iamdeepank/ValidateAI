"""
entity_filters → WHERE
metric_filters → SELECT / validation_targets / comparison engine
validation_config → comparison logic

TODO
"sorting": {},
"group_by": [],
"date_range": {},
"aggregation": {}
"""

from typing import Literal
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------
# Allowed Metric Names
# ---------------------------------------------------------
ALLOWED_METRICS = {
    "t_target_last12",
    "ct_target_last12",
    "ct_last12_delta",
    "t_last12_delta",
    "hltv_wr",
    "age",
}


# ---------------------------------------------------------
# Entity Filters
# ---------------------------------------------------------
class EntityFilters(BaseModel):
    country: str | None = Field(
        default=None,
        description=(
            "Country filter used for dashboard validation. "))

    team: str | None = Field(
        default=None,
        description=(
            "Team filter used for dashboard validation. "
        )
    )

    role: str | None = Field(
        default=None,
        description=(
            "Player role filter. "
        )
    )

    player_name: str | None = Field(
        default=None,
        description=(
            "Specific player name filter. "
        )
    )


# ---------------------------------------------------------
# Validation Configuration
# ---------------------------------------------------------
class ValidationConfig(BaseModel):
    comparison_type: Literal[
        "row_level",
        "aggregate"
    ] = Field(
        default="row_level",
        description=(
            "Defines comparison strategy between "
            "dashboard UI data and backend database data."
        )
    )

    tolerance: float = Field(
        default=0.05,
        ge=0,
        le=1,
        description=(
            "Allowed numeric tolerance during metric comparison. "
            "Used to avoid floating point precision mismatches."
        )
    )


# ---------------------------------------------------------
# Main Validation Request
# ---------------------------------------------------------
class ValidationRequest(BaseModel):
    dashboard: str = Field(
        default="Tableau",
        description=(
            "Dashboard platform name. "
            "Example: Tableau, MicroStrategy, PowerBI."
        )
    )

    screen_name: str = Field(
        default="Overall",
        description=(
            "Dashboard screen or page name."
        )
    )

    environment: Literal[
        "Preprod",
        "Prod",
        "QA",
        "Dev",
        "Staging"
    ] = Field(
        default="Preprod",
        description=(
            "Target environment where validation should run."
        )
    )

    entity_filters: EntityFilters = Field(
        default_factory=EntityFilters,
        description=(
            "Dimension-level filters used for dashboard validation."
        )
    )

    metric_filters: list[str] = Field(
        default_factory=list,
        description=(
            "List of metric columns to validate."
        )
    )

    validation_config: ValidationConfig = Field(
        default_factory=ValidationConfig,
        description=(
            "Configuration controlling validation behavior."
        )
    )

    # ---------------------------------------------------------
    # Metric Validation
    # ---------------------------------------------------------
    @field_validator("metric_filters")
    @classmethod
    def validate_metrics(
            cls,
            metrics: list[str]
    ) -> list[str]:
        invalid_metrics = [
            metric
            for metric in metrics
            if metric not in ALLOWED_METRICS
        ]

        if invalid_metrics:
            raise ValueError(
                f"Invalid metrics detected: {invalid_metrics}"
            )

        return metrics
