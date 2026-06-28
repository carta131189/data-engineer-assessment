import pandas as pd

from app.database import engine
from app.transform.jobs import load_jobs


def test_load_jobs():

    load_jobs()

    jobs = pd.read_sql(
        "SELECT * FROM jobs;",
        engine,
    )

    assert not jobs.empty


def test_expected_columns():

    jobs = pd.read_sql(
        "SELECT * FROM jobs LIMIT 1;",
        engine,
    )

    expected_columns = {
        "job_id",
        "raw_job_id",
        "company_id",
        "location_id",
        "job_title",
        "job_title_short",
        "job_via",
        "job_schedule_type",
        "job_work_from_home",
        "job_posted_date",
        "job_no_degree_mention",
        "job_health_insurance",
        "salary_rate",
        "salary_year_avg",
        "salary_hour_avg",
    }

    assert expected_columns.issubset(jobs.columns)


def test_raw_job_id_unique():

    duplicates = pd.read_sql(
        """
        SELECT
            raw_job_id,
            COUNT(*) total
        FROM jobs
        GROUP BY raw_job_id
        HAVING COUNT(*) > 1;
        """,
        engine,
    )

    assert duplicates.empty


def test_company_fk_integrity():

    invalid = pd.read_sql(
        """
        SELECT j.job_id
        FROM jobs j
        LEFT JOIN companies c
            ON j.company_id = c.company_id
        WHERE c.company_id IS NULL;
        """,
        engine,
    )

    assert invalid.empty


def test_location_fk_integrity():

    invalid = pd.read_sql(
        """
        SELECT j.job_id
        FROM jobs j
        LEFT JOIN locations l
            ON j.location_id = l.location_id
        WHERE l.location_id IS NULL;
        """,
        engine,
    )

    assert invalid.empty


def test_salary_columns_are_numeric():

    jobs = pd.read_sql(
        """
        SELECT
            salary_year_avg,
            salary_hour_avg
        FROM jobs;
        """,
        engine,
    )

    assert pd.api.types.is_numeric_dtype(jobs["salary_year_avg"])

    assert pd.api.types.is_numeric_dtype(jobs["salary_hour_avg"])


def test_jobs_have_company_and_location():

    invalid = pd.read_sql(
        """
        SELECT *
        FROM jobs
        WHERE company_id IS NULL
           OR location_id IS NULL;
        """,
        engine,
    )

    assert invalid.empty