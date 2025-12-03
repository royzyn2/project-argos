"""
Common Quant Factors & Scoring Components
=========================================
Central library for calculating standardized factors as defined in 
Strategy_Reference_Manual_v6.

This ensures consistency across all strategies (TREND, TURNAROUND, SMALL_CAP, etc.).
"""

import pandas as pd
import numpy as np
from scipy import stats

# --- 1. CORE FACTORS (底层基础因子) ---

def calc_earnings_slope(net_income_series: pd.Series, window: int = 8) -> float:
    """
    EARNINGS_SLOPE: Linear regression slope of standardized net income.
    Target: > 0.08 (approx 30% annualized).
    """
    if len(net_income_series) < window:
        return 0.0
    
    # Take the window
    y = net_income_series.tail(window).values
    
    # Standardize (normalize by mean to make slope comparable across stocks)
    mean_val = np.mean(np.abs(y))
    if mean_val == 0: return 0.0
    
    y_norm = y / mean_val
    x = np.arange(len(y))
    
    slope, _, _, _, _ = stats.linregress(x, y_norm)
    
    if np.isnan(slope): return 0.0
    return slope

def calc_surge_factor(current_ni: float, prev_3q_ni_series: pd.Series) -> float:
    """
    SURGE_FACTOR: Current NI / Avg(Last 3 Quarters).
    Target: > 1.5.
    """
    if len(prev_3q_ni_series) < 3:
        return 0.0
        
    avg_3q = prev_3q_ni_series.tail(3).mean()
    
    # Handle negative base
    if avg_3q <= 0:
        if current_ni > 0: return 10.0 # Massive turnaround
        else: return 0.0 # Still losing money
        
    return current_ni / avg_3q

def calc_profit_qoq_acc(current_qoq: float, prev_qoq: float) -> float:
    """
    PROFIT_QOQ_ACC: Current QoQ - Prev QoQ.
    > 0 means acceleration.
    """
    return current_qoq - prev_qoq

def calc_pe_position(current_pe: float, pe_history: pd.Series, window: int = 500) -> float:
    """
    PE_POSITION: (Current - Min) / (Max - Min) over window.
    Target: < 0.2 (Low percentile).
    """
    if len(pe_history) < 20: return 0.5 # Not enough data, assume mid
    
    recent_pe = pe_history.tail(window)
    min_pe = recent_pe.min()
    max_pe = recent_pe.max()
    
    if max_pe == min_pe: return 0.5
    
    # Clip current PE to history range (in case it's a new high/low)
    c_pe = max(min_pe, min(max_pe, current_pe))
    
    return (c_pe - min_pe) / (max_pe - min_pe)

def calc_price_slope(closes: pd.Series, window: int = 60) -> float:
    """
    PRICE_SLOPE: (Current / Price 60 days ago) - 1.
    Simple momentum.
    """
    if len(closes) < window: return 0.0
    return (closes.iloc[-1] / closes.iloc[-window]) - 1

def calc_rsi(closes: pd.Series, window: int = 14) -> float:
    """
    Standard RSI.
    """
    if len(closes) <= window: return 50.0
    
    delta = closes.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calc_profit_stability_cv(net_income_series: pd.Series, window: int = 12) -> float:
    """
    PROFIT_STABILITY_CV: StdDev / Mean.
    Lower is better.
    """
    if len(net_income_series) < 4: return 1.0 # High variance default
    
    recent = net_income_series.tail(window)
    mean_val = recent.mean()
    std_val = recent.std()
    
    if mean_val == 0: return 1.0
    return abs(std_val / mean_val)


# --- 2. SCORING COMPONENTS (上层评分组件) ---

def score_growth_long(earnings_slope, profit_yoy, profit_qoq_acc):
    """
    S_GROWTH (Long):
    - EARNINGS_SLOPE (40%)
    - PROFIT_YOY (30%)
    - PROFIT_QOQ_ACC (30%)
    """
    # Normalize inputs to 0-100 scale approx
    # Slope: 0.08 -> 100
    s_slope = min(100, max(0, earnings_slope * 1250)) 
    
    # YoY: 30% -> 100
    s_yoy = min(100, max(0, profit_yoy * 333))
    
    # Acc: 10% -> 100 (0.10 diff)
    s_acc = min(100, max(0, profit_qoq_acc * 1000))
    
    return s_slope * 0.4 + s_yoy * 0.3 + s_acc * 0.3

