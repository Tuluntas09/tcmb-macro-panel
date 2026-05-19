import streamlit as st
import pandas as pd
from data_processor import get_series, get_cpi_pct, filter_by_range, compute_delta, latest_date
from charts import area_chart, bar_chart, COLORS
from config import DATE_RANGES
from ai_analyst import get_ai_analysis

st.set_page_config(
    page_title="TCMB Makro Panel",
    page_icon="📊",
    layout="wide",
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, .stApp {{ background-color: {COLORS['bg']}; color: {COLORS['text']}; font-family: 'Inter', sans-serif; }}
.metric-card {{
    background: {COLORS['grid']};
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    border: 1px solid #3a3a52;
}}
.metric-label {{ font-size: 12px; color: {COLORS['muted']}; letter-spacing: .5px; text-transform: uppercase; margin-bottom: 6px; }}
.metric-value {{ font-size: 26px; font-weight: 700; color: {COLORS['text']}; }}
.metric-delta-up   {{ font-size: 12px; color: #2A9D8F; margin-top: 4px; }}
.metric-delta-down {{ font-size: 12px; color: {COLORS['red']}; margin-top: 4px; }}
.metric-date {{ font-size: 10px; color: {COLORS['muted']}; margin-top: 2px; }}
div[data-testid="stTabs"] button {{ color: {COLORS['muted']}; }}
div[data-testid="stTabs"] button[aria-selected="true"] {{ color: {COLORS['text']}; font-weight: 600; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── Başlık + tarih filtresi ──────────────────────────────────────────────────
col_title, col_filter = st.columns([3, 1])
with col_title:
    st.markdown("## 📊 TCMB Makro Göstergeler Paneli")
    st.caption("Türkiye Cumhuriyet Merkez Bankası · EVDS · Saatlik önbellekleme")
with col_filter:
    st.markdown("<div style='padding-top:16px'></div>", unsafe_allow_html=True)
    range_label = st.radio("Dönem", list(DATE_RANGES.keys()), index=1, horizontal=True)

start_date = DATE_RANGES[range_label]

# ── Veri yükleme ─────────────────────────────────────────────────────────────
with st.spinner("Veriler yükleniyor..."):
    try:
        usd      = filter_by_range(get_series("usd_try"), start_date)
        eur      = filter_by_range(get_series("eur_try"), start_date)
        rate     = filter_by_range(get_series("policy_rate"), start_date)
        reserves = filter_by_range(get_series("gross_reserves"), start_date)
        cpi_y    = filter_by_range(get_cpi_pct(12), start_date)
        cpi_m    = filter_by_range(get_cpi_pct(1), start_date)
    except ConnectionError as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        st.stop()

# ── Metrik kartları ──────────────────────────────────────────────────────────
def metric_card(col, label: str, df: pd.DataFrame, unit: str, invert: bool = False):
    val, delta = compute_delta(df)
    date = latest_date(df)
    if delta > 0:
        delta_class = "metric-delta-down" if invert else "metric-delta-up"
        arrow = "▲"
    else:
        delta_class = "metric-delta-up" if invert else "metric-delta-down"
        arrow = "▼"
    col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val:.2f} {unit}</div>
            <div class="{delta_class}">{arrow} {abs(delta):.2f} {unit}</div>
            <div class="metric-date">{date}</div>
        </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
metric_card(c1, "USD / TRY", usd, "₺", invert=True)
metric_card(c2, "EUR / TRY", eur, "₺", invert=True)
metric_card(c3, "Politika Faizi", rate, "%", invert=True)
metric_card(c4, "TÜFE Yıllık", cpi_y, "%", invert=True)
metric_card(c5, "Brüt Rezerv", reserves, "mn$")

st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)

# ── Sekmeler ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["💱 Döviz Kurları", "📈 Faiz", "🛒 Enflasyon", "🏦 Rezervler"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(area_chart(usd, "USD / TRY", "₺", COLORS["red"]), use_container_width=True)
    with c2:
        st.plotly_chart(area_chart(eur, "EUR / TRY", "₺", COLORS["blue"]), use_container_width=True)

with tab2:
    st.plotly_chart(area_chart(rate, "Politika Faizi (1 Haftalık Repo)", "%", COLORS["purple"]), use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(area_chart(cpi_y, "TÜFE Yıllık Değişim", "%", COLORS["orange"]), use_container_width=True)
    with c2:
        st.plotly_chart(bar_chart(cpi_m, "TÜFE Aylık Değişim", "%"), use_container_width=True)

with tab4:
    st.plotly_chart(area_chart(reserves, "Brüt Döviz Rezervleri", "mn$", COLORS["teal"]), use_container_width=True)

# ── AI Makro Analiz ──────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
st.markdown(
    f"<div style='font-size:14px; font-weight:600; color:{COLORS['text']}; margin-bottom:8px;'>"
    "🤖 AI Makro Analiz</div>",
    unsafe_allow_html=True,
)

usd_val, usd_delta   = compute_delta(usd)
eur_val, eur_delta   = compute_delta(eur)
rate_val, rate_delta = compute_delta(rate)
cpi_y_val, cpi_y_d  = compute_delta(cpi_y)
cpi_m_val, cpi_m_d  = compute_delta(cpi_m)
res_val, res_delta   = compute_delta(reserves)
last_date            = latest_date(usd)

with st.spinner("Claude analiz üretiyor..."):
    analysis = get_ai_analysis(
        usd=usd_val, usd_prev=usd_val - usd_delta,
        eur=eur_val, eur_prev=eur_val - eur_delta,
        rate=rate_val, rate_prev=rate_val - rate_delta,
        cpi_y=cpi_y_val, cpi_y_prev=cpi_y_val - cpi_y_d,
        cpi_m=cpi_m_val, cpi_m_prev=cpi_m_val - cpi_m_d,
        res=res_val, res_prev=res_val - res_delta,
        date=last_date,
    )

st.markdown(
    f"<div style='background:{COLORS['grid']}; border-radius:12px; padding:20px 22px;"
    f" border:1px solid #3a3a52; color:{COLORS['text']}; font-size:14px; line-height:1.75;'>"
    f"{analysis}"
    f"<div style='margin-top:12px; font-size:10px; color:{COLORS['muted']};'>"
    f"Kural tabanlı analiz · 6 saatte bir yenilenir · TCMB EVDS verileri</div>"
    f"</div>",
    unsafe_allow_html=True,
)

st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<div style='text-align:center; color:{COLORS['muted']}; font-size:12px;'>"
    "Veri kaynağı: <a href='https://evds3.tcmb.gov.tr' style='color:{COLORS[\"muted\"]}'>TCMB EVDS</a> · "
    "Veriler saatlik güncellenir · "
    "Kaynak kodu: <a href='https://github.com/Tuluntas09/tcmb-macro-panel' style='color:{COLORS[\"muted\"]}'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True,
)
