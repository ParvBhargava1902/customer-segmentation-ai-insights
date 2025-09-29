"""Airflow DAG: daily ETL → Train/Score → Publish
Note: Replace 'bash_command' paths with your environment paths.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "analytics",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="churn_etl_train_score",
    default_args=default_args,
    description="Daily churn scoring pipeline",
    schedule_interval="0 3 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["churn","voc","tableau"],
) as dag:

    etl = BashOperator(
        task_id="etl_and_train",
        bash_command="python3 /path/to/repo/etl_churn_model.py",
    )

    publish = BashOperator(
        task_id="publish_scores",
        bash_command="cp /path/to/repo/out/churn_scores.csv /path/to/tableau/drop/churn_scores.csv",
    )

    etl >> publish
