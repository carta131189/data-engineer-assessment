from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine


BASE_DIR = Path(__file__).resolve().parents[2]


def execute_sql(engine: Engine, file_name: str):

    sql_path = BASE_DIR / "sql" / file_name

    sql = sql_path.read_text(encoding="utf-8")

    with engine.begin() as conn:

        conn.execute(text(sql))


def create_raw_table(engine: Engine):

    execute_sql(engine, "raw_tables.sql")


def create_schema(engine: Engine):

    execute_sql(engine, "schema.sql")