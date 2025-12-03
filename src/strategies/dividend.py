"""
DIVIDEND Strategy (Dividend Growth & Stability)
===============================================
Logic:
- Targets consistent dividend payers with stable earnings.
- Rewards improving fundamentals (Margin expansion).

Scoring (100 points total):
- 80% Dividend Score (S_DIV): Yield based (Target 5%).
- 20% Improvement Score (S_IMPROVE): YoY Profit Margin/Growth improvement.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    calc_profit_stability_cv, score_dividend, score_improve
)

class DividendStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("DIVIDEND")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or len(df) < 252: return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        # Large/Mid Cap focus for stability
        if pd.isna(mcap) or mcap < 1e9:
            return pd.DataFrame()
            
        # Must pay dividend
        div = last_row.get('dividend_yield', 0)
        if pd.isna(div) or div <= 0.001: # Min 0.1% yield
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        
        # --- DIVIDEND FACTOR ---
        div_yield = df.iloc[-1].get('dividend_yield', 0)
        
        # Stability Check (Optional Filter or Penalty)
        # We want stable earnings.
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            ni_series = fund_history['net_income']
            stability = calc_profit_stability_cv(ni_series)
            # If unstable, penalize yield score?
            # Strategy says: 80% S_DIV based on yield. 
            # Let's stick to manual logic: S_DIV = Yield / 5% * 100
            
            div_score = score_dividend(div_yield)
            
            # --- IMPROVEMENT FACTOR ---
            # Profit Margin or YoY Growth Improvement
            recent = fund_history.tail(5)
            if len(recent) >= 4:
                # Use YoY diff
                ni_curr = recent.iloc[-1]['net_income']
                ni_yoy = recent.iloc[-4]['net_income']
                
                # Growth now vs growth before?
                # Manual definition: "PROFIT_YOY_DIFF".
                # (Current YoY) - (Previous YoY)
                
                # Calc Current YoY
                yoy_curr = (ni_curr / ni_yoy - 1) if ni_yoy > 0 else 0
                
                # Calc Prev YoY (t-1 vs t-5)
                if len(recent) >= 5:
                    ni_prev = recent.iloc[-2]['net_income']
                    ni_yoy_prev = recent.iloc[-5]['net_income']
                    yoy_prev = (ni_prev / ni_yoy_prev - 1) if ni_yoy_prev > 0 else 0
                else:
                    yoy_prev = 0
                    
                profit_yoy_diff = yoy_curr - yoy_prev
                improve_score = score_improve(profit_yoy_diff)
            else:
                improve_score = 0
        else:
            div_score = 0
            improve_score = 0
            
        df.loc[last_idx, 'div_score'] = div_score
        df.loc[last_idx, 'improve_score'] = improve_score
        df.loc[last_idx, 'div_yield'] = div_yield
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        # Weights: 80/20
        raw_score = (last_row.get('div_score',0) * 0.80 + 
                     last_row.get('improve_score',0) * 0.20)
                     
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"Yield: {last_row.get('div_yield',0):.1%} (Score: {last_row.get('div_score',0):.0f})"
        output_row['secondary_metric'] = f"Improvement: {last_row.get('improve_score',0):.0f}"
        output_row['backtest_type'] = 'CALENDAR'
        
        return output_row
