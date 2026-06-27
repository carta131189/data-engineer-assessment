import pandas as pd
from sqlalchemy import text

from app.database import engine
from app.logger import logger


def load_jobs() -> None:
    """
    Load jobs dimension from raw_jobs.
    """

    logger.info("Loading jobs table...")

    query = """
        SELECT

            r.raw_job_id,

            c.company_id,

            l.location_id,

            r.job_title,

            r.job_title_short,

            r.job_via,

            r.job_schedule_type,

            r.job_work_from_home,

            r.job_posted_date,

            r.job_no_degree_mention,

            r.job_health_insurance,

            r.salary_rate,

            r.salary_year_avg,

            r.salary_hour_avg

        FROM raw_jobs r

        INNER JOIN companies c
            ON TRIM(r.company_name) = c.company_name

        INNER JOIN locations l
            ON COALESCE(TRIM(r.job_location), '') =
               COALESCE(l.job_location, '')
           AND COALESCE(TRIM(r.job_country), '') =
               COALESCE(l.job_country, '')
           AND COALESCE(TRIM(r.search_location), '') =
               COALESCE(l.search_location, '')

        ORDER BY r.raw_job_id;
    """

    jobs = pd.read_sql(query, engine)

    logger.info(f"Jobs extracted: {len(jobs)}")

    # ---------------------------------------------------------
    # Clean numeric columns
    # ---------------------------------------------------------

    jobs["salary_year_avg"] = pd.to_numeric(
        jobs["salary_year_avg"],
        errors="coerce"
    )

    jobs["salary_hour_avg"] = pd.to_numeric(
        jobs["salary_hour_avg"],
        errors="coerce"
    )

    # ---------------------------------------------------------
    # Clean text columns
    # ---------------------------------------------------------

    text_columns = [
        "job_title",
        "job_title_short",
        "job_via",
        "job_schedule_type",
        "salary_rate"
    ]

    for column in text_columns:

        jobs[column] = (
            jobs[column]
            .astype("string")
            .str.strip()
        )

    # ---------------------------------------------------------
    # Replace NaN with None
    # ---------------------------------------------------------

    jobs = jobs.where(pd.notnull(jobs), None)

    with engine.begin() as connection:

        connection.execute(
            text(
                "TRUNCATE TABLE jobs RESTART IDENTITY CASCADE;"
            )
        )

    jobs.to_sql(
        "jobs",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000
    )

    logger.info(
        f"Jobs loaded successfully: {len(jobs)}"
    )

if __name__ == "__main__":
    load_jobs()    