"""
SURGE Strategy (业绩爆发)
=========================
Alpha Source: Davis Double Play - Earnings acceleration + Price momentum.

Logic from Strategy Reference Manual v6:
- Revenue/Profit QoQ acceleration OR YoY explosion
- Stock price in early-stage breakout
- Captures "high-open-high-close" momentum after earnings

Scoring (100 points total):
- 60% Growth Score (Burst mode - QoQ/YoY acceleration)
- 20% Value Score (not overvalued, floor at 65 points)
- 20% Technical Score (price momentum)

Adapted for Project Argos US Equity Data.
"""
import pandas as pd
import numpy as np
from src.strategies.base_strategy import BaseStrategy
from src.utils.math_tools import calculate_linearity
from src.utils.logger import logger
from scipy import stats


class SurgeStrategy(BaseStrategy):
    """
    SURGE: Earnings Explosion Strategy
    
    Targets stocks with:
    1. Explosive earnings growth (QoQ acceleration or YoY > 50%)
    2. Price in early breakout phase (not extended)
    3. Reasonable valuation (not bubble territory)
    """
    
    def __init__(self):
        super().__init__("SURGE")
    
    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Universe Filter:
        - Market Cap > $200M (allow smaller caps for surge plays)
        - Sufficient trading history
        """
        if df.empty or len(df) < 126:
            return pd.DataFrame()
        
        last_row = df.iloc[-1]
        
        # Market Cap Filter (lower threshold for surge plays)
        mcap = last_row.get('market_cap', 0)
        if pd.isna(mcap) or mcap < 2e8:
            return pd.DataFrame()
        
        # Volume Filter
        avg_vol = df['volume'].tail(20).mean()
        price = last_row['close']
        dollar_vol = avg_vol * price
        
        if dollar_vol < 2e6:
            return pd.DataFrame()
        
        return df
    
    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate SURGE-specific signals:
        1. Growth Score (Burst): QoQ acceleration, YoY explosion
        2. Value Score: PE percentile (floor at 65)
        3. Technical Score: Price momentum, breakout detection
        """
        if len(df) < 126:
            return pd.DataFrame()
        
        last_idx = df.index[-1]
        
        # --- SIGNAL 1: Growth Score (Burst Mode) ---
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            
            if len(fund_history) >= 5:
                recent = fund_history.tail(5)
                
                # Revenue metrics
                rev_current = recent.iloc[-1]['revenue']
                rev_prev_q = recent.iloc[-2]['revenue'] if len(recent) >= 2 else rev_current
                rev_yoy = recent.iloc[-4]['revenue'] if len(recent) >= 4 else rev_current
                
                # QoQ Growth
                revenue_qoq = (rev_current / rev_prev_q - 1) if rev_prev_q > 0 else 0
                
                # YoY Growth
                revenue_yoy = (rev_current / rev_yoy - 1) if rev_yoy > 0 else 0
                
                # Profit metrics
                ni_current = recent.iloc[-1]['net_income']
                ni_prev_q = recent.iloc[-2]['net_income'] if len(recent) >= 2 else ni_current
                ni_yoy = recent.iloc[-4]['net_income'] if len(recent) >= 4 else ni_current
                
                # Profit QoQ
                if ni_prev_q > 0 and ni_current > 0:
                    profit_qoq = (ni_current / ni_prev_q - 1)
                elif ni_prev_q < 0 and ni_current > 0:
                    profit_qoq = 1.0  # Turnaround
                else:
                    profit_qoq = 0
                
                # Profit YoY
                if ni_yoy > 0 and ni_current > 0:
                    profit_yoy = (ni_current / ni_yoy - 1)
                elif ni_yoy < 0 and ni_current > 0:
                    profit_yoy = 1.0  # Turnaround
                else:
                    profit_qoq = 0
                
                # Acceleration detection (QoQ improving)
                if len(recent) >= 3:
                    prev_qoq = (recent.iloc[-2]['revenue'] / recent.iloc[-3]['revenue'] - 1) if recent.iloc[-3]['revenue'] > 0 else 0
                    is_accelerating = revenue_qoq > prev_qoq
                else:
                    is_accelerating = False
                
                # Margin Improvement (Gross & Net)
                gm_current = recent.iloc[-1].get('gross_margin', 0)
                gm_prev_q = recent.iloc[-2].get('gross_margin', 0) if len(recent) >= 2 else gm_current
                gm_yoy = recent.iloc[-4].get('gross_margin', 0) if len(recent) >= 4 else gm_current
                
                nm_current = recent.iloc[-1].get('net_margin', 0)
                nm_prev_q = recent.iloc[-2].get('net_margin', 0) if len(recent) >= 2 else nm_current
                nm_yoy = recent.iloc[-4].get('net_margin', 0) if len(recent) >= 4 else nm_current

                # Deltas (Absolute change in margin points)
                gm_qoq_diff = gm_current - gm_prev_q
                gm_yoy_diff = gm_current - gm_yoy
                nm_qoq_diff = nm_current - nm_prev_q
                nm_yoy_diff = nm_current - nm_yoy
                
                # Improvement Score (Margin Expansion)
                # 10pct improvement = 100 points (scaled by 1000)
                avg_improvement = np.mean([gm_qoq_diff, gm_yoy_diff, nm_qoq_diff, nm_yoy_diff])
                improvement_score = min(100, max(0, avg_improvement * 1000))

                # Burst Score: Weighted average with bonus for acceleration
                # Logic Update: Reward simultaneous Revenue AND Profit growth (Double Engine)
                # Weights:
                # - Rev YoY: 25%
                # - Profit YoY: 35% (Profit growth is king)
                # - Rev QoQ: 10%
                # - Profit QoQ: 10%
                # - Double Engine Bonus: 20% (If both Rev YoY > 20% AND Profit YoY > 20%)
                
                burst_base = (revenue_yoy * 0.25 + profit_yoy * 0.35 + revenue_qoq * 0.10 + profit_qoq * 0.10)
                
                # Double Engine Bonus
                double_engine = (revenue_yoy > 0.20) and (profit_yoy > 0.20)
                engine_bonus = 0.20 if double_engine else 0.0
                
                # Acceleration Bonus (from previous logic)
                acc_bonus = 0.05 if is_accelerating else 0.0

                # Total Growth Score (Scaled)
                # Base + Bonuses. 
                # Example: 30% Rev, 40% Profit -> Base ~ 0.25. 
                # + 0.20 (Double) + 0.05 (Acc) = 0.50 Raw
                # Scale: 0.50 * 200 = 100 points.
                
                # New: Boost score based on absolute growth magnitude
                # If profit_yoy > 100% (doubling), give extra boost.
                magnitude_bonus = min(0.20, max(0, (profit_yoy - 0.40) * 0.5)) # Max 20pts for >80% growth
                
                growth_score = min(100, max(0, (burst_base + engine_bonus + acc_bonus + magnitude_bonus) * 200))
                
            else:
                growth_score = 0
                improvement_score = 0
                revenue_yoy = 0
                profit_yoy = 0
                revenue_qoq = 0
                profit_qoq = 0
                is_accelerating = False
        else:
            growth_score = 0
            improvement_score = 0
            revenue_yoy = 0
            profit_yoy = 0
            revenue_qoq = 0
            profit_qoq = 0
            is_accelerating = False
        
        df.loc[last_idx, 'revenue_yoy'] = revenue_yoy
        df.loc[last_idx, 'profit_yoy'] = profit_yoy
        df.loc[last_idx, 'revenue_qoq'] = revenue_qoq
        df.loc[last_idx, 'profit_qoq'] = profit_qoq
        df.loc[last_idx, 'is_accelerating'] = int(is_accelerating)
        df.loc[last_idx, 'growth_score'] = growth_score
        df.loc[last_idx, 'improvement_score'] = improvement_score
        
        # --- SIGNAL 2: Value Score (Floor at 65) ---
        pe = df.iloc[-1].get('pe', None)
        if pd.notna(pe) and pe > 0:
            # Calculate PE percentile over history
            pe_history = df['pe'].dropna()
            if len(pe_history) > 20:
                pe_percentile = (pe_history < pe).mean()
                # Lower percentile = cheaper = higher score
                value_score = max(65, 100 - pe_percentile * 100)
            else:
                value_score = 75  # Default
        else:
            value_score = 75  # Default for missing PE
        
        df.loc[last_idx, 'value_score'] = value_score
        
        # --- SIGNAL 3: Technical Score (Continuous Gaussian: Reward Coiled Springs) ---
        closes = df['close']
        
        # Price vs 50-day MA
        ma_50 = closes.tail(50).mean()
        current_price = closes.iloc[-1]
        price_vs_ma50 = (current_price / ma_50 - 1)
        
        # 3-month momentum
        price_3m_ago = closes.iloc[-63] if len(closes) >= 63 else closes.iloc[0]
        momentum_3m = (current_price / price_3m_ago - 1)
        
        # Technical score: Trend Slope + RSI
        # Replaced Gaussian curve with Slope + RSI logic from Manual.
        
        # 1. Price Slope (Linear Regression over 20 days)
        if len(closes) >= 20:
            y = closes.tail(20).values
            x = np.arange(len(y))
            slope, _, _, _, _ = stats.linregress(x, y)
            # Normalize slope: > 0 is good. steep is better but not parabolic.
            # Let's map slope to 0-100.
            # Normalized by price to get % change per day
            norm_slope = slope / y[0] * 100 
            slope_score = min(100, max(0, norm_slope * 200)) # 0.5% per day -> 100
        else:
            slope_score = 50

        # 2. RSI (14-day)
        if len(closes) >= 15:
            delta = closes.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # RSI Logic: 50-70 is sweet spot (Bullish but not overbought)
            if 50 <= current_rsi <= 75:
                rsi_score = 100
            elif current_rsi > 75:
                rsi_score = max(0, 100 - (current_rsi - 75) * 4) # Penalty for overbought
            else:
                rsi_score = max(0, current_rsi * 2) # Penalty for weak trend
        else:
            rsi_score = 50
            
        # Final Tech Score: 60% Slope + 40% RSI
        tech_score = slope_score * 0.6 + rsi_score * 0.4
        
        df.loc[last_idx, 'price_vs_ma50'] = price_vs_ma50
        df.loc[last_idx, 'momentum_3m'] = momentum_3m
        df.loc[last_idx, 'tech_score'] = tech_score
        
        return df
    
    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        SURGE Scoring:
        - 50% Growth Score (Burst)
        - 10% Improvement Score (Margin Expansion)
        - 20% Value Score (floor 65)
        - 20% Technical Score
        """
        if df.empty or 'growth_score' not in df.columns:
            return pd.DataFrame()
        
        last_row = df.iloc[-1]
        
        # --- RISK CONTROL FILTERS ---
        # 1. ROE > 10%
        roe = last_row.get('roe', 0)
        if roe < 0.10:
            return pd.DataFrame()
            
        # 2. Leverage < 300% (Debt/Equity < 3.0)
        debt_to_equity = last_row.get('debt_to_equity', 0)
        # Handle missing leverage data: if None/NaN, assume it's high risk or check total debt
        if pd.isna(debt_to_equity):
            pass 
        elif debt_to_equity > 3.0:
            return pd.DataFrame()

        # Must have positive earnings growth
        profit_yoy = last_row.get('profit_yoy', 0)
        revenue_yoy = last_row.get('revenue_yoy', 0)
        
        # SURGE requires: Either YoY profit > 30% OR revenue > 20%
        # Adjusted threshold to be less harsh, as scoring will filter better.
        if profit_yoy < 0.30 and revenue_yoy < 0.20:
            return pd.DataFrame()
        
        # Filter: Removed the hard cutoff for > 20% extension.
        # The Continuous Tech Score will naturally penalize extended stocks (Score ~20).
        
        # Calculate final score
        growth_score = last_row.get('growth_score', 0)
        improvement_score = last_row.get('improvement_score', 0)
        value_score = last_row.get('value_score', 65)
        tech_score = last_row.get('tech_score', 50)
        
        # Updated Weights: 50/10/20/20
        raw_score = (growth_score * 0.50) + (improvement_score * 0.10) + (value_score * 0.20) + (tech_score * 0.20)
        
        # Threshold: Must score > 70 (User requested 70)
        if raw_score < 70:
            return pd.DataFrame()
        
        # Build output
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['primary_metric'] = f"{profit_yoy:.1%} (NI YoY) / {revenue_yoy:.1%} (Rev YoY)"
        output_row['secondary_metric'] = f"Imp: {improvement_score:.0f} / {last_row.get('momentum_3m', 0):.1%} (Mom)"
        output_row['backtest_type'] = 'EVENT'  # Event-driven (earnings)
        output_row['strategy_name'] = self.strategy_name
        
        return output_row
