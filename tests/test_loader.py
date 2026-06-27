import pandas as pd

from sqlalchemy import text

from app.database import engine
from app.ingestion.loader import load_raw_jobs


def test_loader_creates_table():

    df = pd.DataFrame(
        {
            "job_title": ["Data Engineer"],
            "job_skills": [["Python"]],
            "job_type_skills": [{"Programming": ["Python"]}]
        }
    )

    load_raw_jobs(df)

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM raw_jobs
                """
            )
        )

        total = result.scalar()

    assert total == 1