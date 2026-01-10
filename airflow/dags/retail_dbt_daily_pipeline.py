from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

DBT_DIR = "/opt/airflow/dbt/retail_dbt"
DBT_BIN = "/home/airflow/.local/bin/dbt"

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),

    # Email alerts (MailHog)
    "email": ["test@local"],
    "email_on_failure": True,
    "email_on_retry": True,
}

with DAG(
    dag_id="retail_dbt_daily_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,   # keep manual while developing
    catchup=False,
    tags=["dbt", "retail"],
) as dag:

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f'bash -lc "cd {DBT_DIR} && {DBT_BIN} deps"',
    )

    # ✅ Best practice: single command to run + test (+ seeds/snapshots if defined)
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f'bash -lc "cd {DBT_DIR} && {DBT_BIN} build"',
    )

    # ✅ Generate docs only after build succeeds
    dbt_docs_generate = BashOperator(
        task_id="dbt_docs_generate",
        bash_command=f'bash -lc "cd {DBT_DIR} && {DBT_BIN} docs generate"',
    )

    dbt_deps >> dbt_build >> dbt_docs_generate

