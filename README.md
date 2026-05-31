<div align="center">

# 📊 TCMB Makro Göstergeler Paneli

**Real-time macroeconomic dashboard for Turkey — powered by TCMB EVDS API**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![TCMB EVDS](https://img.shields.io/badge/Data-TCMB%20EVDS-1B2536?style=for-the-badge)](https://evds3.tcmb.gov.tr)

</div>

---

## Overview

A Bloomberg-style financial dashboard that fetches live macroeconomic data from the **Central Bank of Turkey (TCMB) EVDS API** and visualizes 5 key indicators in real time. Built as a portfolio project targeting fintech and investment roles.

**Live:** https://tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app

---

## Features

| Feature | Description |
|---------|-------------|
| 📈 **5 Live Indicators** | USD/TRY, EUR/TRY, Policy Rate, CPI (YoY + MoM), Gross FX Reserves |
| 🃏 **Metric Cards** | Current value · delta vs previous period · mini sparkline chart |
| 🗂️ **5 Interactive Tabs** | FX, Policy Rate (step), Inflation, Reserves, Correlation Matrix |
| 🔗 **Correlation Heatmap** | Pearson correlation across all series via Plotly heatmap |
| 📅 **Time Range Selector** | 1M / 3M / 6M / 1Y / Max (dynamic cutoff dates) |
| ⬇️ **CSV Export** | One-click download for every data series |
| 🧠 **Auto Macro Analysis** | Rule-based Turkish commentary: FX · inflation · rate · reserves |
| 📊 **Stats Panel** | 52-week range · YoY change · real rate · CPI drop from peak |
| ⚡ **Caching** | `@st.cache_data(ttl=3600)` — hourly refresh, no redundant API calls |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Data** | `tcmb` Python package · TCMB EVDS REST API |
| **Processing** | `pandas` — resample, pct_change, Pearson corr |
| **Charts** | `plotly` — Scatter (area/step), Bar, Heatmap |
| **UI** | `streamlit` — custom CSS, `unsafe_allow_html` |
| **Fonts** | Inter · JetBrains Mono (Google Fonts) |
| **Deploy** | Streamlit Cloud (GitHub push-to-deploy) |

---

## Data Sources

| Indicator | EVDS Series Code | Frequency |
|-----------|-----------------|-----------|
| USD/TRY | `TP.DK.USD.A` | Daily |
| EUR/TRY | `TP.DK.EUR.A` | Daily |
| Policy Rate | `TP.APIFON4` | Monthly |
| CPI Index | `TP.FG.J0` | Monthly |
| Gross FX Reserves | `TP.AB.B1` | Weekly |

All data freely available at [evds3.tcmb.gov.tr](https://evds3.tcmb.gov.tr).

---

## Architecture

```
TCMB EVDS API
      │
      ▼
data_fetcher.py     ← API client, raw series fetch, error handling
      │
      ▼
data_processor.py   ← Cleaning · pct_change · delta · correlation matrix
      │
      ├──▶ charts.py        ← Plotly figure factories (area, dual, bar, heatmap)
      │
      └──▶ ai_analyst.py    ← Rule-based Turkish macro commentary (HTML output)
                │
                ▼
            app.py          ← Streamlit UI · CSS · metric cards · tabs · stats panel
```

---

## Local Setup

```bash
# 1. Clone
git clone https://github.com/Tuluntas09/tcmb-macro-panel.git
cd tcmb-macro-panel

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
# Create a .env file:
echo EVDS_API_KEY=your_api_key_here > .env

# 5. Run
streamlit run app.py
```

> Get a free EVDS API key at [evds3.tcmb.gov.tr](https://evds3.tcmb.gov.tr)

---

## Project Structure

```
tcmb-macro-panel/
├── app.py              # Main Streamlit application
├── charts.py           # Plotly chart factory functions
├── data_fetcher.py     # TCMB EVDS API client
├── data_processor.py   # Data transformation & statistics
├── ai_analyst.py       # Rule-based macro analysis generator
├── config.py           # Series codes & date range config
├── requirements.txt    # Python dependencies
├── .env                # API keys (not committed)
└── .streamlit/
    └── config.toml     # Streamlit light theme config
```

---

## Key Technical Decisions

- **Rule-based analysis over LLM** — avoids API costs, works offline, deterministic output
- **`@st.cache_data(ttl=3600)`** — 1-hour cache prevents redundant EVDS requests
- **Custom CSS over Streamlit themes** — pixel-accurate Bloomberg-style light theme
- **Dual-series area chart** — USD/TRY and EUR/TRY on same canvas for direct comparison
- **Step-shape policy rate** — `line.shape='hv'` accurately represents discrete rate decisions
- **Dynamic date ranges** — cutoffs computed at runtime so "1M ago" is always correct

---

<div align="center">

*Built for fintech/investment portfolio · Data: TCMB EVDS · Not financial advice*

**[Tuluntas09](https://github.com/Tuluntas09)**

</div>
