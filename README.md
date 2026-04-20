# Financial Management Information System - FMIS

A professional-grade, automated data pipeline for financial intelligence. This project demonstrates a complete Modern Data Stack (MDS) implementation, transitioning raw financial data into actionable JSON KPIs.

## 🏗 Architecture
This system integrates five core components to handle data from ingestion to visualization:

1.  **Orchestration:** Apache Airflow manages the ETL lifecycle and task dependencies.
2.  **Storage:** PostgreSQL (Dockerized) serves as the Data Warehouse with a dedicated `warehouse` database.
3.  **Ingestion:** Python & SQLAlchemy logic utilizing "Upsert" operations to ensure data integrity.
4.  **API Layer:** FastAPI provides a high-performance interface for real-time financial KPIs.
5.  **Analytics:** Metabase provides the visualization layer for executive dashboards.

## 🛠 Tech Stack
- **Languages:** Python 3.13, SQL
- **Frameworks:** Apache Airflow 2.7.1, FastAPI, SQLAlchemy 2.0
- **Database:** PostgreSQL 15 (Alpine)
- **Infrastructure:** Docker, Docker Compose
- **Libraries:** Pandas, Faker, Psycopg2-binary

## 🚦 Getting Started

### 1. Environment Setup
Create a `.env` file in the root directory to manage secrets (this file is ignored by git):
```text
AIRFLOW_UID=1000
AIRFLOW_FERNET_KEY=your_generated_fernet_key
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
```

### 2. Launch Infrastructure
Spin up the Docker containers (Postgres, Airflow, Redpanda, Metabase):
```
docker-compose up -d
```

### 3. Run the ETL Pipeline
```
1. Access the Airflow UI at http://localhost:8080.

2. Ensure the postgres_default connection is configured for the warehouse database.

3. Trigger the fmis_full_pipeline DAG.

4. This will process 10,000 transaction records from CSV into the fact_transactions table.

```

### 4. Serve the KPI API
Run the FastAPI service from your local virtual environment:
```
uvicorn api.main:app --reload
```
View the live JSON KPI: ```http://127.0.0.1:8000/kpi/budget-vs-actual```

## 🧪 Data Validation & Integrity

- Row Count: Verified 10,000 source rows vs 10,000 warehouse rows.
- Idempotency: The pipeline uses ON CONFLICT DO NOTHING logic, allowing for safe re-runs without data duplication.
- Port Mapping: Internal Docker traffic uses 5432, while external host access (API/PSQL) uses 5433.

## 📂 Project Structure

- `api/`             # FastAPI application and KPI endpoints
- `dags/`            # Airflow Directed Acyclic Graphs (ETL logic)
- `data/`            # Source files (CSV) and data volume mapping
- `include/`         # External scripts or helper SQL files
- `init-db/`         # Postgres initialization scripts for warehouse setup
- `logs/`            # Airflow execution logs (git-ignored)
- `plugins/`         # Custom Airflow operators or sensors
- `docker-compose.yml` # Infrastructure orchestration (Postgres, Airflow, etc.)
- `.env.example`     # Template for required environment variables
- `requirements.txt` # Python dependencies for API and local tools
