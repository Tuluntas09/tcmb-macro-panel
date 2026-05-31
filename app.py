import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_processor import (
    get_series, get_cpi_pct, filter_by_range,
    compute_delta, latest_date, build_correlation_df,
)
from charts import area_chart, dual_area_chart, bar_chart, correlation_heatmap, COLORS
from config import DATE_RANGES
from ai_analyst import get_ai_analysis

st.set_page_config(
    page_title="TCMB Makro Panel",
    page_icon="📊",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root{
  --bg:#ECEEF3; --card:#FFFFFF;
  --teal:#2F6FD6; --up:#1E9E73; --amber:#C2872F; --red:#D6454D;
  --text:#1B2536; --muted:#697587; --grid:#E4E8EF; --hair:#DCE1E9;
}

html,body,.stApp{
  background-color:var(--bg) !important;
  color:var(--text);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
  -webkit-font-smoothing:antialiased;
}
.stApp>header{ background:transparent !important; }
.block-container{ padding:3.5rem 32px 48px !important; max-width:1400px !important; margin:0 auto; }
footer,#MainMenu,[data-testid="stToolbar"],[data-testid="stDecoration"]{
  visibility:hidden !important; display:none !important;
}
/* remove default streamlit gap between elements */
[data-testid="stVerticalBlock"]>[data-testid="stVerticalBlock"]{gap:0 !important;}

/* ── HEADER ── */
.ph{
  display:flex;align-items:center;justify-content:space-between;
  padding-bottom:18px;margin-bottom:20px;border-bottom:1px solid var(--hair);
}
.brand{display:flex;align-items:center;gap:14px;}
.logo{
  width:42px;height:42px;border-radius:10px;flex-shrink:0;
  background:linear-gradient(155deg,#1F2C46 0%,#141E30 100%);
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 0 1px rgba(78,140,247,.30),0 6px 18px rgba(0,0,0,.25);
}
.brand-title{font-size:18px;font-weight:600;color:var(--text);margin:0;letter-spacing:-.2px;}
.brand-sub{font-size:11px;color:var(--muted);margin-top:3px;letter-spacing:.3px;text-transform:uppercase;}
.live-pill{
  display:inline-flex;align-items:center;gap:8px;font-size:12px;color:var(--muted);
  padding:6px 12px;border:1px solid var(--hair);border-radius:7px;
  background:rgba(27,37,54,.02);
}
.live-pill .lt{color:var(--text);font-weight:500;}
.dot{width:8px;height:8px;border-radius:50%;background:var(--teal);position:relative;display:inline-block;}
.dot::after{
  content:"";position:absolute;inset:-4px;border-radius:50%;
  background:var(--teal);opacity:.4;animation:pulse 1.8s ease-out infinite;
}
@keyframes pulse{0%{transform:scale(.6);opacity:.5;}100%{transform:scale(2.4);opacity:0;}}

/* ── METRIC CARDS ── */
.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px;}
.metric{
  background:var(--card);border:1px solid var(--hair);border-radius:11px;
  padding:16px 17px 15px;position:relative;overflow:hidden;transition:.18s;
}
.metric:hover{border-color:#C4CBD6;transform:translateY(-2px);box-shadow:0 8px 22px rgba(27,37,54,.07);}
.m-acc{position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--teal);opacity:0;transition:.18s;}
.metric:hover .m-acc{opacity:1;}
.m-lbl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;font-weight:600;
  display:flex;align-items:center;gap:6px;}
