from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import psycopg2

from src.config.settings import settings


def get_engine() -> Engine:
    """
    SQLAlchemy Engine
    """

    url = (
        f"postgresql+psycopg2://"
        f"{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_DB}"
    )

    return create_engine(
        url,
        pool_pre_ping=True,
        future=True,
    )


def get_psycopg_connection():
    """
    psycopg2 connection used by COPY.
    """

    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )