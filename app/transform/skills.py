import ast

import pandas as pd
from sqlalchemy import text

from app.database import engine
from app.logger import logger


def load_skills() -> None:
    """
    Extract unique skills from raw_jobs and
    load them into the skills table.
    """

    logger.info("Loading skills table...")

    query = """
        SELECT job_skills
        FROM raw_jobs
        WHERE job_skills IS NOT NULL
    """

    df = pd.read_sql(query, engine)

    unique_skills = set()

    for value in df["job_skills"]:

        if pd.isna(value):
            continue

        try:
            skills = ast.literal_eval(value)

            if not isinstance(skills, list):
                continue

            for skill in skills:

                if skill is None:
                    continue

                skill = str(skill).strip()

                if skill == "":
                    continue

                unique_skills.add(skill)

        except (ValueError, SyntaxError):
            continue

    skills_df = pd.DataFrame(
        sorted(unique_skills),
        columns=["skill_name"]
    )

    logger.info(
        f"Unique skills extracted: {len(skills_df)}"
    )

    with engine.begin() as connection:

        connection.execute(
            text(
                "TRUNCATE TABLE skills RESTART IDENTITY CASCADE;"
            )
        )

    skills_df.to_sql(
        "skills",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000,
    )

    logger.info(
        f"Skills loaded successfully: {len(skills_df)}"
    )