import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    CSV_PATH = os.getenv("CSV_PATH")
    CSV_SEPARATOR = os.getenv("CSV_SEPARATOR", ";")
    CSV_ENCODING = os.getenv("CSV_ENCODING", "cp1252")