import time

from src.database.connection import get_engine
from src.database.create_tables import (
    create_raw_table,
    create_schema,
)
from src.utils.logger import configure_logger

logger = configure_logger()


def initialize_database():
    """
    Creates all required tables.
    """

    logger.info("Creating RAW table...")

    engine = get_engine()

    create_raw_table(engine)

    logger.info("RAW table created.")

    logger.info("Creating 3NF schema...")

    create_schema(engine)

    logger.info("3NF schema created.")

    return engine


def main():

    start_time = time.time()

    logger.info("=" * 70)
    logger.info("DATA ENGINEERING PIPELINE")
    logger.info("=" * 70)

    try:

        engine = initialize_database()

        logger.info("Database initialized successfully.")

        logger.info("Pipeline initialization completed.")

    except Exception as error:

        logger.exception(error)

        raise

    finally:

        elapsed = round(time.time() - start_time, 2)

        logger.info("=" * 70)
        logger.info(f"Execution finished in {elapsed} seconds.")
        logger.info("=" * 70)


if __name__ == "__main__":

    main()