import re


def refine_demo_sql(query: str) -> str:

    # -----------------------------
    # normalize spacing
    # -----------------------------
    query = " ".join(query.split())

    # -----------------------------
    # extract country condition
    # -----------------------------
    country_match = re.search(
        r"country\\s*=\\s*'([^']+)'",
        query,
        flags=re.IGNORECASE
    )

    country = None

    if country_match:
        country = country_match.group(1)

    # -----------------------------
    # build refined query
    # -----------------------------
    refined_query = "SELECT * FROM player_metrics"

    if country:
        refined_query += f" WHERE country = '{country}'"

    return refined_query