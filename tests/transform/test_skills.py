import pandas as pd

from app.database import engine
from app.transform.skills import load_skills


def test_load_skills():

    load_skills()

    skills = pd.read_sql(
        "SELECT * FROM skills;",
        engine,
    )

    assert not skills.empty


def test_skill_name_not_null():

    skills = pd.read_sql(
        """
        SELECT *
        FROM skills
        WHERE skill_name IS NULL;
        """,
        engine,
    )

    assert skills.empty


def test_skill_name_not_empty():

    skills = pd.read_sql(
        """
        SELECT *
        FROM skills
        WHERE TRIM(skill_name) = '';
        """,
        engine,
    )

    assert skills.empty


def test_skills_are_unique():

    duplicates = pd.read_sql(
        """
        SELECT
            skill_name,
            COUNT(*) total
        FROM skills
        GROUP BY skill_name
        HAVING COUNT(*) > 1;
        """,
        engine,
    )

    assert duplicates.empty


def test_expected_columns():

    skills = pd.read_sql(
        "SELECT * FROM skills LIMIT 1;",
        engine,
    )

    expected_columns = {
        "skill_id",
        "skill_name",
    }

    assert expected_columns.issubset(skills.columns)