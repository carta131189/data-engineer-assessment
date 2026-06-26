import pandas as pd


def build_skill_skill_types(
    raw: pd.DataFrame,
    skills: pd.DataFrame,
    skill_types: pd.DataFrame,
):

    skill_lookup = dict(
        zip(
            skills.skill_name,
            skills.skill_id,
        )
    )

    type_lookup = dict(
        zip(
            skill_types.skill_type_name,
            skill_types.skill_type_id,
        )
    )

    rows = []

    for value in raw["job_type_skills"]:

        if value is None:
            continue

        for skill_type, skill_list in value.items():

            for skill in skill_list:

                rows.append(
                    (
                        skill_lookup[skill],
                        type_lookup[skill_type],
                    )
                )

    df = pd.DataFrame(
        rows,
        columns=[
            "skill_id",
            "skill_type_id",
        ],
    )

    return (
        df.drop_duplicates()
        .reset_index(drop=True)
    )