from app.ingestion.extract import extract_csv
from app.ingestion.parser import parse_dataframe
from app.ingestion.loader import load_raw_jobs

from app.logger import logger

from app.transform.companies import load_companies
from app.transform.locations import load_locations
from app.transform.skills import load_skills
from app.transform.jobs import load_jobs
from app.transform.job_skills import load_job_skills
from app.transform.job_type_skills import load_job_type_skills


def main():

    logger.info("=" * 60)
    logger.info("DATA ENGINEER TECHNICAL ASSESSMENT")
    logger.info("=" * 60)

    # =====================================================
    # PHASE 1 - RAW INGESTION
    # =====================================================

    logger.info("Phase 1 - Raw Ingestion")

    df = extract_csv()

    df = parse_dataframe(df)

    load_raw_jobs(df)

    logger.info("Phase 1 completed.")

    # =====================================================
    # PHASE 2 - 3NF TRANSFORMATION
    # =====================================================

    logger.info("=" * 60)
    logger.info("Phase 2 - 3NF Transformation")

    load_companies()

    load_locations()

    load_skills()

    load_jobs()

    load_job_skills()

    load_job_type_skills()

    logger.info("Phase 2 completed.")

    logger.info("=" * 60)
    logger.info("Pipeline completed successfully.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()