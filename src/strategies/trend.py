"""
TREND Strategy (Long-Term Growth)
=================================
Logic:
- High-quality long-term growth (Earnings Slope + YoY Growth).
- Reasonable Valuation (PEG).
- Positive Technical Trend.

Scoring (100 points total):
- 40% Growth (Long): Slope + YoY + QoQ Acc.
- 40% Value (PEG): PEG < 0.8 ideal.
- 20% Tech: Slope + RSI.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    calc_earnings_slope, calc_profit_qoq_acc, calc_price_slope, calc_rsi,
    score_growth_long, score_value_peg, score_tech
)

class TrendStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("TREND")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Universe:
        - Market Cap > 500M (Mid/Large Cap focus)
        - Sufficient history (> 2 years)
        """
        if df.empty or len(df) < 252:
            return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        if pd.isna(mcap) or mcap < 5e8:
            return pd.DataFrame()
            
        # Liquidity
        avg_vol = df['volume'].tail(20).mean()
        price = last_row['close']
        if avg_vol * price < 5e6: # $5M daily volume
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        
        # --- GROWTH FACTORS ---
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            if len(fund_history) >= 8:
                # 1. Earnings Slope (8 quarters)
                ni_series = fund_history['net_income']
                earnings_slope = calc_earnings_slope(ni_series, window=8)
                
                recent = fund_history.tail(5)
                # 2. YoY Growth
                ni_curr = recent.iloc[-1]['net_income']
                ni_yoy = recent.iloc[-4]['net_income'] if len(recent) >= 4 else ni_curr
                
                if ni_yoy > 0 and ni_curr > 0:
                    profit_yoy = (ni_curr / ni_yoy - 1)
                else:
                    profit_yoy = 0.0
                    
                # 3. QoQ Acc
                # Need current QoQ and prev QoQ
                rev_curr = recent.iloc[-1]['revenue']
                rev_prev = recent.iloc[-2]['revenue']
                rev_prev2 = recent.iloc[-3]['revenue']
                
                curr_qoq = (rev_curr/rev_prev - 1) if rev_prev > 0 else 0
                prev_qoq = (rev_prev/rev_prev2 - 1) if rev_prev2 > 0 else 0
                
                profit_qoq_acc = calc_profit_qoq_acc(curr_qoq, prev_qoq)
                
                growth_score = score_growth_long(earnings_slope, profit_yoy, profit_qoq_acc)
                
                # Store factors for metric display
                df.loc[last_idx, 'earnings_slope'] = earnings_slope
                df.loc[last_idx, 'profit_yoy'] = profit_yoy
                
            else:
                growth_score = 0
                df.loc[last_idx, 'earnings_slope'] = 0
                df.loc[last_idx, 'profit_yoy'] = 0
        else:
            growth_score = 0
            
        df.loc[last_idx, 'growth_score'] = growth_score
        
        # --- VALUE FACTORS ---
        pe = df.iloc[-1].get('pe', 0)
        # Growth rate for PEG: Use earnings slope or YoY, capped at reasonable levels
        g_rate = df.loc[last_idx, 'earnings_slope'] * 4 # Rough annualization
        if g_rate <= 0: g_rate = df.loc[last_idx, 'profit_yoy']
        
        value_score = score_value_peg(pe, g_rate)
        df.loc[last_idx, 'value_score'] = value_score
        
        # --- TECH FACTORS ---
        closes = df['close']
        price_slope = calc_price_slope(closes, window=60)
        rsi = calc_rsi(closes, window=14)
        
        tech_score = score_tech(price_slope, rsi)
        df.loc[last_idx, 'tech_score'] = tech_score
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or 'growth_score' not in df.columns:
            return pd.DataFrame()
            
        last_row = df.iloc[-1]
        
        # Weights: 40/40/20
        raw_score = (last_row['growth_score'] * 0.40 + 
                     last_row['value_score'] * 0.40 + 
                     last_row['tech_score'] * 0.20)
                     
        # Threshold
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"Slope: {last_row.get('earnings_slope',0):.2f} / PEG Score: {last_row.get('value_score',0):.0f}"
        output_row['secondary_metric'] = f"Tech: {last_row.get('tech_score',0):.0f}"
        output_row['backtest_type'] = 'CALENDAR'
        
        return output_row
