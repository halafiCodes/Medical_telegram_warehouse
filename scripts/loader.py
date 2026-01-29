import pandas as pd
from sqlalchemy import create_engine
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = '1234'
PORT = 5434
DATABASE = 'medical_dw'

engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

def load_detections_to_postgres(csv_path):
    try:
        df = pd.read_csv(csv_path)

        df.to_sql(
            'yolo_detections_raw', 
            engine, 
            schema='raw', 
            if_exists='replace', 
            index=False
        )
        
        print(f"Successfully loaded {len(df)} rows into raw.yolo_detections_raw")
        
    except Exception as e:
        print(f"An error occurred: {e}")


load_detections_to_postgres('data/yolo_detections.csv')