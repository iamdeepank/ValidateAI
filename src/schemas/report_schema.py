from pydantic import BaseModel
from .comparison_schema import ComparisonSummary,MetricComparisonResult
from typing import List


class FinalReport(BaseModel):

    timestamp: str
    status: str
    dashboard: str
    environment: str
    screen_name: str
    summary: ComparisonSummary
    failed_metrics: List[MetricComparisonResult]
    passed_metrics: List[MetricComparisonResult]
    generated_sql: str