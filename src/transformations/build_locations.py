import pandas as pd


def build_locations(df: pd.DataFrame):

    locations = (

        df[
            [
                "job_location",
                "job_country"
            ]
        ]

        .drop_duplicates()

        .reset_index(drop=True)

    )

    locations.columns = [

        "location_name",
        "country"

    ]

    locations.insert(

        0,

        "location_id",

        range(

            1,

            len(locations) + 1

        )

    )

    return locations