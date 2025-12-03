"""
AI Production Runner (Protocol E - Live Mode)
=============================================
Dedicated engine for running the AI Analysis phase in a production context.
Unlike ai_tester.py, this script:
1. Does NOT calculate future returns (no look-ahead).
2. Processes the FULL candidate list (no top_n limit).
3. Focuses purely on generating the Daily Briefing.

Usage:
    python src/engine/ai_production_runner.py --strategy Aggressive_Compounder --date 2025-11-19
"""

import pandas as pd
import argparse
import os
from pathlib import Path
from src.utils.logger import setup_logger, logger
from src.engine.data_loader import data_loader
from src.engine.backtester import Backtester, STRATEGY_REGISTRY
from src.engine.warehouse_builder import WarehouseBuilder
from src.analysis.llm_runner import LLMRunner
from src.analysis.briefing_gen import BriefingGenerator

def run_production_cycle(strategy_name: str, snapshot_date: str):
    logger.info(f"--- Starting AI Production Cycle: {strategy_name} @ {snapshot_date} ---")
    
    # 1. Get Candidates (Quant Layer)
    if strategy_name not in STRATEGY_REGISTRY:
        logger.error(f"Strategy {strategy_name} not found.")
        return

    strategy = STRATEGY_REGISTRY[strategy_name]()
    
    logger.info("Scanning universe for candidates...")
    market_dir = Path("data/market_data")
    files = list(market_dir.glob("*.parquet"))
    
    candidates = []
    target_date = pd.to_datetime(snapshot_date)
    
    # Scan Loop
    for file_path in files:
        try:
            ticker = file_path.stem
            # Load PIT Data
            df = data_loader.load_merged_data(ticker)
            if df.empty: continue
            
            # Time Travel Slice (Strictly up to today)
            mask = df['date'] <= target_date
            historical_df = df[mask].copy()
            
            if historical_df.empty: continue
            
            # Check data recency
            last_dt = historical_df['date'].iloc[-1]
            if (target_date - last_dt).days > 10: continue
            
            # Run Strategy
            result_row = strategy.run(historical_df)
            if not result_row.empty:
                candidates.append(result_row)
                
        except Exception:
            continue
            
    if not candidates:
        logger.error("No candidates found for this date.")
        return

    candidates_df = pd.concat(candidates, ignore_index=True)
    logger.info(f"Found {len(candidates_df)} candidates.")
    
    # NO TRUNCATION - Process ALL candidates
    # Sort by raw_score just for orderly processing
    if 'raw_score' in candidates_df.columns:
        candidates_df = candidates_df.sort_values('raw_score', ascending=False)
        
    logger.info(f"Selected ALL {len(candidates_df)} candidates for AI Analysis.")
    
    # Save temporary CSV for Warehouse/LLM Runner to consume
    # Using a distinct suffix to avoid confusion with test runs
    run_id = f"{strategy_name}_AI_PROD"
    temp_csv_path = Path(f"data/results/{run_id}.csv")
    temp_csv_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_df.to_csv(temp_csv_path, index=False)
    
    # 2. Build Warehouse (ETL Layer)
    logger.info("Building Data Warehouse (Real Financials)...")
    builder = WarehouseBuilder()
    logger.info(f"Fetching Context for {run_id} (FMP API)...")
    # WarehouseBuilder now defaults to processing ALL candidates in the CSV
    builder.run(strategy_name=run_id)
    logger.info("Warehouse Build Complete.")
    
    # 3. Run AI Analysis (Intelligence Layer)
    logger.info("Running AI Analysis (Gemini)...")
    runner = LLMRunner()
    # LLMRunner now defaults to processing ALL candidates in the CSV
    runner.run() 
    logger.info("AI Analysis Complete.")
    
    # 4. Generate Briefing (Delivery Layer)
    logger.info("Generating Daily Briefing...")
    gen = BriefingGenerator()
    # Pass the run_id so it filters for this specific production run
    gen.run(target_date=snapshot_date, strategy_name=run_id)
    logger.info("Production Cycle Complete.")

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    
    run_production_cycle(args.strategy, args.date)

