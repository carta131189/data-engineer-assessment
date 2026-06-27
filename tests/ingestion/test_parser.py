import pandas as pd

from app.ingestion.parser import (
    parse_json_columns,
    convert_dates,
    parse_dataframe,
)


def test_parse_json_columns(sample_dataframe):

    df = parse_json_columns(sample_dataframe.copy())

    assert isinstance(df.loc[0, "job_skills"], list)

    assert isinstance(df.loc[0, "job_type_skills"], dict)


def test_convert_dates(sample_dataframe):

    df = convert_dates(sample_dataframe.copy())

    assert pd.api.types.is_datetime64_any_dtype(
        df["job_posted_date"]
    )


def test_parse_dataframe(sample_dataframe):

    df = parse_dataframe(sample_dataframe.copy())

    assert isinstance(df.loc[0, "job_skills"], list)

    assert isinstance(df.loc[0, "job_type_skills"], dict)

    assert pd.api.types.is_datetime64_any_dtype(
        df["job_posted_date"]
    )