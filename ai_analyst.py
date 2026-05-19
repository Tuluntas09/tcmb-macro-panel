import streamlit as st


def _trend(delta: float, pct: bool = False) -> str:
    if pct:
        return "yükseldi" if delta > 0 else "geriledi"
    return "değer kaybetti" if delta > 0 else "değer kazandı"


@st.cache_data(ttl=21600, show_spinner=False)
def get_ai_analysis(
    usd: float, usd_prev: float,
    eur: float, eur_prev: float,
    rate: float, rate_prev: float,
    cpi_y: float, cpi_y_prev: float,
    cpi_m: float, cpi_m_prev: float,
    res: float, res_prev: float,
    date: str,
) -> str:
    usd_d  = usd - usd_prev
    eur_d  = eur - eur_prev
    cpi_d  = cpi_y - cpi_y_prev
    res_d  = res - res_prev
    rate_d = rate - rate_prev

    # Döviz yorumu
    if abs(usd_d) < 0.05:
        fx_comment = f"Döviz cephesinde USD/TRY kuru {usd:.2f} ₺ ile yatay seyrediyor."
    elif usd_d > 0:
        fx_comment = (
            f"Türk lirası dolar karşısında {_trend(usd_d)} ve USD/TRY {usd:.2f} ₺ "
            f"seviyesine ulaştı; kur baskısı sürmektedir."
        )
    else:
        fx_comment = (
            f"Türk lirası dolar karşısında güç kazandı; USD/TRY {usd:.2f} ₺'ye "
            f"geriledi."
        )

    # Enflasyon yorumu
    if cpi_y > 50:
        inf_str = "yüksek seyreden"
    elif cpi_y > 20:
        inf_str = "çift haneli"
    else:
        inf_str = "tek haneli"

    if cpi_d > 0:
        inf_comment = (
            f"Yıllık enflasyon %{cpi_y:.1f} ile {inf_str} düzeyde olup "
            f"bir önceki döneme göre {abs(cpi_d):.1f} puan yükseldi."
        )
    elif cpi_d < 0:
        inf_comment = (
            f"Yıllık enflasyon %{cpi_y:.1f} ile {inf_str} düzeyde, "
            f"bir önceki döneme kıyasla {abs(cpi_d):.1f} puanlık gerileme kaydetti."
        )
    else:
        inf_comment = (
            f"Yıllık enflasyon %{cpi_y:.1f} ile {inf_str} düzeyde yatay seyrediyor."
        )

    # Faiz yorumu
    if rate_d > 0:
        rate_comment = (
            f"TCMB politika faizini {abs(rate_d):.0f} baz puan artırarak "
            f"%{rate:.0f}'e yükseltti; sıkılaştırıcı para politikası devam etmektedir."
        )
    elif rate_d < 0:
        rate_comment = (
            f"TCMB politika faizini {abs(rate_d):.0f} baz puan indirerek "
            f"%{rate:.0f}'e çekti; para politikasında gevşeme süreci başladı."
        )
    else:
        rate_comment = (
            f"TCMB politika faizi %{rate:.0f} seviyesinde sabit tutulmaktadır."
        )

    # Rezerv yorumu
    if res_d > 0:
        res_comment = (
            f"Brüt döviz rezervleri {res/1000:.1f} milyar dolar ile "
            f"önceki döneme göre artış kaydetti; rezerv birikimi güçleniyor."
        )
    elif res_d < 0:
        res_comment = (
            f"Brüt döviz rezervleri {res/1000:.1f} milyar dolara geriledi; "
            f"dış tampon kapasite izlenmesi gereken bir başlık olmaya devam etmektedir."
        )
    else:
        res_comment = (
            f"Brüt döviz rezervleri {res/1000:.1f} milyar dolar seviyesinde yatay seyrediyor."
        )

    return f"{fx_comment} {inf_comment} {rate_comment} {res_comment}"
