import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone
import json
import csv
import os

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ARC LAB — Carbon Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── LOGGING ───────────────────────────────────────────────────────────────────
LOG_FILE = "data/arc_lab_logs.csv"

def write_log(event_type, endpoint, status, response_time_ms, cached, error=None):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "event_type", "endpoint", "status",
                             "response_time_ms", "cached", "error"])
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            event_type, endpoint, status,
            round(response_time_ms, 1), cached,
            error or ""
        ])

def get_recent_logs(n=10):
    if not os.path.isfile(LOG_FILE):
        return None
    try:
        df = pd.read_csv(LOG_FILE)
        return df.tail(n)
    except:
        return None

# ── ARC LAB VISUAL IDENTITY ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0D1117;
    color: #FFFFFF;
}

.stApp {
    background: linear-gradient(135deg, #0D1117 0%, #1a1f2e 100%);
    background-attachment: fixed;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

.arc-hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem 1rem;
    border-bottom: 1px solid rgba(0, 229, 255, 0.2);
    margin-bottom: 2rem;
}

.arc-logo {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 900;
    letter-spacing: 0.15em;
    background: linear-gradient(135deg, #00E5FF 0%, #0A84FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.arc-subtitle {
    font-size: 1.1rem;
    color: #8E8E93;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.arc-tagline {
    font-size: 1.05rem;
    color: #AEAEB2;
    font-style: italic;
}

.arc-section-header {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    color: #00E5FF;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-left: 4px solid #00E5FF;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}

.kpi-stack {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin: 0;
}

.kpi-card {
    padding: 1.25rem 1.5rem;
    background: rgba(0, 229, 255, 0.04);
    border: 1.5px solid rgba(0, 229, 255, 0.25);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.3s ease;
}

.kpi-card:hover {
    border-color: #00E5FF;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.12);
}

.kpi-card-left { flex: 1; }

.kpi-label {
    font-size: 0.7rem;
    color: #8E8E93;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.2rem;
}

.kpi-value {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 1.6rem;
    font-weight: 900;
    color: #00E5FF;
    line-height: 1.1;
}

.kpi-value.gold { color: #FFD60A; }
.kpi-value.green { color: #34C759; }
.kpi-value.red { color: #FF3B30; }
.kpi-value.white { color: #FFFFFF; font-size: 1.2rem; }
.kpi-value.small { font-size: 1rem; }

.kpi-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    letter-spacing: 0.05em;
    white-space: nowrap;
}

.badge-green { background: rgba(52,199,89,0.15); color: #34C759; border: 1px solid rgba(52,199,89,0.3); }
.badge-yellow { background: rgba(255,214,10,0.15); color: #FFD60A; border: 1px solid rgba(255,214,10,0.3); }
.badge-red { background: rgba(255,59,48,0.15); color: #FF3B30; border: 1px solid rgba(255,59,48,0.3); }
.badge-blue { background: rgba(0,229,255,0.12); color: #00E5FF; border: 1px solid rgba(0,229,255,0.3); }

.ai-summary-hero {
    background: linear-gradient(135deg, rgba(0,229,255,0.06) 0%, rgba(255,214,10,0.04) 100%);
    border: 2px solid rgba(255, 214, 10, 0.4);
    border-radius: 16px;
    padding: 1.75rem;
    margin: 0.75rem 0;
}

.ai-summary-label {
    font-size: 0.7rem;
    color: #FFD60A;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 1rem;
    font-weight: 700;
}

.ai-summary-text {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #FFFFFF;
}

.best-window-card {
    background: linear-gradient(135deg, rgba(0,229,255,0.08) 0%, rgba(10,132,255,0.08) 100%);
    border: 2px solid #00E5FF;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
}

.best-window-label {
    font-size: 0.7rem;
    color: #8E8E93;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.3rem;
}

.best-window-time {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #00E5FF;
    margin-bottom: 0.25rem;
}

.best-window-detail {
    font-size: 0.85rem;
    color: #AEAEB2;
}

.hist-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1rem 0;
}

.hist-card {
    padding: 1rem;
    background: rgba(0,229,255,0.03);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 12px;
    text-align: center;
}

.hist-value {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.stale-banner {
    background: rgba(255,59,48,0.1);
    border: 1.5px solid rgba(255,59,48,0.4);
    border-radius: 12px;
    padding: 0.75rem 1.25rem;
    color: #FF3B30;
    font-size: 0.85rem;
    margin: 0.5rem 0;
}

.health-panel {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(0,229,255,0.1);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-size: 0.8rem;
    color: #636366;
}

.health-row {
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.health-row:last-child { border-bottom: none; }
.health-key { color: #8E8E93; }
.health-val { color: #AEAEB2; font-family: 'Courier New', monospace; }
.health-ok { color: #34C759; }
.health-err { color: #FF3B30; }

.chart-wrap {
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(0,229,255,0.12);
    border-radius: 14px;
    padding: 0.5rem;
}

.arc-footer {
    text-align: center;
    padding: 2rem 1rem;
    border-top: 1px solid rgba(0,229,255,0.12);
    margin-top: 2.5rem;
    color: #636366;
    font-size: 0.8rem;
    line-height: 1.8;
}

.arc-footer a { color: #00E5FF; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ── WATTTIME AUTH ─────────────────────────────────────────────────────────────
def get_watttime_token():
    t0 = datetime.now(timezone.utc).timestamp()
    try:
        username = st.secrets["watttime"]["username"]
        password = st.secrets["watttime"]["password"]
        response = requests.get(
            "https://api.watttime.org/login",
            auth=(username, password),
            timeout=10
        )
        response.raise_for_status()
        ms = (datetime.now(timezone.utc).timestamp() - t0) * 1000
        write_log("auth", "watttime/login", response.status_code, ms, False)
        return response.json()["token"], None
    except Exception as e:
        ms = (datetime.now(timezone.utc).timestamp() - t0) * 1000
        write_log("auth", "watttime/login", "error", ms, False, str(e))
        return None, str(e)

# ── WATTTIME FORECAST ─────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_forecast(token):
    t0 = datetime.now(timezone.utc).timestamp()
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "https://api.watttime.org/v3/forecast",
            headers=headers,
            params={"region": "CAISO_NORTH", "signal_type": "co2_moer"},
            timeout=10
        )
        response.raise_for_status()
        ms = (datetime.now(timezone.utc).timestamp() - t0) * 1000
        write_log("forecast", "watttime/v3/forecast", response.status_code, ms, False)
        return response.json(), None
    except Exception as e:
        ms = (datetime.now(timezone.utc).timestamp() - t0) * 1000
        write_log("forecast", "watttime/v3/forecast", "error", ms, False, str(e))
        return None, str(e)

def get_forecast_with_refresh(token):
    data, err = get_forecast(token)
    if err and "401" in str(err):
        st.cache_data.clear()
        new_token, token_err = get_watttime_token()
        if new_token:
            return get_forecast(new_token)
        return None, token_err
    return data, err

# ── SCHEDULING ALGORITHM ──────────────────────────────────────────────────────
def find_best_window(forecast_df, duration_hours=2):
    bins_per_hour = 12
    window_size = duration_hours * bins_per_hour
    clean = forecast_df.dropna(subset=["value"])
    clean = clean[clean["value"] > 0].reset_index(drop=True)
    if len(clean) < window_size:
        return None
    rolling = clean["value"].rolling(window=window_size).mean()
    best_end_idx = rolling[rolling == rolling.min()].index[0]
    best_start_idx = best_end_idx - window_size + 1
    if best_start_idx < 0:
        return None
    window_df = clean.loc[best_start_idx:best_end_idx]
    return {
        "start": window_df.iloc[0]["point_time"],
        "end": window_df.iloc[-1]["point_time"],
        "avg_moer": round(rolling[best_end_idx], 1),
        "duration_hours": duration_hours
    }

# ── AI SUMMARY ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_ai_summary(forecast_hash, current_moer, forecast_min, forecast_max,
                   forecast_median, window_start, window_end, window_moer, duration_hours):
    t0 = datetime.now(timezone.utc).timestamp()
    try:
        prompt = f"""You are ARC LAB's carbon intelligence assistant. ARC LAB exists to answer one question in plain language: what is the real environmental cost of using AI?

California grid data (CAISO_NORTH region):
- Current carbon intensity: {current_moer} lbs CO2/MWh
- Today's forecast range: {forecast_min} to {forecast_max} lbs CO2/MWh
- Today's median: {forecast_median} lbs CO2/MWh
- Best {duration_hours}-hour window: {window_start} to {window_end} ({window_moer} lbs CO2/MWh avg)

Write exactly 3 sentences. Be direct and specific. Use the actual numbers.
1. What the current carbon intensity reading means right now
2. How today's grid compares to a typical day
3. One specific, actionable recommendation: when exactly to run AI workloads today and why

Tone: direct, factual, confident. Not folksy. Not preachy. Write like a scientist talking to a smart friend."""

        response = requests.post(
            "https://www.dataexpert.io/api/v1/anthropic/v1/messages",
            headers={
                "x-api-key": st.secrets["anthropic"]["api_key"],
                "x-session-id": "arclab-dashboard",
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 300,
                "stream": False,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        full_text = result["content"][0]["text"]
        ms = (datetime.now(timezone.utc).timestamp() - t0) * 1000
        write_log("ai_summary", "anthropic/messages", response.status_code, ms, False)
        return full_text.strip(), None
    except Exception as e:
        ms = (datetime.now(timezone.utc).timestamp() - t0) * 1000
        write_log("ai_summary", "anthropic/messages", "error", ms, False, str(e))
        return None, str(e)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

# HERO
st.markdown("""
<div class="arc-hero">
    <div class="arc-logo">ARC LAB</div>
    <div class="arc-subtitle">AI · Renewable · Consumption Laboratory</div>
    <div class="arc-tagline">Real-time carbon intelligence for the California grid — in plain language</div>
</div>
""", unsafe_allow_html=True)

# DATA LOAD
token, token_err = get_watttime_token()
if not token:
    st.markdown(f'<div class="stale-banner">⚠️ WattTime authentication failed: {token_err}</div>',
                unsafe_allow_html=True)
    st.stop()

forecast_data, forecast_err = get_forecast_with_refresh(token)

if forecast_data:
    forecast_df = pd.DataFrame(forecast_data["data"])
    forecast_df["point_time"] = pd.to_datetime(forecast_df["point_time"], utc=True)
    forecast_df = forecast_df.sort_values("point_time").reset_index(drop=True)
    valid = forecast_df[forecast_df["value"] > 0]
    current_moer = round(valid.iloc[0]["value"], 1) if len(valid) > 0 else None
    forecast_df["hour"] = forecast_df["point_time"].dt.floor("h")
    hourly_df = forecast_df[forecast_df["value"] > 0].groupby("hour")["value"].mean().reset_index()
    hourly_df.columns = ["point_time", "value"]
    best_window = find_best_window(forecast_df)
    f_min = round(valid["value"].min(), 1)
    f_max = round(valid["value"].max(), 1)
    f_median = round(valid["value"].median(), 1)
    forecast_hash = str(round(f_median)) + str(len(valid))
else:
    current_moer = None
    hourly_df = None
    best_window = None
    forecast_hash = "unavailable"
    f_min = f_max = f_median = None
    st.markdown(f'<div class="stale-banner">⚠️ Forecast unavailable: {forecast_err}</div>',
                unsafe_allow_html=True)

# AI SUMMARY — load before rendering so it's ready
summary = None
summary_err = None
if current_moer and best_window:
    summary, summary_err = get_ai_summary(
        forecast_hash=forecast_hash,
        current_moer=current_moer,
        forecast_min=f_min,
        forecast_max=f_max,
        forecast_median=f_median,
        window_start=pd.to_datetime(best_window["start"]).strftime("%I:%M %p UTC"),
        window_end=pd.to_datetime(best_window["end"]).strftime("%I:%M %p UTC"),
        window_moer=best_window["avg_moer"],
        duration_hours=best_window["duration_hours"]
    )

# STATUS VARS
moer_class = badge_class = status_text = now_utc = ""
if current_moer:
    if current_moer < 400:
        moer_class, badge_class, status_text = "green", "badge-green", "🟢 Clean"
    elif current_moer < 700:
        moer_class, badge_class, status_text = "gold", "badge-yellow", "🟡 Moderate"
    else:
        moer_class, badge_class, status_text = "red", "badge-red", "🔴 High Carbon"
    now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")

# HISTORICAL DATA
hist_avg = hist_min = hist_max = hist_pct = hist_direction = hist_pct_class = None
try:
    hist_df = pd.read_csv("data/carbon_snapshot.csv")
    hist_avg = round(hist_df["avg_intensity"].mean(), 1)
    hist_min = round(hist_df["avg_intensity"].min(), 1)
    hist_max = round(hist_df["avg_intensity"].max(), 1)
    if current_moer and hist_avg:
        pct = round((1 - current_moer / hist_avg) * 100, 1)
        hist_pct = abs(pct)
        hist_direction = "cleaner" if pct > 0 else "dirtier"
        hist_pct_class = "#34C759" if pct > 0 else "#FF3B30"
except:
    pass

# ══════════════════════════════════════════════════════════════════════════════
# TWO-COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([6, 4], gap="large")

# LEFT COLUMN — CHART + HISTORICAL
with col_left:
    st.markdown('<div class="arc-section-header">24-Hour Carbon Intensity Forecast</div>',
                unsafe_allow_html=True)

    if hourly_df is not None and len(hourly_df) > 0:
        bar_colors = ["#34C759" if v < 400 else "#FFD60A" if v < 700 else "#FF3B30"
                      for v in hourly_df["value"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hourly_df["point_time"],
            y=hourly_df["value"],
            marker_color=bar_colors,
            marker_line_width=0,
            hovertemplate="<b>%{x|%I:%M %p UTC}</b><br>%{y:.0f} lbs CO₂/MWh<extra></extra>"
        ))

        if best_window:
            fig.add_vrect(
                x0=best_window["start"], x1=best_window["end"],
                fillcolor="#00E5FF", opacity=0.12,
                line_width=1.5, line_color="#00E5FF",
                annotation_text="Best window",
                annotation_font_color="#00E5FF",
                annotation_font_size=12,
                annotation_position="top left"
            )

        if f_median:
            fig.add_hline(
                y=f_median, line_dash="dash",
                line_color="rgba(255,214,10,0.5)", line_width=1,
                annotation_text=f"Median: {f_median}",
                annotation_font_color="#FFD60A",
                annotation_font_size=10,
                annotation_position="top right"
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.25)",
            font=dict(color="#AEAEB2", family="Inter, sans-serif", size=12),
            xaxis=dict(
                title="Time (UTC)",
                gridcolor="rgba(255,255,255,0.05)",
                linecolor="rgba(0,229,255,0.2)",
                tickformat="%I %p",
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="lbs CO₂/MWh",
                gridcolor="rgba(255,255,255,0.05)",
                linecolor="rgba(0,229,255,0.2)",
                tickfont=dict(size=12)
            ),
            height=440,
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False,
            bargap=0.12,
        )

        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.78rem; color:#636366; text-align:right; margin-top:-0.25rem;">
        🟢 Clean (&lt;400) &nbsp;|&nbsp; 🟡 Moderate (400–700) &nbsp;|&nbsp;
        🔴 High Carbon (&gt;700) &nbsp;|&nbsp; Dashed = today's median
        </div>
        """, unsafe_allow_html=True)

    # Historical context
    if hist_avg:
        st.markdown('<div class="arc-section-header">Historical Context</div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="hist-grid">
            <div class="hist-card">
                <div class="kpi-label">Historical Avg</div>
                <div class="hist-value" style="color:#FFFFFF;">{hist_avg}</div>
                <div class="kpi-label">lbs CO₂/MWh</div>
            </div>
            <div class="hist-card">
                <div class="kpi-label">Cleanest Hour</div>
                <div class="hist-value" style="color:#34C759;">{hist_min}</div>
                <div class="kpi-label">lbs CO₂/MWh</div>
            </div>
            <div class="hist-card">
                <div class="kpi-label">Dirtiest Hour</div>
                <div class="hist-value" style="color:#FF3B30;">{hist_max}</div>
                <div class="kpi-label">lbs CO₂/MWh</div>
            </div>
            <div class="hist-card">
                <div class="kpi-label">vs History</div>
                <div class="hist-value" style="color:{hist_pct_class};">{hist_pct}%</div>
                <div class="kpi-label">{hist_direction} than avg</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# RIGHT COLUMN — INSIGHT FIRST
with col_right:

    # WHAT THIS MEANS — top of right, always visible
    st.markdown('<div class="arc-section-header">What This Means</div>',
                unsafe_allow_html=True)

    if summary:
        st.markdown(f"""
        <div class="ai-summary-hero">
            <div class="ai-summary-label">⚡ ARC LAB Carbon Intelligence</div>
            <div class="ai-summary-text">{summary}</div>
        </div>
        """, unsafe_allow_html=True)
    elif current_moer and best_window:
        w_start = pd.to_datetime(best_window["start"]).strftime("%I:%M %p")
        w_end = pd.to_datetime(best_window["end"]).strftime("%I:%M %p")
        st.markdown(f"""
        <div class="ai-summary-hero">
            <div class="ai-summary-label">⚡ ARC LAB Carbon Intelligence</div>
            <div class="ai-summary-text">
                The California grid is currently running at {current_moer} lbs CO₂/MWh.
                Today's forecast ranges from {f_min} to {f_max} lbs CO₂/MWh.
                The best window to run your AI workloads today is {w_start} – {w_end} UTC,
                when the grid is expected to be at its cleanest.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # BEST WINDOW
    if best_window:
        w_start = pd.to_datetime(best_window["start"]).strftime("%I:%M %p")
        w_end = pd.to_datetime(best_window["end"]).strftime("%I:%M %p")
        st.markdown(f"""
        <div class="best-window-card">
            <div class="best-window-label">🎯 Best window to run AI workloads today</div>
            <div class="best-window-time">{w_start} – {w_end} UTC</div>
            <div class="best-window-detail">
                Avg {best_window['avg_moer']} lbs CO₂/MWh &nbsp;·&nbsp;
                {best_window['duration_hours']}-hour window &nbsp;·&nbsp;
                lowest carbon period today
            </div>
        </div>
        """, unsafe_allow_html=True)

    # KPI STACK
    st.markdown('<div class="arc-section-header">Live Grid Status</div>',
                unsafe_allow_html=True)

    if current_moer:
        st.markdown(f"""
        <div class="kpi-stack">
            <div class="kpi-card">
                <div class="kpi-card-left">
                    <div class="kpi-label">Carbon Intensity</div>
                    <div class="kpi-value {moer_class}">{current_moer} <span style="font-size:0.85rem;font-weight:400;">lbs CO₂/MWh</span></div>
                </div>
                <span class="kpi-badge {badge_class}">{status_text}</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-card-left">
                    <div class="kpi-label">Today's Forecast Range</div>
                    <div class="kpi-value white small">{f_min} – {f_max} lbs CO₂/MWh</div>
                </div>
                <span class="kpi-badge badge-blue">Forecast</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-card-left">
                    <div class="kpi-label">Grid Region</div>
                    <div class="kpi-value white small">CAISO_NORTH · California</div>
                </div>
                <span class="kpi-badge badge-blue">WattTime</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-card-left">
                    <div class="kpi-label">Last Updated</div>
                    <div class="kpi-value white small">{now_utc}</div>
                </div>
                <span class="kpi-badge badge-green">Live</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── SYSTEM HEALTH ─────────────────────────────────────────────────────────────
with st.expander("⚙️ System Health & Logs", expanded=False):
    logs = get_recent_logs(10)
    if logs is not None and len(logs) > 0:
        last_watttime = logs[logs["event_type"].isin(["auth", "forecast"])].tail(1)
        last_ai = logs[logs["event_type"] == "ai_summary"].tail(1)
        errors = logs[logs["status"] == "error"]

        wt_ok = len(last_watttime) > 0 and last_watttime.iloc[0]["status"] != "error"
        ai_ok = len(last_ai) > 0 and last_ai.iloc[0]["status"] != "error"
        error_count = len(errors)

        st.markdown(f"""
        <div class="health-panel">
            <div class="health-row">
                <span class="health-key">WattTime API</span>
                <span class="health-val {'health-ok' if wt_ok else 'health-err'}">{'✅ OK' if wt_ok else '❌ Error'}</span>
            </div>
            <div class="health-row">
                <span class="health-key">AI Summary (Claude)</span>
                <span class="health-val {'health-ok' if ai_ok else 'health-err'}">{'✅ OK' if ai_ok else '❌ Error / Fallback'}</span>
            </div>
            <div class="health-row">
                <span class="health-key">Recent errors (last 10 calls)</span>
                <span class="health-val {'health-err' if error_count > 0 else 'health-ok'}">{error_count}</span>
            </div>
            <div class="health-row">
                <span class="health-key">Cache TTL</span>
                <span class="health-val">5 min (forecast) · 30 min (token)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            logs[["timestamp", "event_type", "endpoint", "status", "response_time_ms", "cached"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.markdown('<div class="health-panel">No logs yet — logs are written on each API call.</div>',
                    unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="arc-footer">
    <strong style="color:#00E5FF;">ARC LAB</strong> — AI | Renewable | Consumption Laboratory &nbsp;·&nbsp; Metric Muse LLC<br>
    Data: <a href="https://www.watttime.org" target="_blank">WattTime API</a>,
    CAISO_NORTH region &nbsp;·&nbsp;
    <a href="https://github.com/metricmuseTA/arc-lab-streamlit" target="_blank">GitHub</a><br><br>
    <em>MOER (Marginal Operating Emissions Rate) reflects the carbon intensity of the next unit of
    electricity added to the grid — not average grid emissions. Scheduling AI workloads during
    low-MOER windows reduces marginal emissions but does not guarantee net reductions under all
    grid conditions.</em>
</div>
""", unsafe_allow_html=True)
