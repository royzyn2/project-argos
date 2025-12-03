from abc import ABC, abstractmethod
import pandas as pd
import os
import yaml
from src.utils.logger import logger

# Minimal required output columns for backtester compatibility
# Strategies can add any additional columns they need (e.g., risk_flag, volatility)
REQUIRED_OUTPUT_COLUMNS = [
    'ticker',           # Stock identifier
    'date',             # Signal date
    'close',            # Price at signal (for return calculation)
    'raw_score',        # 0-100 ranking score
    'strategy_name',    # Routes to correct AI prompt
    'backtest_type',    # 'CALENDAR' or 'EVENT'
]

# Optional but recommended columns for AI context
RECOMMENDED_COLUMNS = [
    'primary_metric',   # Main signal value for AI
    'secondary_metric', # Supporting signal for AI
]

class BaseStrategy(ABC):
    """
    Abstract Base Class for all quantitative strategies in Project Argos.
    
    Developers must implement:
    1. define_universe(df) -> filtered_df
    2. calculate_signals(df) -> df_with_indicators
    3. generate_score(df) -> df_with_score
    
    Output Contract:
    - generate_score() MUST return a DataFrame with REQUIRED_OUTPUT_COLUMNS
    - Additional strategy-specific columns (e.g., risk_flag) are allowed and will pass through
    - The backtester uses only required columns; extras are for AI/human review
    """
    
    def __init__(self, strategy_name: str):
        self.strategy_name = strategy_name
        self.results_dir = "data/results"
        self.load_config()

    def load_config(self):
        """Loads global settings."""
        try:
            with open("config/settings.yaml", 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("config/settings.yaml not found. Using defaults.")
            self.config = {}

    @abstractmethod
    def define_universe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter the universe based on market cap, liquidity, etc.
        Example: return df[df['market_cap'] > 1e9]
        """
        pass

    @abstractmethod
    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical or fundamental indicators.
        Example: df['ma_50'] = df['close'].rolling(50).mean()
        """
        pass

    @abstractmethod
    def generate_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a final score (0-100) and ranking logic.
        Must return dataframe with 'raw_score' column.
        """
        pass

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main execution flow. Orchestrates strategy and validates output schema.
        
        Returns:
            DataFrame with validated output columns, or empty DataFrame if no candidates.
        """
        logger.info(f"Running strategy: {self.strategy_name}")
        
        # 1. Universe Selection
        logger.info("Step 1: Defining Universe...")
        df_universe = self.define_universe(df)
        if df_universe.empty:
            logger.warning("Universe filter returned empty DataFrame.")
            return pd.DataFrame()

        # 2. Signal Calculation
        logger.info("Step 2: Calculating Signals...")
        df_signals = self.calculate_signals(df_universe)
        if df_signals.empty:
            logger.warning("Signal calculation returned empty DataFrame.")
            return pd.DataFrame()

        # 3. Scoring
        logger.info("Step 3: Generating Scores...")
        df_scored = self.generate_score(df_signals)
        
        if df_scored.empty:
            return pd.DataFrame()
        
        # Auto-fill strategy_name if not present
        if 'strategy_name' not in df_scored.columns:
            df_scored['strategy_name'] = self.strategy_name
        
        # Validate Required Columns
        missing_cols = [col for col in REQUIRED_OUTPUT_COLUMNS if col not in df_scored.columns]
        if missing_cols:
            error_msg = f"Strategy '{self.strategy_name}' output missing required columns: {missing_cols}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Warn about missing recommended columns (non-fatal)
        missing_recommended = [col for col in RECOMMENDED_COLUMNS if col not in df_scored.columns]
        if missing_recommended:
            logger.warning(f"Strategy output missing recommended columns: {missing_recommended}")
        
        return df_scored

    def save_results(self, df: pd.DataFrame):
        """
        Saves strategy results to CSV.
        Preserves ALL columns (required + strategy-specific) for AI context.
        """
        if df.empty:
            logger.warning("No results to save.")
            return
            
        output_path = os.path.join(self.results_dir, f"{self.strategy_name}.csv")
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Save ALL columns (not just required) - strategy-specific columns flow to AI
        df.to_csv(output_path, index=False)
        logger.info(f"Strategy results saved to: {output_path}")

