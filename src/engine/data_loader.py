import pandas as pd
import os
from pathlib import Path
from src.utils.logger import logger
from config.settings import data_paths

class DataLoader:
    """
    Centralized data loading module for Project Argos.
    Enforces Point-in-Time (PIT) alignment and data hygiene.
    """
    
    def __init__(self):
        self.market_data_dir = Path(data_paths.get('market_data', 'data/market_data'))
        self.fundamental_path = Path(data_paths.get('fundamental_data', 'data/fundamental_data')) / "master_financials.parquet"
        self._fund_cache = None

    def load_fundamentals(self) -> pd.DataFrame:
        """
        Loads the master financial dataset (Wide Table).
        Uses caching to avoid repeated disk reads.
        """
        if self._fund_cache is not None:
            return self._fund_cache

        if not self.fundamental_path.exists():
            logger.error(f"Fundamental data not found at {self.fundamental_path}")
            raise FileNotFoundError(f"Missing {self.fundamental_path}")

        logger.info("Loading fundamental data...")
        df = pd.read_parquet(self.fundamental_path)
        
        # Ensure PIT key is datetime
        df['filing_date'] = pd.to_datetime(df['filing_date'])
        self._fund_cache = df
        return df

    def load_ticker_market_data(self, ticker: str) -> pd.DataFrame:
        """
        Loads daily OHLCV data for a specific ticker.
        """
        file_path = self.market_data_dir / f"{ticker}.parquet"
        if not file_path.exists():
            logger.warning(f"Market data not found for {ticker}")
            return pd.DataFrame()
        
        return pd.read_parquet(file_path)

    def load_merged_data(self, ticker: str) -> pd.DataFrame:
        """
        Merges daily market data with quarterly fundamental data using strict PIT logic.
        
        Logic:
        - Market Data (Daily) is the 'Left' table.
        - Fundamental Data (Quarterly) is the 'Right' table.
        - Merge On: Market Date vs. Fundamental Filing Date.
        - Direction: Backward (Market Date >= Filing Date).
        
        Returns:
            DataFrame: Daily dataframe with forward-filled fundamental data.
        """
        # 1. Load Market Data
        price_df = self.load_ticker_market_data(ticker)
        if price_df.empty:
            return pd.DataFrame()
            
        # 2. Load Fundamental Data
        all_fund_df = self.load_fundamentals()
        fund_df = all_fund_df[all_fund_df['ticker'] == ticker].copy()
        
        if fund_df.empty:
            logger.warning(f"No fundamental data found for {ticker}. Returning price only.")
            return price_df

        # 3. PIT Merge (The "Iron Law")
        # Sort both by the merge keys
        price_df = price_df.sort_values('date')
        fund_df = fund_df.sort_values('filing_date')

        # Pre-merge cleanup: Rename fundamental 'date' to avoid collision with price 'date'
        # We keep it as 'period_end_date' for reference but don't use it for joining.
        if 'date' in fund_df.columns:
            fund_df = fund_df.rename(columns={'date': 'period_end_date'})

        # merge_asof requires the right table to be sorted by the key
        try:
            merged_df = pd.merge_asof(
                price_df,
                fund_df,
                left_on='date',
                right_on='filing_date',
                direction='backward', # Find the latest filing_date <= current date
                suffixes=('', '_fund') # Handle potential name collisions
            )
            
            # Cleanup: Remove the duplicate ticker column from right table if exists
            if 'ticker_fund' in merged_df.columns:
                merged_df.drop(columns=['ticker_fund'], inplace=True)
                
            return merged_df
            
        except Exception as e:
            logger.error(f"Error merging data for {ticker}: {e}")
            raise

# Global instance
data_loader = DataLoader()

