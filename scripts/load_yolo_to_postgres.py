import os
import pandas as pd
from sqlalchemy import create_engine, text
db_url = os.environ.get("MEDICAL_DW_URL", "postgresql://postgres:1234@localhost:5434/medical_dw")
engine = create_engine(db_url)

csv_path = os.environ.get(
	"YOLO_CSV_PATH",
	os.path.join("..", "data", "yolo_detections.csv"),
)

if not os.path.isfile(csv_path):
	raise FileNotFoundError(f"CSV not found: {csv_path}")

df = pd.read_csv(csv_path)

with engine.begin() as conn:
	conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
	conn.execute(text("DROP VIEW IF EXISTS analytics.stg_yolo"))
	conn.execute(text("DROP TABLE IF EXISTS raw.yolo_detections_raw"))

df.to_sql("yolo_detections_raw", engine, schema="raw", if_exists="replace", index=False)
print("Successfully loaded YOLO detections to Postgres!")
