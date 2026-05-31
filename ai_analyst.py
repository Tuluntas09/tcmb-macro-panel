import streamlit as st


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
    """Kural tabanlı Türkçe makro analiz — HTML paragraf döner."""
    usd_d  = usd - usd_prev
    eur_d  = eur - eur_prev
    cpi_d  = cpi_y - cpi_y_prev
    res_d  = res - res_prev
    rate_d = rate - rate_prev

    # ── Döviz paragrafı ──────────────────────────────────────────────
    if abs(usd_d) < 0.05:
        fx = (
            f"<strong>USD/TRY {usd:.4f} ₺</strong> ile yatay seyrediyor. "
            f"EUR/TRY {eur:.4f} ₺ seviyesinde; çapraz kur görece istikrarlı "
            f"seyrini korumaktadır."
        )
    elif usd_d > 0:
        fx = (
            f"Türk lirası değer kaybetti; <strong>USD/TRY {usd:.4f} ₺</strong> "
            f"seviyesine yükseldi (<strong>+{abs(usd_d):.4f} ₺</strong>). "
            f"EUR/TRY {eur:.4f} ₺ ile paralel bir seyir izledi; kur baskısı "
            f"döviz sepetine yansımaktadır."
        )
    else:
        fx = (
            f"Türk lirası güç kazandı; <strong>USD/TRY {usd:.4f} ₺</strong>'ye "
            f"geriledi (<strong>{usd_d:.4f} ₺</strong>). "
            f"EUR/TRY {eur:.4f} ₺ ile liranın değerlenme eğilimini teyit etmektedir."
        )

    # ── Enflasyon + faiz paragrafı ────────────────────────────────────
    if cpi_y > 50:
        inf_level = "yüksek seyreden"
    elif cpi_y > 20:
        inf_level = "çift haneli"
    else:
        inf_level = "tek haneli"

    if cpi_d > 0:
        inf_move = f"bir önceki döneme göre <strong>{abs(cpi_d):.1f} puan yükseldi</strong>"
    elif cpi_d < 0:
        inf_move = f"bir önceki döneme kıyasla <strong>{abs(cpi_d):.1f} puan geriledi</strong>; dezenflasyon patikası sürmektedir"
    else:
        inf_move = "yatay seyrediyor"

    if rate_d > 0:
        rate_move = (
            f"TCMB politika faizini <strong>{abs(rate_d):.0f} baz puan artırarak "
            f"%{rate:.0f}</strong>'e yükseltti; sıkılaştırıcı para politikası devam etmektedir."
        )
    elif rate_d < 0:
        rate_move = (
            f"TCMB politika faizini <strong>{abs(rate_d):.0f} baz puan indirerek "
            f"%{rate:.0f}</strong>'e çekti; para politikasında temkinli gevşeme süreci başladı."
        )
    else:
        rate_move = (
            f"TCMB politika faizi <strong>%{rate:.0f}</strong> seviyesinde sabit tutulmaktadır."
        )

    inf_rate = (
        f"Yıllık <strong>TÜFE %{cpi_y:.1f}</strong> ile {inf_level} düzeyde, "
        f"{inf_move}. "
        f"{rate_move}"
    )

    # ── Rezerv + genel görünüm paragrafı ─────────────────────────────
    res_bn = res / 1000
    if res_d > 0:
        res_move = (
            f"<strong>Brüt döviz rezervleri {res_bn:.1f} milyar dolar</strong> "
            f"ile artış kaydetti; rezerv birikimi dış tampon kapasiteyi güçlendiriyor."
        )
    elif res_d < 0:
        res_move = (
            f"<strong>Brüt döviz rezervleri {res_bn:.1f} milyar dolara</strong> geriledi; "
            f"dış tampon kapasite yakından izlenmesi gereken bir başlık olmaya devam etmektedir."
        )
    else:
        res_move = (
            f"<strong>Brüt döviz rezervleri {res_bn:.1f} milyar dolar</strong> "
            f"seviyesinde yatay seyrediyor."
        )

    # Özet değerlendirme
    if cpi_d < 0 and res_d >= 0:
        outlook = "Genel görünüm <strong>temkinli pozitif</strong>: dezenflasyon + rezerv birikimi olumlu olmakla birlikte küresel risk iştahı ve enerji fiyatları başlıca yukarı yönlü kur riski olmayı sürdürüyor."
    elif usd_d > 0.5 or cpi_d > 1:
        outlook = "Genel görünüm <strong>temkinli negatif</strong>: kur baskısı ve/veya enflasyondaki yükseliş para politikasında ek sıkılaştırma gerektiren baskıları canlı tutmaktadır."
    else:
        outlook = "Genel görünüm <strong>nötr</strong>: temel göstergeler sınırlı hareketle izleme modunda; veri akışı yakından takip edilmektedir."

    return (
        f"<p>{fx}</p>"
        f"<p>{inf_rate}</p>"
        f"<p>{res_move} {outlook}</p>"
    )
