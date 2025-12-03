import argparse
import sys
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import logger
from src.engine.data_loader import data_loader
from src.engine.backtester import Backtester, STRATEGY_REGISTRY, MODE_CALENDAR, MODE_EVENT
from src.strategies.compounder import AggressiveCompounder
from src.engine.metadata_builder import build_metadata
from src.engine.production_runner import run_production
from src.engine.data_updater import DataUpdater

def run_strategy_scan(strategy_name: str):
    """
    Runs the specified strategy against all available tickers.
    """
    logger.info(f"Initializing Strategy: {strategy_name}")
    
    # Strategy Factory
    if strategy_name in STRATEGY_REGISTRY:
        strategy = STRATEGY_REGISTRY[strategy_name]()
    else:
        logger.error(f"Unknown strategy: {strategy_name}. Available: {list(STRATEGY_REGISTRY.keys())}")
        return

    # Get list of tickers
    market_dir = Path("data/market_data")
    files = list(market_dir.glob("*.parquet"))
    tickers = [f.stem for f in files]
    
    logger.info(f"Scanning {len(tickers)} tickers...")
    
    results = []
    
    for ticker in tqdm(tickers):
        try:
            # 1. Load Data (Merged PIT)
            df = data_loader.load_merged_data(ticker)
            if df.empty:
                continue
                
            # 2. Run Strategy via Standard Interface
            result_df = strategy.run(df)
            if not result_df.empty:
                results.append(result_df)
                
        except Exception as e:
            # logger.error(f"Error processing {ticker}: {e}")
            continue
            
    # 3. Save Aggregated Results
    if results:
        final_df = pd.concat(results, ignore_index=True)
        # Sort by score
        final_df.sort_values('raw_score', ascending=False, inplace=True)
        
        strategy.save_results(final_df)
        
        logger.info(f"Scan Complete. Found {len(final_df)} candidates.")
        
        # Display Top 10
        print("\n--- TOP 10 CANDIDATES ---")
        # Handle optional columns safely for display
        disp_cols = ['ticker', 'date', 'raw_score']
        if 'primary_metric' in final_df.columns: disp_cols.append('primary_metric')
        if 'secondary_metric' in final_df.columns: disp_cols.append('secondary_metric')
        
        print(final_df[disp_cols].head(10).to_string(index=False))
    else:
        logger.info("Scan Complete. No candidates found.")

def main():
    """
    Main entry point for Project Argos.
    """
    parser = argparse.ArgumentParser(description="Project Argos - Quant Factory CLI")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command: Run Strategy
    run_parser = subparsers.add_parser('run_strategy', help='Run a specific strategy')
    run_parser.add_argument('--name', type=str, required=True, help='Name of the strategy class (e.g., Aggressive_Compounder)')
    
    # Command: Update Data
    data_parser = subparsers.add_parser('update_data', help='Update market and fundamental data')
    data_parser.add_argument('--mode', type=str, choices=['market', 'fundamental', 'meta', 'repair'], default='market', help='Update mode')
    
    # Command: Backtest
    backtest_parser = subparsers.add_parser('backtest', help='Run backtest on strategy results')
    backtest_parser.add_argument('--strategy', type=str, required=True, help='Strategy name')
    backtest_parser.add_argument('--tag', type=str, required=True, help='Experiment tag for versioning')
    backtest_parser.add_argument('--samples', type=int, default=5, help='Number of random dates to test (Calendar Mode)')
    backtest_parser.add_argument('--mode', type=str, choices=['CALENDAR', 'STRESS', 'EVENT', 'EVENT_LITE'], default='CALENDAR', help='Backtest Mode')

    # Command: Production
    prod_parser = subparsers.add_parser('production', help='Run Production Pipeline (Phase 5)')
    prod_parser.add_argument('--strategy', type=str, required=True, help='Strategy name')
    prod_parser.add_argument('--mode', type=str, choices=['LATEST', 'DATE'], default='LATEST', help='Run mode: LATEST (most recent data) or DATE (specific date)')
    prod_parser.add_argument('--date', type=str, help='Specific date (YYYY-MM-DD) if mode is DATE')
    prod_parser.add_argument('--top_n', type=int, default=10000, help='Max candidates to process')

    args = parser.parse_args()
    
    if args.command == 'run_strategy':
        run_strategy_scan(args.name)
        
    elif args.command == 'update_data':
        logger.info(f"Updating data modules (Mode: {args.mode})...")
        updater = DataUpdater()
        if args.mode == 'market':
            updater.update_market_data()
        elif args.mode == 'fundamental':
            updater.update_financials()
        elif args.mode == 'meta':
            updater.update_metadata()
        elif args.mode == 'repair':
            updater.repair_financials()
        
    elif args.command == 'backtest':
        logger.info(f"Starting {args.mode} backtest for {args.strategy} with tag {args.tag}")
        
        tester = Backtester(args.strategy, args.tag)
        
        if args.mode == 'CALENDAR':
            tester.run_calendar_test(n_samples=args.samples)
        elif args.mode == 'STRESS':
            tester.run_stress_test()
        elif args.mode == 'EVENT':
            tester.run_protocol_c()
        elif args.mode == 'EVENT_LITE':
            tester.run_protocol_c2()

    elif args.command == 'production':
        target_date = args.date
        if args.mode == 'LATEST':
            # Find the latest available date in market data to ensure alignment
            market_dir = Path("data/market_data")
            files = list(market_dir.glob("*.parquet"))
            if files:
                latest_date = None
                for f in files[:10]: # Sample check
                    try:
                        df = pd.read_parquet(f)
                        d = pd.to_datetime(df['date'].iloc[-1])
                        if latest_date is None or d > latest_date:
                            latest_date = d
                    except: pass
                
                if latest_date:
                    target_date = latest_date.strftime('%Y-%m-%d')
                    logger.info(f"Auto-detected latest market date: {target_date}")
                else:
                    target_date = datetime.today().strftime('%Y-%m-%d')
            else:
                target_date = datetime.today().strftime('%Y-%m-%d')
        
        if not target_date:
            logger.error("Target date is required if not using LATEST mode.")
            return

        run_production(args.strategy, target_date, args.top_n)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
