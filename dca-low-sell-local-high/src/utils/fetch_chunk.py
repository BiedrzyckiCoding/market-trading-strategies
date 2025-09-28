import random
import requests
import time


def fetch_chunk(url, params, headers, retries=3):
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            wait = (2 ** attempt) + random.random()
            print(f"⚠ Error: {e} — retrying in {wait:.1f}s...")
            time.sleep(wait)
    print("❌ Failed after retries")
    return None