import os
from dotenv import load_dotenv
from tcmb import Client
import pandas as pd

load_dotenv()
_client = Client(api_key=os.getenv("EVDS_API_KEY"))


def fetch_series(series_code: str, start: str = "01-01-2022") -> pd.DataFrame:
    df = _client.read(series_code, start_date=start)
    df = df.reset_index()
    df.columns = ["tarih", "deger"]
    df["deger"] = pd.to_numeric(df["deger"], errors="coerce")
    df = df.dropna().sort_values("tarih").reset_index(drop=True)
    return df
