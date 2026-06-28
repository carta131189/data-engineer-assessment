from pandera.errors import SchemaError

from app.logger import logger
from app.quality.raw_jobs_schema import raw_jobs_schema


def validate_raw_jobs(df):

    logger.info("Running Pandera validation...")

    try:

        validated = raw_jobs_schema.validate(df)

        logger.info("Data quality validation passed.")

        return validated

    except SchemaError as e:

        logger.error("Data quality validation failed.")

        raise e