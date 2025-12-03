import requests
import os
import pandas as pd

api_key = os.getenv("FMP_API_KEY")
ticker = "STLD"
cutoff_date = pd.to_datetime("2022-05-13")

# url = f"https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/{ticker}?year=2022&apikey={api_key}"
url = f"https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/{ticker}?year=2022&apikey={api_key}"
print(f"Fetching: {url.replace(api_key, '***')}")

try:
    resp = requests.get(url)
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Found {len(data)} transcripts.")
        for t in data:
            t_date = pd.to_datetime(t['date'])
            print(f"  - {t['quarter']} {t['year']} : {t_date} (PIT Valid: {t_date <= cutoff_date})")
            
        # Simulate filtering
        valid = [t for t in data if pd.to_datetime(t['date']) <= cutoff_date]
        if valid:
            valid.sort(key=lambda x: x['date'], reverse=True)
            latest = valid[0]
            print(f"\nSelected Latest: {latest['quarter']} {latest['year']} ({latest['date']})")
        else:
            print("\nNo valid transcripts found before cutoff.")
    else:
        print("Error response:", resp.text)
except Exception as e:
    print(f"Exception: {e}")

