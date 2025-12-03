
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

# Setup path
sys.path.append(os.getcwd())

from src.engine.data_loader import data_loader
from src.strategies.surge import SurgeStrategy

def debug_universe_stats():
    print("--- Debugging Universe Stats ---")
    date_str = "2020-10-25"
    start_dt = pd.to_datetime(date_str)
    
    # Load universe
    universe = pd.read_csv("data/meta_data/stocks.csv")['ticker'].tolist()
    print(f"Universe size: {len(universe)}")
    
    # Sample 20 tickers
    import random
    random.seed(42)
    sample_tickers = random.sample(universe, 20)
    
    print(f"Testing returns for date: {date_str}")
    
    for ticker in sample_tickers:
        try:
            df = data_loader.load_ticker_market_data(ticker)
            if df.empty: continue
            
            # Entry
            history = df[df['date'] <= start_dt]
            if history.empty: continue
            entry_price = history.iloc[-1]['close']
            entry_date = history.iloc[-1]['date']
            
            # Exit (3M)
            future = df[df['date'] > start_dt]
            if future.empty: continue
            
            period_data = future.head(63)
            end_price = period_data.iloc[-1]['close']
            end_date = period_data.iloc[-1]['date']
            
            ret = (end_price / entry_price) - 1
            
            print(f"{ticker}: Entry={entry_price:.2f} ({entry_date.date()}), Exit={end_price:.2f} ({end_date.date()}), Ret={ret:.2%}")
            
        except Exception as e:
            print(f"Error {ticker}: {e}")

def debug_surge_count():
    print("\n--- Debugging SURGE Candidate Count ---")
    date_str = "2020-10-25"
    target_date = pd.to_datetime(date_str)
    
    strategy = SurgeStrategy()
    
    # Test random sample of 200 tickers + known winners
    test_tickers = ["FUTU", "JFIN", "QFIN", "ZLAB", "UMC"] 
    
    market_dir = Path("data/market_data")
    files = list(market_dir.glob("*.parquet"))
    if len(files) > 200:
        test_tickers.extend([f.stem for f in files[:200]])
    else:
        test_tickers.extend([f.stem for f in files])
    
    print(f"Scanning {len(test_tickers)} tickers for {date_str}...")
    
    count = 0
    for ticker in test_tickers:
        try:
            df = data_loader.load_merged_data(ticker)
            if df.empty: continue
            
            # Slice to date
            mask = df['date'] <= target_date
            historical = df[mask]
            if historical.empty: continue
            
            # Run
            res = strategy.run(historical)
            if not res.empty:
                count += 1
                # print(f"Pass: {ticker} Score: {res.iloc[0]['raw_score']:.1f}")
                
        except Exception:
            pass
            
    print(f"Found {count} candidates in sample of {len(test_tickers)}")

if __name__ == "__main__":
    debug_universe_stats()
    debug_surge_count()

