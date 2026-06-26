import pandera.pandas as pa
from pandera import Check


def validate_raw_jobs(df):
    """
    Validate dataframe before loading into PostgreSQL.
    """

    schema = pa.DataFrameSchema(
        {

            "job_title": pa.Column(
                str,
                nullable=False
            ),

            "company_name": pa.Column(
                str,
                nullable=True
            ),

            "job_country": pa.Column(
                str,
                nullable=True
            ),

            "job_work_from_home": pa.Column(
                bool,
                nullable=True
            ),

            "job_posted_date": pa.Column(
                pa.DateTime,
                nullable=True
            ),

            "salary_year_avg": pa.Column(
                float,
                nullable=True
            ),

            "salary_hour_avg": pa.Column(
                float,
                nullable=True
            ),

        },
        strict=False,
        coerce=True,
    )

    return schema.validate(df)