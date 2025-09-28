import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from utils.fetch_chunk import fetch_chunk

# Load CryptoCompare API key from .env
load_dotenv()
API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
if not API_KEY:
    raise ValueError("❌ API key not found. Please add CRYPTOCOMPARE_API_KEY to your .env file")

# Config
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "solana_hourly.csv")
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

SYMBOL = "SOL"
CURRENCY = "USD"
LIMIT = 2000  # max data points per request
HISTORICAL = True  # fetch historical data until a target start date
START_DATE = datetime(2024, 6, 1)

# Base endpoint
BASE_URL = "https://min-api.cryptocompare.com/data/v2/histohour"

# DataFrame to store results
df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

# Helper function to fetch one chunk
def fetch_chunk(to_ts):
    params = {
        "fsym": SYMBOL,
        "tsym": CURRENCY,
        "limit": LIMIT - 1,  # CryptoCompare returns limit+1 rows
        "toTs": int(to_ts.timestamp()),
        "api_key": API_KEY
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    return r.json()

# Fetch historical data in chunks
to_ts = datetime.utcnow()
while to_ts > START_DATE:
    try:
        data = fetch_chunk(to_ts)
        hist = data["Data"]["Data"]
        if not hist:
            print(f"⚠ No data returned for {to_ts}")
            break

        # Convert to DataFrame
        chunk_df = pd.DataFrame(hist)
        chunk_df["timestamp"] = pd.to_datetime(chunk_df["time"], unit="s")
        chunk_df = chunk_df[["timestamp", "open", "high", "low", "close", "volumefrom"]]
        chunk_df.rename(columns={"volumefrom": "volume"}, inplace=True)

        df = pd.concat([chunk_df, df], ignore_index=True)  # prepend older data

        # Prepare next chunk (oldest timestamp - 1 hour)
        oldest_ts = chunk_df["timestamp"].min()
        to_ts = oldest_ts - pd.Timedelta(hours=1)
        print(f"✅ Fetched chunk ending {oldest_ts}, total rows={len(df)}")

        time.sleep(1)  # respect rate limits

    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}, retrying in 5s...")
        time.sleep(5)

# Save CSV
df.to_csv(OUTPUT_FILE, index=False)
print(f"🎉 Done! Saved {len(df)} rows to {OUTPUT_FILE}")