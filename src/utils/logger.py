import logging
import os


def configure_logger() -> logging.Logger:
    """
    Configure application logger.
    """

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("data-engineering")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        "logs/pipeline.log"
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger