from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import os

# Internal Docker URL for Python tasks - Points to WAREHOUSE
DB_URL = "postgresql+psycopg2://airflow:airflow@postgres:5432/warehouse"


def load_csv():
    engine = create_engine(DB_URL)
    file_path = "/opt/airflow/data/raw/transactions.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing file at {file_path}")
    df = pd.read_csv(file_path)
    # This creates stg_transactions in the WAREHOUSE database
    df.to_sql("stg_transactions", engine, if_exists="replace", index=False)


with DAG(
    "fmis_full_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    create_schema = PostgresOperator(
        task_id="create_schema",
        postgres_conn_id="postgres_default",
        database="warehouse",
        sql="""
        CREATE TABLE IF NOT EXISTS dim_account (account_key SERIAL PRIMARY KEY, account_code VARCHAR(20) UNIQUE);
        CREATE TABLE IF NOT EXISTS dim_department (dept_key SERIAL PRIMARY KEY, dept_id INT UNIQUE);
        CREATE TABLE IF NOT EXISTS fact_transactions (
            fact_key SERIAL PRIMARY KEY,
            transaction_id UUID UNIQUE NOT NULL,
            amount DECIMAL(18, 2),
            source_system VARCHAR(50)
        );
        """,
    )

    load_stg = PythonOperator(task_id="load_csv_to_stg", python_callable=load_csv)

    transform_data = PostgresOperator(
        task_id="stg_to_fact",
        postgres_conn_id="postgres_default",
        database="warehouse",
        sql="""
        INSERT INTO fact_transactions (transaction_id, amount, source_system)
        SELECT transaction_id::uuid, amount, 'CSV_IMPORT'
        FROM stg_transactions
        ON CONFLICT (transaction_id) DO NOTHING;
        """,
    )

    create_schema >> load_stg >> transform_data
