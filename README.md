# Medical Telegram Warehouse

This project scrapes medical data from Telegram channels, stores it in a PostgreSQL warehouse, and transforms it using dbt.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Create a `.env` file with your Telegram API credentials:
    ```
    API_ID=your_api_id
    API_HASH=your_api_hash
    SESSION_NAME=medical_session
    ```

3.  **Run Scraper:**
    ```bash
    python src/scraper.py
    ```

4.  **Load to Warehouse:**
    ```bash
    python scripts/load_to_postgres.py
    ```

5.  **Run dbt Transformations:**
    ```bash
    cd medical_warehouse
    dbt run
    dbt test
    ```
