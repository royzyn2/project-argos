"""
TURNAROUND Strategy (Reversal)
==============================
Logic:
- Companies reversing from loss to profit OR significant fundamental repair.
- Fixed high scores for Growth/Value if criteria met, differentiation via Tech.

Scoring (100 points total):
- 50% Growth: Fixed 90 if Turnaround detected.
- 30% Value: Fixed 80 if Turnaround detected.
- 20% Tech: Standard S_TECH.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    calc_price_slope, calc_rsi, score_tech
)

class TurnaroundStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("TURNAROUND")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        # Any cap size, but need history
        if df.empty or len(df) < 126:
            return pd.DataFrame()
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        is_turnaround = False
        
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            if len(fund_history) >= 4:
                recent = fund_history.tail(4)
                
                # Logic 1: Loss to Profit (Net Income)
                # Current positive, previous negative
                ni_curr = recent.iloc[-1]['net_income']
                ni_prev = recent.iloc[-2]['net_income']
                
                if ni_curr > 0 and ni_prev < 0:
                    is_turnaround = True
                    
                # Logic 2: Massive operational improvement (Operating Margin)
                # If we had operating income data, we'd use that. 
                # Fallback: Net Margin improvement > 500bps
                nm_curr = recent.iloc[-1].get('net_margin', 0)
                nm_prev = recent.iloc[-2].get('net_margin', 0)
                if (nm_curr - nm_prev) > 0.05: 
                    is_turnaround = True
                    
        df.loc[last_idx, 'is_turnaround'] = int(is_turnaround)
        
        # Scores
        if is_turnaround:
            df.loc[last_idx, 'growth_score'] = 90
            df.loc[last_idx, 'value_score'] = 80
        else:
            df.loc[last_idx, 'growth_score'] = 0
            df.loc[last_idx, 'value_score'] = 0
            
        # Tech
        closes = df['close']
        price_slope = calc_price_slope(closes, window=60)
        rsi = calc_rsi(closes, window=14)
        tech_score = score_tech(price_slope, rsi)
        
        df.loc[last_idx, 'tech_score'] = tech_score
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        if not last_row.get('is_turnaround', 0):
            return pd.DataFrame()
            
        raw_score = (90 * 0.50) + (80 * 0.30) + (last_row['tech_score'] * 0.20)
        
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = "Turnaround Detected"
        output_row['secondary_metric'] = f"Tech: {last_row['tech_score']:.0f}"
        output_row['backtest_type'] = 'EVENT'
        
        return output_row
