from pathlib import Path

import pandas as pd

from app.config import Config
from app.logger import logger


def extract_csv() -> pd.DataFrame:

    logger.info("Reading CSV file...")

    file_path = Path(Config.CSV_PATH)

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1",
        "iso-8859-1",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
    ]

    last_error = None

    for encoding in encodings:

        try:

            logger.info(f"Trying encoding: {encoding}")

            df = pd.read_csv(
                file_path,
                sep=";",
                encoding=encoding,
            )

            logger.info(f"Encoding detected: {encoding}")
            logger.info(f"Rows loaded: {len(df)}")

            return df

        except Exception as e:
            last_error = e

    raise RuntimeError(
        f"Could not read CSV with any supported encoding.\n{last_error}"
    )