# Data Engineer Technical Assessment – End-to-End ETL Pipeline

End-to-end ETL pipeline that ingests raw job posting data, validates data quality, transforms it into a normalized 3NF PostgreSQL schema, and lays the foundation for analytical modeling using a Star Schema.

## 1. Overview

This repository contains the solution for the **Data Engineer Technical Assessment**.

The objective is to build an end-to-end ETL pipeline that ingests job posting data from a CSV file, stores the raw information in PostgreSQL, transforms it into a fully normalized Third Normal Form (3NF) relational model, and prepares the data for future analytical workloads.

The project follows Data Engineering best practices, including:

- Dockerized environment
- PostgreSQL database
- Python-based ETL pipeline
- Environment variable configuration
- Logging
- Data quality validation with Pandera
- Unit testing with Pytest
- Continuous Integration using GitHub Actions
- Modular and maintainable project structure

---

# 2. Technology Stack

- Python 3.12
- PostgreSQL 16
- Docker & Docker Compose
- SQLAlchemy
- Pandas
- Pandera
- Pytest
- GitHub Actions

---

# 3. Project Structure

```text
data-engineer-assessment/

├── app/
│   ├── ingestion/
│   │   ├── extract.py
│   │   ├── parser.py
│   │   └── loader.py
│   │
│   ├── transform/
│   │   ├── companies.py
│   │   ├── locations.py
│   │   ├── skills.py
│   │   ├── jobs.py
│   │   ├── job_skills.py
│   │   └── job_type_skills.py
│   │
│   ├── quality/
│   │   ├── raw_jobs_schema.py
│   │   └── validator.py
│   │
│   ├── database.py
│   ├── config.py
│   ├── logger.py
│   └── main.py
│
├── sql/
│   └── 3nf_schema.sql
│
├── data/
│   └── data_jobs.csv
│
├── tests/
│
├── logs/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 4. Architecture Overview

The pipeline follows a layered architecture inspired by the Medallion approach.

```text
CSV File
    │
    ▼
Raw Ingestion
(raw_jobs)
    │
    ▼
Data Quality Validation
(Pandera)
    │
    ▼
Transformation Layer
(3NF Model)
    │
    ▼
Normalized Relational Database
    │
    ▼
Future Analytical Layer
(Star Schema)
```

Keeping a RAW layer preserves the original dataset, making the pipeline reproducible, auditable, and easier to maintain.

---

# 5. ETL Pipeline

The ETL process is executed through the main entry point:

```bash
python -m app.main
```

Execution flow:

1. CSV extraction
2. Encoding detection
3. JSON parsing
4. Date conversion
5. Numeric conversion
6. Boolean conversion
7. Data quality validation (Pandera)
8. Raw table loading
9. 3NF transformations
10. Relationship loading

---

# 6. Data Quality

Before loading the data into PostgreSQL, the ingestion layer validates the dataset using **Pandera**.

Current validation rules include:

- Schema validation
- Timestamp validation
- Numeric field validation
- Boolean field validation
- Text normalization
- Safe JSON parsing
- Duplicate removal
- Referential integrity through foreign keys

These validations ensure malformed or inconsistent records are detected before entering the relational model.

---

# 7. Database Design (3NF)

The operational database is modeled in **Third Normal Form (3NF)** to eliminate redundancy and preserve referential integrity.

## Main Entities

### companies

- company_id (PK)
- company_name (UNIQUE)

---

### locations

- location_id (PK)
- job_location
- job_country
- search_location

---

### skills

- skill_id (PK)
- skill_name

---

### jobs

- job_id (PK)
- raw_job_id
- company_id (FK)
- location_id (FK)

Additional attributes:

- job_title
- job_title_short
- job_schedule_type
- work_from_home
- salary_year_avg
- salary_hour_avg
- posted_date

---

### job_skills

Many-to-many relationship.

Composite Primary Key:

```
(job_id, skill_id)
```

---

### job_type_skills

Many-to-many relationship extracted from the structured JSON field.

Composite Primary Key:

```
(job_id, skill_id)
```

---

# 8. Conceptual OLAP Model (Star Schema)

Although the ETL pipeline delivers a normalized relational model (3NF), analytical workloads are typically served through a dimensional model.

The following conceptual Star Schema would be built downstream from the normalized database.

---

## Fact Table

### fact_job_postings

**Granularity**

One row represents one job posting.

### Foreign Keys

- company_id
- location_id
- date_id
- job_flags_id

### Measures

- salary_year_avg
- salary_hour_avg
- total_jobs

---

## Dimensions

### dim_company

- company_id
- company_name

---

### dim_location

- location_id
- job_location
- job_country
- search_location

---

### dim_date

- date_id
- full_date
- year
- quarter
- month
- week
- day
- weekday

---

### dim_skill

- skill_id
- skill_name

---

## Bridge Table

### bridge_job_skill

Because one job can require multiple skills and one skill can belong to multiple jobs, a bridge table is required.

Columns:

- job_id
- skill_id

This enables analyses such as:

- Most requested skills
- Skills by company
- Skills by location
- Skills by salary range

---

## Junk Dimension

Boolean attributes with low cardinality can be grouped into a Junk Dimension.

### dim_job_flags

Attributes:

- job_flags_id
- work_from_home
- no_degree_mention
- health_insurance

Benefits:

- Reduces redundancy
- Simplifies filtering
- Improves dimensional modeling

---

## Conceptual Star Schema

```text
                    dim_company
                         │
                         │
