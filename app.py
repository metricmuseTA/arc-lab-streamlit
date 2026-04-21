import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ARC LAB — Carbon Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── ARC LAB VISUAL IDENTITY ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@300;400;600;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0D1117;
    color: #FFFFFF;
}

.stApp {
    background: linear-gradient(135deg, #0D1117 0%, #1a1f2e 100%);
    background-attachment: fixed;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Hero header */
.arc-hero {
    text-align: center;
    padding: 3rem 1rem 2rem 1rem;
    border-bottom: 1px solid rgba(0, 229, 255, 0.2);
    margin-bottom: 2.5rem;
}

.arc-logo {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 900;
    letter-spacing: 0.15em;
    background: linear-gradient(135deg, #00E5FF 0%, #0A84FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.arc-subtitle {
    font-size: 1rem;
    color: #8E8E93;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.arc-tagline {
    font-size: 1rem;
    color: #AEAEB2;
    font-style: italic;
}

/* Section headers */
.arc-section-header {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #00E5FF;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-left: 4px solid #00E5FF;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
}

/* KPI cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.kpi-card {
    padding: 1.5rem;
    background: rgba(0, 229, 255, 0.04);
    border: 1.5px solid rgba(0, 229, 255, 0.3);
    border-radius: 16px;
    text-align: center;
    transition: all 0.3s ease;
}

.kpi-card:hover {
    border-color: #00E5FF;
    box-shadow: 0 0 24px rgba(0, 229, 255, 0.15);
    transform: translateY(-2px);
}

.kpi-label {
    font-size: 0.7rem;
    color: #8E8E93;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.5rem;
}

.kpi-value {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 1.8rem;
    font-weight: 900;
    color: #00E5FF;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}

.kpi-value.gold { color: #FFD60A; }
.kpi-value.green { color: #34C759; }
.kpi-value.red { color: #FF3B30; }
.kpi-value.white { color: #FFFFFF; font-size: 1.3rem; }

.kpi-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    letter-spacing: 0.05em;
}

.badge-green { background: rgba(52, 199, 89, 0.15); color: #34C759; }
.badge-yellow { background: rgba(255, 214, 10, 0.15); color: #FFD60A; }
.badge-red { background: rgba(255, 59, 48, 0.15); color: #FF3B30; }
.badge-blue { background: rgba(0, 229, 255, 0.15); color: #00E5FF; }

/* Best window callout */
.best-window-card {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(10, 132, 255, 0.08) 100%);
    border: 2px solid #00E5FF;
    border-radius: 16px;
    padding: 1.25rem 1.75rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.best-window-icon { font-size: 1.75rem; }

.best-window-label {
    font-size: 0.7rem;
    color: #8E8E93;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.2rem;
}

.best-window-time {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: #00E5FF;
}

.best-window-detail {
    font-size: 0.85rem;
    color: #AEAEB2;
    margin-top: 0.15rem;
}

/* AI summary card */
.ai-summary-card {
    background: rgba(28, 28, 30, 0.6);
    border: 1.5px solid rgba(255, 214, 10, 0.3);
    border-radius: 16px;
    padding: 1.75rem;
    margin: 1rem 0;
    line-height: 1.7;
    font-size: 1.05rem;
    color: #FFFFFF;
}

.ai-summary-label {
    font-size: 0.7rem;
    color: #FFD60A;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.75rem;
    font-weight: 600;
}

/* Stale data warning */
.stale-banner {
    background: rgba(255, 59, 48, 0.1);
    border: 1.5px solid rgba(255, 59, 48, 0.4);
    border-radius: 12px;
    padding: 0.75rem 1.25rem;
    color: #FF3B30;
    font-size: 0.85rem;
    margin: 0.5rem 0;
}

/* Footer */
.arc-footer {
    text-align: center;
    padding: 2rem 1rem;
    border-top: 1px solid rgba(0, 229, 255, 0.15);
    margin-top: 3rem;
    color: #636366;
    font-size: 0.8rem;
    line-height: 1.7;
}

.arc-footer a { color: #00E5FF; text-decoration: none; }

/* Divider */
.arc-divider {
    border: none;
    border-top: 1px solid rgba(0, 229, 255, 0.15);
    margin: 2rem 0;
}

/* Streamlit metric overrides */
[data-testid="metric-container"] {
    background: rgba(0, 229, 255, 0.04);
    border: 1.5px solid rgba(0, 229, 255, 0.25);
    border-radius: 16px;
    padding: 1rem;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', 'Courier New', monospace !important;
    color: #00E5FF !important;
}

/* Chart container */
.chart-container {
    background: rgba(0, 0, 0, 0.3);
    border: 1.5px solid rgba(0, 229, 255, 0.15);
    border-radius: 16px;
    padding: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── WATTTIME AUTH ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800)
def get_watttime_token():
    try:
        username = st.secrets["watttime"]["username"]
        password = st.secrets["watttime"]["password"]
        response = requests.get(
            "https://api.watttime.org/login",
            auth=(username, password),
            timeout=10
        )
        response.raise_for_status()
        return response.json()["token"], None
    except Exception as e:
        return None, str(e)

# ── WATTTIME FORECAST ─────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_forecast(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "https://api.watttime.org/v3/forecast",
            headers=headers,
            params={"region": "CAISO_NORTH", "signal_type": "co2_moer"},
            timeout=10
        )
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

# ── SCHEDULING ALGORITHM ──────────────────────────────────────────────────────
def find_best_window(forecast_df, duration_hours=2):
    """Programmatically find lowest-carbon window. Never delegate this to the LLM."""
    bins_per_hour = 12  # 5-minute bins
    window_size = duration_hours * bins_per_hour

    # Drop NaN values, require enough data
    clean = forecast_df.dropna(subset=["value"])
    clean = clean[clean["value"] > 0]

    if len(clean) < window_size:
        return None

    rolling = clean["value"].rolling(window=window_size).mean()
    best_end_idx = rolling.idxmin()
    best_start_idx = best_end_idx - window_size + 1

    if best_start_idx < 0:
        return None

    window_df = clean.loc[best_start_idx:best_end_idx]

    return {
        "start": window_df.iloc[0]["point_time"],
        "end": window_df.iloc[-1]["point_time"],
        "avg_moer": round(clean["value"].rolling(window=window_size).mean()[best_end_idx], 1),
        "duration_hours": duration_hours
    }

# ── AI SUMMARY ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_ai_summary(forecast_hash, current_moer, forecast_min, forecast_max,
                   forecast_median, window_start, window_end, window_moer, duration_hours):
    try:
        prompt = f"""You are ARC LAB's carbon intelligence assistant. ARC LAB exists to answer one question in plain language: what is the real environmental cost of using AI?

California grid data (CAISO_NORTH region):
- Current carbon intensity: {current_moer} lbs CO2/MWh
- Today's forecast range: {forecast_min} to {forecast_max} lbs CO2/MWh
- Today's median: {forecast_median} lbs CO2/MWh
- Best {duration_hours}-hour window: {window_start} to {window_end} ({window_moer} lbs CO2/MWh avg)

Write exactly 3 sentences. Be direct and specific. Use the actual numbers.
1. What the current carbon intensity reading means right now — no analogies, just a clear statement of whether the grid is clean or dirty and by how much
2. How today's grid compares to a typical day — is this a good day or a bad day to use AI?
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
        
        # Parse response
        result = response.json()
        full_text = result["content"][0]["text"]
        return full_text.strip(), None

    except Exception as e:
        return None, str(e)

# ── HERO HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="arc-hero">
    <div class="arc-logo">ARC LAB</div>
    <div class="arc-subtitle">AI · Renewable · Consumption Laboratory</div>
    <div class="arc-tagline">Real-time carbon intelligence for the California grid — in plain language</div>
</div>
""", unsafe_allow_html=True)

# ── DATA LOAD ─────────────────────────────────────────────────────────────────
token, token_err = get_watttime_token()

if not token:
    st.markdown(f'<div class="stale-banner">⚠️ WattTime authentication failed: {token_err}</div>',
                unsafe_allow_html=True)
    st.stop()

forecast_data, forecast_err = get_forecast(token)

# Parse forecast
if forecast_data:
    forecast_df = pd.DataFrame(forecast_data["data"])
    forecast_df["point_time"] = pd.to_datetime(forecast_df["point_time"], utc=True)
    forecast_df = forecast_df.sort_values("point_time").reset_index(drop=True)

    # Current = first non-zero value
    valid = forecast_df[forecast_df["value"] > 0]
    current_moer = round(valid.iloc[0]["value"], 1) if len(valid) > 0 else None
    current_time = valid.iloc[0]["point_time"] if len(valid) > 0 else None

    # Aggregate 5-min bins to hourly for chart display
    forecast_df["hour"] = forecast_df["point_time"].dt.floor("h")
    hourly_df = forecast_df[forecast_df["value"] > 0].groupby("hour")["value"].mean().reset_index()
    hourly_df.columns = ["point_time", "value"]

    # Best window (on native 5-min resolution)
    best_window = find_best_window(forecast_df)

    # Forecast stats
    f_min = round(valid["value"].min(), 1)
    f_max = round(valid["value"].max(), 1)
    f_median = round(valid["value"].median(), 1)
    forecast_hash = str(round(f_median)) + str(len(valid))

else:
    current_moer = None
    hourly_df = None
    best_window = None
    forecast_hash = "unavailable"
    st.markdown(f'<div class="stale-banner">⚠️ Forecast unavailable: {forecast_err}</div>',
                unsafe_allow_html=True)

# ── KPI TILES ─────────────────────────────────────────────────────────────────
st.markdown('<div class="arc-section-header">Live Grid Status</div>', unsafe_allow_html=True)

if current_moer:
    if current_moer < 400:
        moer_class = "green"
        badge_class = "badge-green"
        status_text = "🟢 Clean"
    elif current_moer < 700:
        moer_class = "gold"
        badge_class = "badge-yellow"
        status_text = "🟡 Moderate"
    else:
        moer_class = "red"
        badge_class = "badge-red"
        status_text = "🔴 High Carbon"

    now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Carbon Intensity</div>
            <div class="kpi-value {moer_class}">{current_moer}</div>
            <div class="kpi-label">lbs CO₂/MWh</div>
            <span class="kpi-badge {badge_class}">{status_text}</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Today's Range</div>
            <div class="kpi-value white">{f_min} – {f_max}</div>
            <div class="kpi-label">lbs CO₂/MWh</div>
            <span class="kpi-badge badge-blue">Forecast</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Grid Region</div>
            <div class="kpi-value white" style="font-size:1rem; padding-top:0.5rem;">CAISO_NORTH</div>
            <div class="kpi-label" style="margin-top:0.5rem;">California</div>
            <span class="kpi-badge badge-blue">WattTime API</span>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Last Updated</div>
            <div class="kpi-value white" style="font-size:1.1rem; padding-top:0.5rem;">{now_utc}</div>
            <div class="kpi-label" style="margin-top:0.5rem;">5-min refresh</div>
            <span class="kpi-badge badge-green">Live</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── BEST WINDOW CALLOUT ───────────────────────────────────────────────────────
if best_window:
    w_start = pd.to_datetime(best_window["start"]).strftime("%I:%M %p")
    w_end = pd.to_datetime(best_window["end"]).strftime("%I:%M %p")
    w_moer = best_window["avg_moer"]

    st.markdown(f"""
    <div class="best-window-card">
        <div class="best-window-icon">🎯</div>
        <div>
            <div class="best-window-label">Best window to run AI workloads today</div>
            <div class="best-window-time">{w_start} – {w_end} UTC</div>
            <div class="best-window-detail">Avg {w_moer} lbs CO₂/MWh · {best_window['duration_hours']}-hour window · lowest carbon period today</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FORECAST CHART ────────────────────────────────────────────────────────────
st.markdown('<div class="arc-section-header">24-Hour Carbon Intensity Forecast</div>',
            unsafe_allow_html=True)

if hourly_df is not None and len(hourly_df) > 0:
    bar_colors = []
    for val in hourly_df["value"]:
        if val < 400:
            bar_colors.append("#34C759")
        elif val < 700:
            bar_colors.append("#FFD60A")
        else:
            bar_colors.append("#FF3B30")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=hourly_df["point_time"],
        y=hourly_df["value"],
        marker_color=bar_colors,
        marker_line_width=0,
        name="CO₂ Intensity",
        hovertemplate="<b>%{x|%I:%M %p UTC}</b><br>%{y:.0f} lbs CO₂/MWh<extra></extra>"
    ))

    # Highlight best window on chart
    if best_window:
        fig.add_vrect(
            x0=best_window["start"],
            x1=best_window["end"],
            fillcolor="#00E5FF",
            opacity=0.12,
            line_width=1.5,
            line_color="#00E5FF",
            annotation_text="Best window",
            annotation_font_color="#00E5FF",
            annotation_font_size=11,
            annotation_position="top left"
        )

    # Median line
    if f_median:
        fig.add_hline(
            y=f_median,
            line_dash="dash",
            line_color="rgba(255,214,10,0.5)",
            line_width=1,
            annotation_text=f"Today's median: {f_median}",
            annotation_font_color="#FFD60A",
            annotation_font_size=10,
            annotation_position="top right"
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font=dict(color="#AEAEB2", family="Inter, sans-serif", size=11),
        xaxis=dict(
            title="Time (UTC)",
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(0,229,255,0.2)",
            tickformat="%I %p",
        ),
        yaxis=dict(
            title="lbs CO₂/MWh",
            gridcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(0,229,255,0.2)",
        ),
        height=380,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False,
        bargap=0.15,
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.75rem; color:#636366; text-align:right; margin-top:-0.5rem;">
    🟢 Clean (&lt;400) &nbsp;|&nbsp; 🟡 Moderate (400–700) &nbsp;|&nbsp; 🔴 High Carbon (&gt;700) &nbsp;|&nbsp;
    Dashed line = today's median
    </div>
    """, unsafe_allow_html=True)

# ── AI SUMMARY ────────────────────────────────────────────────────────────────
st.markdown('<div class="arc-section-header">What This Means</div>', unsafe_allow_html=True)

if current_moer and best_window:
    with st.spinner(""):
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

    if summary:
        st.markdown(f"""
        <div class="ai-summary-card">
            <div class="ai-summary-label">⚡ ARC LAB Carbon Intelligence</div>
            {summary}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"DEBUG: {summary_err}")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="arc-footer">
    <strong style="color:#00E5FF;">ARC LAB</strong> — AI | Renewable | Consumption Laboratory &nbsp;·&nbsp; Metric Muse LLC<br>
    Data: <a href="https://www.watttime.org" target="_blank">WattTime API</a>, CAISO_NORTH region &nbsp;·&nbsp;
    <a href="https://github.com/metricmuseTA/arc-lab-streamlit" target="_blank">GitHub</a><br><br>
    <em>MOER (Marginal Operating Emissions Rate) reflects the carbon intensity of the next unit of electricity
    added to the grid — not average grid emissions. Scheduling AI workloads during low-MOER windows reduces
    marginal emissions but does not guarantee net reductions under all grid conditions.</em>
</div>
""", unsafe_allow_html=True)