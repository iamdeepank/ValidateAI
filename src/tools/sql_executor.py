from sqlalchemy import text

from src.db.connection import engine


FORBIDDEN = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER"
]


def validate_query(query: str):

    upper_query = query.upper()

    for keyword in FORBIDDEN:
        if keyword in upper_query:
            raise ValueError(f"Forbidden SQL keyword: {keyword}")


def execute_query(query: str):

    validate_query(query)

    with engine.connect() as conn:

        result = conn.execute(text(query))

        return [dict(r._mapping) for r in result]