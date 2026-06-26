import pandas as pd


def build_companies(df: pd.DataFrame):

    companies = (
        df[["company_name"]]
        .dropna()
        .drop_duplicates()
        .reset_index(drop=True)
    )

    companies.insert(
        0,
        "company_id",
        range(1, len(companies) + 1),
    )

    return companies