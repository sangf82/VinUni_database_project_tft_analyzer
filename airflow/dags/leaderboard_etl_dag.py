from datetime import datetime, timedelta
import sys
import os
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from Steps.extract import extract_data_from_api, extract_leaderboard_data, extract_player_details_from_summoner_id
from Steps.process import process, process_leaderboard_data
from Steps.load import load_to_sql, load_leaderboard_to_sql, load_combined_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 5, 26),
}

def extract_leaderboard_task(**kwargs):
    """Extract leaderboard data from Riot API"""
    print("Extracting leaderboard data...")
    return extract_leaderboard_data()

def process_leaderboard_task(**kwargs):
    """Process raw leaderboard data into database format"""
    ti = kwargs['ti']
    leaderboard_data = ti.xcom_pull(task_ids='extract_leaderboard')
    
    if not leaderboard_data:
        print("No leaderboard data received from extraction")
        return []
    
    print("Processing leaderboard data...")
    return process_leaderboard_data(leaderboard_data)

def load_leaderboard_task(**kwargs):
    """Load processed leaderboard data to database"""
    ti = kwargs['ti']
    processed_leaderboard = ti.xcom_pull(task_ids='process_leaderboard')
    
    if not processed_leaderboard:
        print("No processed leaderboard data to load")
        return
    
    print("Loading leaderboard data to database...")
    return load_leaderboard_to_sql(processed_leaderboard)

def extract_individual_player_task(**kwargs):
    """Extract individual player data (existing functionality)"""
    # Example player info - you might want to parameterize this
    tag_line = 'YBY1'
    game_name = 'TLN YBY1'
    print(f"Extracting data for player: {game_name}#{tag_line}")
    return extract_data_from_api(tag_line, game_name)

def process_individual_player_task(**kwargs):
    """Process individual player data (existing functionality)"""
    ti = kwargs['ti']
    data, game_name, tag_line = ti.xcom_pull(task_ids='extract_individual_player')
    
    if not data:
        print("No individual player data received from extraction")
        return None
    
    print(f"Processing data for player: {game_name}#{tag_line}")
    return process(data, game_name, tag_line)

def load_individual_player_task(**kwargs):
    """Load individual player data to database (existing functionality)"""
    ti = kwargs['ti']
    processed_data = ti.xcom_pull(task_ids='process_individual_player')
    
    if not processed_data:
        print("No processed individual player data to load")
        return
    
    print("Loading individual player data to database...")
    return load_to_sql(processed_data)

# Leaderboard ETL DAG
with DAG(
    'tft_leaderboard_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for TFT leaderboard data',
    schedule=timedelta(hours=6),  # Run every 6 hours to keep leaderboard fresh
    catchup=False,
    tags=['tft', 'leaderboard', 'etl'],
) as leaderboard_dag:
    
    # Leaderboard ETL tasks
    extract_leaderboard = PythonOperator(
        task_id='extract_leaderboard',
        python_callable=extract_leaderboard_task
    )
    
    process_leaderboard = PythonOperator(
        task_id='process_leaderboard',
        python_callable=process_leaderboard_task
    )
    
    load_leaderboard = PythonOperator(
        task_id='load_leaderboard',
        python_callable=load_leaderboard_task
    )
    
    # Set task dependencies
    extract_leaderboard >> process_leaderboard >> load_leaderboard

# Combined ETL DAG (both individual players and leaderboard)
with DAG(
    'tft_combined_etl_pipeline',
    default_args=default_args,
    description='Combined ETL pipeline for TFT individual player and leaderboard data',
    schedule=timedelta(days=1),  # Run daily
    catchup=False,
    tags=['tft', 'combined', 'etl'],
) as combined_dag:
    
    # Individual player ETL tasks
    extract_individual = PythonOperator(
        task_id='extract_individual_player',
        python_callable=extract_individual_player_task
    )
    
    process_individual = PythonOperator(
        task_id='process_individual_player',
        python_callable=process_individual_player_task
    )
    
    load_individual = PythonOperator(
        task_id='load_individual_player',
        python_callable=load_individual_player_task
    )
    
    # Leaderboard ETL tasks (same as above)
    extract_leaderboard_combined = PythonOperator(
        task_id='extract_leaderboard',
        python_callable=extract_leaderboard_task
    )
    
    process_leaderboard_combined = PythonOperator(
        task_id='process_leaderboard',
        python_callable=process_leaderboard_task
    )
    
    load_leaderboard_combined = PythonOperator(
        task_id='load_leaderboard',
        python_callable=load_leaderboard_task
    )
    
    # Set task dependencies - both pipelines can run in parallel
    extract_individual >> process_individual >> load_individual
    extract_leaderboard_combined >> process_leaderboard_combined >> load_leaderboard_combined
