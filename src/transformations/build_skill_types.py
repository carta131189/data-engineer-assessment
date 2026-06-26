import pandas as pd


def build_skill_types(df):

    types = []

    for row in df["job_type_skills"]:

        if row:

            types.extend(

                row.keys()

            )

    types = sorted(

        set(types)

    )

    types = pd.DataFrame(

        {

            "skill_type_name": types

        }

    )

    types.insert(

        0,

        "skill_type_id",

        range(

            1,

            len(types)+1

        )

    )

    return types