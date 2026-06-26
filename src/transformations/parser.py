import pandas as pd


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize date columns.
    """

    df["job_posted_date"] = pd.to_datetime(
        df["job_posted_date"],
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )

    return df