import io
import json

import pandas as pd


def load_raw(df: pd.DataFrame, conn):
    """
    Bulk load a DataFrame into PostgreSQL using COPY.
    """

    df = df.copy()

    # Convert Python objects into JSON strings
    for column in ["job_skills", "job_type_skills"]:

        df[column] = df[column].apply(
            lambda value: json.dumps(value)
            if value is not None
            else None
        )

    buffer = io.StringIO()

    df.to_csv(
        buffer,
        sep="\t",
        header=False,
        index=False,
        na_rep="\\N",
    )

    buffer.seek(0)

    cursor = conn.cursor()

    cursor.copy_from(
        file=buffer,
        table="raw_jobs",
        sep="\t",
        null="\\N",
        columns=list(df.columns),
    )

    conn.commit()

    cursor.close()