import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv() 
API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY") 
if not API_KEY: 
    raise ValueError("❌ API key not found. Please add CRYPTOCOMPARE_API_KEY to your .env file")

URL = "https://openapiv1.coinstats.app/insights/fear-and-greed/chart"

# Safe path setup (avoids issues when __file__ is not defined, e.g., in Jupyter)
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", "market-trading-strategies", "fear-greed-index-action"))
OUTPUT_FILE_PATH = os.path.join(BASE_DIR, "data", "daily_crypto_fear_greed_index.csv")
os.makedirs(os.path.dirname(OUTPUT_FILE_PATH), exist_ok=True)

def fetch_fear_greed_chart():
    headers = {
        "X-API-KEY": API_KEY
    }
    resp = requests.get(URL, headers=headers)
    resp.raise_for_status()
    return resp.json()

def to_dataframe(data_json):
    data = data_json.get("data", [])
    df = pd.DataFrame(data)
    # Ensure timestamp is numeric and convert to datetime
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s")
    return df[["date", "value", "value_classification"]]

def filter_last_year(df):
    # Ensure 'date' column is datetime64[ns]
    df["date"] = pd.to_datetime(df["date"])
    one_year_ago = pd.to_datetime(datetime.utcnow()) - pd.Timedelta(days=365)
    return df[df["date"] >= one_year_ago]

def main():
    json_data = fetch_fear_greed_chart()
    df = to_dataframe(json_data)
    df = filter_last_year(df)
    df.to_csv(OUTPUT_FILE_PATH, index=False)
    print(f"✅ Saved to {OUTPUT_FILE_PATH}")

if __name__ == "__main__":
    main()