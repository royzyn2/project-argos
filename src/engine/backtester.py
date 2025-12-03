import pandas as pd
import numpy as np
import random
import os
from pathlib import Path
from scipy import stats
from src.utils.logger import logger
from src.engine.data_loader import data_loader
from src.strategies.compounder import AggressiveCompounder
from src.strategies.dip import DipStrategy
from src.strategies.surge import SurgeStrategy
from src.strategies.trend import TrendStrategy
from src.strategies.turnaround import TurnaroundStrategy
from src.strategies.small_cap import SmallCapStrategy
from src.strategies.dividend import DividendStrategy
from src.strategies.core_value import CoreValueStrategy
from src.strategies.core_stable import CoreStableStrategy
from src.strategies.super_cycle import SuperCycleStrategy
from config.settings import data_paths

# Backtest Modes
MODE_CALENDAR = "CALENDAR" # Blind Time Travel
MODE_EVENT = "EVENT"       # Event Study

# Stress Scenarios (Protocol B)
STRESS_SCENARIOS = {
    "COVID_CRASH": "2020-02-20",      # Just before the plunge
    "RATE_HIKE_2022": "2022-01-03",   # Start of bear market
    "INFLATION_SPIKE": "2022-06-01",  # Peak CPI fear
    "LIQUIDITY_CRUNCH_2018": "2018-09-20" # Q4 2018 Meltdown (Manual Requirement)
}

# Strategy Registry
STRATEGY_REGISTRY = {
    "Aggressive_Compounder": AggressiveCompounder,
    "DIP": DipStrategy,
    "SURGE": SurgeStrategy,
    "TREND": TrendStrategy,
    "TURNAROUND": TurnaroundStrategy,
    "SMALL_CAP": SmallCapStrategy,
    "DIVIDEND": DividendStrategy,
    "CORE_VALUE": CoreValueStrategy,
    "CORE_STABLE": CoreStableStrategy,
    "SUPER_CYCLE": SuperCycleStrategy,
}

