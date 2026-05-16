import psycopg2
import pandas as pd


def load_to_postgres(host='postgres', port=5432, database='student_db', 
                     user='airflow', password='airflow'):
    """
    Load transformed data into PostgreSQL database.
    
    Input:
        /opt/airflow/data/processed/transformed_data.csv
    
    Args:
        host: PostgreSQL host
        port: PostgreSQL port
        database: Database name
        user: Database user
        password: Database password
    
    Returns:
        None
    """
    input_path = '/opt/airflow/data/processed/transformed_data.csv'
    df = pd.read_csv(input_path)
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS student_performance (
        id SERIAL PRIMARY KEY,
        student_id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        subject VARCHAR(50) NOT NULL,
        marks NUMERIC(5,2) NOT NULL,
        pass_fail VARCHAR(4) NOT NULL,
        grade VARCHAR(1) NOT NULL,
        processed_at TIMESTAMP NOT NULL
    )
    """
    cursor.execute(create_table_sql)
    
    cursor.execute("TRUNCATE TABLE student_performance RESTART IDENTITY")
    
    for _, row in df.iterrows():
        insert_sql = """
        INSERT INTO student_performance 
        (student_id, name, subject, marks, pass_fail, grade, processed_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (
            int(row['student_id']),
            str(row['name']),
            str(row['subject']),
            float(row['marks']),
            str(row['pass_fail']),
            str(row['grade']),
            row['processed_at']
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Successfully loaded {len(df)} rows to PostgreSQL")