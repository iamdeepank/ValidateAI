import re
from src.schemas import AgentState

def refine_demo_sql(state: AgentState) -> str:
    parsed_input = state.parsed_input

    if parsed_input and parsed_input.entity_filters.country:
        country = parsed_input.entity_filters.country

    print("countryyyyyy",country)
    refined_query = "SELECT * FROM player_metrics"

    if country:
        refined_query += f" WHERE country = '{country}'"

    return refined_query