import pandas as pd

from app.ingestion.extract import extract_csv


def test_extract_csv_returns_dataframe():

    df = extract_csv()

    assert isinstance(df, pd.DataFrame)


def test_extract_csv_is_not_empty():

    df = extract_csv()

    assert not df.empty


def test_extract_csv_expected_columns():

    df = extract_csv()

    expected_columns = [
        "job_title",
        "company_name",
        "job_skills",
        "job_type_skills",
        "job_posted_date",
    ]

    for column in expected_columns:
        assert column in df.columns