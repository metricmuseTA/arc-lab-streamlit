# ARC LAB — AI Renewable Consumption Laboratory

**Live App:** [arc-lab.streamlit.app](https://arc-lab.streamlit.app)

> Real-time carbon intelligence for the California grid — in plain language.

---

## The Finding

Scheduling AI workloads in hours 18–23 instead of hours 3–6 reduces carbon intensity from **972 lbs CO₂/MWh down to 57 lbs CO₂/MWh** — a **94% reduction** — on the CAISO_NORTH grid (California ISO).

This isn't a marginal improvement. It's the difference between running on mostly fossil fuels versus mostly renewables. The only variable is *when* you schedule the compute.

---

## What This Project Is

ARC LAB is an independent research initiative quantifying the carbon cost of AI workloads using public grid data. This capstone project builds a full Bronze → Silver → Gold medallion pipeline on Databricks using WattTime CAISO_NORTH carbon intensity data, with a live Streamlit app on top powered by LangChain and a RAG assistant.

**Key components:**
- Full medallion pipeline (Bronze → Silver → Gold) on Databricks
- Gold table: `bootcamp_students.gold.carbon_intensity_hourly`
- LLM-powered carbon forecasting via LangChain + Databricks Vector Search
- RAG assistant for natural language queries about grid data
- Token auto-refresh with Parquet fallback for resilience
- Live deployed at [arc-lab.streamlit.app](https://arc-lab.streamlit.app)

---

## Stack

| Layer | Technology |
|---|---|
| Data platform | Databricks (dbc-7b106152-caf3.cloud.databricks.com) |
| Storage | Delta Lake |
| Data source | WattTime API — CAISO_NORTH grid region |
| Language | Python, Spark SQL |
| LLM integration | LangChain (`databricks_langchain`) |
| Vector Search | Databricks Vector Search (`zachy_vs` endpoint) |
| RAG index | `bootcamp_students.zachy_ceresrain.bootcamp_docs_index` |
| App framework | Streamlit |
| Fallback | Parquet snapshot (`carbon_snapshot.csv`) |

---

## Pipeline Architecture

```
WattTime API (CAISO_NORTH)
        ↓
Bronze — Raw ingestion into Delta Lake (no transformations)
        ↓
Silver — Timestamps normalized, nulls handled, schema enforced
        ↓
Gold   — carbon_intensity_hourly
         Hourly averages, Optimal/Moderate/Avoid classifications
         Weekday/weekend splits
        ↓
Streamlit App + LangChain RAG Assistant
```

---

## Run Instructions

### Prerequisites

- Python 3.9+
- Databricks workspace access (or use the Parquet fallback)
- WattTime API credentials (optional — fallback data included)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/metricmuseTA/arc-lab-carbon-pipeline
cd arc-lab-carbon-pipeline

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABRICKS_HOST=https://dbc-7b106152-caf3.cloud.databricks.com
export DATABRICKS_TOKEN=your_token_here

# Run the Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`. If the Databricks connection is unavailable, it will automatically fall back to the included `carbon_snapshot.csv`.

### Live App

No setup required — the app is live at [arc-lab.streamlit.app](https://arc-lab.streamlit.app).

---

## Key Technical Workarounds

These are documented for reproducibility — specific to the Databricks bootcamp environment:

```python
# TIMESTAMP_NTZ epoch math — direct cast fails
# ❌ col("ts_utc").cast("long")  → returns null
# ✅ Correct:
unix_timestamp(col("ts_utc").cast("timestamp"))

# LangChain import path for Databricks runtime
# ❌ from langchain_community.chat_models import ChatDatabricks
# ✅ Correct:
from databricks_langchain import ChatDatabricks

# No INTERVAL syntax in Spark SQL — use epoch math
# ❌ ts_utc >= current_timestamp() - INTERVAL 7 DAYS
# ✅ Correct:
ts_utc >= current_timestamp() - (7 * 86400)
```

---

## Results

| Window | Avg CO₂ Intensity | Classification |
|---|---|---|
| Hours 18–23 (optimal) | 57 lbs CO₂/MWh | ✅ Optimal |
| Hours 6–17 (moderate) | ~300 lbs CO₂/MWh | 🟡 Moderate |
| Hours 3–6 (avoid) | 972 lbs CO₂/MWh | ❌ Avoid |

**94% reduction** available by shifting AI compute from worst to best window.

---

## What's Next

- Expanding beyond CAISO to other grid regions
- Real-time scheduling recommendation API
- OSV Fellowship submitted for research funding

---

## About ARC LAB

ARC LAB (AI Renewable Consumption Laboratory) is an independent research initiative building open, publicly accessible infrastructure to measure the carbon cost of AI workloads.

The core thesis: AI's energy footprint is growing faster than our ability to measure it. ARC LAB is building the open infrastructure to change that.

---

*Built during the DataExpert.io Databricks Bootcamp, March–April 2026*
*Tiffani Anderson · [Metric Muse](https://github.com/metricmuseTA) · La Mesa, CA*
