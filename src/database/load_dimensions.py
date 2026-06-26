import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def truncate_tables(engine: Engine) -> None:
    """
    Clean all 3NF tables before loading.

    This keeps the raw table untouched.
    """

    tables = [
        "job_skills",
        "skill_skill_types",
        "jobs",
        "skills",
        "skill_types",
        "locations",
        "companies",
    ]

    with engine.begin() as conn:

        for table in tables:

            conn.execute(
                text(
                    f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"
                )
            )

    logger.info("3NF tables truncated successfully.")


def load_table(
    df: pd.DataFrame,
    table_name: str,
    engine: Engine,
) -> None:
    """
    Generic DataFrame loader.
    """

    if df.empty:

        logger.warning(f"{table_name} is empty. Skipping...")

        return

    df.to_sql(
        table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000,
    )

    logger.info(
        f"{len(df):,} rows inserted into {table_name}"
    )


def load_dimensions(
    companies: pd.DataFrame,
    locations: pd.DataFrame,
    skills: pd.DataFrame,
    skill_types: pd.DataFrame,
    engine: Engine,
) -> None:
    """
    Load dimension tables.
    """

    logger.info("Loading dimensions...")

    load_table(companies, "companies", engine)

    load_table(locations, "locations", engine)

    load_table(skill_types, "skill_types", engine)

    load_table(skills, "skills", engine)

    logger.info("Dimensions loaded successfully.")


def load_facts(
    jobs: pd.DataFrame,
    job_skills: pd.DataFrame,
    skill_skill_types: pd.DataFrame,
    engine: Engine,
) -> None:
    """
    Load fact and bridge tables.
    """

    logger.info("Loading fact tables...")

    load_table(jobs, "jobs", engine)

    load_table(job_skills, "job_skills", engine)

    load_table(
        skill_skill_types,
        "skill_skill_types",
        engine,
    )

    logger.info("Fact tables loaded successfully.")