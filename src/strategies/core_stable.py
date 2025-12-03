"""
CORE_STABLE Strategy (Defensive Giants)
=======================================
Logic:
- Extremely large, stable companies. "Too big to fail".
- Pure S_CORE play.

Scoring (100 points total):
- 100% Core Score (S_CORE): Market Cap + ROE.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import score_core

class CoreStableStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("CORE_STABLE")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or len(df) < 252: return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        # Mega Cap Focus (> 50B)
        if pd.isna(mcap) or mcap < 5e10:
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        
        # --- CORE FACTOR ---
        mcap = df.iloc[-1]['market_cap']
        roe = df.iloc[-1].get('roe', 0)
        if pd.isna(roe): roe = 0
        
        core_score = score_core(mcap, roe)
        df.loc[last_idx, 'core_score'] = core_score
        df.loc[last_idx, 'roe'] = roe
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        # Weights: 100% Core
        raw_score = last_row.get('core_score',0)
                     
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"Core Score: {raw_score:.0f}"
        output_row['secondary_metric'] = f"ROE: {last_row.get('roe',0):.1%} / Cap: {last_row['market_cap']/1e9:.0f}B"
        output_row['backtest_type'] = 'CALENDAR'
        
        return output_row

