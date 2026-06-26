import pandas as pd


def build_jobs(
    df,
    companies,
    locations,
):

    jobs = df.copy()

    jobs = jobs.merge(

        companies,

        on="company_name",

        how="left",

    )

    jobs = jobs.merge(

        locations,

        left_on=[

            "job_location",

            "job_country"

        ],

        right_on=[

            "location_name",

            "country"

        ],

        how="left"

    )

    jobs = jobs[

        [

            "job_title",

            "job_title_short",

            "company_id",

            "location_id",

            "job_schedule_type",

            "job_work_from_home",

            "job_posted_date",

            "job_no_degree_mention",

            "job_health_insurance",

            "salary_rate",

            "salary_year_avg",

            "salary_hour_avg"

        ]

    ]

    jobs.insert(

        0,

        "job_id",

        range(

            1,

            len(jobs)+1

        )

    )

    return jobs