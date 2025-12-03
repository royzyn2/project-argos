
import pandas as pd
import argparse
import os
from pathlib import Path
from src.utils.logger import setup_logger, logger
from src.engine.warehouse_builder import WarehouseBuilder
from src.analysis.llm_runner import LLMRunner

def run_single_ticker_ai(strategy_name, ticker, date_str):
    logger.info(f"--- Running Single Ticker AI Analysis: {ticker} @ {date_str} ---")
    
    # 1. Create a dummy result CSV for the WarehouseBuilder and LLMRunner to consume
    # This mimics the output of the quantitative strategy phase
    results_dir = Path("data/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Use the standard _AI_TEST suffix which LLMRunner already knows how to handle
    # LLMRunner logic: if "_AI_TEST" in strategy_name: original_strat = strategy_name.replace("_AI_TEST", "")
    csv_filename = f"{strategy_name}_AI_TEST.csv" 
    csv_path = results_dir / csv_filename
    
    df = pd.DataFrame([{
        'ticker': ticker,
        'date': date_str,
        'raw_score': 99, # Mock score to ensure it's processed
        'final_score': 99
    }])
    
    df.to_csv(csv_path, index=False)
    logger.info(f"Created temporary input file: {csv_path}")

    # 2. Build Warehouse (ETL)
    # The WarehouseBuilder reads all CSVs in data/results.
    logger.info("Building Data Warehouse...")
    builder = WarehouseBuilder()
    builder.run() # This will process all strategies found in results

    # 3. Run AI Analysis (LLM)
    logger.info("Running AI Analysis...")
    runner = LLMRunner()
    runner.run()

    # 4. Retrieve and Print Result
    # The output folder will be based on the CSV filename (stem)
    output_folder = f"{strategy_name}_AI_TEST"
    report_path = Path(f"data/reports/{output_folder}/{ticker}_{date_str}.json")
    
    if report_path.exists():
        logger.info(f"\n\n--- Analysis Result for {ticker} ---")
        with open(report_path, 'r') as f:
            print(f.read())
    else:
        logger.error(f"Report not generated at {report_path}")

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    
    run_single_ticker_ai(args.strategy, args.ticker, args.date)
