import pandas as pd
from pathlib import Path
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import logger
from config.settings import data_paths

def build_metadata():
    """
    Reconstructs meta_data from the ingested L1 data.
    1. stocks.csv: Master list of all tickers found in market_data.
    2. trading_calendar.csv: Union of all dates found across tickers.
    """
    try:
        logger.info("Building Metadata...")
        market_dir = Path(data_paths.get('market_data', 'data/market_data'))
        meta_dir = Path("data/meta_data")
        meta_dir.mkdir(parents=True, exist_ok=True)
        
        files = list(market_dir.glob("*.parquet"))
        if not files:
            logger.warning("No market data found to build metadata.")
            return

        tickers = []
        all_dates = set()
        
        # Use a sample or iterate all (iterating all is safer for a "Master Calendar")
        # For speed, we can trust SPY or AAPL for the calendar, but let's be robust.
        
        logger.info(f"Scanning {len(files)} files for metadata...")
        
        for f in files:
            ticker = f.stem
            tickers.append(ticker)
            
            # For calendar, we only need to read one major index ETF, or union them all.
            # Reading 5000 files just for dates is slow. 
            # Let's pick a few major ones to construct the calendar (AAPL, MSFT, SPY if exists).
            if ticker in ['AAPL', 'SPY', 'MSFT', 'NVDA']:
                df = pd.read_parquet(f)
                all_dates.update(df['date'].dt.date.astype(str).tolist())
        
        # 1. Save Stocks Master List
        stocks_df = pd.DataFrame({'ticker': sorted(tickers)})
        stocks_path = meta_dir / "stocks.csv"
        stocks_df.to_csv(stocks_path, index=False)
        logger.info(f"Saved universe definition to {stocks_path}")
        
        # 2. Save Trading Calendar
        if all_dates:
            calendar_df = pd.DataFrame({'date': sorted(list(all_dates))})
            calendar_path = meta_dir / "trading_calendar.csv"
            calendar_df.to_csv(calendar_path, index=False)
            logger.info(f"Saved trading calendar to {calendar_path}")
        else:
            # Fallback if no major tickers found, read the first one
            if files:
                df = pd.read_parquet(files[0])
                all_dates = df['date'].dt.date.astype(str).tolist()
                calendar_df = pd.DataFrame({'date': sorted(all_dates)})
                calendar_path = meta_dir / "trading_calendar.csv"
                calendar_df.to_csv(calendar_path, index=False)
                logger.info(f"Saved trading calendar (from sample) to {calendar_path}")

    except Exception as e:
        logger.error(f"Failed to build metadata: {e}")

if __name__ == "__main__":
    build_metadata()
