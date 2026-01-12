# Retail Analytics Engineering

## What is this project?

This project is an end-to-end Analytics Engineering platform that demonstrates how raw retail data can be transformed into analytics-ready tables using modern data engineering tools.

It showcases a real-world workflow where:

- **dbt** is used to model, test, and document data
- **Apache Airflow** orchestrates dbt transformations
- **Snowflake** serves as the cloud data warehouse
- **GitHub Actions** provides safe Continuous Integration (CI)
- **Docker** enables reproducible local development


---
## Why does this project exist?

Analytics teams often struggle with:

- Unstructured SQL logic

- Manual data refreshes

- Poor documentation

- No automated validation

- Fragile pipelines that break silently

This project exists to demonstrate best practices that solve those problems:

- Modular data modeling using dbt (staging → marts)

- Automated orchestration with Airflow instead of manual runs

- Built-in testing and documentation via dbt

- Safe CI checks that validate dbt projects on every commit

- Production-style project structure suitable for team collaboration

In short, this project shows how analytics engineering should be done, not just how to write SQL.

## How to use this project?
### 1. Prerequisites

You need:

- Docker & Docker Compose

- Git

- A Snowflake account (for full dbt runs)

### 2. Run the platform locally

From the project root:

docker compose up -d --build


This will start:

Airflow Webserver

Airflow Scheduler

PostgreSQL (Airflow metadata DB)

dbt Docs service

### 3. Access the interfaces

Airflow UI: http://localhost:8080

dbt Docs: http://localhost:8081

### 4. Trigger the analytics pipeline

You can trigger the dbt workflow via Airflow:

docker exec -it airflow-webserver airflow dags trigger retail_dbt_daily_pipeline


The DAG performs:

dbt deps

dbt build

dbt docs generate

### 5. Explore the analytics models

Using dbt Docs, you can:

View model lineage

Understand table-level documentation

Inspect tests and dependencies

Explore staging and mart layers

This makes the data warehouse self-documenting.

---

## Architecture Overview

**Tech Stack**
- **dbt** – SQL transformations, tests, documentation
- **Apache Airflow** – Orchestration of dbt workflows
- **Snowflake** – Cloud data warehouse
- **GitHub Actions** – CI (safe, parse-only)
- **Docker** – Local development environment

**High-level flow:**

Raw Data → dbt Staging → dbt Marts → dbt Tests  
⬇  
Airflow DAG orchestrates dbt runs  
⬇  
dbt Docs generated and served  
⬇  
CI validates dbt models on every commit

---

## Project Structure

```text
.
├── dags/                     # Airflow DAGs
│   └── retail_dbt_daily_pipeline.py
├── dbt/
│   └── retail_dbt/
│       ├── models/
│       │   ├── staging/
│       │   ├── marts/
│       ├── snapshots/
│       ├── tests/
│       └── dbt_project.yml
├── .github/
│   └── workflows/
│       └── dbt-ci.yml         # CI (parse-only)
├── docker-compose.yml
└── README.md
---

## Continuous Integration (CI)

This project uses GitHub Actions for CI.

What CI does

Runs dbt deps

Runs dbt parse

Validates SQL, model references, and schema files

Why parse-only CI?

No Snowflake credentials required

No warehouse costs

No risk of leaking secrets

Fast feedback on pull requests

CI ensures that broken dbt changes are caught before they reach production.

---

## Key Takeaways

This project demonstrates:

Analytics engineering best practices

dbt model layering and testing

Orchestration with Apache Airflow

Safe CI design for data projects

Production-ready repository structure

It is designed as a portfolio project that reflects real-world analytics engineering workflows.
---