from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)