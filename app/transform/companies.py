import pandas as pd
from sqlalchemy import text

from app.database import engine
from app.logger import logger


def load_companies() -> None:
    """
    Extract unique companies from raw_jobs and
    load them into the companies table.
    """

    logger.info("Loading companies table...")

    query = """
        SELECT DISTINCT
            TRIM(company_name) AS company_name
        FROM raw_jobs
        WHERE company_name IS NOT NULL
          AND TRIM(company_name) <> ''
        ORDER BY company_name;
    """

    companies = pd.read_sql(query, engine)

    logger.info(
        f"Companies extracted: {len(companies)}"
    )

    with engine.begin() as connection:

        connection.execute(
            text("TRUNCATE TABLE companies RESTART IDENTITY CASCADE;")
        )

    companies.to_sql(
        "companies",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000,
    )

    logger.info(
        f"Companies loaded successfully: {len(companies)}"
    )