.m-unit{color:#5d6679;font-weight:500;letter-spacing:.2px;text-transform:none;font-size:10px;}
.m-val{
  font-size:28px;font-weight:600;margin:11px 0 9px;letter-spacing:-.5px;line-height:1;
  color:var(--text);font-family:'JetBrains Mono',ui-monospace,monospace;
}
.m-row{display:flex;align-items:center;justify-content:space-between;}
.delta{
  display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:600;
  padding:3px 8px;border-radius:6px;font-family:'JetBrains Mono',monospace;
}
.delta-up  {color:#1E9E73;background:rgba(30,158,115,.12);}
.delta-down{color:#D6454D;background:rgba(214,69,77,.12);}
.delta-flat{color:var(--muted);background:rgba(105,117,135,.12);}
.m-upd{font-size:10px;color:#5d6679;font-family:'JetBrains Mono',monospace;}
.spark{position:absolute;right:0;bottom:0;width:64px;height:34px;opacity:.45;pointer-events:none;}

/* ── TABS ── */
div[data-testid="stTabs"]{
  background:var(--card) !important;
  border:1px solid var(--hair) !important;
  border-radius:13px !important;
  overflow:hidden !important;
}
div[data-testid="stTabs"] [role="tablist"]{
  background:rgba(27,37,54,.022) !important;
  border-bottom:1px solid var(--hair) !important;
  padding:0 8px !important;
}
div[data-testid="stTabs"] [role="tab"]{
  color:var(--muted) !important;font-size:13px !important;font-weight:500 !important;
  padding:14px 18px !important;border-radius:0 !important;background:transparent !important;
  transition:.16s !important;letter-spacing:.1px !important;
}
div[data-testid="stTabs"] [role="tab"]:hover{color:var(--text) !important;}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"]{
  color:var(--text) !important;font-weight:600 !important;
  border-bottom:2px solid var(--teal) !important;
}
div[data-testid="stTabs"] [role="tabpanel"]{
  padding:16px 20px 20px !important;background:var(--card) !important;
}

/* ── CHART HEAD ── */
.ch{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:4px;}
.ct{font-size:16px;font-weight:600;letter-spacing:-.2px;color:var(--text);}
.cm{font-size:11.5px;color:var(--muted);font-weight:400;margin-top:5px;letter-spacing:.2px;}
.leg{display:flex;gap:16px;align-items:center;padding-top:6px;}
.leg-item{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--muted);}
.leg-sw{width:11px;height:3px;border-radius:2px;display:inline-block;}

/* ── DOWNLOAD BUTTON ── */
div[data-testid="stDownloadButton"]>button{
  background:transparent !important;border:1px solid var(--hair) !important;
  color:var(--muted) !important;font-size:11px !important;font-weight:500 !important;
  padding:4px 12px !important;border-radius:6px !important;letter-spacing:.3px !important;
  transition:all .15s !important;
}
div[data-testid="stDownloadButton"]>button:hover{
  border-color:var(--teal) !important;color:var(--teal) !important;
  background:rgba(47,111,214,.06) !important;
}

/* ── ANALYSIS + STATS ── */
.ac{
  background:var(--card);border:1px solid var(--hair);border-left:3px solid var(--teal);
  border-radius:11px;padding:20px 22px;
}
.ac h3{margin:0 0 4px;font-size:13px;font-weight:600;letter-spacing:.3px;
  display:flex;align-items:center;gap:9px;color:var(--text);}
.atag{
  font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--teal);
  border:1px solid rgba(47,111,214,.40);padding:2px 7px;border-radius:5px;letter-spacing:.5px;
}
.adate{font-size:11px;color:#5d6679;margin-bottom:13px;}
.abody{font-size:13.5px;line-height:1.65;color:#46505F;}
.abody strong{color:var(--text);font-weight:600;}
.abody p{margin:0 0 11px;}
.abody p:last-child{margin-bottom:0;}

.sc{background:var(--card);border:1px solid var(--hair);border-radius:11px;overflow:hidden;}
.sr{display:flex;align-items:center;justify-content:space-between;
  padding:13px 20px;border-bottom:1px solid var(--grid);}
.sr:last-child{border-bottom:none;}
.sk{font-size:12.5px;color:var(--muted);}
.sv{font-size:13px;font-weight:600;font-family:'JetBrains Mono',monospace;color:var(--text);}
.sv.pos{color:#1E9E73;} .sv.neg{color:#D6454D;}

/* ── FOOTER ── */
.pf{
  display:flex;align-items:center;justify-content:space-between;
  margin-top:22px;padding-top:16px;border-top:1px solid var(--hair);
  font-size:11px;color:#5d6679;
}
.pf a{color:var(--teal);text-decoration:none;}
.pf a:hover{text-decoration:underline;}

/* ── RANGE RADIO → button group ── */
div[data-testid="stRadio"]>div:last-child{
  display:flex !important;flex-direction:row !important;gap:2px !important;
  background:var(--card) !important;padding:3px !important;
  border-radius:8px !important;border:1px solid var(--hair) !important;
  width:fit-content !important;align-items:center !important;
}
div[data-testid="stRadio"]>div:last-child>label{
  display:flex !important;align-items:center !important;justify-content:center !important;
  font-family:'JetBrains Mono',monospace !important;font-size:12px !important;
  font-weight:500 !important;color:var(--muted) !important;
  padding:6px 12px !important;border-radius:6px !important;cursor:pointer !important;
  letter-spacing:.2px !important;min-width:36px !important;
  text-align:center !important;transition:.16s !important;
}
div[data-testid="stRadio"]>div:last-child>label:has(input:checked){
  background:var(--teal) !important;color:#fff !important;font-weight:600 !important;
}
/* Hide radio inputs and ALL circle indicators */
div[data-testid="stRadio"] input[type="radio"]{ display:none !important; }
div[data-testid="stRadio"] > label{ display:none !important; }
div[data-testid="stRadio"] [data-baseweb="radio"]{ display:none !important; }
div[data-testid="stRadio"] svg{ display:none !important; }
/* Nuclear: hide everything except the last child (text) in each option's wrapper div */
div[data-testid="stRadio"] label > div{ gap:0 !important; }
div[data-testid="stRadio"] label > div > *:not(:last-child){
  display:none !important; width:0 !important; height:0 !important;
  min-width:0 !important; min-height:0 !important; overflow:hidden !important;
}
div[data-testid="stRadio"] label p{
  margin:0 !important;line-height:1 !important;font-size:12px !important;
  font-family:'JetBrains Mono',monospace !important;letter-spacing:.2px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper functions ──────────────────────────────────────────────────────────
def sparkline_svg(df: pd.DataFrame, color: str, last_n: int = 90) -> str:
    vals = df["deger"].values
    if len(vals) < 2:
        return ""
    vals = vals[-last_n:]
    mn, mx = float(vals.min()), float(vals.max())
    rng = mx - mn or 1.0
    w, h = 64, 34
    pts = " ".join(
        f"{i / (len(vals)-1) * w:.1f},{h - 2 - ((v - mn) / rng) * (h - 6):.1f}"
        for i, v in enumerate(vals)
    )
    return (
        f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
        f'<polyline points="{pts}" fill="none" stroke="{color}" '
        f'stroke-width="1.5" stroke-linejoin="round"/></svg>'
    )


def metric_card(
    col,
    label: str,
    unit_tag: str,
    df: pd.DataFrame,
    df_raw: pd.DataFrame,
    suffix: str,
    prefix: str,
    invert: bool,
    spark_color: str,
    dec: int = 2,
    scale: float = 1.0,
) -> None:
    val, delta = compute_delta(df)
    val   *= scale
    delta *= scale
    date   = latest_date(df)
    if delta == 0:
        cls, arrow = "delta-flat", "▬"
    elif delta > 0:
        cls, arrow = ("delta-down" if invert else "delta-up"), "▲"
    else:
        cls, arrow = ("delta-up" if invert else "delta-down"), "▼"
    val_s   = f"{prefix}{val:,.{dec}f}{suffix}".replace(",", ".")
    delta_s = f"{arrow} {abs(delta):,.{dec}f}{suffix}".replace(",", ".")
    spark   = sparkline_svg(df_raw, spark_color)
    col.markdown(f"""
        <div class="metric">
          <div class="m-acc"></div>
          <div class="m-lbl">{label} <span class="m-unit">{unit_tag}</span></div>
          <div class="m-val">{val_s}</div>
          <div class="m-row">
            <span class="delta {cls}">{delta_s}</span>
            <span class="m-upd">{date}</span>
          </div>
          {spark}
        </div>
    """, unsafe_allow_html=True)


def chart_head(title: str, meta: str, legend: list[dict] | None = None) -> None:
    leg_html = ""
    if legend:
        items = "".join(
            f'<div class="leg-item">'
            f'<span class="leg-sw" style="background:{l["c"]}"></span>{l["t"]}'
            f'</div>'
            for l in legend
        )
        leg_html = f'<div class="leg">{items}</div>'
    st.markdown(f"""
        <div class="ch">
          <div>
            <div class="ct">{title}</div>
            <div class="cm">{meta}</div>
          </div>
          {leg_html}
        </div>
    """, unsafe_allow_html=True)


def csv_btn(df: pd.DataFrame, filename: str) -> None:
    csv = (
        df.rename(columns={"tarih": "Tarih", "deger": "Değer"})
        .to_csv(index=False)
        .encode("utf-8")
    )
    st.download_button("⬇ CSV İndir", csv, file_name=filename, mime="text/csv")


# ── Header ────────────────────────────────────────────────────────────────────
col_brand, col_range = st.columns([3, 1])

with col_brand:
    now_str = datetime.now().strftime("%d %b %Y, %H:%M TSİ")
    st.markdown(f"""
        <div class="ph">
          <div class="brand">
            <div class="logo">
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                <polyline points="2,15 7,10 11,12.5 20,3"
                  stroke="#4E8CF7" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="20" cy="3" r="2" fill="#4E8CF7"/>
                <line x1="2" y1="19" x2="20" y2="19"
                  stroke="#4E8CF7" stroke-width="1.4"
                  stroke-linecap="round" opacity="0.35"/>
              </svg>
            </div>
            <div>
              <div class="brand-title">TCMB Makro Göstergeler Paneli</div>
              <div class="brand-sub">Türkiye Cumhuriyet Merkez Bankası · Makroekonomik İzleme</div>
            </div>
          </div>
          <div class="live-pill">
            <span class="dot"></span>
            <span class="lt">CANLI</span> · {now_str}
          </div>
        </div>
    """, unsafe_allow_html=True)

with col_range:
    st.markdown("<div style='padding-top:8px'></div>", unsafe_allow_html=True)
    range_label = st.radio(
        "Dönem",
        list(DATE_RANGES.keys()),
        index=3,
        horizontal=True,
        label_visibility="hidden",
    )

start_date = DATE_RANGES[range_label]

# ── Data loading ──────────────────────────────────────────────────────────────
with st.spinner("Veriler yükleniyor..."):
    try:
        usd_raw      = get_series("usd_try")
        eur_raw      = get_series("eur_try")
        rate_raw     = get_series("policy_rate")
        reserves_raw = get_series("gross_reserves")
        cpi_y_raw    = get_cpi_pct(12)
        cpi_m_raw    = get_cpi_pct(1)

        usd      = filter_by_range(usd_raw,      start_date)
        eur      = filter_by_range(eur_raw,       start_date)
        rate     = filter_by_range(rate_raw,      start_date)
        reserves = filter_by_range(reserves_raw,  start_date)
        cpi_y    = filter_by_range(cpi_y_raw,     start_date)
        cpi_m    = filter_by_range(cpi_m_raw,     start_date)
    except ConnectionError as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        st.stop()

# ── Metric cards ──────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
metric_card(c1, "USD / TRY",      "Spot",      usd,      usd_raw,      "₺",   "",  invert=True,  spark_color=COLORS["teal"],  dec=4)
metric_card(c2, "EUR / TRY",      "Spot",      eur,      eur_raw,      "₺",   "",  invert=True,  spark_color=COLORS["amber"], dec=4)
metric_card(c3, "Politika Faizi", "1H Repo",   rate,     rate_raw,     "%",   "",  invert=True,  spark_color=COLORS["up"])
metric_card(c4, "TÜFE Yıllık",   "YoY",       cpi_y,    cpi_y_raw,    "%",   "",  invert=True,  spark_color=COLORS["red"],   dec=1)
metric_card(c5, "Brüt Rezerv",   "Milyar $",  reserves, reserves_raw, "B",   "$", invert=False, spark_color=COLORS["teal"],  dec=1, scale=1/1000)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Tab panel ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💱 Döviz Kurları", "📈 Politika Faizi",
    "🛒 Enflasyon", "🏦 Rezervler", "🔗 Korelasyon",
])

with tab1:
    chart_head(
        "Döviz Kurları — USD/TRY & EUR/TRY",
        "Spot kapanış, günlük · TCMB gösterge niteliğinde",
        legend=[{"c": COLORS["teal"], "t": "USD/TRY"}, {"c": COLORS["amber"], "t": "EUR/TRY"}],
    )
    st.plotly_chart(
        dual_area_chart(usd, eur, "USD/TRY", "EUR/TRY", "₺", COLORS["teal"], COLORS["amber"]),
        use_container_width=True,
    )
    cb1, cb2 = st.columns(2)
    with cb1: csv_btn(usd, "usd_try.csv")
    with cb2: csv_btn(eur, "eur_try.csv")

with tab2:
    chart_head(
        "TCMB Politika Faizi",
        "1 hafta vadeli repo ihale faiz oranı (%) · adımsal",
        legend=[{"c": COLORS["teal"], "t": "Politika Faizi"}],
    )
    st.plotly_chart(
        area_chart(rate, "Politika Faizi", "%", COLORS["teal"], step=True),
        use_container_width=True,
    )
    csv_btn(rate, "politika_faizi.csv")

with tab3:
    chart_head(
        "Tüketici Enflasyonu (TÜFE)",
        "Yıllık % değişim · TÜİK · dezenflasyon patikası",
        legend=[{"c": COLORS["amber"], "t": "TÜFE YoY"}, {"c": COLORS["teal"], "t": "TÜFE Aylık"}],
    )
    cc1, cc2 = st.columns(2)
    with cc1:
        st.plotly_chart(
            area_chart(cpi_y, "TÜFE Yıllık", "%", COLORS["amber"]),
            use_container_width=True,
        )
        csv_btn(cpi_y, "tufe_yillik.csv")
    with cc2:
        st.plotly_chart(
            bar_chart(cpi_m, "TÜFE Aylık", "%"),
            use_container_width=True,
        )
        csv_btn(cpi_m, "tufe_aylik.csv")

with tab4:
    chart_head(
        "Brüt Döviz Rezervleri",
        "Altın dahil brüt rezervler (mn USD) · TCMB haftalık",
        legend=[{"c": COLORS["teal"], "t": "Brüt Rezerv"}],
    )
    st.plotly_chart(
        area_chart(reserves, "Brüt Rezerv", "mn$", COLORS["teal"]),
        use_container_width=True,
    )
    csv_btn(reserves, "brut_rezerv.csv")

with tab5:
    chart_head(
        "Korelasyon Matrisi",
        "Günlük değişimlerin Pearson korelasyonu · tüm veri geçmişi",
    )
    corr_df = build_correlation_df(usd_raw, eur_raw, rate_raw, cpi_y_raw, reserves_raw)
    st.plotly_chart(correlation_heatmap(corr_df), use_container_width=True)
    st.markdown(
        f"<div style='font-size:11.5px;color:{COLORS['muted']};margin-top:-8px;padding-bottom:4px;'>"
        "Değerler −1 (ters yönlü) ile +1 (aynı yönlü) arasında değişir. "
        "Tüm veri geçmişi kullanılmıştır.</div>",
        unsafe_allow_html=True,
    )

# ── Deltas ────────────────────────────────────────────────────────────────────
usd_val,  usd_d   = compute_delta(usd)
eur_val,  eur_d   = compute_delta(eur)
rate_val, rate_d  = compute_delta(rate)
cpi_y_val, cpi_yd = compute_delta(cpi_y)
cpi_m_val, cpi_md = compute_delta(cpi_m)
res_val,  res_d   = compute_delta(reserves)
last_date          = latest_date(usd)

# ── AI analysis ───────────────────────────────────────────────────────────────
with st.spinner("Analiz üretiliyor..."):
    analysis = get_ai_analysis(
        usd=usd_val,   usd_prev=usd_val   - usd_d,
        eur=eur_val,   eur_prev=eur_val   - eur_d,
        rate=rate_val, rate_prev=rate_val - rate_d,
        cpi_y=cpi_y_val, cpi_y_prev=cpi_y_val - cpi_yd,
        cpi_m=cpi_m_val, cpi_m_prev=cpi_m_val - cpi_md,
        res=res_val,   res_prev=res_val   - res_d,
        date=last_date,
    )

# ── Stats (right column) ──────────────────────────────────────────────────────
_cutoff_1y = (datetime.today() - timedelta(days=365)).strftime("%d-%m-%Y")

usd_1y = filter_by_range(usd_raw, _cutoff_1y)
usd_52lo = float(usd_1y["deger"].min()) if len(usd_1y) else 0.0
usd_52hi = float(usd_1y["deger"].max()) if len(usd_1y) else 0.0
usd_yoy  = (usd_val / float(usd_1y["deger"].iloc[0]) - 1) * 100 if len(usd_1y) else 0.0

real_rate = rate_val - cpi_y_val

cpi_peak  = float(cpi_y_raw["deger"].max()) if len(cpi_y_raw) else cpi_y_val
cpi_drop  = cpi_peak - cpi_y_val

res_1y    = filter_by_range(reserves_raw, _cutoff_1y)
res_yoy   = (res_val / float(res_1y["deger"].iloc[0]) - 1) * 100 if len(res_1y) else 0.0

usd_cpi_rho = float(corr_df.loc["USD/TRY", "TÜFE Yıllık"]) if "USD/TRY" in corr_df.index else 0.0

stats_rows = [
    ("USD/TRY 52-hafta",    f"{usd_52lo:.2f} – {usd_52hi:.2f}",                        None),
    ("Yıllık değişim",      f"{'+'if usd_yoy>0 else ''}{usd_yoy:.1f}%",               "neg" if usd_yoy > 0 else "pos"),
    ("Reel politika faizi", f"{'+'if real_rate>0 else ''}{real_rate:.1f} puan",        "pos" if real_rate > 0 else "neg"),
    ("TÜFE zirveden düşüş", f"−{cpi_drop:.1f} puan",                                   "pos" if cpi_drop > 0 else None),
    ("Rezerv YoY",          f"{'+'if res_yoy>0 else ''}{res_yoy:.1f}%",               "pos" if res_yoy > 0 else "neg"),
    ("USD ↔ TÜFE (ρ)",      f"{usd_cpi_rho:+.2f}",                                     None),
]

stats_html = "".join(
    f'<div class="sr">'
    f'<span class="sk">{k}</span>'
    f'<span class="sv {c or ""}">{v}</span>'
    f'</div>'
    for k, v, c in stats_rows
)

# ── Lower section: Analysis + Stats ──────────────────────────────────────────
col_an, col_st = st.columns([1.55, 1])

with col_an:
    st.markdown(f"""
        <div class="ac">
          <h3><span class="atag">MAKRO ANALİZ</span> Piyasa Değerlendirmesi</h3>
          <div class="adate">{last_date} · Kapanış değerlendirmesi</div>
          <div class="abody">{analysis}</div>
        </div>
    """, unsafe_allow_html=True)

with col_st:
    st.markdown(f'<div class="sc">{stats_html}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="pf">
      <div>
        Kaynak: <a href="https://evds3.tcmb.gov.tr">TCMB EVDS</a>
        &nbsp;·&nbsp; TÜİK
        &nbsp;·&nbsp; Veriler saatlik güncellenir
      </div>
      <div>
        Eğitim amaçlıdır · Yatırım tavsiyesi değildir
        &nbsp;·&nbsp; <a href="https://github.com/Tuluntas09/tcmb-macro-panel">GitHub</a>
      </div>
    </div>
""", unsafe_allow_html=True)
