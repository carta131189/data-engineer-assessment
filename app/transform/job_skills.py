import ast

import pandas as pd
from sqlalchemy import text

from app.database import engine
from app.logger import logger


def load_job_skills() -> None:
    """
    Load the many-to-many relationship
    between jobs and skills.
    """

    logger.info("Loading job_skills table...")

    jobs_query = """
        SELECT

            j.job_id,

            r.job_skills

        FROM jobs j

        INNER JOIN raw_jobs r
            ON j.raw_job_id = r.raw_job_id

        WHERE r.job_skills IS NOT NULL;
    """

    skills_query = """
        SELECT

            skill_id,

            skill_name

        FROM skills;
    """

    jobs_df = pd.read_sql(jobs_query, engine)

    skills_df = pd.read_sql(skills_query, engine)

    logger.info(f"Jobs with skills: {len(jobs_df)}")

    skill_lookup = {
        row.skill_name.strip().lower(): row.skill_id
        for row in skills_df.itertuples(index=False)
    }

    records = []

    for row in jobs_df.itertuples(index=False):

        if row.job_skills is None:
            continue

        # PostgreSQL JSON puede venir como list o como string
        if isinstance(row.job_skills, list):

            skills = row.job_skills

        elif isinstance(row.job_skills, str):

            try:
                skills = ast.literal_eval(row.job_skills)

            except (ValueError, SyntaxError):

                continue

        else:

            continue

        if not isinstance(skills, list):
                continue

        if len(skills) == 0:
                continue

        for skill in skills:

            if skill is None:
                continue

            skill = str(skill).strip()

            if skill == "":
                continue

            skill_id = skill_lookup.get(
                skill.lower()
            )

            if skill_id is None:
                continue

            records.append(
                {
                    "job_id": row.job_id,
                    "skill_id": skill_id,
                }
            )

    job_skills = pd.DataFrame(
        records,
        columns=[
            "job_id",
            "skill_id",
        ],
    )

    if job_skills.empty:

        logger.warning(
            "No relationships found."
        )

        return

    job_skills = (
        job_skills
        .drop_duplicates()
        .sort_values(
            by=[
                "job_id",
                "skill_id",
            ]
        )
    )

    logger.info(
        f"Relationships extracted: {len(job_skills)}"
    )

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                TRUNCATE TABLE job_skills
                RESTART IDENTITY;
                """
            )
        )

    job_skills.to_sql(
        "job_skills",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=10000,
    )

    logger.info(
        f"job_skills loaded successfully: {len(job_skills)}"
    )


if __name__ == "__main__":
    load_job_skills()