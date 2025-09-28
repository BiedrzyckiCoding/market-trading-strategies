import pandas as pd
import os

# Config
INPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "solana_hourly.csv")
os.makedirs(os.path.dirname(INPUT_FILE), exist_ok=True)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "strategy_results.csv")
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

BUY_AMOUNT = 20  # $20 per buy
START_BALANCE_USD = 0
START_BALANCE_SOL = 0

# Load data
df = pd.read_csv(INPUT_FILE, parse_dates=["timestamp"])
df["avg_price"] = (df["open"] + df["close"]) / 2

# Initialize
balance_usd = 0.0
balance_sol = 0.0
total_spent = 0.0
last_buy_price = None

# Store simulation records
records = []

for i, row in df.iterrows():
    price = row["close"]  # ✅ use the closing price as market price

    if last_buy_price is None:
        # First action: BUY
        sol_bought = BUY_AMOUNT / price
        balance_sol += sol_bought
        total_spent += BUY_AMOUNT
        last_buy_price = price

        records.append({
            "timeframe": row["timestamp"],
            "total_spent [$]": total_spent,
            "balance [$]": balance_sol * price + balance_usd,
            "balance SOL": balance_sol,
            "current price": price,
            "event type": "buy",
            "percentage movement": 0.0
        })
        continue

    pct_move = (price - last_buy_price) / last_buy_price

    if pct_move > 0:
        # SELL event
        usd_to_sell = BUY_AMOUNT * (1.5 + pct_move)
        sol_to_sell = min(usd_to_sell / price, balance_sol)
        usd_gained = sol_to_sell * price
        balance_sol -= sol_to_sell
        balance_usd += usd_gained

        records.append({
            "timeframe": row["timestamp"],
            "total_spent [$]": total_spent,
            "balance [$]": balance_sol * price + balance_usd,
            "balance SOL": balance_sol,
            "current price": price,
            "event type": "sell",
            "percentage movement": round(pct_move * 100, 2)
        })

        last_buy_price = price

    else:
        # BUY event
        sol_bought = BUY_AMOUNT / price
        balance_sol += sol_bought
        total_spent += BUY_AMOUNT
        last_buy_price = price

        records.append({
            "timeframe": row["timestamp"],
            "total_spent [$]": total_spent,
            "balance [$]": balance_sol * price + balance_usd,
            "balance SOL": balance_sol,
            "current price": price,
            "event type": "buy",
            "percentage movement": round(pct_move * 100, 2)
        })

# Save CSV
output_df = pd.DataFrame(records)
output_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Strategy simulation completed and saved to {OUTPUT_FILE}")