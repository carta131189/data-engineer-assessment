import pandas as pd

from app.database import engine
from app.transform.job_skills import load_job_skills


def test_load_job_skills():

    load_job_skills()

    relationships = pd.read_sql(
        "SELECT * FROM job_skills;",
        engine,
    )

    assert not relationships.empty


def test_expected_columns():

    relationships = pd.read_sql(
        "SELECT * FROM job_skills LIMIT 1;",
        engine,
    )

    expected_columns = {
        "job_id",
        "skill_id",
    }

    assert expected_columns.issubset(relationships.columns)


def test_relationships_are_unique():

    duplicates = pd.read_sql(
        """
        SELECT
            job_id,
            skill_id,
            COUNT(*) total
        FROM job_skills
        GROUP BY
            job_id,
            skill_id
        HAVING COUNT(*) > 1;
        """,
        engine,
    )

    assert duplicates.empty


def test_job_fk_integrity():

    invalid = pd.read_sql(
        """
        SELECT js.job_id
        FROM job_skills js
        LEFT JOIN jobs j
            ON js.job_id = j.job_id
        WHERE j.job_id IS NULL;
        """,
        engine,
    )

    assert invalid.empty


def test_skill_fk_integrity():

    invalid = pd.read_sql(
        """
        SELECT js.skill_id
        FROM job_skills js
        LEFT JOIN skills s
            ON js.skill_id = s.skill_id
        WHERE s.skill_id IS NULL;
        """,
        engine,
    )

    assert invalid.empty


def test_relationship_count():

    relationships = pd.read_sql(
        """
        SELECT COUNT(*) total
        FROM job_skills;
        """,
        engine,
    )

    assert relationships.iloc[0]["total"] > 0


def test_jobs_have_skills():

    jobs_without_skills = pd.read_sql(
    """
    SELECT COUNT(*) total
    FROM jobs j
    WHERE EXISTS (
        SELECT 1
        FROM raw_jobs r
        WHERE r.raw_job_id = j.raw_job_id
          AND json_array_length(r.job_skills) > 0
    )
    AND NOT EXISTS (
        SELECT 1
        FROM job_skills js
        WHERE js.job_id = j.job_id
    );
    """,
    engine,
    ) 

    assert jobs_without_skills.iloc[0]["total"] == 0