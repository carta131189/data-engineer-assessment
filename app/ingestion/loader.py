import json

from sqlalchemy.types import BIGINT, JSON

from app.database import engine
from app.logger import logger


def load_raw_jobs(df):
    """
    Load raw_jobs table.
    """

    logger.info("Loading raw_jobs table...")

    df = df.copy()

    # ---------------------------------------------------------
    # Generate surrogate key
    # ---------------------------------------------------------

    df.insert(
        0,
        "raw_job_id",
        range(1, len(df) + 1)
    )

    # ---------------------------------------------------------
    # Convert JSON columns
    # ---------------------------------------------------------

    df["job_skills"] = df["job_skills"].apply(json.dumps)

    df["job_type_skills"] = df["job_type_skills"].apply(json.dumps)


    print(df.dtypes)

    print(df["job_posted_date"].dtype)

    print(df["job_posted_date"].head())
    # ---------------------------------------------------------
    # Load table
    # ---------------------------------------------------------

    df.to_sql(
        name="raw_jobs",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={
            "raw_job_id": BIGINT,
            "job_skills": JSON,
            "job_type_skills": JSON,
        },
    )

    logger.info(
        f"raw_jobs loaded successfully: {len(df)} rows."
    )


if __name__ == "__main__":
    from app.ingestion.extract import extract_csv
    from app.ingestion.parser import parse_json_columns

    df = extract_csv()
    df = parse_json_columns(df)
    load_raw_jobs(df)