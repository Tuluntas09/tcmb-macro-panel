# TCMB Macro Panel

Real-time Turkey macroeconomic dashboard using TCMB EVDS data, Plotly charts,
correlation analysis, CSV exports, and Streamlit deployment.

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![TCMB EVDS](https://img.shields.io/badge/Data-TCMB%20EVDS-1B2536?style=for-the-badge)](https://evds3.tcmb.gov.tr)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

## 30-Second Scan

| Area | What this project shows |
|---|---|
| Finance workflow | A live macro dashboard for Turkey covering FX, policy rate, inflation, reserves, and correlations |
| Data engineering | TCMB EVDS API ingestion, cleaning, resampling, caching, and CSV export |
| Analytics | Delta cards, 52-week ranges, real-rate context, CPI trend commentary, and correlation matrix |
| Dashboard UX | Streamlit app with Plotly charts, tabs, metric cards, and Bloomberg-style presentation |
| Deployment | Public Streamlit Cloud app linked from the repository homepage |

## Streamlit App

Open the deployed dashboard link:
[tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app](https://tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app)

## Features

- Five live indicators: USD/TRY, EUR/TRY, policy rate, CPI, and gross FX reserves.
- Interactive time ranges for `1M`, `3M`, `6M`, `1Y`, and full history.
- Plotly charts for area, step, bar, dual-axis, and heatmap views.
- Rule-based Turkish macro commentary for FX, inflation, rates, and reserves.
- CSV export for every data series.
- Hourly Streamlit cache with `@st.cache_data(ttl=3600)`.

## Tech Stack

| Layer | Tools |
|---|---|
| App | Python, Streamlit |
| Data | `tcmb` package, TCMB EVDS REST API |
| Processing | pandas |
| Charts | Plotly |
| Deployment | Streamlit Cloud |

## Data Sources

| Indicator | EVDS series code | Frequency |
|---|---|---|
| USD/TRY | `TP.DK.USD.A` | Daily |
| EUR/TRY | `TP.DK.EUR.A` | Daily |
| Policy rate | `TP.APIFON4` | Monthly |
| CPI index | `TP.FG.J0` | Monthly |
| Gross FX reserves | `TP.AB.B1` | Weekly |

## Architecture

```text
TCMB EVDS API
    -> data_fetcher.py
    -> data_processor.py
    -> charts.py / ai_analyst.py
    -> app.py
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Validation

- Run `streamlit run app.py` and confirm all five tabs render.
- Run `python test_fetch.py` to check EVDS data access.
- Confirm the Streamlit app link and repository homepage point to the intended deployment.

## License

MIT License. See [LICENSE](LICENSE).
