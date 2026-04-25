# ARC LAB — Carbon Intelligence Dashboard
**AI | Renewable | Consumption Laboratory**  
**Metric Muse LLC · Tiffani Anderson**

[![Live App](https://img.shields.io/badge/Live%20App-arc--lab.streamlit.app-00E5FF?style=flat-square)](https://arc-lab.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-metricmuseTA-FFD60A?style=flat-square)](https://github.com/metricmuseTA/arc-lab-streamlit)

---

## What This Is

ARC LAB is a live, AI-powered carbon intelligence dashboard that answers one question in plain language: **what is the real environmental cost of using AI?**

The dashboard pulls real-time carbon intensity data from the WattTime API for the California grid (CAISO_NORTH), visualizes a 24-hour forecast, and uses a LangChain + Claude AI layer to translate raw numbers into a plain-language summary and scheduling recommendation — when exactly to run your AI workloads today to minimize your carbon impact.

Built as the AI Engineering Boot Camp capstone project (DataExpert.io, Spring 2026). Grounded in a Bronze-to-Gold Databricks medallion pipeline built during the Data Engineering Boot Camp.

---

## Live URL

**[https://arc-lab.streamlit.app](https://arc-lab.streamlit.app)**

Auto-deploys from `main` branch on every push.

---

## Architecture

```
WattTime API /v3/forecast (JSON)
        ↓
Streamlit App (Python)
        ↓                          ↓
24-hr Forecast Chart         LangChain + Claude
Best Window Algorithm        Plain-language summary
(programmatic, not LLM)      Scheduling recommendation
        ↓
Historical Context Panel
(data/carbon_snapshot.csv — Gold table snapshot)
        ↓
User — one page, no technical knowledge required
```

### Data Sources
| Source | Role | Format |
|---|---|---|
| WattTime API v3 | Live carbon intensity — current + 24hr forecast | JSON |
| Databricks Gold Table | Historical CAISO_NORTH hourly data | Delta (exported as CSV) |

### Stack
| Tool | Role |
|---|---|
| Streamlit | Web application framework |
| Streamlit Community Cloud | Hosting + deployment |
| WattTime API | Live grid carbon intensity data |
| LangChain + Claude | AI plain-language summary |
| Plotly | Interactive forecast chart |
| Python | Primary language |
| GitHub | Version control + auto-deploy trigger |

---

## Key Features

- **Live carbon intensity** — real MOER values from WattTime, refreshed every 5 minutes
- **24-hour forecast chart** — color coded green/yellow/red by carbon intensity level
- **Programmatic scheduling algorithm** — finds the lowest-carbon 2-hour window using a rolling mean over 5-minute forecast bins. The LLM never computes the window — it only explains it.
- **AI plain-language summary** — 3-sentence Claude response: what the reading means, how today compares, what to do
- **Historical context** — compared against Gold table averages from the Data Engineering capstone
- **Graceful fallbacks** — if WattTime or Claude fails, the app shows cached data and rule-based text rather than crashing
- **Application logging** — every API call logged to `data/arc_lab_logs.csv` with timestamp, status, response time, and cache flag
- **System health panel** — collapsible panel showing API status, error count, cache TTL

---

## Data Quality

- WattTime API responses cached at 5-minute TTL — prevents rate limit exposure
- Auth token refreshed automatically on 401 without user impact
- NaN and zero-value bins dropped before scheduling algorithm runs
- Tie-breaking: earliest window wins when two windows have equal rolling mean
- Forecast resolution: native 5-minute bins for scheduler, aggregated to hourly for chart display
- AI summary cached by forecast hash — Claude is not called if forecast hasn't changed

**Failure handling:**
| Scenario | Behavior |
|---|---|
| WattTime API error | Shows last cached value with stale-data flag |
| Incomplete forecast | Chart renders available data; scheduler skips if insufficient bins |
| Claude API error | Rule-based fallback text renders instead |
| Historical CSV missing | Historical panel suppressed silently |

---

## Project Structure

```
arc-lab-streamlit/
├── app.py                    ← Main Streamlit application
├── requirements.txt          ← Python dependencies
├── data/
│   ├── carbon_snapshot.csv   ← Gold table snapshot (historical context)
│   └── arc_lab_logs.csv      ← Application logs (auto-generated)
├── pages/                    ← Reserved for future multi-page expansion
├── .streamlit/
│   ├── config.toml           ← Streamlit configuration
│   └── secrets.toml          ← Local secrets (gitignored)
├── .gitignore
├── LICENSE
└── README.md
```

---

## Running Locally

### Prerequisites
- Python 3.10+
- WattTime account (register at [watttime.org](https://watttime.org))
- Anthropic API key or DataExpert.io proxy key

### Setup

**1. Clone the repo**
```bash
git clone https://github.com/metricmuseTA/arc-lab-streamlit.git
cd arc-lab-streamlit
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure secrets**

Create `.streamlit/secrets.toml` (never commit this file):
```toml
[watttime]
username = "your_watttime_username"
password = "your_watttime_password"

[anthropic]
api_key = "your_anthropic_or_proxy_key"
base_url = "https://api.anthropic.com"  # or your proxy URL
```

**4. Run the app**
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## Deploying to Streamlit Community Cloud

1. Push repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **Create app** → select `metricmuseTA/arc-lab-streamlit`, branch `main`, file `app.py`
4. Under **Advanced settings → Secrets**, paste your `secrets.toml` contents
5. Click **Deploy** — auto-deploys on every push to `main`

---

## WattTime API Notes

- Endpoint: `GET https://api.watttime.org/v3/forecast`
- Auth: `GET https://api.watttime.org/login` with Basic auth → returns bearer token
- Region: `CAISO_NORTH` (California)
- Signal type: `co2_moer`
- Token expiry: ~30 minutes (app refreshes automatically on 401)
- Free tier: sufficient for this application's polling frequency

**Attribution:** Data provided by [WattTime](https://www.watttime.org). MOER (Marginal Operating Emissions Rate) reflects the carbon intensity of the next unit of electricity added to the grid — not average grid emissions.

---

## MOER Disclaimer

Scheduling AI workloads during low-MOER windows reduces marginal emissions but does not guarantee net reductions under all grid conditions. MOER is a marginal signal, not an average emissions signal. Results reflect conditions in the CAISO_NORTH region only.

---

## Related Repositories

- **Data Engineering Capstone (Bronze→Gold Pipeline):** [metricmuseTA/arc-lab-carbon-pipeline](https://github.com/metricmuseTA/arc-lab-carbon-pipeline)

---

## About ARC LAB

ARC LAB (AI | Renewable | Consumption Laboratory) is a research initiative under Metric Muse LLC quantifying the carbon cost of AI workloads using public grid data. The independent, open, public positioning is a deliberate strategic moat — making AI energy data legible to everyone, not just developers and researchers.

*Tagline: Where AI energy data arcs toward insight.*

---

*Tiffani Anderson · Metric Muse LLC · La Mesa, CA*  
*DataExpert.io AI Engineering Boot Camp · Spring 2026*
