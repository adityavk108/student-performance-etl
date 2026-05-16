import pandas as pd
import os
from datetime import datetime


def transform_data(df=None):
    """
    Transform raw data by cleaning, validating, and adding derived columns.
    Dual-mode function: testable and production-ready.
    
    Args:
        df: Optional DataFrame. If None, reads from temp CSV (production).
            If provided, uses directly (test mode).
    
    Returns:
        DataFrame: Transformed data with grade, pass_fail, processed_at columns
    
    Production behavior:
        - Reads from /opt/airflow/data/temp/raw_data.csv
        - Saves to /opt/airflow/data/processed/transformed_data.csv
        - Returns DataFrame
    
    Test behavior:
        - Uses provided DataFrame directly
        - Returns DataFrame (no file save needed for tests)
    """
    production_mode = (df is None)
    
    if production_mode:
        df = pd.read_csv('/opt/airflow/data/temp/raw_data.csv')
    
    required_cols = ['student_id', 'name', 'subject', 'marks']
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")
    
    df['name'] = df['name'].str.strip()
    df['subject'] = df['subject'].str.strip()
    
    df = df.drop_duplicates(subset=['student_id', 'subject'], keep='first')
    
    df = df.dropna(subset=['student_id', 'name', 'subject', 'marks'])
    
    df['marks'] = pd.to_numeric(df['marks'], errors='coerce')
    df = df.dropna(subset=['marks'])
    
    if (df['marks'] < 0).any() or (df['marks'] > 100).any():
        raise ValueError("Marks must be between 0 and 100")
    
    df['pass_fail'] = df['marks'].apply(lambda x: 'PASS' if x >= 50 else 'FAIL')
    
    def get_grade(marks):
        if marks >= 90:
            return 'A'
        elif marks >= 75:
            return 'B'
        elif marks >= 50:
            return 'C'
        else:
            return 'D'
    
    df['grade'] = df['marks'].apply(get_grade)
    
    df['processed_at'] = datetime.utcnow()
    
    if production_mode:
        os.makedirs('/opt/airflow/data/processed', exist_ok=True)
        output_path = '/opt/airflow/data/processed/transformed_data.csv'
        df.to_csv(output_path, index=False)
    
    return df