def score_growth_burst(surge_factor, profit_yoy, profit_qoq_acc):
    """
    S_GROWTH (Burst):
    - SURGE_FACTOR (40%)
    - PROFIT_YOY (30%)
    - PROFIT_QOQ_ACC (30%)
    """
    # Surge Factor: 1.5 -> 100. Base is 1.0. So (Factor - 1.0) * 200?
    # 1.5 - 1.0 = 0.5 * 200 = 100.
    s_surge = min(100, max(0, (surge_factor - 1.0) * 200))
    
    # YoY: 50% -> 100 (Burst needs higher growth)
    s_yoy = min(100, max(0, profit_yoy * 200))
    
    # Acc: 10% -> 100
    s_acc = min(100, max(0, profit_qoq_acc * 1000))
    
    return s_surge * 0.4 + s_yoy * 0.3 + s_acc * 0.3

def score_value_peg(pe, growth_rate):
    """
    S_VALUE (PEG):
    PEG = PE / (Growth * 100).
    PEG < 0.8 -> 100
    PEG > 2.0 -> 40
    """
    if growth_rate <= 0.01: return 40 # No growth, expensive
    if pe <= 0: return 50 # Negative PE
    
    peg = pe / (growth_rate * 100)
    
    if peg < 0.8: return 100
    if peg > 2.0: return 40
    
    # Linear interp between 0.8 (100) and 2.0 (40)
    # Slope = (40 - 100) / (2.0 - 0.8) = -60 / 1.2 = -50
    # Score = 100 - 50 * (peg - 0.8)
    return max(40, 100 - 50 * (peg - 0.8))

def score_tech(price_slope, rsi):
    """
    S_TECH:
    - PRICE_SLOPE (60%)
    - RSI (40%)
    """
    # Slope: 20% in 60 days -> 100?
    s_slope = min(100, max(0, price_slope * 500))
    
    # RSI: 50-70 Ideal (100). >80 penalty. <40 penalty.
    if 50 <= rsi <= 75:
        s_rsi = 100
    elif rsi > 75:
        s_rsi = max(0, 100 - (rsi - 75) * 4)
    else:
        s_rsi = max(0, rsi * 2)
        
    return s_slope * 0.6 + s_rsi * 0.4

def score_dividend(div_yield):
    """
    S_DIV:
    Yield 5% -> 100.
    """
    return min(100, max(0, (div_yield / 0.05) * 100))

def score_improve(profit_yoy_diff):
    """
    S_IMPROVE:
    10pct improvement -> 100.
    """
    return min(100, max(0, profit_yoy_diff * 1000))

def score_core(market_cap, roe):
    """
    S_CORE:
    - Market Cap (40%): > 100B -> 100
    - ROE (60%): > 20% -> 100
    """
    # Cap in Billions. 100e9
    s_cap = min(100, max(0, (market_cap / 100e9) * 100))
    
    # ROE
    s_roe = min(100, max(0, (roe / 0.20) * 100))
    
    return s_cap * 0.4 + s_roe * 0.6

def score_pos(pe_position):
    """
    POS_SCORE:
    Position < 0 (Min) -> 100.
    Position > 1 (Max) -> 0.
    """
    return max(0, 100 - pe_position * 100)

def score_mv_reward(market_cap):
    """
    S_MV:
    Small Cap Reward. < 300M -> 100.
    Decreases as cap grows. > 2B -> 0.
    """
    if market_cap < 3e8: return 100
    if market_cap > 2e9: return 0
    
    # Linear decay from 300M to 2B
    # Range = 1.7B.
    # Score = 100 * (1 - (Cap - 300M)/1.7B)
    return 100 * (1 - (market_cap - 3e8) / 1.7e9)

