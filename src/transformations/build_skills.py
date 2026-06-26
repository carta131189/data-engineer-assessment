import pandas as pd


def build_skills(df):

    skills = []

    for row in df["job_skills"]:

        if row:

            skills.extend(row)

    skills = sorted(set(skills))

    skills = pd.DataFrame(

        {

            "skill_name": skills

        }

    )

    skills.insert(

        0,

        "skill_id",

        range(

            1,

            len(skills)+1

        )

    )

    return skills