"""
CORE_VALUE Strategy (Large Cap Quality)
=======================================
Logic:
- Large, high-quality companies (S_CORE) at a fair/low price (POS_SCORE).
- "Buffett Style": Good business, fair price.

Scoring (100 points total):
- 50% Core Score (S_CORE): Market Cap + ROE.
- 50% Position Score (POS_SCORE): Low relative PE.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    score_core, calc_pe_position, score_pos
)

class CoreValueStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("CORE_VALUE")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or len(df) < 252: return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        # Large Cap Focus (> 10B)
        if pd.isna(mcap) or mcap < 1e10:
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
        
        # --- POSITION FACTOR ---
        pe = df.iloc[-1].get('pe', 0)
        pe_history = df['pe'].dropna()
        pe_pos = calc_pe_position(pe, pe_history)
        pos_score = score_pos(pe_pos)
        df.loc[last_idx, 'pos_score'] = pos_score
        
        df.loc[last_idx, 'roe'] = roe
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        # Weights: 50/50
        raw_score = (last_row.get('core_score',0) * 0.50 + 
                     last_row.get('pos_score',0) * 0.50)
                     
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"Core Score: {last_row.get('core_score',0):.0f} (ROE: {last_row.get('roe',0):.1%})"
        output_row['secondary_metric'] = f"Pos Score: {last_row.get('pos_score',0):.0f}"
        output_row['backtest_type'] = 'CALENDAR'
        
        return output_row
