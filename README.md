# Data Engineer Technical Assessment

## Overview

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
├── diagrams/
│
├── logs/
│
├── sql/
│
├── src/
│
├── tests/
│
├── .github/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── main.py
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

# Architecture

The project follows a layered ETL architecture.

```
CSV

↓

Raw Ingestion

↓

Raw Table

↓

Transformation Layer

↓

3NF Relational Model

↓

Data Quality Validation

↓

Unit Tests
```

Keeping a RAW layer allows the original data to remain unchanged, making the pipeline reproducible, auditable, and easier to maintain.

---

# Development Status

## Phase 1

Project initialization.

Completed:

* Project structure
* Docker environment
* PostgreSQL configuration
* Environment variables
* Dependencies
* Git repository initialization

Next:

* Database connection
* Raw ingestion
* 3NF implementation

---

# How to Run

Clone the repository.

Create a `.env` file using `.env.example`.

Build the containers:

```bash
docker compose up --build
```

---

# Author

Johan Cartagena
