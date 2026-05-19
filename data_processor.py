import pandas as pd
import streamlit as st
from data_fetcher import fetch_series
from config import SERIES


@st.cache_data(ttl=3600)
def get_series(key: str) -> pd.DataFrame:
    return fetch_series(SERIES[key]["code"])


@st.cache_data(ttl=3600)
def get_cpi_pct(period: int = 12) -> pd.DataFrame:
    df = get_series("cpi_index").copy()
    df = df.set_index("tarih").resample("ME").last().reset_index()
    df["deger"] = df["deger"].pct_change(period) * 100
    return df.dropna().reset_index(drop=True)


def filter_by_range(df: pd.DataFrame, start: str) -> pd.DataFrame:
    cutoff = pd.to_datetime(start, dayfirst=True)
    return df[df["tarih"] >= cutoff].reset_index(drop=True)


def compute_delta(df: pd.DataFrame) -> tuple[float, float]:
    """Son değer ve bir önceki döneme göre mutlak fark döndürür."""
    if len(df) < 2:
        return df["deger"].iloc[-1], 0.0
    current = df["deger"].iloc[-1]
    previous = df["deger"].iloc[-2]
    return current, current - previous


def latest_date(df: pd.DataFrame) -> str:
    return df["tarih"].iloc[-1].strftime("%d.%m.%Y")


def build_correlation_df(usd, eur, rate, cpi_y, reserves) -> pd.DataFrame:
    def to_monthly(df, name):
        return df.set_index("tarih").resample("ME")["deger"].last().rename(name)

    combined = pd.concat([
        to_monthly(usd,      "USD/TRY"),
        to_monthly(eur,      "EUR/TRY"),
        to_monthly(rate,     "Politika Faizi"),
        to_monthly(cpi_y,    "TÜFE Yıllık"),
        to_monthly(reserves, "Brüt Rezerv"),
    ], axis=1).dropna()
    return combined.corr()
