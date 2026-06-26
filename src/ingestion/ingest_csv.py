import pandas as pd


def read_csv(path: str, chunksize: int = 10000):
    """
    Read CSV in chunks.
    """

    return pd.read_csv(
        filepath_or_buffer=path,
        sep=";",
        encoding="utf-8",
        quotechar='"',
        low_memory=False,
        chunksize=chunksize,
    )