dim_location ─── fact_job_postings ─── dim_date
                         │
                         │
                  bridge_job_skill
                         │
                    dim_skill

                 dim_job_flags
                         │
                         │
                 fact_job_postings
```

---

## Analytical Use Cases

The dimensional model supports analyses such as:

- Number of job postings by country
- Hiring trends over time
- Average salary by company
- Average salary by location
- Remote vs On-site job distribution
- Health insurance availability
- No-degree-required opportunities
- Most demanded technical skills
- Salary trends by skill
- Top-paying technologies

---

## Why 3NF for ETL and Star Schema for BI?

The operational database uses **Third Normal Form (3NF)** to minimize redundancy, maintain referential integrity, and simplify transactional operations.

For Business Intelligence and OLAP workloads, a **Star Schema** provides faster query performance, fewer joins, and a structure optimized for analytical reporting.

The dimensional model would therefore be generated as a downstream layer from the normalized relational database.

---

# 9. Performance Considerations

Several optimizations were implemented to improve scalability:

- Batch inserts using `to_sql(method="multi")`
- Chunked loading
- Dictionary lookups (O(1))
- Indexed foreign keys
- Composite primary keys
- Duplicate removal before inserts
- Full transactional loads

---

# 10. Testing

The project includes automated unit tests using **Pytest**.

Current coverage includes:

- CSV extraction
- JSON parsing
- Date conversion
- Boolean conversion
- Data quality validation
- Entity transformations
- Referential integrity
- Many-to-many relationships

Run all tests:

```bash
pytest
```

Run a specific module:

```bash
pytest tests/transform/test_jobs.py -v
```

---

# 11. Continuous Integration

A GitHub Actions workflow is included under:

```text
.github/workflows/ci.yml
```

The workflow automatically executes on every push and pull request.

Pipeline steps include:

- Python setup
- Dependency installation
- Test execution with Pytest

This ensures new changes do not introduce regressions into the ETL pipeline.

---

# 12. Data Volume

| Table | Records |
|--------|---------:|
| raw_jobs | 785,741 |
| companies | 139,941 |
| locations | 23,783 |
| skills | 252 |
| jobs | 785,444 |
| job_skills | 3,593,556 |
| job_type_skills | 3,593,556 |

---

# 13. Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_engineer
DB_USER=postgres
DB_PASSWORD=postgres

CSV_PATH=data/data_jobs.csv
```

---

# 14. Future Improvements

Potential enhancements include:

- Incremental loading (CDC)
- Apache Airflow orchestration
- dbt analytical models
- Great Expectations integration
- Slowly Changing Dimensions (SCD)
- Data Warehouse implementation
- Power BI / Tableau dashboards

---

# 15. Run Instructions

Clone the repository.

```bash
git clone <repository-url>
cd data-engineer-assessment
```

Create the environment file.

```bash
cp .env.example .env
```

Build the containers.

```bash
docker compose up --build
```

Execute the ETL pipeline.

```bash
python -m app.main
```

Run all tests.

```bash
pytest
```

---

# Author

**Johan Cartagena**