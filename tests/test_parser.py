import pandas as pd

from app.ingestion.parser import (
    parse_json_columns,
    convert_dates,
)


def test_parse_job_skills():

    df = pd.DataFrame(
        {
            "job_skills": ["['Python', 'SQL']"],
            "job_type_skills": ['{"Programming":["Python"]}']
        }
    )

    result = parse_json_columns(df)

    assert isinstance(result.loc[0, "job_skills"], list)
    assert result.loc[0, "job_skills"] == ["Python", "SQL"]


def test_parse_job_type_skills():

    df = pd.DataFrame(
        {
            "job_skills": ["[]"],
            "job_type_skills": ['{"Programming":["Python","SQL"]}']
        }
    )

    result = parse_json_columns(df)

    assert isinstance(result.loc[0, "job_type_skills"], dict)
    assert "Programming" in result.loc[0, "job_type_skills"]


def test_invalid_json_returns_none():

    df = pd.DataFrame(
        {
            "job_skills": ["INVALID"],
            "job_type_skills": ["INVALID"]
        }
    )

    result = parse_json_columns(df)

    assert result.loc[0, "job_skills"] is None
    assert result.loc[0, "job_type_skills"] is None


def test_convert_dates():

    df = pd.DataFrame(
        {
            "job_posted_date": [
                "2024-01-15 08:30:00"
            ]
        }
    )

    result = convert_dates(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["job_posted_date"]
    )