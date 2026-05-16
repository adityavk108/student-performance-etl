from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

sys.path.insert(0, '/opt/airflow')

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_to_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    'student_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Student Performance ETL Pipeline',
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )
    
    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres,
    )
    
    extract_task >> transform_task >> load_task