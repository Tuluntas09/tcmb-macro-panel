from data_fetcher import fetch_series
from config import SERIES

for key, meta in SERIES.items():
    try:
        df = fetch_series(meta["code"])
        print(f"OK  {meta['name']}: {len(df)} satir, son deger: {df['deger'].iloc[-1]:.2f}")
    except Exception as e:
        print(f"ERR {meta['name']}: {e}")
