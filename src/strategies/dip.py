"""
DIP Strategy (Quality Pullback)
===============================
Logic:
- High-quality long-term grower (S_GROWTH Long).
- Price is currently suppressed (POS_SCORE) but tech is recovering.
- Expected Return Gap (GAP) is high.

Scoring (100 points total):
- 40% Growth (Long): S_GROWTH (Long) logic.
- 40% Position (POS_SCORE): Low PE position relative to history.
- 20% Gap: (Growth Score - Tech Score). If fundamentals > price action.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    calc_earnings_slope, calc_profit_qoq_acc, calc_pe_position,
    calc_price_slope, calc_rsi,
    score_growth_long, score_pos, score_tech
)

class DipStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("DIP")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or len(df) < 252: return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        # Mid/Large Cap preference for DIPs
        if pd.isna(mcap) or mcap < 1e9:
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        
        # --- GROWTH FACTORS (Long) ---
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            if len(fund_history) >= 8:
                ni_series = fund_history['net_income']
                earnings_slope = calc_earnings_slope(ni_series, window=8)
                
                recent = fund_history.tail(5)
                ni_curr = recent.iloc[-1]['net_income']
                ni_yoy = recent.iloc[-4]['net_income'] if len(recent) >= 4 else ni_curr
                profit_yoy = (ni_curr / ni_yoy - 1) if (ni_yoy > 0 and ni_curr > 0) else 0
                
                # QoQ Acc
                rev_curr = recent.iloc[-1]['revenue']
                rev_prev = recent.iloc[-2]['revenue']
                rev_prev2 = recent.iloc[-3]['revenue']
                curr_qoq = (rev_curr/rev_prev - 1) if rev_prev > 0 else 0
                prev_qoq = (rev_prev/rev_prev2 - 1) if rev_prev2 > 0 else 0
                profit_qoq_acc = calc_profit_qoq_acc(curr_qoq, prev_qoq)
                
                growth_score = score_growth_long(earnings_slope, profit_yoy, profit_qoq_acc)
            else:
                growth_score = 0
        else:
            growth_score = 0
            
        df.loc[last_idx, 'growth_score'] = growth_score
        
        # --- POSITION SCORE ---
        pe = df.iloc[-1].get('pe', 0)
        pe_history = df['pe'].dropna()
        pe_pos = calc_pe_position(pe, pe_history)
        pos_score = score_pos(pe_pos)
        df.loc[last_idx, 'pos_score'] = pos_score
        
        # --- GAP SCORE ---
        # Gap = Growth Score - Tech Score
        # Need to calc tech score first
        closes = df['close']
        price_slope = calc_price_slope(closes, window=60)
        rsi = calc_rsi(closes, window=14)
        tech_score = score_tech(price_slope, rsi)
        df.loc[last_idx, 'tech_score'] = tech_score
        
        # If Growth is 90 and Tech is 20 (Dipped), Gap is 70.
        # Normalize Gap? Let's just use raw diff, clipped 0-100.
        gap_raw = max(0, growth_score - tech_score)
        # Scaling: A gap of 50 is huge. 50 -> 100.
        gap_score = min(100, gap_raw * 2)
        df.loc[last_idx, 'gap_score'] = gap_score
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        # Weights: 40/40/20
        raw_score = (last_row.get('growth_score',0) * 0.40 + 
                     last_row.get('pos_score',0) * 0.40 + 
                     last_row.get('gap_score',0) * 0.20)
                     
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"Pos Score: {last_row['pos_score']:.0f} (Low PE)"
        output_row['secondary_metric'] = f"Gap: {last_row['gap_score']:.0f} (Fund > Price)"
        output_row['backtest_type'] = 'CALENDAR' # Dip can be calendar based
        
        return output_row