class Backtester:
    """
    The Validation Engine for Project Argos.
    Implements Protocol A (Blind Time Travel) and Protocol B (Kryptonite Test).
    """
    
    def __init__(self, strategy_name: str, experiment_tag: str, benchmark_ticker: str = 'SPX'):
        self.strategy_name = strategy_name
        self.experiment_tag = experiment_tag
        self.benchmark_ticker = benchmark_ticker
        
        # Initialize Strategy from Registry
        if strategy_name in STRATEGY_REGISTRY:
            self.strategy = STRATEGY_REGISTRY[strategy_name]()
        else:
            available = ", ".join(STRATEGY_REGISTRY.keys())
            raise ValueError(f"Unknown strategy: {strategy_name}. Available: {available}")
            
        # Load Metadata
        meta_dir = Path("data/meta_data")
        self.calendar = pd.read_csv(meta_dir / "trading_calendar.csv")['date'].tolist()
        # Fixed column name from 'ticker' to 'symbol' based on actual CSV schema
        self.universe = pd.read_csv(meta_dir / "stocks.csv")['symbol'].tolist()
        
        # Setup Output
        self.output_dir = Path(f"experiments/{strategy_name}/{experiment_tag}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _run_strategy_snapshot(self, date_str: str) -> pd.DataFrame:
        """
        Runs the strategy for a specific date on the entire universe.
        """
        # This helper was missing in the previous file read but implied by usage.
        # I need to implement it or find where it was.
        # Wait, I might have missed it in the previous `read_file` output? 
        # No, it wasn't there. It seems I need to implement it.
        # The strategy.run() expects a dataframe.
        # We need to reconstruct the helper.
        
        candidates = []
        
        # We need to load data for tickers. 
        # To be efficient, we might want to parallelize or just loop.
        # For now, simple loop.
        
        # logger.info(f"Running snapshot for {date_str}")
        
        # We can't easily run for ALL tickers efficiently without a proper engine.
        # But we can iterate through what we have.
        
        # Note: loading 6000 tickers one by one is slow.
        # In a real factory, we'd have a date-indexed store.
        # Here we have ticker-indexed parquet.
        
        # Optimization: We can't check every ticker efficiently.
        # But `run_strategy_scan` in main.py does exactly that.
        # So we replicate that logic but filtered for date.
        
        market_dir = Path("data/market_data")
        files = list(market_dir.glob("*.parquet"))
        
        # We'll sample or use all? The prompt implies "all available tickers".
        # Using all.
        
        target_date = pd.to_datetime(date_str)
        
        for file_path in files:
            try:
                ticker = file_path.stem
                # Load ONLY up to target date to save memory/time?
                # load_merged_data loads everything.
                # We should probably use data_loader to load properly.
                
                # Optimized Load:
                # We only need history up to target_date.
                # But `load_merged_data` does merge_asof which needs fundamentals.
                
                df = data_loader.load_merged_data(ticker)
                if df.empty:
                    continue
                
                # Slice up to date
                mask = df['date'] <= target_date
                historical_df = df[mask].copy()
                
                if historical_df.empty:
                    continue
                
                # Check if the last date is reasonably close to target_date (e.g. within 10 days)
                # If the stock delisted years ago, we shouldn't trade it now.
                last_dt = historical_df['date'].iloc[-1]
                if (target_date - last_dt).days > 10:
                    continue
                
                # Run Strategy
                result_row = self.strategy.run(historical_df)
                if not result_row.empty:
                    candidates.append(result_row)
                    
            except Exception as e:
                continue
        
        if candidates:
            return pd.concat(candidates, ignore_index=True)
        else:
            return pd.DataFrame()

    def _get_benchmark_return(self, start_date: str, days: int) -> float:
        """Calculates benchmark return over the period."""
        try:
            bench_df = data_loader.load_ticker_market_data(self.benchmark_ticker)
            if bench_df.empty:
                return 0.0
                
            start_dt = pd.to_datetime(start_date)
            future = bench_df[bench_df['date'] > start_dt].head(days)
            
            if future.empty:
                return 0.0
                
            # Find closest start price (snapshot price)
            history = bench_df[bench_df['date'] <= start_dt].tail(1)
            if history.empty:
                return 0.0
                
            start_price = history.iloc[-1]['close']
            end_price = future.iloc[-1]['close']
            return (end_price / start_price) - 1
        except Exception:
            return 0.0

    def run_stress_test(self):
        """
        Protocol B: Kryptonite Test.
        Runs the strategy specifically during known historical market crashes.
        """
        logger.info(f"Starting Protocol B: Kryptonite Stress Test (Bench: {self.benchmark_ticker})...")
        
        results = []
        
        for scenario_name, date_str in STRESS_SCENARIOS.items():
            logger.info(f"Running Stress Test: {scenario_name} ({date_str})")
            
            candidates = self._run_strategy_snapshot(date_str)
            
            if candidates.empty:
                logger.warning(f"No candidates found for {scenario_name}")
                continue
                
            candidates.sort_values('raw_score', ascending=False, inplace=True)
            top_candidates = candidates.head(100).copy()
            
            # Calculate Strategy Returns (Multi-Horizon)
            # Remove 'months=3' as signature changed
            returns = self._calculate_forward_returns(top_candidates, date_str)
            returns['Scenario'] = scenario_name
            
            # Calculate Benchmark Return & Alpha for 3M (Stress Focus)
            # We will focus on 3M for the main stress report but keep others available
            bench_ret_3m = self._get_benchmark_return(date_str, 63)
            returns['Benchmark_3M'] = bench_ret_3m
            returns['Alpha_3M'] = returns['Return_3M'] - bench_ret_3m
            
            results.append(returns)
            
        if results:
            final_df = pd.concat(results, ignore_index=True)
            self._generate_stress_report(final_df)
            logger.info("Stress Test Complete.")
        else:
            logger.error("Stress Test Failed to generate results.")

    def _generate_stress_report(self, df: pd.DataFrame):
        """
        Generates the 'Kryptonite Report' with Benchmark comparison.
        Focuses on 3M Horizon as the primary 'Survival' metric.
        """
        report_path = self.output_dir / "stress_test_report.md"
        
        # Aggregate by Scenario using 3M metrics
        summary = df.groupby('Scenario')[['Return_3M', 'Benchmark_3M', 'Alpha_3M', 'MaxDD_3M']].mean()
        summary.columns = ['Strategy Return (3M)', 'Benchmark Return (3M)', 'Alpha (3M)', 'Avg Drawdown (3M)']
        
        # Format summary
        for col in summary.columns:
            summary[col] = summary[col].apply(lambda x: f"{x:.2%}")
        
        with open(report_path, "w") as f:
            f.write(f"# Kryptonite Test Report: {self.strategy_name}\n")
            f.write(f"**Experiment Tag:** {self.experiment_tag}\n")
            f.write(f"**Benchmark:** {self.benchmark_ticker}\n\n")
            
            f.write("## 1. Scenario Performance (3-Month Survival)\n")
            f.write("Did the strategy survive better than the market?\n\n")
            f.write(summary.to_markdown())
            f.write("\n\n")
            
            f.write("## 2. Detailed Breakdown\n")
            for scenario in df['Scenario'].unique():
                f.write(f"### {scenario}\n")
                sub = df[df['Scenario'] == scenario]
                
                win_rate = (sub['Alpha_3M'] > 0).mean()
                f.write(f"* **Win Rate (vs Bench):** {win_rate:.1%}\n")
                
                f.write("#### Worst Drawdowns (3M)\n")
                worst = sub.sort_values('MaxDD_3M', ascending=True).head(5)
                worst_disp = worst[['ticker', 'Return_3M', 'Alpha_3M', 'MaxDD_3M']].copy()
                for col in ['Return_3M', 'Alpha_3M', 'MaxDD_3M']:
                    worst_disp[col] = worst_disp[col].apply(lambda x: f"{x:.1%}")
                f.write(worst_disp.to_markdown(index=False))
                f.write("\n\n")

    def run_protocol_c(self):
        """
        Protocol C: Event-Aligned Backtest (Full Version).
        Tests ALL available earnings seasons (approx 18).
        """
        logger.info(f"Starting Protocol C: Event Study (Full) for {self.strategy_name}")
        self._run_event_study_logic(sample_all=True)

    def run_protocol_c2(self):
        """
        Protocol C2: Event-Aligned Backtest (Lite Version).
        Tests 5 random earnings seasons for rapid iteration.
        """
        logger.info(f"Starting Protocol C2: Event Study (Lite) for {self.strategy_name}")
        self._run_event_study_logic(sample_all=False, n_samples=5)

    def _run_event_study_logic(self, sample_all: bool = True, n_samples: int = 5):
        """
        Shared logic for Protocol C and C2.
        """
        fund_df = data_loader.load_fundamentals()
        max_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        
        # Sample logic (Earnings Seasons)
        potential_dates = []
        years = range(2019, 2025)
        months = [4, 7, 10] 
        
        for y in years:
            for m in months:
                d = pd.Timestamp(f"{y}-{m:02d}-25")
                if d < max_date:
                    potential_dates.append(d)
        
        if sample_all:
            sample_dates = potential_dates
        else:
            if len(potential_dates) < n_samples:
                sample_dates = potential_dates
            else:
                sample_dates = sorted(random.sample(potential_dates, n_samples))

        logger.info(f"Testing {len(sample_dates)} earnings seasons...")
        
        results = []
        
        for test_date in sample_dates:
            date_str = test_date.strftime('%Y-%m-%d')
            logger.info(f"Testing Earnings Season: {date_str}")
            
            candidates = self._run_strategy_snapshot(date_str)
            
            if candidates.empty:
                continue
            
            candidates.sort_values('raw_score', ascending=False, inplace=True)
            # Remove limit to include all candidates
            top_candidates = candidates.copy()
            logger.info(f"Found {len(top_candidates)} candidates for {date_str}")
            
            # Calculate Returns (Multi-Horizon)
            returns = self._calculate_forward_returns(top_candidates, date_str)
            
            # Calculate Benchmark Returns
            for horizon in ['3M', '6M', '1Y', 'MAX']:
                days = {'3M': 63, '6M': 126, '1Y': 252, 'MAX': 504}[horizon]
                bench_ret = self._get_benchmark_return(date_str, days)
                returns[f'Benchmark_{horizon}'] = bench_ret
                returns[f'Alpha_{horizon}'] = returns[f'Return_{horizon}'] - bench_ret
            
            results.append(returns)
            
        if results:
            final_df = pd.concat(results, ignore_index=True)
            
            # Different filenames for C and C2
            filename = "protocol_c_results.csv" if sample_all else "protocol_c2_results.csv"
            output_path = self.output_dir / filename
            final_df.to_csv(output_path, index=False)
            
            # Generate Universe Stats for Comparison (Post-Process to avoid loop lag)
            logger.info("Calculating Universe Distribution Benchmarks (Sample 2000)...")
            # Use 2000 samples as proxy for "Full Universe" to find Top Winners
            universe_stats, top_winners = self._calculate_universe_stats(sample_dates, n_samples=2000, scan_all=False)
            
            mode_label = "EVENT_FULL" if sample_all else "EVENT_LITE"
            self._generate_report(final_df, [d.strftime('%Y-%m-%d') for d in sample_dates], mode=mode_label, universe_stats=universe_stats, top_winners=top_winners)
            logger.info(f"Protocol {mode_label} complete. Results saved to {output_path}")
        else:
            logger.warning(f"Protocol produced no results.")

    def run_calendar_test(self, n_samples: int = 5, lookahead_months: int = 6):
        """
        Protocol A: Blind Time Travel.
        """
        logger.info(f"Starting Protocol A (Calendar Backtest) - {n_samples} samples")
        
        min_history = 504
        min_future = 252
        
        valid_indices = range(min_history, len(self.calendar) - min_future)
        
        if not valid_indices:
            logger.error("Calendar too short.")
            return

        if len(valid_indices) < n_samples:
            sample_indices = list(valid_indices)
        else:
            sample_indices = random.sample(valid_indices, n_samples)
            
        sample_dates = [self.calendar[i] for i in sample_indices]
        sample_dates.sort()
        
        results = []
        
        for test_date in sample_dates:
            logger.info(f"Testing Snapshot Date: {test_date}")
            candidates = self._run_strategy_snapshot(test_date)
            
            if candidates.empty:
                continue
            
            candidates.sort_values('raw_score', ascending=False, inplace=True)
            top_candidates = candidates.head(100).copy()
            
            # Calculate Returns (Multi-Horizon)
            returns = self._calculate_forward_returns(top_candidates, test_date)
            
            # Benchmark Comparison
            for horizon in ['3M', '6M', '1Y', 'MAX']:
                days = {'3M': 63, '6M': 126, '1Y': 252, 'MAX': 504}[horizon]
                bench_ret = self._get_benchmark_return(test_date, days)
                returns[f'Benchmark_{horizon}'] = bench_ret
                returns[f'Alpha_{horizon}'] = returns[f'Return_{horizon}'] - bench_ret
            
            results.append(returns)
            
        if results:
            final_df = pd.concat(results, ignore_index=True)
            output_path = self.output_dir / "protocol_a_results.csv"
            final_df.to_csv(output_path, index=False)
            
            # Generate Universe Stats for Comparison
            logger.info("Calculating Universe Distribution Benchmarks (Sample 2000)...")
            universe_stats, top_winners = self._calculate_universe_stats(sample_dates, n_samples=2000, scan_all=False)
            
            self._generate_report(final_df, sample_dates, mode="CALENDAR", universe_stats=universe_stats, top_winners=top_winners)
            logger.info(f"Protocol A complete. Results saved to {output_path}")
        else:
            logger.warning("Backtest produced no results.")

    def _calculate_universe_stats(self, dates: list, n_samples: int = 500, scan_all: bool = False) -> pd.DataFrame:
        """
        Samples the universe on the given dates to create a baseline return distribution.
        If scan_all=True, it scans the ENTIRE universe to find the TRUE Top 50 winners (for Recall Analysis).
        
        Returns a DataFrame with:
        - Distribution percentiles (always)
        - List of Top 50 Winners per date (if scan_all=True) embedded in metadata or a separate return?
        - To keep signature simple, we will store Top 50 in a class attribute or return a tuple?
        - Better: Return a tuple (stats_df, top_winners_df)
        """
        # NOTE: Changing return signature requires updating callers!
        # Callers: run_protocol_c, run_protocol_c2, run_calendar_test
        
        all_metrics = []
        all_top_winners = []
        
        for date_val in dates:
            # Handle both string and timestamp inputs
            date_str = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else date_val
            start_dt = pd.to_datetime(date_str)
            
            # Sample logic
            if scan_all:
                sample_tickers = self.universe
                logger.info(f"Scanning FULL UNIVERSE ({len(sample_tickers)} tickers) for {date_str}...")
            else:
                if len(self.universe) > n_samples:
                    sample_tickers = random.sample(self.universe, n_samples)
                else:
                    sample_tickers = self.universe
                
            date_returns = [] # List of dicts
            sample_debug_count = 0
            
            for ticker in sample_tickers:
                try:
                    full_df = data_loader.load_ticker_market_data(ticker)
                    if full_df.empty: continue
                    
                    # Ensure proper types and sort
                    full_df['date'] = pd.to_datetime(full_df['date'])
                    full_df.sort_values('date', inplace=True)
                    
                    # Entry logic: Price on or before snapshot date
                    history = full_df[full_df['date'] <= start_dt]
                    if history.empty: continue
                    
                    entry_row = history.iloc[-1]
                    entry_price = entry_row['close']
                    entry_date = entry_row['date']
                    
                    # FILTER: Ignore penny stocks (< $5) and potential bad data
                    if entry_price < 5.0: continue
                    
                    # Future prices
                    future_prices = full_df[full_df['date'] > start_dt]
                    if future_prices.empty: continue
                    
                    horizons = {'3M': 63, '6M': 126, '1Y': 252}
                    ticker_rets = {'ticker': ticker, 'date': date_str}
                    
                    for h, days in horizons.items():
                        period_data = future_prices.head(days)
                        if period_data.empty:
                            ticker_rets[f'Return_{h}'] = np.nan
                        else:
                            end_price = period_data.iloc[-1]['close']
                            
                            # Calculate Return
                            raw_ret = (end_price / entry_price) - 1
                            
                            # Sanity Check: Cap unrealistic returns for universe stats (e.g. > 500% in 3M is likely reverse split or data error)
                            if raw_ret > 5.0: 
                                raw_ret = np.nan
                            
                            ticker_rets[f'Return_{h}'] = raw_ret
                            
                            # Debug log for first few samples
                            if sample_debug_count < 3 and h == '3M':
                                logger.info(f"[UnivSample] {ticker} @ {date_str}: Entry={entry_price:.2f} ({entry_date.date()}) -> Exit={end_price:.2f} -> Ret={raw_ret:.2%}")
                    
                    # Only add if at least one return is valid
                    if any(pd.notna(v) for k,v in ticker_rets.items() if k.startswith('Return')):
                        date_returns.append(ticker_rets)
                        sample_debug_count += 1
                        
                except Exception as e:
                    # logger.warning(f"Error processing {ticker} for univ stats: {e}")
                    continue
            
            if not date_returns:
                logger.warning(f"No valid universe samples found for {date_str}")
                continue
                
            stats = pd.DataFrame(date_returns)
            
            # 1. Calculate Distribution Percentiles
            date_stats = {'date': date_str}
            for h in ['3M', '6M', '1Y']:
                col = f'Return_{h}'
                if col in stats.columns:
                    clean_series = stats[col].dropna()
                    if not clean_series.empty:
                        date_stats[f'Univ_{h}_25'] = clean_series.quantile(0.25)
                        date_stats[f'Univ_{h}_50'] = clean_series.median()
                        date_stats[f'Univ_{h}_75'] = clean_series.quantile(0.75)
            all_metrics.append(date_stats)
            
            # 2. Extract Top 50 Winners (Always, from the sample)
            if 'Return_6M' in stats.columns:
                # If sample is large enough (e.g. 2000), the Top 50 here are a good proxy for market leaders
                top_50 = stats.sort_values('Return_6M', ascending=False).head(50)
                all_top_winners.append(top_50)

        if not all_metrics:
            return pd.DataFrame(), pd.DataFrame()
            
        # Return tuple: (Distribution Stats, Top Winners)
        winners_df = pd.concat(all_top_winners, ignore_index=True) if all_top_winners else pd.DataFrame()
        return pd.DataFrame(all_metrics), winners_df

    def _calculate_forward_returns(self, candidates: pd.DataFrame, start_date: str) -> pd.DataFrame:
        """
        Computes multi-horizon performance: 3M, 6M, 1Y, MAX.
        """
        start_dt = pd.to_datetime(start_date)
        horizons = {
            '3M': 63,
            '6M': 126,
            '1Y': 252,
            'MAX': 504 
        }
        
        enriched = candidates.copy()
        enriched['snapshot_date'] = start_date
        
        results = []
        
        for idx, row in candidates.iterrows():
            ticker = row['ticker']
            full_df = data_loader.load_ticker_market_data(ticker)
            
            future = full_df[full_df['date'] > start_dt].copy()
            start_price = row['close']
            
            row_metrics = {}
            
            if future.empty:
                for h in horizons:
                    row_metrics[f'Return_{h}'] = 0.0
                    row_metrics[f'MaxDD_{h}'] = 0.0
            else:
                for h_name, days in horizons.items():
                    period_data = future.head(days)
                    if period_data.empty:
                        ret = 0.0
                        dd = 0.0
                    else:
                        end_price = period_data.iloc[-1]['close']
                        ret = (end_price / start_price) - 1
                        
                        prices = pd.concat([pd.Series([start_price]), period_data['close']])
                        rolling_max = prices.cummax()
                        dd_series = (prices - rolling_max) / rolling_max
                        dd = dd_series.min()
                    
                    row_metrics[f'Return_{h_name}'] = ret
                    row_metrics[f'MaxDD_{h_name}'] = dd
            
            results.append(row_metrics)
            
        metrics_df = pd.DataFrame(results)
        result = pd.concat([enriched.reset_index(drop=True), metrics_df], axis=1)
        return result

    def _generate_report(self, df: pd.DataFrame, dates_tested: list, mode: str = "CALENDAR", universe_stats: pd.DataFrame = None, top_winners: pd.DataFrame = None):
        """
        Generates a rich Markdown report with multi-horizon analysis and Universe comparison.
        """
        report_path = self.output_dir / "backtest_report.md"
        
        # Primary Horizon for Summary Stats
        primary_horizon = '6M'
        ret_col = f'Return_{primary_horizon}'
        alpha_col = f'Alpha_{primary_horizon}'
        
        # Summary Stats
        avg_return = df[ret_col].mean()
        win_rate = (df[ret_col] > 0).mean()
        avg_alpha = df[alpha_col].mean()
        alpha_win_rate = (df[alpha_col] > 0).mean()
        
        # Calculate Strategy Distribution
        strat_dist = {}
        for h in ['3M', '6M', '1Y']:
            col = f'Return_{h}'
            strat_dist[f'Strat_{h}_25'] = df[col].quantile(0.25)
            strat_dist[f'Strat_{h}_50'] = df[col].median()
            strat_dist[f'Strat_{h}_75'] = df[col].quantile(0.75)

        # Universe Aggregates
        univ_agg = {}
        if universe_stats is not None and not universe_stats.empty:
            for h in ['3M', '6M', '1Y']:
                univ_agg[f'Univ_{h}_25'] = universe_stats[f'Univ_{h}_25'].mean()
                univ_agg[f'Univ_{h}_50'] = universe_stats[f'Univ_{h}_50'].mean()
                univ_agg[f'Univ_{h}_75'] = universe_stats[f'Univ_{h}_75'].mean()
        
        # IC Analysis
        if len(df) > 2:
            score_corr, p_value = stats.pearsonr(df['raw_score'], df[ret_col])
            ic_significance = "Significant" if p_value < 0.05 else "Not Significant"
        else:
            score_corr, p_value = 0.0, 1.0
            ic_significance = "N/A"
            
        with open(report_path, "w") as f:
            f.write(f"# Strategy Report Card: {self.strategy_name} ({mode})\n")
            f.write(f"**Experiment Tag:** {self.experiment_tag}\n")
            f.write(f"**Benchmark:** {self.benchmark_ticker}\n\n")
            
            f.write("## 1. Executive Summary (6M Horizon)\n")
            f.write(f"* **Total Candidates:** {len(df)}\n")
            f.write(f"* **Dates Sampled:** {len(dates_tested)}\n")
            f.write(f"* **Win Rate:** {win_rate:.1%}\n")
            f.write(f"* **Alpha Win Rate:** {alpha_win_rate:.1%}\n")
            f.write(f"* **Avg Alpha:** {avg_alpha:.2%}\n\n")
            
            f.write("## 2. Distribution Analysis: Strategy vs Universe\n")
            f.write("Comparison of return percentiles (25th, Median, 75th) across horizons.\n")
            
            dist_rows = []
            for h in ['3M', '6M', '1Y']:
                row = {'Horizon': h}
                # Strategy Stats
                row['Strat 25%'] = f"{strat_dist.get(f'Strat_{h}_25', 0):.1%}"
                row['Strat Med'] = f"{strat_dist.get(f'Strat_{h}_50', 0):.1%}"
                row['Strat 75%'] = f"{strat_dist.get(f'Strat_{h}_75', 0):.1%}"
                
                # Universe Stats
                if univ_agg:
                    row['Univ 25%'] = f"{univ_agg.get(f'Univ_{h}_25', 0):.1%}"
                    row['Univ Med'] = f"{univ_agg.get(f'Univ_{h}_50', 0):.1%}"
                    row['Univ 75%'] = f"{univ_agg.get(f'Univ_{h}_75', 0):.1%}"
                    
                    # Comparison: Is Strategy Top 25% better than Univ Top 25%?
                    strat_75 = strat_dist.get(f'Strat_{h}_75', 0)
                    univ_75 = univ_agg.get(f'Univ_{h}_75', 0)
                    row['Top Quartile Alpha'] = f"{strat_75 - univ_75:.1%}"
                
                dist_rows.append(row)
            
            f.write(pd.DataFrame(dist_rows).to_markdown(index=False))
            f.write("\n\n")

            f.write("## 3. Multi-Horizon Performance\n")
            horizon_stats = []
            for h in ['3M', '6M', '1Y', 'MAX']:
                h_ret = df[f'Return_{h}'].mean()
                h_alpha = df[f'Alpha_{h}'].mean()
                h_win = (df[f'Return_{h}'] > 0).mean()
                horizon_stats.append({
                    'Horizon': h,
                    'Avg Return': f"{h_ret:.2%}",
                    'Avg Alpha': f"{h_alpha:.2%}",
                    'Win Rate': f"{h_win:.1%}"
                })
            f.write(pd.DataFrame(horizon_stats).to_markdown(index=False))
            f.write("\n\n")
            
            f.write("## 4. Period Breakdown\n")
            # Count per period
            period_counts = df['snapshot_date'].value_counts().sort_index()
            period_perf = df.groupby('snapshot_date')[[ret_col, alpha_col]].mean()
            period_summary = pd.concat([period_counts, period_perf], axis=1)
            period_summary.columns = ['Count', 'Avg Return (6M)', 'Avg Alpha (6M)']
            
            # Format
            period_summary['Avg Return (6M)'] = period_summary['Avg Return (6M)'].apply(lambda x: f"{x:.1%}")
            period_summary['Avg Alpha (6M)'] = period_summary['Avg Alpha (6M)'].apply(lambda x: f"{x:.1%}")
            
            f.write(period_summary.to_markdown())
            f.write("\n\n")

            f.write("## 5. Predictive Power Analysis (Multi-Horizon)\n")
            f.write("Correlation between Strategy Score and Future Returns (Information Coefficient).\n")
            
            ic_data = []
            for h in ['3M', '6M', '1Y', 'MAX']:
                col = f'Return_{h}'
                if len(df) > 2 and col in df.columns:
                    # Drop NaNs for correlation
                    valid_df = df.dropna(subset=['raw_score', col])
                    if len(valid_df) > 2:
                        corr, p_val = stats.pearsonr(valid_df['raw_score'], valid_df[col])
                        sig = "**Yes**" if p_val < 0.05 else "No"
                    else:
                        corr, p_val, sig = 0.0, 1.0, "N/A"
                else:
                    corr, p_val, sig = 0.0, 1.0, "N/A"
                    
                ic_data.append({
                    'Horizon': h,
                    'IC (Correlation)': f"{corr:.3f}",
                    'P-Value': f"{p_val:.4f}",
                    'Significant?': sig
                })
            
            f.write(pd.DataFrame(ic_data).to_markdown(index=False))
            f.write("\n\n")

            # --- NEW: Component Correlation Analysis ---
            # Find columns ending with '_score' (excluding raw_score if desired, but including it is fine)
            score_cols = [c for c in df.columns if c.endswith('_score') and c != 'raw_score']
            
            if score_cols:
                f.write("### Score Component Correlation (Driver Analysis)\n")
                f.write("Which specific factor drives returns?\n")
                
                comp_corr_data = []
                for sc in score_cols:
                    row = {'Component': sc}
                    for h in ['3M', '6M', '1Y']:
                        col = f'Return_{h}'
                        if col in df.columns:
                            valid_df = df.dropna(subset=[sc, col])
                            if len(valid_df) > 2:
                                corr, _ = stats.pearsonr(valid_df[sc], valid_df[col])
                                row[h] = f"{corr:.3f}"
                            else:
                                row[h] = "N/A"
                        else:
                            row[h] = "N/A"
                    comp_corr_data.append(row)
                
                f.write(pd.DataFrame(comp_corr_data).to_markdown(index=False))
                f.write("\n\n")
            # -------------------------------------------
            
            # Quantile Analysis
            try:
                df['bucket'] = pd.qcut(df['raw_score'], 3, labels=["Bottom 33%", "Middle 33%", "Top 33%"])
                bucket_perf = df.groupby('bucket')[[ret_col, alpha_col]].mean()
                bucket_perf.columns = ['Avg Return', 'Avg Alpha']
                for col in bucket_perf.columns:
                    bucket_perf[col] = bucket_perf[col].apply(lambda x: f"{x:.2%}")
                f.write("### Score Bucket Performance\n")
                f.write(bucket_perf.to_markdown())
                f.write("\n\n")
            except Exception:
                f.write("Insufficient data for quantile analysis.\n\n")
            
            f.write("## 6. Top Winners (Alpha Leaders - 6M)\n")
            cols = ['ticker', 'snapshot_date', 'raw_score', ret_col, alpha_col]
            display_df = df[cols].sort_values(alpha_col, ascending=False).head(10)
            for c in [ret_col, alpha_col]:
                display_df[c] = display_df[c].apply(lambda x: f"{x:.1%}")
            f.write(display_df.to_markdown(index=False))
            f.write("\n\n")

            # --- NEW: Theoretical Ceiling Analysis ---
            f.write("### Theoretical Ceiling (Perfect Selection)\n")
            f.write("If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?\n")
            
            ceiling_data = []
            for h in ['3M', '6M', '1Y']:
                col = f'Return_{h}'
                if col in df.columns:
                    top_10_perf = df.sort_values(col, ascending=False).head(10)[col].mean()
                    ceiling_data.append({'Horizon': h, 'Top 10 Avg Return': f"{top_10_perf:.2%}"})
            
            f.write(pd.DataFrame(ceiling_data).to_markdown(index=False))
            f.write("\n\n")
            
            # --- NEW: Recall Analysis (The Munger Metric) ---
            if top_winners is not None and not top_winners.empty:
                f.write("### Recall Analysis (The Munger Metric)\n")
                f.write(f"Of the Top {len(top_winners)} performers in the Universe Sample, how many did we catch?\n")
                
                # 'top_winners' contains ticker, date, Return_6M
                # 'df' contains our candidates with same columns
                
                # Merge to find intersection
                # We need to match on ticker AND date (approximate match or exact?)
                # Exact match on snapshot_date
                
                # Prepare merge keys
                top_winners['match_key'] = top_winners['ticker'] + "_" + top_winners['date']
                df['match_key'] = df['ticker'] + "_" + df['snapshot_date']
                
                caught_winners = top_winners[top_winners['match_key'].isin(df['match_key'])]
                recall_count = len(caught_winners)
                recall_rate = recall_count / len(top_winners)
                
                f.write(f"* **Recall Rate:** {recall_rate:.1%} ({recall_count}/{len(top_winners)})\n")
                
                if recall_count > 0:
                    f.write("\n#### Caught Winners:\n")
                    disp = caught_winners[['ticker', 'date', 'Return_6M']].copy()
                    disp['Return_6M'] = disp['Return_6M'].apply(lambda x: f"{x:.1%}")
                    f.write(disp.to_markdown(index=False))
                else:
                    f.write("\n*No Top 50 winners were captured by the strategy.*")
            elif universe_stats is not None and not universe_stats.empty:
                 # Fallback to simple bagger count if top_winners not provided but stats are
                f.write("### Recall Analysis (Proxy)\n")
                baggers_3m = len(df[df['Return_3M'] > 0.5])
                baggers_6m = len(df[df['Return_6M'] > 1.0])
                f.write(f"* **>50% Gainers (3M):** {baggers_3m} candidates\n")
                f.write(f"* **>100% Gainers (6M):** {baggers_6m} candidates\n")
            # -------------------------------------------
