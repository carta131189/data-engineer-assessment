import pandas as pd

from app.database import engine
from app.transform.locations import load_locations


def test_load_locations():

    load_locations()

    locations = pd.read_sql(
        "SELECT * FROM locations;",
        engine,
    )

    assert not locations.empty


def test_location_table_has_expected_columns():

    locations = pd.read_sql(
        "SELECT * FROM locations LIMIT 1;",
        engine,
    )

    expected_columns = {
        "location_id",
        "job_location",
        "job_country",
        "search_location",
    }

    assert expected_columns.issubset(locations.columns)


def test_locations_are_unique():

    duplicates = pd.read_sql(
        """
        SELECT
            job_location,
            job_country,
            search_location,
            COUNT(*) total
        FROM locations
        GROUP BY
            job_location,
            job_country,
            search_location
        HAVING COUNT(*) > 1;
        """,
        engine,
    )

    assert duplicates.empty