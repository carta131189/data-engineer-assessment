import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe():
    """
    Sample dataframe used across unit tests.
    """

    return pd.DataFrame(
        {
            "job_title": ["Data Engineer"],
            "job_title_short": ["Data Engineer"],
            "company_name": ["OpenAI"],
            "job_location": ["Medellín"],
            "job_country": ["Colombia"],
            "job_skills": ["['Python', 'SQL']"],
            "job_type_skills": [
                "{'Programming': ['Python'], 'Database': ['SQL']}"
            ],
            "job_posted_date": ["25/06/2026 10:30"],
            "salary_year_avg": [80000],
            "salary_hour_avg": [40],

            "job_work_from_home": [True],
            "job_no_degree_mention": [False],
            "job_health_insurance": [True],
        }
    )