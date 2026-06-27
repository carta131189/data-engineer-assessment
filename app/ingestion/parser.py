import ast
import pandas as pd


JSON_COLUMNS = [
    "job_skills",
    "job_type_skills",
]


def parse_json_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse semi-structured columns.
    """

    for column in JSON_COLUMNS:

        def parser(value):

            if pd.isna(value):
                return None

            try:
                return ast.literal_eval(value)

            except Exception:
                return None

        df[column] = df[column].apply(parser)

    return df


def convert_dates(df: pd.DataFrame):

    df["job_posted_date"] = pd.to_datetime(
        df["job_posted_date"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
        
    )

    return df


def parse_dataframe(df: pd.DataFrame):

    df = parse_json_columns(df)

    df = convert_dates(df)

    return df