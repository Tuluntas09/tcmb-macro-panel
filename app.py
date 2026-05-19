import streamlit as st
import pandas as pd
from data_processor import get_series, get_cpi_pct, filter_by_range, compute_delta, latest_date, build_correlation_df
from charts import area_chart, bar_chart, correlation_heatmap, COLORS
from config import DATE_RANGES
from ai_analyst import get_ai_analysis

st.set_page_config(
    page_title="TCMB Makro Panel",
    page_icon="📊",
    layout="wide",
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

html, body, .stApp {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-family: 'Inter', sans-serif;
}}

/* ── Header ── */
.panel-header {{
    padding: 8px 0 20px 0;
    border-bottom: 1px solid #2a2a3e;
    margin-bottom: 24px;
}}
.panel-title {{
    font-size: 22px;
    font-weight: 700;
    color: {COLORS['text']};
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.panel-subtitle {{
    font-size: 12px;
    color: {COLORS['muted']};
    margin-top: 4px;
    letter-spacing: 0.2px;
}}
.live-dot {{
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {COLORS['teal']};
    box-shadow: 0 0 6px {COLORS['teal']};
    margin-right: 6px;
    vertical-align: middle;
}}

/* ── Metric cards ── */
.metric-card {{
    background: linear-gradient(145deg, #262638 0%, #222234 100%);
    border-radius: 14px;
    padding: 18px 16px 14px;
    text-align: center;
    border: 1px solid #32324a;
    border-top: 3px solid var(--accent);
    transition: transform .15s ease, box-shadow .15s ease;
    position: relative;
    overflow: hidden;
}}
.metric-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% -20%, rgba(255,255,255,.04) 0%, transparent 70%);
    pointer-events: none;
}}
.metric-label {{
    font-size: 10px;
    font-weight: 600;
    color: {COLORS['muted']};
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}}
.metric-value {{
    font-size: 28px;
    font-weight: 700;
    color: {COLORS['text']};
    letter-spacing: -0.5px;
    line-height: 1;
}}
.metric-unit {{
    font-size: 14px;
    font-weight: 400;
    color: {COLORS['muted']};
    margin-left: 2px;
}}
.metric-delta-up   {{
    display: inline-flex; align-items: center; gap: 3px;
    font-size: 12px; font-weight: 500;
    color: {COLORS['teal']};
    background: rgba(42,157,143,.12);
    border-radius: 20px; padding: 2px 8px;
    margin-top: 8px;
}}
.metric-delta-down {{
    display: inline-flex; align-items: center; gap: 3px;
    font-size: 12px; font-weight: 500;
    color: {COLORS['red']};
    background: rgba(230,57,70,.12);
    border-radius: 20px; padding: 2px 8px;
    margin-top: 8px;
}}
.metric-date {{
    font-size: 10px;
    color: {COLORS['muted']};
    margin-top: 6px;
    opacity: .7;
}}

/* ── Tabs ── */
div[data-testid="stTabs"] {{
    border-bottom: 1px solid #2a2a3e;
}}
div[data-testid="stTabs"] button {{
    color: {COLORS['muted']};
    font-size: 13px;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 0;
    transition: color .15s;
}}
div[data-testid="stTabs"] button:hover {{
    color: {COLORS['text']};
}}
div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {COLORS['text']};
    font-weight: 600;
    border-bottom: 2px solid {COLORS['teal']};
}}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {{
    background: transparent;
    border: 1px solid #3a3a52;
    color: {COLORS['muted']};
    font-size: 11px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: .3px;
    transition: all .15s;
}}
div[data-testid="stDownloadButton"] > button:hover {{
    border-color: {COLORS['teal']};
    color: {COLORS['teal']};
    background: rgba(42,157,143,.08);
}}

