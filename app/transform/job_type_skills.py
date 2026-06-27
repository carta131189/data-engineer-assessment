import json

import pandas as pd
from sqlalchemy import text

from app.database import engine
from app.logger import logger


def load_job_type_skills() -> None:
    """
    Load relationships between jobs and skills
    from the job_type_skills JSON column.
    """

    logger.info("Loading job_type_skills table...")

    jobs_query = """
        SELECT
            j.job_id,
            r.job_type_skills
        FROM jobs j
        INNER JOIN raw_jobs r
            ON j.raw_job_id = r.raw_job_id
        WHERE r.job_type_skills IS NOT NULL;
    """

    skills_query = """
        SELECT
            skill_id,
            skill_name
        FROM skills;
    """

    jobs_df = pd.read_sql(jobs_query, engine)

    skills_df = pd.read_sql(skills_query, engine)

    logger.info(
        f"Jobs with job_type_skills: {len(jobs_df)}"
    )

    skill_lookup = {
        row.skill_name.strip().lower(): row.skill_id
        for row in skills_df.itertuples(index=False)
    }

    records = []

    for row in jobs_df.itertuples(index=False):

        if row.job_type_skills is None:
            continue

        text_json = str(row.job_type_skills).strip()

        if (
            text_json == ""
            or text_json.lower() == "null"
        ):
            continue

        try:
            data = json.loads(text_json)

        except Exception:
            continue

        if not isinstance(data, dict):
            continue

        for category, values in data.items():

            if not isinstance(values, list):
                continue

            for skill in values:

                if skill is None:
                    continue

                skill = str(skill).strip().lower()

                if skill == "":
                    continue

                skill_id = skill_lookup.get(skill)

                if skill_id is None:
                    continue

                records.append(
                    {
                        "job_id": row.job_id,
                        "skill_id": skill_id,
                    }
                )

    job_type_skills = pd.DataFrame(records)

    if job_type_skills.empty:
        logger.warning("No relationships found.")
        return

    job_type_skills = job_type_skills.drop_duplicates()

    logger.info(
        f"Relationships extracted: {len(job_type_skills)}"
    )

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                TRUNCATE TABLE job_type_skills CASCADE;
                """
            )
        )

    job_type_skills.to_sql(
        "job_type_skills",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=10000,
    )

    logger.info(
        f"job_type_skills loaded successfully: {len(job_type_skills)}"
    )


if __name__ == "__main__":
    load_job_type_skills()