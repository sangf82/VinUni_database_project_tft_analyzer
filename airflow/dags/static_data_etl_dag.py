"""
DAG for TFT static data ETL pipeline.
This pipeline extracts, processes, and loads static TFT data including:
- Champions
- Items
- Traits
- Tacticians (Little Legends/Pets)
- Augments
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import our static data ETL functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Steps.static_data import (
    get_latest_version,
    fetch_champions_data, process_champions_data, load_champions_to_sql,
    fetch_tacticians_data, process_tacticians_data, load_tacticians_to_sql,
    fetch_items_data, process_items_data, load_items_to_sql,
    fetch_traits_data, process_traits_data, load_traits_to_sql,
    fetch_augments_data, process_augments_data, load_augments_to_sql
)

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'tft_static_data_etl_pipeline',
    default_args=default_args,
    description='TFT Static Data ETL Pipeline',
    schedule_interval=timedelta(days=7),  # Run weekly
    start_date=datetime(2025, 5, 27),
    catchup=False,
    tags=['tft', 'static_data'],
)

# Task to get the latest version
def get_version_task():
    version = get_latest_version()
    if not version:
        raise ValueError("Failed to get latest Data Dragon version")
    return version

t_get_version = PythonOperator(
    task_id='get_latest_version',
    python_callable=get_version_task,
    dag=dag,
)

# Champions ETL tasks
def fetch_champions_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    champions_data = fetch_champions_data(version)
    if not champions_data:
        raise ValueError("Failed to fetch champions data")
    return champions_data

def process_champions_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    champions_data = ti.xcom_pull(task_ids='fetch_champions')
    processed_champions = process_champions_data(champions_data, version)
    if not processed_champions:
        raise ValueError("Failed to process champions data")
    return processed_champions

def load_champions_task(ti):
    processed_champions = ti.xcom_pull(task_ids='process_champions')
    load_champions_to_sql(processed_champions)

t_fetch_champions = PythonOperator(
    task_id='fetch_champions',
    python_callable=fetch_champions_task,
    dag=dag,
)

t_process_champions = PythonOperator(
    task_id='process_champions',
    python_callable=process_champions_task,
    dag=dag,
)

t_load_champions = PythonOperator(
    task_id='load_champions',
    python_callable=load_champions_task,
    dag=dag,
)

# Tacticians (Little Legends/Pets) ETL tasks
def fetch_tacticians_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    tacticians_data = fetch_tacticians_data(version)
    if not tacticians_data:
        raise ValueError("Failed to fetch tacticians data")
    return tacticians_data

def process_tacticians_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    tacticians_data = ti.xcom_pull(task_ids='fetch_tacticians')
    processed_tacticians = process_tacticians_data(tacticians_data, version)
    if not processed_tacticians:
        raise ValueError("Failed to process tacticians data")
    return processed_tacticians

def load_tacticians_task(ti):
    processed_tacticians = ti.xcom_pull(task_ids='process_tacticians')
    load_tacticians_to_sql(processed_tacticians)

t_fetch_tacticians = PythonOperator(
    task_id='fetch_tacticians',
    python_callable=fetch_tacticians_task,
    dag=dag,
)

t_process_tacticians = PythonOperator(
    task_id='process_tacticians',
    python_callable=process_tacticians_task,
    dag=dag,
)

t_load_tacticians = PythonOperator(
    task_id='load_tacticians',
    python_callable=load_tacticians_task,
    dag=dag,
)

# Items ETL tasks
def fetch_items_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    items_data = fetch_items_data(version)
    if not items_data:
        raise ValueError("Failed to fetch items data")
    return items_data

def process_items_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    items_data = ti.xcom_pull(task_ids='fetch_items')
    processed_items = process_items_data(items_data, version)
    if not processed_items:
        raise ValueError("Failed to process items data")
    return processed_items

def load_items_task(ti):
    processed_items = ti.xcom_pull(task_ids='process_items')
    load_items_to_sql(processed_items)

t_fetch_items = PythonOperator(
    task_id='fetch_items',
    python_callable=fetch_items_task,
    dag=dag,
)

t_process_items = PythonOperator(
    task_id='process_items',
    python_callable=process_items_task,
    dag=dag,
)

t_load_items = PythonOperator(
    task_id='load_items',
    python_callable=load_items_task,
    dag=dag,
)

# Traits ETL tasks
def fetch_traits_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    traits_data = fetch_traits_data(version)
    if not traits_data:
        raise ValueError("Failed to fetch traits data")
    return traits_data

def process_traits_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    traits_data = ti.xcom_pull(task_ids='fetch_traits')
    processed_traits = process_traits_data(traits_data, version)
    if not processed_traits:
        raise ValueError("Failed to process traits data")
    return processed_traits

def load_traits_task(ti):
    processed_traits = ti.xcom_pull(task_ids='process_traits')
    load_traits_to_sql(processed_traits)

t_fetch_traits = PythonOperator(
    task_id='fetch_traits',
    python_callable=fetch_traits_task,
    dag=dag,
)

t_process_traits = PythonOperator(
    task_id='process_traits',
    python_callable=process_traits_task,
    dag=dag,
)

t_load_traits = PythonOperator(
    task_id='load_traits',
    python_callable=load_traits_task,
    dag=dag,
)

# Augments ETL tasks
def fetch_augments_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    augments_data = fetch_augments_data(version)
    # Augments might not be available through standard Data Dragon, so don't raise error
    return augments_data or {}

def process_augments_task(ti):
    version = ti.xcom_pull(task_ids='get_latest_version')
    augments_data = ti.xcom_pull(task_ids='fetch_augments')
    # Process if data is available
    if augments_data:
        processed_augments = process_augments_data(augments_data, version)
        return processed_augments
    return []

def load_augments_task(ti):
    processed_augments = ti.xcom_pull(task_ids='process_augments')
    if processed_augments:
        load_augments_to_sql(processed_augments)

t_fetch_augments = PythonOperator(
    task_id='fetch_augments',
    python_callable=fetch_augments_task,
    dag=dag,
)

t_process_augments = PythonOperator(
    task_id='process_augments',
    python_callable=process_augments_task,
    dag=dag,
)

t_load_augments = PythonOperator(
    task_id='load_augments',
    python_callable=load_augments_task,
    dag=dag,
)

# Set task dependencies
t_get_version >> t_fetch_champions >> t_process_champions >> t_load_champions
t_get_version >> t_fetch_tacticians >> t_process_tacticians >> t_load_tacticians
t_get_version >> t_fetch_items >> t_process_items >> t_load_items
t_get_version >> t_fetch_traits >> t_process_traits >> t_load_traits
t_get_version >> t_fetch_augments >> t_process_augments >> t_load_augments
