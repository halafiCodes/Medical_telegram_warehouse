import subprocess
import sys
import os
import pathlib

from dagster import Definitions, In, Nothing, op, job, schedule

@op
def scrape_telegram_data():
    """Run the scraper script to collect raw JSON and images."""
    subprocess.run([sys.executable, "src/scraper.py"], check=True)
    return "Scraping Complete"

@op(ins={"start": In(Nothing)})
def load_raw_to_postgres():
    """Load the local JSON data lake into PostgreSQL raw schema."""
    subprocess.run([sys.executable, "scripts/load_to_postgres.py"], check=True)

@op(ins={"start": In(Nothing)})
def run_dbt_transformations():
    """Execute dbt models to transform data into star schema."""
    subprocess.run([sys.executable, "-m", "dbt", "build", "--project-dir", "medical_warehouse"], check=True)

@op(ins={"start": In(Nothing)})
def run_yolo_enrichment():
    """Run object detection on the downloaded images."""
    subprocess.run([sys.executable, "src/yolo_detect.py"], check=True)

@op(ins={"start": In(Nothing)})
def load_yolo_to_postgres():
    """Load YOLO detections CSV into PostgreSQL raw schema."""
    subprocess.run([sys.executable, "scripts/load_yolo_to_postgres.py"], check=True)

@job
def medical_data_pipeline():
    scraped = scrape_telegram_data()

    loaded = load_raw_to_postgres(start=scraped)

    yolo_done = run_yolo_enrichment(start=loaded)
    yolo_loaded = load_yolo_to_postgres(start=yolo_done)

    run_dbt_transformations(start=yolo_loaded)

@schedule(cron_schedule="0 0 * * *", job=medical_data_pipeline, execution_timezone="UTC")
def daily_medical_pipeline_schedule():
    """Runs the pipeline every day at midnight."""
    return {}


defs = Definitions(
    jobs=[medical_data_pipeline],
    schedules=[daily_medical_pipeline_schedule],
)