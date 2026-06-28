# Data Engineer Technical Assessment

## 1. Overview

This repository contains the solution for the **Data Engineer Technical Assessment**.

The objective is to build an end-to-end ETL pipeline that ingests job posting data from a CSV file, stores the raw information in PostgreSQL, transforms it into a fully normalized Third Normal Form (3NF) relational model, and prepares the data for future analytical use.

The project follows common Data Engineering best practices including:

* Dockerized environment
* PostgreSQL database
* Python-based ETL
* Environment variables
* Logging
* Unit testing
* Data quality validation
* Modular project structure

---

# Project Structure

```
data-engineer-assessment/

│
├── data/  
│
├── logs/
│
├── sql/
│
├── app/ 
│     │   │
│     │   ├── ingestion/
│     │   ├── extract.py
│     │   ├── parser.py
│     │   └── loader.py
│     │
├     │   ── transform/
│     │   ├── companies.py
│     │   ├── locations.py
│     │   ├── skills.py
│     │   ├── jobs.py
│     │   ├── job_skills.py
│     │   └── job_type_skills.py
│     │
│     ├── database.py
│     ├── logger.py
│     └── main.py
│
sql/
│
└── 3nf_schema.sql

data/
│
└── data_jobs.csv
│
├── tests/
│
├── dbt/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Technology Stack

* Python 3.12
* PostgreSQL 16
* Docker Compose
* SQLAlchemy
* Pandas
* Pandera
* Pytest

---

## 2. Architecture Overview

The pipeline follows a layered architecture inspired by Medallion principles (simplified):

```
CSV
  ↓
RAW INGESTION (raw_jobs)
  ↓
TRANSFORMATION LAYER (3NF)
  ↓
NORMALIZED MODEL

companies → jobs → locations
jobs → job_skills / job_type_skills → skills
```

---

## 3. Design Principles

### Separation of Concerns
- Ingestion Layer: Extract + parsing + raw persistence
- Transformation Layer: Entity normalization (3NF)
- Load Layer: Batch inserts into PostgreSQL

### Raw Layer Strategy
- Preserves original dataset
- Enables reprocessing
- Provides auditability

### Normalization Strategy (3NF)
Entities:
- companies
- locations
- skills
- jobs

Relationships:
- job_skills
- job_type_skills

---

## 4. Handling Semi-Structured Data

### job_skills
- Parsed from list-like structure
- Expanded into atomic records
- Loaded into bridge table

### job_type_skills
- Dictionary-based structure
- Preserved for taxonomy analysis

---

## 5. Data Quality Strategy

- Timestamp normalization
- Text trimming
- Deduplication (companies, locations, skills)
- Referential integrity via FK constraints
- Safe parsing of malformed fields

---

## 6. Performance Considerations

- Batch inserts (chunksize=10000)
- Dictionary lookup for skills (O(1))
- Indexed foreign keys
- Pre-aggregation of relationships

---

## 7. Data Model (3NF)

### companies
- company_id (PK)
- company_name (UNIQUE)

### locations
- location_id (PK)
- job_location
- job_country

### skills
- skill_id (PK)
- skill_name

### jobs
- job_id (PK)
- raw_job_id (FK reference)
- company_id (FK)
- location_id (FK)
- salary fields
- job metadata

---

### job_skills
(PK: job_id, skill_id)

### job_type_skills
(PK: job_id, skill_id)

---

## 8. Data Volume

| Table | Records |
|------|--------:|
| raw_jobs | 785,741 |
| companies | 139,941 |
| locations | 23,783 |
| skills | 252 |
| jobs | 785,444 |
| job_skills | 3,593,556 |
| job_type_skills | 3,593,556 |

---

## 9. Orchestration

```bash
python -m app.main
```

Pipeline order:
1. Extract
2. Parse
3. Load raw
4. Transform entities
5. Load relationships

---

## 10. Key Design Decisions

- 3NF first approach (before OLAP modeling)
- Python ETL for flexibility
- Raw layer for reproducibility
- TRUNCATE + full reload for determinism

---

## 11. Analytical Model (Star Schema)

### Fact Table: fact_job_postings
- salary measures
- job metrics
- foreign keys to dimensions

### Dimensions
- dim_company
- dim_location
- dim_date
- dim_skill (via bridge)

### Bridge
- fact_job_skills

---

## 12. Future Improvements

- Incremental ingestion (CDC)
- dbt transformation layer
- Airflow orchestration
- Great Expectations validation
- CI/CD pipelines

---

## Environment Variables

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

## Continuous Integration

The project includes a GitHub Actions workflow located in:

```
.github/workflows/ci.yml
```

The pipeline automatically executes on every push and pull request.

It performs:

- Dependency installation
- Test execution with Pytest

This ensures that changes do not break the ETL pipeline.

## 13. Run Instructions

```bash
docker compose up --build
python -m app.main
```

---

## Author
Johan Cartagena