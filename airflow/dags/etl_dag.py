from datetime import datetime, timedelta
import sys
import os
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from Steps.extract import extract_data_from_api
from Steps.process import process
from Steps.load import load_to_sql

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 5, 26),
}

def extract_task(**kwargs):
    # Example player info - you might want to parameterize this
    tag_line = 'YBY1'
    game_name = 'TLN YBY1'
    return extract_data_from_api(tag_line, game_name)

def process_task(**kwargs):
    ti = kwargs['ti']
    data, game_name, tag_line = ti.xcom_pull(task_ids='extract')
    return process(data, game_name, tag_line)

def load_task(**kwargs):
    ti = kwargs['ti']
    processed_data = ti.xcom_pull(task_ids='process')
    return load_to_sql(processed_data)

with DAG(
    'tft_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for TFT data',
    schedule=timedelta(days=1),
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id='extract', python_callable=extract_task)
    t2 = PythonOperator(task_id='process', python_callable=process_task)
    t3 = PythonOperator(task_id='load', python_callable=load_task)
    
    t1 >> t2 >> t3