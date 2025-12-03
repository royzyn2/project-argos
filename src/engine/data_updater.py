"""
Data Updater (Factory Model)
============================
Responsible for keeping the Data Warehouse (Level 1) fresh.
Updates Market Data, Fundamental Data, and Metadata using FMP API.

Usage:
    python src/engine/data_updater.py --mode [market|fundamental|all] --tickers [all|list]

Design:
- Incremental updates: Only fetches missing data since the last record.
- Robustness: Retries on API failures.
- Schema Consistency: Ensures new data matches existing Parquet schemas.
"""

import os
import time
import pandas as pd
import requests
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.utils.logger import setup_logger, logger
from dotenv import load_dotenv

# Load env vars
load_dotenv()

class DataUpdater:
    def __init__(self):
        self.fmp_key = os.getenv("FMP_API_KEY")
        if not self.fmp_key:
            logger.error("FMP_API_KEY not found in .env")
            raise ValueError("FMP_API_KEY missing")

        self.market_data_dir = Path("data/market_data")
        self.fundamental_dir = Path("data/fundamental_data")
        self.meta_dir = Path("data/meta_data")
        
        self.market_data_dir.mkdir(parents=True, exist_ok=True)
        self.fundamental_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)

        # Session Setup
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def update_market_data(self, tickers=None):
        """
        Updates daily OHLCV for specified tickers (or all in market_data).
        """
        logger.info("--- Starting Market Data Update ---")
        
        if not tickers:
            # Scan existing files
            files = list(self.market_data_dir.glob("*.parquet"))
            tickers = [f.stem for f in files]
        
        logger.info(f"Updating {len(tickers)} tickers...")
        
        count = 0
        for ticker in tickers:
            try:
                self._update_single_ticker_price(ticker)
                count += 1
                if count % 50 == 0:
                    logger.info(f"Updated {count}/{len(tickers)} tickers")
            except Exception as e:
                logger.error(f"Failed to update {ticker}: {e}")
                
        logger.info("Market Data Update Complete.")

    def _update_single_ticker_price(self, ticker):
        file_path = self.market_data_dir / f"{ticker}.parquet"
        
        start_date = "2010-01-01" # Default for new
        existing_df = pd.DataFrame()
        
        if file_path.exists():
            try:
                existing_df = pd.read_parquet(file_path)
                if not existing_df.empty:
                    existing_df = existing_df.sort_values('date')
                    last_date = pd.to_datetime(existing_df['date'].iloc[-1])
                    # Start from next day
                    start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                    
                    # If up to date, skip
                    if start_date > datetime.now().strftime('%Y-%m-%d'):
                        return
            except Exception as e:
                logger.warning(f"Corrupt parquet for {ticker}, redownloading: {e}")
                
        # Fetch from FMP
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={start_date}&apikey={self.fmp_key}"
        resp = self.session.get(url, timeout=10)
        
        if resp.status_code != 200:
            logger.warning(f"FMP Error {resp.status_code} for {ticker}")
            return
            
        data = resp.json()
        if not data or 'historical' not in data:
            return # No new data
            
        new_records = data['historical']
        if not new_records:
            return
            
        new_df = pd.DataFrame(new_records)
        
        # Normalize columns
        # FMP: date, open, high, low, close, adjClose, volume, unadjustedVolume, change, changePercent, vwap, label, changeOverTime
        # Target: date, open, high, low, close, volume (typically)
        
        cols_map = {
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close', # We usually use close or adjClose depending on strategy preference. 
                              # Assuming 'close' in existing parquet is Split-Adjusted? 
                              # FMP 'close' is split adjusted usually? No, 'adjClose' is.
                              # Let's check existing schema or just stick to 'close' if that's what's there.
            'volume': 'volume'
        }
        
        # Check existing schema
        if not existing_df.empty:
            # Ensure we match existing columns
            common_cols = [c for c in new_df.columns if c in existing_df.columns]
            new_df = new_df[common_cols]
        else:
            # Default minimal schema
            keep_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
            new_df = new_df[[c for c in keep_cols if c in new_df.columns]]

        new_df['date'] = pd.to_datetime(new_df['date'])
        
        # Combine
        if not existing_df.empty:
            combined = pd.concat([existing_df, new_df]).drop_duplicates(subset=['date']).sort_values('date')
        else:
            combined = new_df.sort_values('date')
            
        combined.to_parquet(file_path, index=False)

    def update_metadata(self):
        """
        Updates stock list and trading calendar in data/meta_data.
        """
        logger.info("--- Starting Metadata Update ---")
        
        # 1. Update Stocks List
        stocks_path = self.meta_dir / "stocks.csv"
        url_stocks = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={self.fmp_key}"
        
        try:
            logger.info("Fetching stock list...")
            resp = self.session.get(url_stocks, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                df = pd.DataFrame(data)
                if not df.empty:
                    # Filter for relevant exchanges if needed, or keep all
                    df.to_csv(stocks_path, index=False)
                    logger.info(f"Updated stocks.csv with {len(df)} records.")
        except Exception as e:
            logger.error(f"Error updating stock list: {e}")

        # 2. Update Trading Calendar (Earnings Calendar as proxy or actual market hours)
        # FMP has 'is-the-market-open' or earnings calendar. 
        # For backtesting, we usually just need market days. 
        # Let's fetch SPY history as the 'master calendar'.
        
        calendar_path = self.meta_dir / "trading_calendar.csv"
        try:
            logger.info("Updating trading calendar (using SPY history)...")
            url_spy = f"https://financialmodelingprep.com/api/v3/historical-price-full/SPY?from=2000-01-01&apikey={self.fmp_key}"
            resp = self.session.get(url_spy, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if 'historical' in data:
                    dates = [item['date'] for item in data['historical']]
                    dates.sort()
                    pd.DataFrame({'date': dates}).to_csv(calendar_path, index=False)
                    logger.info(f"Updated trading_calendar.csv with {len(dates)} days.")
        except Exception as e:
            logger.error(f"Error updating trading calendar: {e}")
            
        logger.info("Metadata Update Complete.")

    def update_financials(self):
        """
        Updates master_financials.parquet with latest quarterly results.
        """
        logger.info("--- Starting Fundamental Data Update ---")
        
        master_path = self.fundamental_dir / "master_financials.parquet"
        if not master_path.exists():
            logger.error(f"Master financials not found at {master_path}. Cannot update incrementally safely.")
            return
            
        master_df = pd.read_parquet(master_path)
        # Ensure datetime
        master_df['filing_date'] = pd.to_datetime(master_df['filing_date'])
        master_df['date'] = pd.to_datetime(master_df['date'])
        
        # Get universe from market data
        tickers = [f.stem for f in self.market_data_dir.glob("*.parquet")]
        logger.info(f"Scanning {len(tickers)} tickers for new financials...")
        
        new_rows = []
        
        for i, ticker in enumerate(tickers):
            try:
                # Check last filing in master
                ticker_df = master_df[master_df['ticker'] == ticker]
                if not ticker_df.empty:
                    last_filing = ticker_df['filing_date'].max() # Using filing_date as PIT proxy
                else:
                    last_filing = pd.Timestamp("2010-01-01")
                
                # Fetch Income Statement & Key Metrics (Quarterly)
                # We fetch last 4 quarters to be safe and check for updates
                
                # 1. Income Statement
                inc_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=quarter&limit=4&apikey={self.fmp_key}"
                inc_data = self._safe_get(inc_url)
                
                if not inc_data: continue
                
                # 2. Key Metrics
                key_url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period=quarter&limit=4&apikey={self.fmp_key}"
                key_data = self._safe_get(key_url)

                # 3. Balance Sheet (Added for Leverage/Equity robustness)
                bs_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period=quarter&limit=4&apikey={self.fmp_key}"
                bs_data = self._safe_get(bs_url)
                
                # Convert to DF
                inc_df = pd.DataFrame(inc_data)
                key_df = pd.DataFrame(key_data)
                bs_df = pd.DataFrame(bs_data)
                
                if inc_df.empty: continue
                
                # Pre-process dates
                inc_df['date'] = pd.to_datetime(inc_df['date']) # Period End
                inc_df['fillingDate'] = pd.to_datetime(inc_df['fillingDate']) # Filing Date
                
                # Filter for new data
                # IMPORTANT: master_financials 'date' column seems to hold Filing Date based on analysis
                # And 'filing_date' holds Period End.
                # Wait, analysis showed:
                # Parquet 'date' (2015-11-23) > Parquet 'filing_date' (2015-09-30)
                # FMP 'date' = Period End (2015-09-30)
                # FMP 'fillingDate' = Filing (2015-11-xx)
                # SO MAPPING IS:
                # Parquet 'date' = FMP 'fillingDate'
                # Parquet 'filing_date' = FMP 'date'
                
                # We check against parquet 'filing_date' (Period End) to see if we have this quarter.
                
                new_quarters = inc_df[inc_df['date'] > last_filing].copy()
                
                if new_quarters.empty:
                    continue
                    
                # Merge with Key Metrics
                if not key_df.empty:
                    key_df['date'] = pd.to_datetime(key_df['date'])
                    merged = pd.merge(new_quarters, key_df, on='date', how='left', suffixes=('', '_key'))
                else:
                    merged = new_quarters

                # Merge with Balance Sheet
                if not bs_df.empty:
                    bs_df['date'] = pd.to_datetime(bs_df['date'])
                    # Avoid column collision if necessary, but 'date' is the key.
                    # Common cols like 'symbol', 'period' might exist.
                    cols_to_use = bs_df.columns.difference(merged.columns).tolist()
                    cols_to_use.append('date')
                    merged = pd.merge(merged, bs_df[cols_to_use], on='date', how='left', suffixes=('', '_bs'))

                    
                # Profile for Sector/Industry (if needed)
                # For efficiency, maybe just reuse existing or fetch once.
                # Assuming we can get it from existing rows or fetch.
                sector = "Unknown"
                industry = "Unknown"
                if not ticker_df.empty:
                    sector = ticker_df.iloc[0]['sector']
                    industry = ticker_df.iloc[0]['industry']
                
                # Construct Rows
                for _, row in merged.iterrows():
                    new_row = {
                        'date': row.get('fillingDate'), # FMP fillingDate -> Parquet date (Available)
                        'ticker': ticker,
                        'company_name': ticker, # Placeholder or fetch profile
                        'industry': industry,
                        'sector': sector,
                        'revenue': row.get('revenue'),
                        'net_income': row.get('netIncome'),
                        'ebitda': row.get('ebitda'),
                        'calendar_year': row.get('calendarYear'),
                        'calendar_period': row.get('period'),
                        'filing_date': row.get('date'), # FMP date -> Parquet filing_date (Period End)
                        'market_cap': row.get('marketCap'), # From Key Metrics usually
                        'pe': row.get('peRatio'),
                        'pb': row.get('pbRatio'),
                        'dividend_yield': row.get('dividendYield'),
                        'roe': row.get('roe'),
                        'debt_to_equity': row.get('debtToEquity') if pd.notna(row.get('debtToEquity')) else (row.get('totalDebt', 0) / row.get('totalStockholdersEquity', 1) if row.get('totalStockholdersEquity', 0) != 0 else None),
                        'total_debt': row.get('totalDebt'),
                        'total_equity': row.get('totalStockholdersEquity'),
                        'gross_profit': row.get('grossProfit'),
                        'gross_margin': row.get('grossProfitRatio'),
                        'net_margin': row.get('netIncomeRatio')
                    }
                    
                    # Handle missing Filing Date (use date + lag if missing)
                    if pd.isnull(new_row['date']):
                         # Fallback: 45 days after period end
                         new_row['date'] = new_row['filing_date'] + timedelta(days=45)
                         
                    new_rows.append(new_row)
                    
                if i % 20 == 0:
                    logger.info(f"Processed {i}/{len(tickers)} tickers...")
                    
            except Exception as e:
                logger.warning(f"Error updating financials for {ticker}: {e}")
                
        if new_rows:
            logger.info(f"Appending {len(new_rows)} new financial records...")
            new_df = pd.DataFrame(new_rows)
            # Align types
            new_df = new_df.astype(master_df.dtypes.to_dict(), errors='ignore')
            
            updated_master = pd.concat([master_df, new_df]).drop_duplicates(subset=['ticker', 'filing_date'])
            updated_master.to_parquet(master_path, index=False)
            logger.info("Master Financials Updated.")
        else:
            logger.info("No new financials found.")

    def repair_financials(self):
        """
        Scans existing master_financials for missing critical fields (Leverage, ROE)
        and fetches them from FMP to backfill history.
        """
        logger.info("--- Starting Financial Data Repair (Backfill) ---")
        
        master_path = self.fundamental_dir / "master_financials.parquet"
        if not master_path.exists():
            logger.error("No master financials to repair.")
            return
            
        master_df = pd.read_parquet(master_path)
        
        # Ensure columns exist
        required_cols = ['debt_to_equity', 'total_debt', 'total_equity', 'roe']
        for col in required_cols:
            if col not in master_df.columns:
                master_df[col] = np.nan
                
        # Identify tickers with missing data (e.g., checking debt_to_equity)
        # We group by ticker and check if a significant portion is NaN
        tickers_to_repair = []
        for ticker, group in master_df.groupby('ticker'):
            if group['debt_to_equity'].isna().mean() > 0.5: # If >50% missing
                tickers_to_repair.append(ticker)
                
        logger.info(f"Found {len(tickers_to_repair)} tickers with missing leverage data.")
        
        # Iterate and fetch full history for these tickers
        updated_rows = []
        # We might need to rebuild the DF for these tickers entirely or merge.
        # Simpler strategy: Fetch full history for these tickers and replace their rows.
        
        for i, ticker in enumerate(tickers_to_repair):
            try:
                # Fetch Full History (Balance Sheet & Key Metrics)
                # Limit=100 covers ~25 years of quarterly data
                bs_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period=quarter&limit=100&apikey={self.fmp_key}"
                key_url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period=quarter&limit=100&apikey={self.fmp_key}"
                inc_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=quarter&limit=100&apikey={self.fmp_key}"
                
                bs_data = self._safe_get(bs_url)
                key_data = self._safe_get(key_url)
                inc_data = self._safe_get(inc_url)
                
                if not inc_data: continue # Core requirement
                
                inc_df = pd.DataFrame(inc_data)
                bs_df = pd.DataFrame(bs_data) if bs_data else pd.DataFrame()
                key_df = pd.DataFrame(key_data) if key_data else pd.DataFrame()
                
                # Process Dates
                inc_df['date'] = pd.to_datetime(inc_df['date'])
                inc_df['fillingDate'] = pd.to_datetime(inc_df['fillingDate'])
                
                if not bs_df.empty: bs_df['date'] = pd.to_datetime(bs_df['date'])
                if not key_df.empty: key_df['date'] = pd.to_datetime(key_df['date'])
                
                # Merge
                merged = inc_df
                if not bs_df.empty:
                    cols = bs_df.columns.difference(merged.columns).tolist() + ['date']
                    merged = pd.merge(merged, bs_df[cols], on='date', how='left', suffixes=('', '_bs'))
                if not key_df.empty:
                    cols = key_df.columns.difference(merged.columns).tolist() + ['date']
                    merged = pd.merge(merged, key_df[cols], on='date', how='left', suffixes=('', '_key'))
                
                # Get static info from existing DF if possible
                sector = "Unknown"
                existing_ticker_rows = master_df[master_df['ticker'] == ticker]
                if not existing_ticker_rows.empty:
                    sector = existing_ticker_rows.iloc[0].get('sector', 'Unknown')
                    industry = existing_ticker_rows.iloc[0].get('industry', 'Unknown')
                else:
                    industry = "Unknown"

                # Reconstruct Rows
                for _, row in merged.iterrows():
                    new_row = {
                        'date': row.get('fillingDate'), 
                        'ticker': ticker,
                        'company_name': ticker,
                        'industry': industry,
                        'sector': sector,
                        'revenue': row.get('revenue'),
                        'net_income': row.get('netIncome'),
                        'ebitda': row.get('ebitda'),
                        'calendar_year': row.get('calendarYear'),
                        'calendar_period': row.get('period'),
                        'filing_date': row.get('date'),
                        'market_cap': row.get('marketCap'),
                        'pe': row.get('peRatio'),
                        'pb': row.get('pbRatio'),
                        'dividend_yield': row.get('dividendYield'),
                        'roe': row.get('roe'),
                        'debt_to_equity': row.get('debtToEquity') if pd.notna(row.get('debtToEquity')) else (row.get('totalDebt', 0) / row.get('totalStockholdersEquity', 1) if row.get('totalStockholdersEquity', 0) != 0 else None),
                        'total_debt': row.get('totalDebt'),
                        'total_equity': row.get('totalStockholdersEquity'),
                        'gross_profit': row.get('grossProfit'),
                        'gross_margin': row.get('grossProfitRatio'),
                        'net_margin': row.get('netIncomeRatio')
                    }
                    
                    if pd.isnull(new_row['date']):
                         new_row['date'] = new_row['filing_date'] + timedelta(days=45)
                    
                    updated_rows.append(new_row)
                    
                if i % 10 == 0:
                    logger.info(f"Repaired {i}/{len(tickers_to_repair)} tickers...")
                    
            except Exception as e:
                logger.error(f"Failed to repair {ticker}: {e}")
        
        if updated_rows:
            logger.info(f"Rebuilding master dataframe with {len(updated_rows)} repaired rows...")
            repaired_df = pd.DataFrame(updated_rows)
            repaired_df = repaired_df.astype(master_df.dtypes.to_dict(), errors='ignore')
            
            # Drop old rows for repaired tickers
            master_df = master_df[~master_df['ticker'].isin(tickers_to_repair)]
            
            # Concat
            final_df = pd.concat([master_df, repaired_df], ignore_index=True)
            final_df = final_df.sort_values(['ticker', 'filing_date'])
            
            final_df.to_parquet(master_path, index=False)
            logger.info("Financial Data Repair Complete.")
        else:
            logger.info("No rows updated.")

    def _safe_get(self, url):
        try:
            r = self.session.get(url, timeout=10)
            if r.status_code == 200: return r.json()
        except: pass
        return []

if __name__ == "__main__":
    setup_logger()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=['market', 'fundamental', 'meta', 'repair', 'all'], default='all')
    args = parser.parse_args()
    
    updater = DataUpdater()
    
    if args.mode in ['meta', 'all']:
        updater.update_metadata()

    if args.mode in ['market', 'all']:
        updater.update_market_data()
        
    if args.mode in ['fundamental', 'all']:
        updater.update_financials()
        
    if args.mode == 'repair':
        updater.repair_financials()

