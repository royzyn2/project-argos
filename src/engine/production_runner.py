"""
Production Runner
=================
Executes the Project Argos pipeline for a Production run (Phase 5).

1. Quant Scan: Runs specified strategy on latest data (or target date) to get candidates.
   - Defaults to fetching ALL candidates (no top_n limit).
2. Data Warehouse: Builds rich context (Real Financials + Metadata) for candidates.
3. AI Analysis: Runs Gemini on the candidates.
4. Reporting: Generates the Daily Briefing.

Usage:
  python src/engine/production_runner.py --strategy Aggressive_Compounder --date 2025-11-19
"""

import argparse
import pandas as pd
import shutil
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import setup_logger, logger
from src.engine.data_loader import data_loader
from src.engine.backtester import STRATEGY_REGISTRY
from src.engine.warehouse_builder import WarehouseBuilder
from src.analysis.llm_runner import LLMRunner
from src.analysis.briefing_gen import BriefingGenerator

def run_production(strategy_name: str, date: str, top_n: int):
    logger.info(f"--- Starting PRODUCTION RUN: {strategy_name} @ {date} ---")

    # 1. Quant Scan
    if strategy_name not in STRATEGY_REGISTRY:
        logger.error(f"Strategy {strategy_name} not found.")
        return

    strategy = STRATEGY_REGISTRY[strategy_name]()
    target_date = pd.to_datetime(date)

    logger.info("Scanning universe for candidates...")
    market_dir = Path("data/market_data")
    files = list(market_dir.glob("*.parquet"))
    
    candidates = []
    for file_path in files:
        try:
            ticker = file_path.stem
            df = data_loader.load_merged_data(ticker)
            if df.empty: continue
            
            mask = df['date'] <= target_date
            historical_df = df[mask].copy()
            
            if historical_df.empty: continue
            
            # Check staleness (production data must be recent)
            last_dt = historical_df['date'].iloc[-1]
            if (target_date - last_dt).days > 10: 
                # In production, we might be stricter, or laxer if data isn't updating daily. 
                # Let's keep the 10 day check.
                continue
            
            result_row = strategy.run(historical_df)
            if not result_row.empty:
                candidates.append(result_row)
        except Exception:
            continue
            
    if not candidates:
        logger.error("No candidates found.")
        return

    candidates_df = pd.concat(candidates, ignore_index=True)
    logger.info(f"Found {len(candidates_df)} candidates.")
    
    # Filter Top N (Default is effectively infinite)
    if 'raw_score' in candidates_df.columns:
         candidates_df = candidates_df.sort_values('raw_score', ascending=False).head(top_n)
    else:
         candidates_df = candidates_df.head(top_n)
         
    logger.info(f"Selected {len(candidates_df)} for AI Analysis.")
    
    # Define Production Strategy Name
    prod_strategy_name = f"{strategy_name}_PRODUCTION"
    
    # Save Candidates
    temp_csv_path = Path(f"data/results/{prod_strategy_name}.csv")
    temp_csv_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_df.to_csv(temp_csv_path, index=False)
    
    # 2. Warehouse
    logger.info("Building Data Warehouse...")
    builder = WarehouseBuilder()
    builder.run(strategy_name=prod_strategy_name)
    
    # 3. AI Analysis
    logger.info("Running AI Analysis...")
    
    # Ensure Prompt Exists (Logic Handled by LLMRunner via suffix check)
    runner = LLMRunner()
    # Run ONLY for this production strategy
    runner.run(target_strategy=prod_strategy_name)
    
    # 4. Briefing
    logger.info("Generating Daily Briefing...")
    gen = BriefingGenerator()
    gen.run(target_date=date, strategy_name=prod_strategy_name)
    
    logger.info("--- PRODUCTION RUN COMPLETE ---")

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--top_n", type=int, default=10000, help="Max candidates (default: 10000)")
    args = parser.parse_args()
    
    run_production(args.strategy, args.date, args.top_n)

