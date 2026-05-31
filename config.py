from datetime import datetime, timedelta

SERIES = {
    "usd_try": {
        "code": "TP.DK.USD.A",
        "name": "USD/TRY",
        "unit": "₺",
        "frequency": "daily",
    },
    "eur_try": {
        "code": "TP.DK.EUR.A",
        "name": "EUR/TRY",
        "unit": "₺",
        "frequency": "daily",
    },
    "policy_rate": {
        "code": "TP.APIFON4",
        "name": "Politika Faizi",
        "unit": "%",
        "frequency": "monthly",
    },
    "cpi_index": {
        "code": "TP.FG.J0",
        "name": "TÜFE Endeksi",
        "unit": "",
        "frequency": "monthly",
    },
    "gross_reserves": {
        "code": "TP.AB.B1",
        "name": "Brüt Döviz Rezervi",
        "unit": "mn$",
        "frequency": "weekly",
    },
}

_today = datetime.today()
DATE_RANGES = {
    "1A":  (_today - timedelta(days=30)).strftime("%d-%m-%Y"),
    "3A":  (_today - timedelta(days=90)).strftime("%d-%m-%Y"),
    "6A":  (_today - timedelta(days=180)).strftime("%d-%m-%Y"),
    "1Y":  (_today - timedelta(days=365)).strftime("%d-%m-%Y"),
    "Max": "01-01-2003",
}

DEFAULT_START = "01-01-2022"
