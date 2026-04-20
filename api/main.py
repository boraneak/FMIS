from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd

app = FastAPI(title="FMIS Financial API")

# Use the same warehouse DB we built with Airflow
DB_URL = "postgresql://airflow:airflow@localhost:5433/warehouse"
engine = create_engine(DB_URL)


@app.get("/kpi/budget-vs-actual")
def get_budget_vs_actual():
    query = """
    SELECT 
        TO_CHAR(ingested_at, 'YYYY-MM') as month,
        SUM(amount) as actual_spend,
        500000000 as monthly_budget -- Mock budget for now
    FROM fact_transactions
    GROUP BY month
    ORDER BY month;
    """

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    # Calculate Variance
    df["variance"] = df["monthly_budget"] - df["actual_spend"]

    return df.to_dict(orient="records")


@app.get("/health")
def health_check():
    return {"status": "online", "warehouse": "connected"}
