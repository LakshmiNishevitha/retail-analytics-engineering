from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

DBT_DIR = "/opt/airflow/dbt/retail_dbt"
DBT_PROFILES_DIR = "/home/airflow/.dbt"

with DAG(
    dag_id="retail_dbt_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["dbt", "retail"],
) as dag:

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {DBT_DIR} && dbt deps",
        env={"DBT_PROFILES_DIR": DBT_PROFILES_DIR},
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run",
        env={"DBT_PROFILES_DIR": DBT_PROFILES_DIR},
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test",
        env={"DBT_PROFILES_DIR": DBT_PROFILES_DIR},
    )

    dbt_deps >> dbt_run >> dbt_test
