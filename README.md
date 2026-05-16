# Student Performance ETL Pipeline

A production-quality ETL pipeline that processes student marks from CSV files and loads them into PostgreSQL, orchestrated by Apache Airflow.

**Technology Stack:** Apache Airflow, PostgreSQL, Python, Pandas, Docker

**Suitable for:** College projects, demonstrations, learning ETL concepts

---

## Architecture

```
┌─────────────────┐     ┌─────────────┐     ┌──────────────┐     ┌────────────┐
│  CSV Input      │────▶│  Extract    │────▶│  Transform   │────▶│  Load      │
│  data/input/   │     │  data/temp/ │     │  data/processed/│   │  PostgreSQL │
└─────────────────┘     └─────────────┘     └──────────────┘     └────────────┘
                                                                       
                         Airflow Orchestration (DAG)
```

**Components:**
- **CSV Input**: Source files in `data/input/`
- **Extract**: Reads CSV, saves to `data/temp/raw_data.csv`
- **Transform**: Reads from temp/, cleans data, adds grade/pass_fail, saves to `data/processed/transformed_data.csv`
- **Load**: Reads from processed/, inserts into PostgreSQL
- **Airflow**: Orchestrates the entire flow

---

## ETL Explanation

### Extract
- Reads CSV from `data/input/student_marks.csv`
- Saves raw data to `data/temp/raw_data.csv`

### Transform
- Reads from `data/temp/raw_data.csv`
- Cleans and validates data
- Adds calculated columns:
  - **Grade Assignment:**
    - Grade A: marks >= 90
    - Grade B: marks 75-89
    - Grade C: marks 50-74
    - Grade D: marks < 50
  - **Pass/Fail:**
    - PASS: marks >= 50
    - FAIL: marks < 50
- Saves to `data/processed/transformed_data.csv`

### Load
- Reads from `data/processed/transformed_data.csv`
- Inserts into PostgreSQL table `student_performance`
- Truncates table before each insert to prevent duplicates

**File-based handoff:** Data is passed between tasks via files in temp/ and processed/ directories, ensuring reliable data transfer without XCom serialization issues.

---

## DAG Explanation

**DAG Name:** `student_etl_pipeline`

| Task | Description |
|------|-------------|
| `extract_data` | Reads CSV file |
| `transform_data` | Cleans and enriches data |
| `load_to_postgres` | Inserts to database |

**Task Dependencies:** extract_data → transform_data → load_to_postgres

**Trigger:** Manual (no schedule)

---

## Prerequisites

- Docker Desktop installed and running
- Git (for cloning)
- Web browser (for Airflow UI)
- Terminal/Command Prompt

---

## Docker Setup

1. Clone the repository
2. Navigate to project directory
3. Ensure Docker Desktop is running
4. Run: `docker compose up --build`
5. Wait 2-3 minutes for initialization
6. Access services

---

## How to Run Locally

```bash
docker compose up --build
```

- **First run:** Downloads images (~1-2GB), builds containers
- **Subsequent runs:** Faster
- **To stop:** `docker compose down`

---

## How to Access Airflow UI

- **URL:** http://localhost:8080
- **Username:** airflow
- **Password:** airflow
- **Find DAG:** student_etl_pipeline
- **Trigger:** Click "Trigger DAG" button

---

## How to Verify PostgreSQL Data

### Method 1: Using docker exec
```bash
docker exec -it <postgres_container> psql -U airflow -d student_db -c "SELECT * FROM student_performance;"
```

### Method 2: Using Python script
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="student_db",
    user="airflow",
    password="airflow"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM student_performance;")
print(cursor.fetchall())
conn.close()
```

---

## CI/CD

- **GitHub Actions workflow:** `.github/workflows/ci.yml`
- **Triggers:** push to main, pull_request
- **Steps:** Checkout → Setup Python → Install deps → Run pytest
- **DAG validation:** Done locally in Docker (Airflow not installed in CI)
- **View results:** Repository → Actions tab

---

## Testing

```bash
pytest
```

- **Test location:** `tests/`
- **Test coverage:** Grade logic, pass/fail logic, output columns

---

## Project Structure

```
student-performance-etl/
├── dags/              # Airflow DAGs
├── data/
│   ├── input/         # Source CSV files
│   ├── temp/          # Extract task output
│   └── processed/     # Transform task output
├── etl/               # ETL modules
├── scripts/           # SQL scripts
├── tests/             # Test files
├── .github/
│   └── workflows/     # CI/CD workflows
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Troubleshooting

- **Airflow not starting:** Check Docker Desktop is running
- **Cannot access localhost:8080:** Wait 2-3 minutes, check port not in use
- **PostgreSQL connection failed:** Check postgres container is running
- **DAG not visible:** Check dags folder is mounted correctly
- **airflow-init fails:** Check postgres is ready first
- **Task fails with file not found:** Check temp/processed directories exist
- **Login fails:** Wait for airflow-init to complete before accessing UI

---
