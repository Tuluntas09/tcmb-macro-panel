import streamlit as st
from data_processor import get_series, get_cpi_pct, latest_value, latest_date
from charts import line_chart

st.set_page_config(
    page_title="TCMB Makro Panel",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
    <style>
    .stApp { background-color: #1D1D2E; color: #F1FAEE; }
    .metric-card { background: #2E2E42; border-radius: 10px; padding: 16px; text-align: center; }
    .metric-label { font-size: 13px; color: #A8DADC; margin-bottom: 4px; }
    .metric-value { font-size: 28px; font-weight: bold; color: #F1FAEE; }
    .metric-date { font-size: 11px; color: #888; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 TCMB Makro Göstergeler Paneli")
st.caption("Türkiye Cumhuriyet Merkez Bankası · EVDS verileri · Saatlik güncelleme")

with st.spinner("Veriler yükleniyor..."):
    usd = get_series("usd_try")
    eur = get_series("eur_try")
    rate = get_series("policy_rate")
    cpi_yillik = get_cpi_pct(period=12)
    cpi_aylik = get_cpi_pct(period=1)

# Özet metrik kartları
col1, col2, col3, col4, col5 = st.columns(5)

metrics = [
    (col1, "USD/TRY", usd, "₺"),
    (col2, "EUR/TRY", eur, "₺"),
    (col3, "Politika Faizi", rate, "%"),
    (col4, "TÜFE Yıllık", cpi_yillik, "%"),
    (col5, "TÜFE Aylık", cpi_aylik, "%"),
]

for col, label, df, unit in metrics:
    val = latest_value(df)
    date = latest_date(df)
    col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val:.2f} {unit}</div>
            <div class="metric-date">{date}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Grafikler
tab1, tab2, tab3 = st.tabs(["💱 Döviz Kurları", "📈 Faiz", "🛒 Enflasyon"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(line_chart(usd, "USD/TRY", "₺", "#E63946"), use_container_width=True)
    with c2:
        st.plotly_chart(line_chart(eur, "EUR/TRY", "₺", "#457B9D"), use_container_width=True)

with tab2:
    st.plotly_chart(line_chart(rate, "Politika Faizi (1 Haftalık Repo)", "%", "#A8DADC"), use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(line_chart(cpi_yillik, "TÜFE Yıllık Değişim", "%", "#F4A261"), use_container_width=True)
    with c2:
        st.plotly_chart(line_chart(cpi_aylik, "TÜFE Aylık Değişim", "%", "#2A9D8F"), use_container_width=True)
