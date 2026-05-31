# TCMB Makro Göstergeler Paneli

> Türkiye Cumhuriyet Merkez Bankası · EVDS API · Gerçek zamanlı makroekonomik izleme paneli

🔗 **Canlı:** [tcmb-macro-panel.streamlit.app](https://tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app)

---

## Özellikler

| # | Özellik |
|---|---------|
| 📈 | **5 canlı gösterge** — USD/TRY, EUR/TRY, Politika Faizi, TÜFE (yıllık + aylık), Brüt Döviz Rezervi |
| 🃏 | **Metrik kartlar** — anlık değer, önceki döneme delta (▲/▼), mini sparkline grafik |
| 🗂️ | **5 interaktif sekme** — Döviz, Faiz (adımsal), Enflasyon, Rezervler, Korelasyon matrisi |
| 🔗 | **Pearson korelasyon matrisi** — tüm seriler arası ilişki ısı haritası |
| 📅 | **Dönem filtresi** — 1A / 3A / 6A / 1Y / Max |
| ⬇️ | **CSV export** — her serinin verisini tek tıkla indir |
| 🧠 | **Otomatik makro analiz** — kural tabanlı Türkçe piyasa değerlendirmesi |
| 📊 | **İstatistik paneli** — 52-hafta aralık, yıllık değişim, reel faiz, zirveden düşüş |

---

## Ekran Görüntüsü

> Cobalt-blue / açık tema · JetBrains Mono rakamlar · Bloomberg tarzı düzen

---

## Veri Kaynakları

| Gösterge | EVDS Seri Kodu | Frekans |
|----------|---------------|---------|
| USD/TRY | `TP.DK.USD.A` | Günlük |
| EUR/TRY | `TP.DK.EUR.A` | Günlük |
| Politika Faizi | `TP.APIFON4` | Aylık |
| TÜFE Endeksi | `TP.FG.J0` | Aylık |
| Brüt Döviz Rezervi | `TP.AB.B1` | Haftalık |

Tüm veriler [TCMB EVDS](https://evds3.tcmb.gov.tr) üzerinden ücretsiz olarak erişilebilir.

---

## Teknoloji Stack

| Katman | Teknoloji |
|--------|-----------|
| Veri çekme | `tcmb` Python paketi + EVDS REST API |
| Veri işleme | `pandas` (resample, pct_change, corr) |
| Görselleştirme | `plotly` (area, bar, heatmap) |
| Arayüz | `streamlit` (custom CSS, unsafe_allow_html) |
| Deploy | Streamlit Cloud (GitHub push-to-deploy) |
| Font | Inter + JetBrains Mono (Google Fonts) |

---

## Mimari

```
TCMB EVDS API
      ↓
data_fetcher.py    — API bağlantısı, ham seri çekme
      ↓
data_processor.py  — Temizleme, yüzde hesabı, delta, korelasyon
      ↓
charts.py          — Plotly grafik fonksiyonları (area, dual, bar, heatmap)
      ↓
ai_analyst.py      — Kural tabanlı Türkçe makro yorum üretici
      ↓
app.py             — Streamlit UI (CSS, metrik kartlar, sekmeler, istatistik paneli)
```

---

## Kurulum

```bash
git clone https://github.com/Tuluntas09/tcmb-macro-panel.git
cd tcmb-macro-panel
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

`.env` dosyası oluştur:
```
EVDS_API_KEY=senin_evds_anahtarin
```

```bash
streamlit run app.py
```

EVDS API anahtarı için [evds3.tcmb.gov.tr](https://evds3.tcmb.gov.tr) adresinden ücretsiz kayıt yapılabilir.

---

*Geliştirici: [Tuluntas09](https://github.com/Tuluntas09) · Eğitim amaçlıdır, yatırım tavsiyesi değildir.*
