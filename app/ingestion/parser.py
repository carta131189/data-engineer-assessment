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

NUMERIC_COLUMNS = [
    "salary_year_avg",
    "salary_hour_avg",
]


def convert_numeric(df: pd.DataFrame):

    for column in NUMERIC_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


BOOLEAN_COLUMNS = [
    "job_work_from_home",
    "job_no_degree_mention",
    "job_health_insurance",
]


def convert_booleans(df: pd.DataFrame) -> pd.DataFrame:
    for column in BOOLEAN_COLUMNS:
        df[column] = df[column].astype("boolean")  # dtype booleano nullable de pandas
    return df


def parse_dataframe(df: pd.DataFrame):

    df = parse_json_columns(df)

    df = convert_numeric(df)

    df = convert_dates(df)

    df = convert_booleans(df)

    return df