import pandas as pd
from data_fetcher import fetch_series
from config import SERIES
import streamlit as st


@st.cache_data(ttl=3600)
def get_series(key: str) -> pd.DataFrame:
    code = SERIES[key]["code"]
    df = fetch_series(code)
    return df


@st.cache_data(ttl=3600)
def get_cpi_pct(period: int = 12) -> pd.DataFrame:
    """Endeks verisinden yüzde değişim hesaplar. period=12 yıllık, period=1 aylık."""
    df = get_series("cpi_annual").copy()
    df = df.set_index("tarih").resample("ME").last().reset_index()
    df["deger"] = df["deger"].pct_change(period) * 100
    return df.dropna().reset_index(drop=True)


def latest_value(df: pd.DataFrame) -> float:
    return df["deger"].iloc[-1]


def latest_date(df: pd.DataFrame) -> str:
    return df["tarih"].iloc[-1].strftime("%d.%m.%Y")
