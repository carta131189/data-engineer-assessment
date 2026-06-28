import pandera.pandas as pa
from pandera import Check
import pandas as pd


raw_jobs_schema = pa.DataFrameSchema(
    {
        "job_title": pa.Column(
            str,
            nullable=True,
        ),

        "job_title_short": pa.Column(
            str,
            nullable=True,
        ),

        "company_name": pa.Column(
            str,
            nullable=True,
            checks=[
              Check.str_length(
                min_value=1
              )
            ],
        ),

        "job_location": pa.Column(
            str,
            nullable=True,
        ),

        "job_country": pa.Column(
            str,
            nullable=True,
        ),

        "search_location": pa.Column(
            str,
            nullable=True,
        ),

        "salary_year_avg": pa.Column(
            float,
            nullable=True,
            coerce=True,
            checks=[
               Check.ge(0)
            ],
        ),

        "salary_hour_avg": pa.Column(
            float,
            nullable=True,
            coerce=True,
            checks=[
              Check.ge(0)
            ],
        ),

        "job_posted_date": pa.Column(
            pa.DateTime,
            nullable=True,
            checks=[
              Check(lambda s: s <= pd.Timestamp.now())
            ],
        ),
    },

    strict=False,
)