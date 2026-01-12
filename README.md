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
### Prerequisites

You need:

- Docker & Docker Compose

- Git

- A Snowflake account (for full dbt runs)


### Step 1 — Clone the repo

```bash
git clone https://github.com/LakshmiNishevitha/retail-analytics-engineering.git
cd retail-analytics-engineering
```

---

### Step 2 — Confirm Docker is installed

```bash
docker --version
docker compose version
```

---

### Step 3 — Set up Snowflake credentials (required for dbt build)

Your dbt profile should exist at:

```bash
cat ~/.dbt/profiles.yml
```

You should have a profile like `retail_dbt:` in that file.

Then set your Snowflake password as an environment variable:

### macOS / Linux

```bash
export SNOWFLAKE_PASSWORD="YOUR_PASSWORD"
```

### Windows (PowerShell)

```powershell
setx SNOWFLAKE_PASSWORD "YOUR_PASSWORD"
```

Validate dbt connection locally:

```bash
cd dbt/retail_dbt
dbt debug
cd ../../
```

---

### Step 4 — Start the platform (Airflow + Postgres + MailHog + dbt Docs)

From repo root:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

---

### Step 5 — Open the UIs

* **Airflow UI:** [http://localhost:8080](http://localhost:8080)
* **dbt Docs:** [http://localhost:8081](http://localhost:8081)
* **MailHog (email inbox):** [http://localhost:8025](http://localhost:8025)

---

### Step 6 — Trigger the Airflow DAG (runs dbt pipeline)

Trigger the pipeline:

```bash
docker exec -it airflow-webserver airflow dags trigger retail_dbt_daily_pipeline
```

List DAG runs (to see status):

```bash
docker exec -it airflow-webserver airflow dags list-runs -d retail_dbt_daily_pipeline -o table
```

List tasks in this DAG:

```bash
docker exec -it airflow-webserver airflow tasks list retail_dbt_daily_pipeline
```

---

### Step 7 — What the DAG does (in order)

Airflow orchestrates dbt commands in this order:

1. `dbt deps`
2. `dbt build`
3. `dbt docs generate`

---

### Step 8 — Run dbt manually (optional, without Airflow)

If someone wants to run dbt without Airflow:

```bash
cd dbt/retail_dbt
dbt deps
dbt build
dbt docs generate
dbt docs serve --port 8081 --no-browser
```

---

### Step 9 — Stop everything

```bash
docker compose down
```

---

### Step 10 — Rebuild cleanly (if something breaks)

```bash
docker compose down
docker compose up -d --build
```

---

### Step 11 — Check logs (debug)

```bash
docker logs --tail 80 airflow-webserver
docker logs --tail 80 airflow-scheduler
docker logs --tail 80 dbt-docs
```

---

### Explore the analytics models

Using dbt Docs, you can:

- View model lineage

- Understand table-level documentation

- Inspect tests and dependencies

- Explore staging and mart layers

- This makes the data warehouse self-documenting.

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

```
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