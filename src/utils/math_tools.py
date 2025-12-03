import pandas as pd
import numpy as np
from typing import Union

def calculate_cagr(start_val: float, end_val: float, periods: float) -> float:
    """
    Calculates Compound Annual Growth Rate.
    """
    if start_val <= 0 or periods <= 0:
        return 0.0
    return (end_val / start_val) ** (1 / periods) - 1

def calculate_linearity(series: pd.Series) -> float:
    """
    Calculates the R-squared of the log-linear regression of a series.
    Used to measure how "smooth" a trend is.
    
    Args:
        series: Time series of prices.
        
    Returns:
        float: 0.0 to 1.0 (1.0 = perfect straight line)
    """
    y = np.log(series.replace(0, np.nan).dropna())
    if len(y) < 10:
        return 0.0
        
    x = np.arange(len(y))
    
    # Simple linear regression
    correlation_matrix = np.corrcoef(x, y)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2
    
    return r_squared

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Relative Strength Index (RSI).
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_max_drawdown(series: pd.Series) -> float:
    """
    Calculates the maximum drawdown from peak.
    """
    rolling_max = series.cummax()
    drawdown = (series - rolling_max) / rolling_max
    return drawdown.min()

