from sqlalchemy import text

from src.database.connection import get_engine
from src.utils.logger import configure_logger


logger = configure_logger()


def main():

    logger.info("Starting pipeline...")

    engine = get_engine()

    with engine.connect() as connection:

        connection.execute(text("SELECT 1"))

    logger.info("Database connection successful.")

    logger.info("Pipeline finished successfully.")


if __name__ == "__main__":

    main()