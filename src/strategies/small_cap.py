"""
SMALL_CAP Strategy (Small Cap Burst)
====================================
Logic:
- Targets smaller companies (<$2B) with explosive earnings growth.
- Rewards smaller market cap (higher growth potential).

Scoring (100 points total):
- 40% Growth (Burst): S_GROWTH (Burst) logic.
- 50% Market Cap (S_MV): Smaller is better (<$300M ideal).
- 10% Tech: S_TECH.
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    calc_surge_factor, calc_profit_qoq_acc, calc_price_slope, calc_rsi,
    score_growth_burst, score_mv_reward, score_tech
)

class SmallCapStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("SMALL_CAP")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Universe:
        - Market Cap < 2B.
        - Market Cap > 50M (Avoid micro-nano caps).
        """
        if df.empty or len(df) < 126:
            return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        if pd.isna(mcap) or mcap > 2e9 or mcap < 5e7:
            return pd.DataFrame()
            
        # Liquidity check (looser for small caps)
        avg_vol = df['volume'].tail(20).mean()
        price = last_row['close']
        if avg_vol * price < 1e6: # $1M daily volume
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        
        # --- GROWTH FACTORS (Burst) ---
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            if len(fund_history) >= 5:
                recent = fund_history.tail(5)
                
                # 1. Surge Factor
                ni_curr = recent.iloc[-1]['net_income']
                prev_3q = recent['net_income'].iloc[-4:-1]
                surge_factor = calc_surge_factor(ni_curr, prev_3q)
                
                # 2. YoY Growth
                ni_yoy = recent.iloc[-4]['net_income'] if len(recent) >= 4 else ni_curr
                profit_yoy = (ni_curr / ni_yoy - 1) if (ni_yoy > 0 and ni_curr > 0) else 0
                
                # 3. QoQ Acc
                rev_curr = recent.iloc[-1]['revenue']
                rev_prev = recent.iloc[-2]['revenue']
                rev_prev2 = recent.iloc[-3]['revenue']
                
                curr_qoq = (rev_curr/rev_prev - 1) if rev_prev > 0 else 0
                prev_qoq = (rev_prev/rev_prev2 - 1) if rev_prev2 > 0 else 0
                profit_qoq_acc = calc_profit_qoq_acc(curr_qoq, prev_qoq)
                
                growth_score = score_growth_burst(surge_factor, profit_yoy, profit_qoq_acc)
            else:
                growth_score = 0
        else:
            growth_score = 0
            
        df.loc[last_idx, 'growth_score'] = growth_score
        
        # --- MV FACTOR ---
        mcap = df.iloc[-1]['market_cap']
        mv_score = score_mv_reward(mcap)
        df.loc[last_idx, 'mv_score'] = mv_score
        
        # --- TECH FACTORS ---
        closes = df['close']
        price_slope = calc_price_slope(closes, window=60)
        rsi = calc_rsi(closes, window=14)
        tech_score = score_tech(price_slope, rsi)
        df.loc[last_idx, 'tech_score'] = tech_score
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        # Weights: 40/50/10
        raw_score = (last_row.get('growth_score',0) * 0.40 + 
                     last_row.get('mv_score',0) * 0.50 + 
                     last_row.get('tech_score',0) * 0.10)
                     
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"MV Score: {last_row.get('mv_score',0):.0f} (Cap: {last_row['market_cap']/1e6:.1f}M)"
        output_row['secondary_metric'] = f"Growth: {last_row.get('growth_score',0):.0f}"
        output_row['backtest_type'] = 'EVENT'
        
        return output_row

