import pandas as pd
import numpy as np
from src.strategies.base_strategy import BaseStrategy
from src.utils.math_tools import calculate_linearity, calculate_cagr
from src.utils.logger import logger
from scipy import stats

class AggressiveCompounder(BaseStrategy):
    """
    Aggressive Compounder Strategy.
    
    Philosophy:
    "Stronger for Longer". We seek stocks with:
    1. High Structural Linearity (Price moves in a straight line up, low volatility trend).
    2. High Velocity (Fast enough to generate Alpha).
    3. Fundamental Consistency (Earnings backup the price action).
    
    Reference Logic:
    - Linearity (R-Squared of Log-Price) > 0.90 (Ideal)
    - Slope (Annualized Growth) > 20%
    - Fundamental Consistency Score > 0.7
    """
    
    def __init__(self):
        super().__init__("Aggressive_Compounder")

    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters for liquid, mid-to-large cap stocks.
        """
        if df.empty:
            return pd.DataFrame()

        last_row = df.iloc[-1]
        ticker = last_row.get('ticker', 'Unknown')
        
        # Check Market Cap
        mcap = last_row.get('market_cap', 0)
        if pd.isna(mcap): mcap = 0
        
        if mcap < 5e8:
            # logger.debug(f"REJECT {ticker}: Market Cap {mcap} < 500M")
            return pd.DataFrame()

        # Check Volume
        vol = df['volume'].tail(20).mean()
        price = last_row['close']
        dollar_vol = vol * price
        
        if dollar_vol < 5e6:
            # logger.debug(f"REJECT {ticker}: Dollar Vol {dollar_vol:,.0f} < 5M")
            return pd.DataFrame()
            
        return df

    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates Linearity, Slope, and Fundamental Consistency.
        """
        if len(df) < 504: # Need 2 years for structural trend
            return pd.DataFrame()

        # 1. Structural Trend (2 Year)
        # We calculate rolling linearity if we want a time-series signal, 
        # but for a screener snapshot, we just take the tail.
        # However, to support BACKTESTING, we must calculate these as rolling series.
        
        # Window sizes
        window_2y = 504
        window_6m = 126
        
        # Calculate Rolling Log-Linearity
        # Note: rolling apply is slow. For vectorization, we often approximate or use specialized tools.
        # For now, we use a simplified approach for the "Current Signal" (last row) 
        # IF this is a screener run. 
        # BUT, if this is a backtest run, we need the whole series.
        # The Manual implies we generate a CSV of "Candidates" (Snapshot).
        # But Backtesting requires history.
        
        # Optimization: We will compute indicators for the whole series to support Event Backtests.
        
        # Helper for rolling linearity (R-Squared)
        def rolling_linearity(series, window):
            def r_squared(y):
                x = np.arange(len(y))
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                return r_value**2
            
            return series.rolling(window).apply(r_squared, raw=True)

        # Helper for rolling slope (Annualized)
        def rolling_slope(series, window):
            def get_slope(y):
                x = np.arange(len(y))
                slope, _, _, _, _ = stats.linregress(x, np.log(y))
                return (np.exp(slope * 252) - 1)
            
            return series.rolling(window).apply(get_slope, raw=True)

        # --- SIGNAL 1: Price Action ---
        # Using closing prices
        closes = df['close']
        
        # Since rolling linregress is very slow in pandas apply, 
        # for the "Strategy Card" definition, we often only care about the signal *at time of trade*.
        # For optimization in this phase, I will implement the signal for the *latest* point only 
        # if we are in "Screening Mode". 
        # However, to remain pure to the "Factory" model, I should calculate it properly.
        # Let's implement a faster vectorized approximation or just compute the latest if valid.
        
        # For MVP: Compute only for the latest available date to generate the "Candidate List" CSV.
        # This aligns with "generate_score" producing a snapshot.
        
        hist_2y = closes.iloc[-window_2y:]
        hist_6m = closes.iloc[-window_6m:]
        
        lin_2y = calculate_linearity(hist_2y)
        
        # Calculate Slope manually using math_tools helpers or local logic
        # Re-using the logic from the user's reference file for slope
        y_6m = np.log(hist_6m.replace(0, np.nan).dropna())
        if len(y_6m) > 10:
            x_6m = np.arange(len(y_6m))
            slope_6m, _, _, _, _ = stats.linregress(x_6m, y_6m)
            growth_6m = (np.exp(slope_6m * 252) - 1)
        else:
            growth_6m = 0.0

        # Assign to the last row of the dataframe (Snapshot Logic)
        df.loc[df.index[-1], 'linearity_2y'] = lin_2y
        df.loc[df.index[-1], 'growth_6m'] = growth_6m
        
        # --- SIGNAL 2: Fundamental Consistency ---
        # User logic: "Correlation(Revenue, NetIncome) > 0.7" or Spearman rank of Net Income
        # We need to look at the 'net_income' column which is merged (quarterly, forward filled)
        # We need to extract the unique values to avoid counting the daily forward-filled dupes.
        
        # Extract unique fundamentals history
        if 'filing_date' in df.columns:
            fund_history = df.drop_duplicates(subset=['filing_date']).sort_values('filing_date')
            recent_funds = fund_history.tail(8) # Last 8 quarters (2 years)
            
            if len(recent_funds) >= 4:
                ni = recent_funds['net_income'].values
                # Spearman rank correlation with time
                if np.std(ni) > 0:
                    ni_corr, _ = stats.spearmanr(np.arange(len(ni)), ni)
                    fund_score = 0.0 if np.isnan(ni_corr) else ni_corr
                else:
                    fund_score = 0.0
            else:
                fund_score = 0.0
        else:
            fund_score = 0.0
            
        df.loc[df.index[-1], 'fund_consistency'] = fund_score
        
        # --- SIGNAL 3: Volatility (Risk Flag) ---
        # Calculate 60-day realized volatility (annualized)
        returns = df['close'].pct_change()
        volatility_60d = returns.tail(60).std() * np.sqrt(252)
        df.loc[df.index[-1], 'volatility'] = volatility_60d
        
        return df

    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scoring Logic:
        40% Linearity + 40% Velocity + 20% Fundamental Consistency
        
        Risk Management:
        - High volatility stocks are flagged (not rejected) for AI review
        - Score is penalized based on excess volatility
        """
        if df.empty or 'linearity_2y' not in df.columns:
            return pd.DataFrame()
            
        last_row = df.iloc[-1]
        
        lin_2y = last_row.get('linearity_2y', 0)
        growth_6m = last_row.get('growth_6m', 0)
        fund_score = last_row.get('fund_consistency', 0)
        volatility = last_row.get('volatility', 0.5)
        
        # Filters (Relaxed for Backtest Validation - Tighten Later)
        # Original: (fund_score >= 0.5) and (growth_6m >= 0.15) and (lin_2y >= 0.5)
        is_pass = (fund_score >= 0.0) and (growth_6m >= 0.10) and (lin_2y >= 0.3)
        
        if not is_pass:
            return pd.DataFrame()
        
        # --- Risk Flag (Inform, Don't Reject) ---
        if volatility > 0.60:
            risk_flag = "HIGH_VOL"
        elif volatility > 0.40:
            risk_flag = "ELEVATED"
        else:
            risk_flag = "NORMAL"
        
        # --- Scoring with Volatility Penalty ---
        velocity_score = np.clip(growth_6m, 0, 1.0)
        base_score = (lin_2y * 40) + (velocity_score * 40) + (fund_score * 20)
        
        # Penalize excess volatility (above 40% annualized)
        # Max penalty: 20 points for stocks with 100%+ vol
        vol_penalty = max(0, (volatility - 0.40) * 33.3)  # 0-20 point penalty
        raw_score = base_score - vol_penalty
        
        # Populate required output columns
        output_row = df.iloc[[-1]].copy()
        output_row['raw_score'] = raw_score
        output_row['risk_flag'] = risk_flag
        output_row['volatility'] = volatility
        output_row['primary_metric'] = f"{lin_2y:.2f} (Lin) / {growth_6m:.1%} (Gro)"
        output_row['secondary_metric'] = f"{fund_score:.2f} (Fund) / {volatility:.0%} (Vol)"
        output_row['backtest_type'] = 'CALENDAR'
        output_row['strategy_name'] = self.strategy_name
        
        return output_row

