import pandas as pd
import os


def extract_data():
    """
    Extract data from CSV file and save to temp storage.
    
    Input:
        /opt/airflow/data/input/student_marks.csv
    
    Output:
        /opt/airflow/data/temp/raw_data.csv
    
    Returns:
        None (data passed via file)
    """
    input_path = '/opt/airflow/data/input/student_marks.csv'
    temp_path = '/opt/airflow/data/temp/raw_data.csv'
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"CSV file not found: {input_path}")
    
    os.makedirs('/opt/airflow/data/temp', exist_ok=True)
    
    df = pd.read_csv(input_path)
    df.to_csv(temp_path, index=False)