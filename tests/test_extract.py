import pandas as pd

from app.ingestion.extract import extract_csv


def test_extract_csv():

    df = extract_csv()

    assert isinstance(df, pd.DataFrame)

    assert len(df) > 0