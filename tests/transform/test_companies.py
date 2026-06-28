import pandas as pd

from app.database import engine
from app.transform.companies import load_companies


def test_load_companies():

    load_companies()

    companies = pd.read_sql(
        "SELECT * FROM companies;",
        engine,
    )

    assert not companies.empty


def test_company_name_not_null():

    companies = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE company_name IS NULL;
        """,
        engine,
    )

    assert companies.empty


def test_company_names_are_unique():

    duplicates = pd.read_sql(
        """
        SELECT
            company_name,
            COUNT(*) total
        FROM companies
        GROUP BY company_name
        HAVING COUNT(*) > 1;
        """,
        engine,
    )

    assert duplicates.empty