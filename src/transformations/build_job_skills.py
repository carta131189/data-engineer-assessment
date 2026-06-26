import pandas as pd


def build_job_skills(
    jobs,
    skills,
    raw
):

    mapping = {

        row.skill_name: row.skill_id

        for _, row

        in skills.iterrows()

    }

    rows = []

    for idx, record in raw.iterrows():

        if record["job_skills"]:

            for skill in record["job_skills"]:

                rows.append(

                    [

                        jobs.loc[idx,"job_id"],

                        mapping[skill]

                    ]

                )

    return pd.DataFrame(

        rows,

        columns=[

            "job_id",

            "skill_id"

        ]

    )