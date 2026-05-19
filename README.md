# 📊 TCMB Makro Göstergeler Paneli

Türkiye Cumhuriyet Merkez Bankası'nın açık EVDS API'sinden gerçek zamanlı makroekonomik veri çeken, interaktif web tabanlı gösterge paneli.

🔗 **Canlı uygulama:** [tcmb-macro-panel.streamlit.app](https://tcmb-macro-panel-vctrkyq2bfjkqejgxjaudp.streamlit.app)

---

## Özellikler

- **5 temel gösterge:** USD/TRY, EUR/TRY, Politika Faizi, TÜFE (yıllık/aylık), Brüt Döviz Rezervi
- **Delta metrikler:** Her kartda bir önceki döneme göre değişim yönü ve miktarı
- **Tarih filtresi:** 1Y / 3Y / Max aralığı seçimi
- **İnteraktif grafikler:** Alan grafiği (Plotly), hover detayı, zoom
- **Saatlik önbellekleme:** API'ye gereksiz yük bindirmeden güncel veri
- **Hata yönetimi:** API erişim sorunu durumunda kullanıcıya anlamlı mesaj

---

## Ekran Görüntüsü

> Metrik kartlar, dönem filtresi ve interaktif grafikler

![Panel Görünümü](screenshot.png)

---

## Veri Kaynakları

| Gösterge | EVDS Seri Kodu | Frekans |
|---|---|---|
| USD/TRY | `TP.DK.USD.A` | Günlük |
| EUR/TRY | `TP.DK.EUR.A` | Günlük |
| Politika Faizi | `TP.APIFON4` | Aylık |
| TÜFE Endeksi | `TP.FG.J0` | Aylık |
| Brüt Döviz Rezervi | `TP.AB.B1` | Haftalık |

Tüm veriler [TCMB EVDS](https://evds3.tcmb.gov.tr) üzerinden ücretsiz olarak erişilebilir.

---

## Teknoloji Stack

| Katman | Teknoloji |
|---|---|
| Veri çekme | `tcmb` Python paketi |
| Veri işleme | `pandas` |
| Görselleştirme | `plotly` |
| Arayüz | `streamlit` |
| Deploy | Streamlit Cloud |

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

Uygulamayı başlat:
```bash
streamlit run app.py
```

EVDS API anahtarı için [evds3.tcmb.gov.tr](https://evds3.tcmb.gov.tr) adresinden ücretsiz kayıt olabilirsiniz.

---

## Mimari

```
TCMB EVDS API
      ↓
data_fetcher.py   — API bağlantısı ve ham veri
      ↓
data_processor.py — Temizleme, yüzde hesabı, delta, tarih filtresi
      ↓
charts.py         — Plotly grafik şablonları
      ↓
app.py            — Streamlit arayüzü
```

---

*Geliştirici: [Tuluntas09](https://github.com/Tuluntas09)*
