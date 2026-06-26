from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config.settings import settings


def get_engine() -> Engine:

    connection_string = (
        f"postgresql+psycopg2://"
        f"{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:"
        f"{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )

    return create_engine(
        connection_string,
        echo=False,
        future=True
    )