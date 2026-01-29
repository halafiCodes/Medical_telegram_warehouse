# Medical Telegram Data Warehouse


---

## 📌 Project Overview

This project delivers an **end-to-end ELT data product** that extracts data from public Ethiopian medical Telegram channels, transforms it into a clean analytical warehouse, enriches it using **computer vision (YOLOv8)**, and exposes insights through a **FastAPI analytical API**. The pipeline is automated and observable using **Dagster**.

The platform answers key business questions such as:

* What are the most frequently mentioned medical products?
* How do prices or availability vary across channels?
* Which channels use the most visual content?
* What are daily and weekly posting trends?

---

## 🏗️ Architecture (High-Level)

**Telegram → Data Lake → PostgreSQL Warehouse → dbt Transformations → YOLO Enrichment → FastAPI → Dagster Orchestration**

* **Extract & Load:** Telethon + Python
* **Transform:** dbt (Star Schema)
* **Enrich:** YOLOv8 object detection
* **Serve:** FastAPI (Analytical API)
* **Orchestrate:** Dagster
* **Infra:** Docker & Docker Compose

---

## 📂 Project Structure

```
medical-telegram-warehouse/
├── .github/workflows/        # CI (unit tests)
├── .env                     # Secrets (DO NOT COMMIT)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── data/
│   └── raw/
│       ├── telegram_messages/YYYY-MM-DD/
│       └── images/{channel_name}/
├── medical_warehouse/        # dbt project
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
├── src/
│   ├── scraper.py            # Telegram scraping
│   ├── load_raw_to_db.py     # Load JSON → PostgreSQL
│   └── yolo_detect.py        # YOLO object detection
├── api/
│   ├── main.py               # FastAPI app
│   ├── database.py
│   └── schemas.py
├── scripts/
├── tests/
└── README.md
```

---

## 🧩 Data Sources

Public Telegram channels selling medical, pharmaceutical, and cosmetic products:

* CheMed Telegram Channel
* Lobelia Cosmetics – [https://t.me/lobelia4cosmetics](https://t.me/lobelia4cosmetics)
* Tikvah Pharma – [https://t.me/tikvahpharma](https://t.me/tikvahpharma)
* Additional channels from [https://et.tgstat.com/medicine](https://et.tgstat.com/medicine)

**Collected Fields**

* `message_id`, `channel_name`, `message_date`
* `message_text`, `views`, `forwards`
* `has_media`, `image_path`

---

## ✅ Task Breakdown

### **Task 1: Data Scraping & Collection (Extract & Load)**

**Goal:** Build a reliable Telegram scraping pipeline.

**Key Features:**

* Telegram API access via **Telethon**
* Extract messages, metadata, and media
* Download images per channel and message
* Store raw data as partitioned JSON files
* Logging of scraping activity and errors

**Outputs:**

* `src/scraper.py`
* `data/raw/telegram_messages/YYYY-MM-DD/*.json`
* `data/raw/images/{channel}/{message_id}.jpg`

---

### **Task 2: Data Modeling & Transformation (dbt)**

**Goal:** Transform raw data into a trusted analytical warehouse.

**Warehouse Design (Star Schema):**

* **Dimensions**

  * `dim_channels`
  * `dim_dates`
* **Facts**

  * `fct_messages`

**dbt Features:**

* Staging models for cleaning and standardization
* Mart models optimized for analytics
* Tests: `not_null`, `unique`, `relationships`
* Custom tests (no future dates, non-negative views)
* Auto-generated documentation

**Outputs:**

* Fully tested dbt project
* `dbt docs generate` & `dbt docs serve`

---

### **Task 3: Data Enrichment with YOLOv8**

**Goal:** Add analytical value from images.

**Process:**

* YOLOv8 nano model for object detection
* Detect objects with confidence scores
* Classify images into:

  * `promotional`
  * `product_display`
  * `lifestyle`
  * `other`

**Integration:**

* Results stored in CSV
* Loaded into warehouse via dbt
* New fact table: `fct_image_detections`

---

### **Task 4: Analytical API (FastAPI)**

**Goal:** Expose insights via REST API.

**Endpoints:**

* `GET /api/reports/top-products`
* `GET /api/channels/{channel_name}/activity`
* `GET /api/search/messages`
* `GET /api/reports/visual-content`

**Features:**

* SQLAlchemy for DB access
* Pydantic schemas for validation
* Auto-generated OpenAPI docs (`/docs`)

---

### **Task 5: Pipeline Orchestration (Dagster)**

**Goal:** Automate and monitor the full pipeline.

**Dagster Ops:**

1. Scrape Telegram data
2. Load raw data to PostgreSQL
3. Run dbt transformations
4. Run YOLO enrichment

**Capabilities:**

* DAG-based execution
* Logging and observability
* Daily scheduling
* Local UI at `http://localhost:3000`

---

## 🚀 Getting Started

### 1. Clone Repository

```
git clone <repo-url>
cd medical-telegram-warehouse
```

### 2. Environment Setup

* Create `.env` file with:

  * Telegram API credentials
  * PostgreSQL connection details

### 3. Run with Docker

```
docker-compose up --build
```

### 4. Run dbt

```
dbt run
dbt test
```

### 5. Start API

```
uvicorn api.main:app --reload
```

### 6. Start Dagster

```
dagster dev -f pipeline.py
```

---

## 📦 Deliverables

* End-to-end ELT data pipeline
* Star schema data warehouse
* YOLO-enriched analytical tables
* FastAPI analytical service
* Dagster-orchestrated workflow
* dbt documentation & tests

---

## 🧠 Learning Outcomes

* Telegram data extraction
* Dimensional modeling (Kimball)
* dbt-based transformations & testing
* Computer vision for data enrichment
* API-driven analytics
* Production-grade orchestration

---

## 👥 Team & Support

**Tutors:** Kerod, Mahbubah, Filimon, Smegnsh
**Slack:** `#all-week8`
**Office Hours:** Mon–Fri, 08:00–15:00 UTC



---


