"""
Warehouse Builder (ETL Engine)
==============================
Responsible for fetching, cleaning, and storing "Level 2" (Deep) data for AI analysis.

Logic:
1. Reads candidate lists from data/results/*.csv.
2. Identifies 'active' candidates (based on date).
3. Fetches supplementary data (Transcripts, Segment Revenue, News) for them.
   - Implements robust SSL retries to handle transient connection errors.
4. Stores structured JSON in data/warehouse/{ticker}/.
"""

import os
import pandas as pd
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path
from datetime import datetime
from src.utils.logger import logger
from src.engine.data_loader import data_loader

class WarehouseBuilder:
    def __init__(self):
        self.results_dir = Path("data/results")
        self.warehouse_dir = Path("data/warehouse")
        self.warehouse_dir.mkdir(parents=True, exist_ok=True)
        self.fmp_key = os.getenv("FMP_API_KEY")
        
        # Configure Requests with Retry Strategy
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1, # 1s, 2s, 4s, 8s...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        # Mount adapter for both HTTP and HTTPS
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def run(self, strategy_name: str = None):
        """
        Main ETL loop.
        """
        logger.info("Starting Warehouse ETL...")
        
        files = list(self.results_dir.glob("*.csv"))
        if strategy_name:
            # Match strategy name (exact or partial if needed)
            files = [f for f in files if strategy_name in f.stem]
            
        if not files:
            logger.warning("No result files found to process.")
            return

        for csv_file in files:
            self._process_strategy_file(csv_file)
                
        logger.info("Warehouse ETL Complete.")

    def _process_strategy_file(self, file_path: Path):
            try:
            df = pd.read_csv(file_path)
            if df.empty: return
                
            # Process ALL candidates (Removing 30 limit for production run)
            if 'raw_score' in df.columns:
                top_candidates = df.sort_values('raw_score', ascending=False)
            else:
                top_candidates = df
                
            logger.info(f"Processing {len(top_candidates)} candidates from {file_path.stem}...")
                
            for _, row in top_candidates.iterrows():
                self._build_ticker_warehouse(row)
                    
            except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    def _build_ticker_warehouse(self, row: pd.Series):
        ticker = row['ticker']
        date_str = row['date']
        
        ticker_dir = self.warehouse_dir / ticker
        ticker_dir.mkdir(exist_ok=True)
        
        context_path = ticker_dir / f"{date_str}_context.json"
        
        # 1. Base Metadata
        context_data = {
            "ticker": ticker,
            "snapshot_date": date_str,
            "strategy_score": row.get('raw_score', 0),
            "primary_metric": row.get('primary_metric', ''),
            "secondary_metric": row.get('secondary_metric', ''),
        }

        # 2. Real Financials (Local PIT Parquet - Fast)
        try:
            merged_df = data_loader.load_merged_data(ticker)
            if not merged_df.empty:
                snapshot_dt = pd.to_datetime(date_str)
                merged_df['date'] = pd.to_datetime(merged_df['date'])
                row_at_date = merged_df[merged_df['date'] == snapshot_dt]
                
                if not row_at_date.empty:
                    fin_data = row_at_date.iloc[0].to_dict()
                    for k, v in fin_data.items():
                        if isinstance(v, (pd.Timestamp, datetime)):
                            fin_data[k] = v.strftime('%Y-%m-%d')
                    context_data["financials_summary"] = fin_data
        except Exception as e:
            logger.error(f"Error fetching local financials for {ticker}: {e}")

        # 3. Deep Data (FMP API - Slow/Costly)
        # Only fetch if we have a key
        if self.fmp_key:
            self._fetch_deep_data(ticker, date_str, context_data)
            # Fetch Profile for Sector/Industry
            try:
                prof_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={self.fmp_key}"
                prof_resp = self.session.get(prof_url, timeout=10)
                if prof_resp.status_code == 200:
                    prof_data = prof_resp.json()
                    if prof_data and isinstance(prof_data, list):
                        p = prof_data[0]
                        context_data['sector'] = p.get('sector', 'Unknown')
                        context_data['industry'] = p.get('industry', 'Unknown')
                        context_data['description'] = p.get('description', '')
            except Exception as e:
                logger.warning(f"Error fetching profile for {ticker}: {e}")
        else:
            # Mock if no key
            context_data.update({
                "transcript_summary": "MOCK TRANSCRIPT (No FMP Key)",
                "deep_financials": "MOCK FINANCIALS (No FMP Key)"
            })
        
        with open(context_path, "w") as f:
            json.dump(context_data, f, indent=2, default=str)

    def _fetch_deep_data(self, ticker, date_str, context_data):
        """
        Fetches Transcripts and Detailed Financials from FMP respecting PIT.
        """
        cutoff_date = pd.to_datetime(date_str)
        
        # A. Transcripts
        # Strategy: Iterate backwards from the snapshot date's quarter.
        # We try to find the latest transcript available ON or BEFORE the cutoff date.
        
        current_year = cutoff_date.year
        current_quarter = (cutoff_date.month - 1) // 3 + 1
        
        found_transcript = False
        
        # Check up to 4 quarters back
        for _ in range(5):
            # Construct URL for specific quarter
            # v3/earning_call_transcript/{ticker}?year=2022&quarter=1
            transcript_url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?year={current_year}&quarter={current_quarter}&apikey={self.fmp_key}"
            
            try:
                # Use self.session.get instead of requests.get for retry logic
                resp = self.session.get(transcript_url, timeout=10) 
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 0:
                        # Usually returns a list of 1 for a specific quarter
                        t = data[0]
                        t_date = pd.to_datetime(t['date'])
                        
                        if t_date <= cutoff_date:
                            # Found it!
                            context_data['transcript'] = {
                                'date': t['date'],
                                'quarter': t['quarter'],
                                'year': t['year'],
                                'content': t.get('content', '')[:15000] # Approx 3-4k tokens
                            }
                            found_transcript = True
                            break
                        else:
                            # Transcript is from future relative to cutoff (e.g. we are in Q2 but earnings released late Q2)
                            # Continue searching backwards
                            pass
            except Exception as e:
                logger.warning(f"Error fetching transcript {current_year} Q{current_quarter}: {e}")
            
            # Move to previous quarter
            if current_quarter == 1:
                current_quarter = 4
                current_year -= 1
            else:
                current_quarter -= 1
                
        if not found_transcript:
            logger.warning(f"No PIT transcript found for {ticker} before {cutoff_date}")

        # B. 5-Year Annual & 4-Q Quarterly Financials
        endpoints = {
            "income-statement": "income_statement",
            "balance-sheet-statement": "balance_sheet",
            "cash-flow-statement": "cash_flow"
        }
        
        deep_fin = {"annual": {}, "quarterly": {}}
        
        for ep, name in endpoints.items():
            # Annual (Limit 10 to be safe)
            url = f"https://financialmodelingprep.com/api/v3/{ep}/{ticker}?limit=10&apikey={self.fmp_key}"
            data = self._safe_get(url)
            deep_fin["annual"][name] = self._filter_pit(data, cutoff_date, limit=5)
            
            # Quarterly
            url_q = f"https://financialmodelingprep.com/api/v3/{ep}/{ticker}?period=quarter&limit=20&apikey={self.fmp_key}"
            data_q = self._safe_get(url_q)
            deep_fin["quarterly"][name] = self._filter_pit(data_q, cutoff_date, limit=4)
            
        context_data['deep_financials'] = deep_fin

    def _safe_get(self, url):
        try:
            # Use self.session for retries
            r = self.session.get(url, timeout=10)
            if r.status_code == 200: return r.json()
        except: pass
        return []

    def _filter_pit(self, data_list, cutoff_date, limit=5):
        if not isinstance(data_list, list): return []
        clean = []
        for item in data_list:
            # FMP uses 'fillingDate' or 'date'
            d_str = item.get('fillingDate', item.get('date'))
            if not d_str: continue
            if pd.to_datetime(d_str) <= cutoff_date:
                clean.append(item)
        # Sort desc and take limit
        clean.sort(key=lambda x: x.get('date', ''), reverse=True)
        return clean[:limit]

if __name__ == "__main__":
    builder = WarehouseBuilder()
    builder.run()
