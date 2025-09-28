import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# Config
API_KEY = "YOUR_COINGECKO_API_KEY"  # 👈 insert your CoinGecko API key here
COIN_ID = "solana"
VS_CURRENCY = "usd"
OUTPUT_FILE = "./data/solana_hourly.csv"

# Date range
start = datetime(2024, 6, 1)
end = datetime(2025, 6, 1)

# Prepare DataFrame
df = pd.DataFrame(columns=["timestamp", "price"])

# Endpoint
BASE_URL = f"https://pro-api.coingecko.com/api/v3/coins/{COIN_ID}/market_chart/range"

# Break into 90-day chunks (CoinGecko limit)
chunk_start = start
while chunk_start < end:
    chunk_end = min(chunk_start + timedelta(days=90), end)

    params = {
        "vs_currency": VS_CURRENCY,
        "from": int(chunk_start.timestamp()),
        "to": int(chunk_end.timestamp())
    }

    headers = {"x-cg-pro-api-key": API_KEY}

    try:
        r = requests.get(BASE_URL, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()

        # "prices" is a list of [timestamp_ms, price]
        for ts, price in data.get("prices", []):
            ts_dt = datetime.utcfromtimestamp(ts / 1000)
            df.loc[len(df)] = [ts_dt.isoformat(), price]

        print(f"Fetched {chunk_start.date()} → {chunk_end.date()}, rows={len(data.get('prices', []))}")

    except Exception as e:
        print(f"Error fetching {chunk_start.date()} → {chunk_end.date()}: {e}")

    # Move to next chunk
    chunk_start = chunk_end

    # Respect rate limit (50–100 calls/min depending on plan)
    time.sleep(2)

# Save final result
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Done! Saved {len(df)} rows to {OUTPUT_FILE}")
