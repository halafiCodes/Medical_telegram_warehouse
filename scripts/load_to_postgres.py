import json
import os
from datetime import date

import pandas as pd
from sqlalchemy import create_engine, text
db_url = os.environ.get("MEDICAL_DW_URL", "postgresql://postgres:1234@localhost:5434/medical_dw")
engine = create_engine(db_url)

data_date = os.environ.get("TELEGRAM_DATA_DATE", date.today().isoformat())
data_dir = os.environ.get(
    "TELEGRAM_DATA_DIR",
    os.path.join("..", "data", "raw", "telegram_messages", data_date),
)
files = os.environ.get(
    "TELEGRAM_FILES",
    "CheMed123.json,lobelia4cosmetics.json,tikvahpharma.json",
).split(",")

if not os.path.isdir(data_dir):
    raise FileNotFoundError(f"Data directory not found: {data_dir}")

all_data = []
missing_files = []
for file in files:
    file = file.strip()
    if not file:
        continue
    file_path = os.path.join(data_dir, file)
    if not os.path.isfile(file_path):
        missing_files.append(file)
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        for entry in content:
            entry["source_channel"] = file.replace(".json", "")
        all_data.extend(content)

if missing_files:
    print(f"Warning: missing files skipped: {', '.join(missing_files)}")

if not all_data:
    raise ValueError("No data loaded. Check your data directory and file list.")

df = pd.DataFrame(all_data)

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

df.to_sql("telegram_messages", engine, schema="raw", if_exists="replace", index=False)
print("Successfully loaded raw data to Postgres!")