/* ── Analiz kartı ── */
.analiz-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    margin-top: 8px;
}}
.analiz-badge {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: .8px;
    text-transform: uppercase;
    color: {COLORS['teal']};
    background: rgba(42,157,143,.12);
    border: 1px solid rgba(42,157,143,.25);
    border-radius: 20px;
    padding: 3px 10px;
}}
.analiz-title {{
    font-size: 15px;
    font-weight: 600;
    color: {COLORS['text']};
}}
.analiz-card {{
    background: linear-gradient(145deg, #262638 0%, #222234 100%);
    border-radius: 14px;
    padding: 22px 24px;
    border: 1px solid #32324a;
    border-left: 3px solid {COLORS['teal']};
    color: {COLORS['text']};
    font-size: 14px;
    line-height: 1.8;
}}
.analiz-meta {{
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #2a2a3e;
    font-size: 10px;
    color: {COLORS['muted']};
    display: flex;
    align-items: center;
    gap: 6px;
}}

/* ── Footer ── */
.footer {{
    text-align: center;
    color: {COLORS['muted']};
    font-size: 11px;
    padding: 16px 0 8px;
    border-top: 1px solid #2a2a3e;
    margin-top: 8px;
}}
.footer a {{ color: {COLORS['muted']}; text-decoration: none; }}
.footer a:hover {{ color: {COLORS['text']}; }}

footer {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── Başlık + tarih filtresi ──────────────────────────────────────────────────
col_title, col_filter = st.columns([3, 1])
with col_title:
    st.markdown("""
        <div class="panel-header">
            <div class="panel-title">📊 TCMB Makro Göstergeler Paneli</div>
            <div class="panel-subtitle">
                <span class="live-dot"></span>
                Türkiye Cumhuriyet Merkez Bankası · EVDS · Saatlik önbellekleme
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_filter:
    st.markdown("<div style='padding-top:20px'></div>", unsafe_allow_html=True)
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
def metric_card(col, label: str, df: pd.DataFrame, unit: str, accent: str, invert: bool = False):
    val, delta = compute_delta(df)
    date = latest_date(df)
    if delta > 0:
        delta_class = "metric-delta-down" if invert else "metric-delta-up"
        arrow = "▲"
    else:
        delta_class = "metric-delta-up" if invert else "metric-delta-down"
        arrow = "▼"
    col.markdown(f"""
        <div class="metric-card" style="--accent: {accent}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val:.2f}<span class="metric-unit">{unit}</span></div>
            <div><span class="{delta_class}">{arrow} {abs(delta):.2f}{unit}</span></div>
            <div class="metric-date">{date}</div>
        </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
metric_card(c1, "USD / TRY",      usd,      "₺",   COLORS["red"],    invert=True)
metric_card(c2, "EUR / TRY",      eur,      "₺",   COLORS["blue"],   invert=True)
metric_card(c3, "Politika Faizi", rate,     "%",   COLORS["purple"], invert=True)
metric_card(c4, "TÜFE Yıllık",    cpi_y,    "%",   COLORS["orange"], invert=True)
metric_card(c5, "Brüt Rezerv",    reserves, "mn$", COLORS["teal"])

st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)

# ── Sekmeler ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💱 Döviz Kurları", "📈 Faiz", "🛒 Enflasyon", "🏦 Rezervler", "🔗 Korelasyon"])


def _csv_btn(df, filename):
    csv = df.rename(columns={"tarih": "Tarih", "deger": "Değer"}).to_csv(index=False).encode("utf-8")
    st.download_button("⬇ CSV İndir", csv, file_name=filename, mime="text/csv", use_container_width=False)


with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(area_chart(usd, "USD / TRY", "₺", COLORS["red"]), use_container_width=True)
        _csv_btn(usd, "usd_try.csv")
    with c2:
        st.plotly_chart(area_chart(eur, "EUR / TRY", "₺", COLORS["blue"]), use_container_width=True)
        _csv_btn(eur, "eur_try.csv")

with tab2:
    st.plotly_chart(area_chart(rate, "Politika Faizi (1 Haftalık Repo)", "%", COLORS["purple"]), use_container_width=True)
    _csv_btn(rate, "politika_faizi.csv")

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(area_chart(cpi_y, "TÜFE Yıllık Değişim", "%", COLORS["orange"]), use_container_width=True)
        _csv_btn(cpi_y, "tufe_yillik.csv")
    with c2:
        st.plotly_chart(bar_chart(cpi_m, "TÜFE Aylık Değişim", "%"), use_container_width=True)
        _csv_btn(cpi_m, "tufe_aylik.csv")

with tab4:
    st.plotly_chart(area_chart(reserves, "Brüt Döviz Rezervleri", "mn$", COLORS["teal"]), use_container_width=True)
    _csv_btn(reserves, "brut_rezerv.csv")

with tab5:
    usd_full      = get_series("usd_try")
    eur_full      = get_series("eur_try")
    rate_full     = get_series("policy_rate")
    reserves_full = get_series("gross_reserves")
    cpi_y_full    = get_cpi_pct(12)
    corr_df = build_correlation_df(usd_full, eur_full, rate_full, cpi_y_full, reserves_full)
    st.plotly_chart(correlation_heatmap(corr_df), use_container_width=True)
    st.markdown(
        f"<div style='font-size:12px; color:{COLORS['muted']}; margin-top:-8px;'>"
        "Tüm veri geçmişi kullanılmıştır (Max aralığı). "
        "Değerler −1 (ters yönlü) ile +1 (aynı yönlü) arasında değişir.</div>",
        unsafe_allow_html=True,
    )

# ── Makro Analiz ─────────────────────────────────────────────────────────────
usd_val, usd_delta   = compute_delta(usd)
eur_val, eur_delta   = compute_delta(eur)
rate_val, rate_delta = compute_delta(rate)
cpi_y_val, cpi_y_d  = compute_delta(cpi_y)
cpi_m_val, cpi_m_d  = compute_delta(cpi_m)
res_val, res_delta   = compute_delta(reserves)
last_date            = latest_date(usd)

with st.spinner("Analiz üretiliyor..."):
    analysis = get_ai_analysis(
        usd=usd_val, usd_prev=usd_val - usd_delta,
        eur=eur_val, eur_prev=eur_val - eur_delta,
        rate=rate_val, rate_prev=rate_val - rate_delta,
        cpi_y=cpi_y_val, cpi_y_prev=cpi_y_val - cpi_y_d,
        cpi_m=cpi_m_val, cpi_m_prev=cpi_m_val - cpi_m_d,
        res=res_val, res_prev=res_val - res_delta,
        date=last_date,
    )

st.markdown("""
    <div class="analiz-header">
        <span class="analiz-badge">Makro Analiz</span>
        <span class="analiz-title">Güncel Ekonomik Görünüm</span>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="analiz-card">'
    f'{analysis}'
    f'<div class="analiz-meta">'
    f'<span class="live-dot"></span>'
    f'Kural tabanlı analiz · 6 saatte bir yenilenir · TCMB EVDS verileri · {last_date}'
    f'</div></div>',
    unsafe_allow_html=True,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    'Veri kaynağı: <a href="https://evds3.tcmb.gov.tr">TCMB EVDS</a>'
    ' &nbsp;·&nbsp; Veriler saatlik güncellenir'
    ' &nbsp;·&nbsp; <a href="https://github.com/Tuluntas09/tcmb-macro-panel">GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)
