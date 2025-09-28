import pandas as pd
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "solana_hourly.csv")
os.makedirs(os.path.dirname(INPUT_FILE), exist_ok=True)

# Load CSV
df = pd.read_csv(INPUT_FILE, parse_dates=["timestamp"])

if df.empty:
    print("⚠ The CSV file is empty.")
    exit()

# Calculate absolute percentage movements
df["abs_pct_open_close"] = ((df["close"] - df["open"]).abs() / df["open"]) * 100
df["abs_pct_high_low"] = ((df["high"] - df["low"]).abs() / df["low"]) * 100

# Calculate averages over the entire dataset
avg_open_close = df["abs_pct_open_close"].mean()
avg_high_low = df["abs_pct_high_low"].mean()

print(f"Average absolute % movement (Open → Close) over entire dataset: {avg_open_close:.4f}%")
print(f"Average absolute % movement (High → Low) over entire dataset: {avg_high_low:.4f}%")
