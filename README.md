# Retail Analytics Engineering

An end-to-end Analytics Engineering project demonstrating how raw retail data is transformed into analytics-ready tables using dbt, orchestrated with Apache Airflow, documented via dbt Docs, and validated using CI with GitHub Actions.

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
