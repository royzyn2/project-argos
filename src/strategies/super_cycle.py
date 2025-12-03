"""
SUPER_CYCLE Strategy (Long-Term Compounders)
============================================
Logic:
- Identifies "Forever Stocks" that win across cycles.
- Lookback: 5 Years (approx 1260 trading days).
- Core Filter: High Growth + High ROE + Resilience (Linearity).

Scoring (100 points total):
- 40% Growth: 5-Year CAGR of Revenue & Net Income.
- 30% Quality: Stable/Expanding Margins (Continuous) & High ROE.
- 20% Valuation: PEG based.
- 10% Resilience: Price Linearity (R²) to penalize Black Swan volatility.
"""

import pandas as pd
import numpy as np
from src.strategies.base_strategy import BaseStrategy
from src.strategies.common_factors import (
    score_value_peg
)
from src.utils.math_tools import calculate_linearity
from scipy import stats

class SuperCycleStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("SUPER_CYCLE")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Universe:
        - Market Cap > $2B (Proven winners).
        - History > 5 Years (Critical for cycle analysis).
        """
        if df.empty or len(df) < 1260:
            return pd.DataFrame()
        
        last_row = df.iloc[-1]
        mcap = last_row.get('market_cap', 0)
        
        if pd.isna(mcap) or mcap < 2e9:
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        last_idx = df.index[-1]
        
        # --- 1. TECHNICAL FILTER (Uptrend) ---
        closes = df['close']
        ma_200 = closes.tail(200).mean()
        price = closes.iloc[-1]
        # Must be above 200-day MA to be in a "Super Cycle"
        # Note: In deep Black Swan (like 2008 depth), price might dip below MA200.
        # But for entry, we generally want uptrend. 
        # Relaxed: If not above MA200, check if Linearity is very high (resilient pullback).
        is_uptrend = price > ma_200
        
        # --- 2. RESILIENCE SCORE (Linearity) ---
        # Calculate R² over 5 years. High R² means the stock shrugs off black swans quickly.
        # 5 Years = 1260 days
        long_term_closes = closes.tail(1260)
        linearity = calculate_linearity(long_term_closes)
        
        # Score: R²=0.9 -> 100, R²=0.6 -> 0
        resilience_score = max(0, min(100, (linearity - 0.6) / 0.3 * 100))
        
        df.loc[last_idx, 'is_uptrend'] = is_uptrend
        df.loc[last_idx, 'linearity'] = linearity
        df.loc[last_idx, 'resilience_score'] = resilience_score
        
        # --- 3. FUNDAMENTAL GROWTH (5Y CAGR) ---
        growth_score = 0
        rev_cagr = 0
        prof_cagr = 0
        
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            
            # Need ~20 quarters for 5 years
            if len(fund_history) >= 20:
                # 5-Year Lookback
                start_row = fund_history.iloc[-20]
                end_row = fund_history.iloc[-1]
                
                # Revenue CAGR
                r_start = start_row['revenue']
                r_end = end_row['revenue']
                if r_start > 0 and r_end > 0:
                    rev_cagr = (r_end / r_start)**(1/5) - 1
                
                # Profit CAGR
                p_start = start_row['net_income']
                p_end = end_row['net_income']
                if p_start > 0 and p_end > 0:
                    prof_cagr = (p_end / p_start)**(1/5) - 1
                
                # Combined Growth Metric
                # Target: > 15% CAGR is excellent for large caps
                avg_cagr = (rev_cagr + prof_cagr) / 2
                # Score: 15% -> 80pts, 25% -> 100pts
                growth_score = min(100, max(0, avg_cagr / 0.20 * 100))
                
                # --- 4. QUALITY (Continuous Margin Trend + ROE) ---
                # Margin Trend (Slope)
                margins = fund_history['net_margin'].tail(20)
                if len(margins) >= 10:
                    slope, _, _, _, _ = stats.linregress(np.arange(len(margins)), margins)
                    
                    # Continuous Scoring (Sigmoid-like mapping)
                    # Slope = 0.005 (50bps/qtr) -> 100 pts
                    # Slope = 0.000 (Stable) -> 70 pts
                    # Slope = -0.005 (-50bps/qtr) -> 0 pts
                    
                    # Linear mapping between -0.005 and +0.005
                    # y = kx + b
                    # 0 = k*(-0.005) + b
                    # 100 = k*(0.005) + b
                    # -> k = 10000, b = 50
                    
                    margin_score = min(100, max(0, slope * 10000 + 50))
                    
                else:
                    margin_score = 50
                
                # ROE
                roe = end_row.get('roe', 0)
                # ROE > 20% is world class
                roe_score = min(100, max(0, roe / 0.20 * 100))
                
                quality_score = (margin_score * 0.6 + roe_score * 0.4) # Margin trend slightly more weight
                
            else:
                growth_score = 0
                quality_score = 0
        else:
            growth_score = 0
            quality_score = 0
            
        df.loc[last_idx, 'growth_score'] = growth_score
        df.loc[last_idx, 'quality_score'] = quality_score
        df.loc[last_idx, 'rev_cagr'] = rev_cagr
        
        # --- 5. VALUATION ---
        pe = df.iloc[-1].get('pe', 0)
        # Use 5Y CAGR as expected growth rate
        value_score = score_value_peg(pe, rev_cagr) # Using Rev CAGR as proxy for long term
        df.loc[last_idx, 'value_score'] = value_score
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty: return pd.DataFrame()
        last_row = df.iloc[-1]
        
        # Filters
        # 1. Must have real growth (>10% CAGR)
        if last_row.get('rev_cagr', 0) < 0.10:
            return pd.DataFrame()
            
        # 2. Trend Check (Relaxed for Black Swans if Resilience is high)
        is_uptrend = last_row.get('is_uptrend', False)
        linearity = last_row.get('linearity', 0)
        
        # If not in uptrend (Price < MA200), only accept if Linearity > 0.8 (Proven compounder in a dip)
        if not is_uptrend and linearity < 0.8:
            return pd.DataFrame()
            
        # Weights: 40/30/20/10
        raw_score = (last_row.get('growth_score',0) * 0.40 + 
                     last_row.get('quality_score',0) * 0.30 + 
                     last_row.get('value_score',0) * 0.20 + 
                     last_row.get('resilience_score',0) * 0.10)
                     
        if raw_score < 70:
            return pd.DataFrame()
            
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"5Y CAGR: {last_row.get('rev_cagr',0):.1%} / R²: {linearity:.2f}"
        output_row['secondary_metric'] = f"Qual: {last_row.get('quality_score',0):.0f} / Val: {last_row.get('value_score',0):.0f}"
        output_row['backtest_type'] = 'CALENDAR'
        output_row['strategy_name'] = self.strategy_name
        
        return output_row
