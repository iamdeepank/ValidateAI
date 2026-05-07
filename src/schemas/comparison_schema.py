from typing import Optional
from typing import List

from pydantic import BaseModel


# -----------------------------
# Metric Level Result
# -----------------------------
class MetricComparisonResult(BaseModel):

    player_name: Optional[str] = None
    metric: Optional[str] = None
    ui_value: Optional[float] = None
    db_value: Optional[float] = None
    difference: Optional[float] = None
    tolerance: Optional[float] = None
    status: str
    reason: Optional[str] = None


# -----------------------------
# Summary
# -----------------------------
class ComparisonSummary(BaseModel):

    total_ui_rows: int
    total_db_rows: int
    matched_rows: int
    failed_rows: int


# -----------------------------
# Final Comparison Output
# -----------------------------
class ComparisonResult(BaseModel):

    status: str
    summary: ComparisonSummary
    metric_results: List[MetricComparisonResult]