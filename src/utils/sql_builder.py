def build_query(parsed_input):

    filters = parsed_input.filters

    conditions = []

    # -----------------------------
    # Dynamic Filters
    # -----------------------------
    if filters.country:
        conditions.append(
            f"country = '{filters.country}'"
        )

    if filters.team:
        conditions.append(
            f"team = '{filters.team}'"
        )

    if filters.role:
        conditions.append(
            f"role = '{filters.role}'"
        )

    # -----------------------------
    # Metrics
    # -----------------------------
    metrics = parsed_input.metrics

    metric_conditions = []

    for metric in metrics:
        metric_conditions.append(
            f"metric_name = '{metric}'"
        )

    metric_sql = " OR ".join(metric_conditions)

    if metric_sql:
        conditions.append(f"({metric_sql})")

    # -----------------------------
    # WHERE Clause
    # -----------------------------
    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # -----------------------------
    # Final Query
    # -----------------------------
    query = f'''
    SELECT *
    FROM player_metrics
    {where_clause}
    '''

    return " ".join(query.split())