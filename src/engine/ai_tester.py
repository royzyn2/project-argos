"""
AI Backtester (Standardized Protocol)
=====================================
Standardized process for testing Phase 4 (AI Analysis).
1. Picks a past date (Time Travel).
2. Runs Quant Strategy to get candidates.
3. Builds Data Warehouse (Real Financials + Mock Text).
4. Runs AI Analysis (Real LLM Call).
5. Calculates Forward Returns.
6. Generates Correlation Report.
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

def run_ai_backtest(strategy_name: str, snapshot_date: str, top_n: int = 1000):
    logger.info(f"--- Starting AI Backtest: {strategy_name} @ {snapshot_date} ---")
    
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
            
            # Time Travel Slice
            mask = df['date'] <= target_date
            historical_df = df[mask].copy()
            
            if historical_df.empty: continue
            
            # Check delisting/stale data
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
    
    # Filter Top N (Dynamically set to full length if high limit provided)
    if 'raw_score' in candidates_df.columns:
        # If top_n is very high (like 1000), just take all.
        candidates_df = candidates_df.sort_values('raw_score', ascending=False).head(top_n)
    else:
        candidates_df = candidates_df.head(top_n)
        
    logger.info(f"Selected Top {len(candidates_df)} for AI Analysis.")
    
    # Save temporary CSV for Warehouse/LLM Runner to consume
    temp_csv_path = Path(f"data/results/{strategy_name}_AI_TEST.csv")
    # Ensure directory exists
    temp_csv_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_df.to_csv(temp_csv_path, index=False)
    
    # 2. Build Warehouse (ETL Layer)
    logger.info("Building Data Warehouse (Real Financials)...")
    builder = WarehouseBuilder()
    logger.info(f"Fetching Context for {strategy_name}_AI_TEST (FMP API)...")
    builder.run(strategy_name=f"{strategy_name}_AI_TEST")
    logger.info("Warehouse Build Complete.")
    
    # 3. Run AI Analysis (Intelligence Layer)
    logger.info("Running AI Analysis (Gemini)...")
    runner = LLMRunner()
    runner.run() # This will process _AI_TEST.csv
    logger.info("AI Analysis Complete.")
    
    # 4. Collect AI Results & Calculate Returns
    logger.info("Calculating Performance...")
    
    report_dir = Path(f"data/reports/{strategy_name}_AI_TEST")
    
    ai_results = []
    if report_dir.exists():
        for json_file in report_dir.glob("*.json"):
            import json
            with open(json_file, "r") as f:
                try:
                    data = json.load(f)
                    # Filter for only this date's results if multiple exist in folder
                    if data.get('date') == snapshot_date:
                         ai_results.append(data)
                except: pass

    if not ai_results:
        logger.error("No AI reports generated for this date.")
        return
        
    ai_df = pd.DataFrame(ai_results)
    
    # Calculate Forward Returns & Alpha
    results_df = _calculate_returns(ai_df, snapshot_date)
    
    # 5. Generate Report
    _generate_ai_report(results_df, strategy_name, snapshot_date)

def _calculate_returns(ai_df, start_date):
    # Simplified version of Backtester._calculate_forward_returns
    start_dt = pd.to_datetime(start_date)
    horizons = {'3M': 63, '6M': 126, '1Y': 252, 'MAX': 504}
    
    # Load Benchmark Data (SPX)
    bench_df = data_loader.load_ticker_market_data('SPX') # Ensure SPX data exists
    bench_start_price = 1.0
    bench_future = pd.DataFrame()
    
    if not bench_df.empty:
         history = bench_df[bench_df['date'] <= start_dt]
         if not history.empty:
             bench_start_price = history.iloc[-1]['close']
             bench_future = bench_df[bench_df['date'] > start_dt]

    results = []
    
    for _, row in ai_df.iterrows():
        ticker = row['ticker']
        full_df = data_loader.load_ticker_market_data(ticker)
        
        # Get Entry Price (Close on snapshot date)
        history = full_df[full_df['date'] <= start_dt]
        if history.empty: continue
        start_price = history.iloc[-1]['close']
        
        future = full_df[full_df['date'] > start_dt]
        
        row_res = row.to_dict()
        
        for h, days in horizons.items():
            # Stock Return
            period = future.head(days)
            if period.empty:
                stk_ret = 0.0
            else:
                end_price = period.iloc[-1]['close']
                stk_ret = (end_price / start_price) - 1
            
            row_res[f'Return_{h}'] = stk_ret
            
            # Benchmark Return
            if not bench_future.empty:
                bench_period = bench_future.head(days)
                if bench_period.empty:
                    bench_ret = 0.0
                else:
                    bench_end = bench_period.iloc[-1]['close']
                    bench_ret = (bench_end / bench_start_price) - 1
            else:
                bench_ret = 0.0
                
            row_res[f'Benchmark_{h}'] = bench_ret
            row_res[f'Alpha_{h}'] = stk_ret - bench_ret
                
        results.append(row_res)
        
    return pd.DataFrame(results)

def _generate_ai_report(df, strategy, date):
    # Create a dedicated 'v11_ai_validation' folder to keep reports organized
    # instead of cluttering the main experiment folder.
    # Or stick to the user's request: "AI backtests should also have a new properlly named folder"
    # Let's use: experiments/{strategy}/AI_Backtests/{date}/report.md
    
    output_dir = Path(f"experiments/{strategy}/AI_Backtests/{date}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "report.md"
    
    with open(output_file, "w") as f:
        f.write(f"# AI Backtest Report: {strategy}\n")
        f.write(f"**Snapshot Date:** {date}\n")
        f.write(f"**Benchmark:** SPX\n\n")
        
        f.write("## 1. AI Score vs Future Returns (Multi-Horizon)\n")
        
        # Robust type conversion for final_score
        if 'final_score' in df.columns:
            # Extract numeric score from string if necessary (e.g. "8 - Surge")
            df['final_score'] = df['final_score'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
            df['final_score'] = pd.to_numeric(df['final_score'], errors='coerce').fillna(0)
        
        # Dynamic column selection for all horizons
        disp_cols = ['ticker', 'final_score', 'verdict']
        horizon_cols = []
        for h in ['3M', '6M', '1Y', 'MAX']:
            if f'Return_{h}' in df.columns:
                horizon_cols.append(f'Return_{h}')
        
        final_cols = disp_cols + horizon_cols
        
        if horizon_cols:
            disp = df[final_cols].sort_values('final_score', ascending=False)
            for c in horizon_cols:
                disp[c] = disp[c].apply(lambda x: f"{x:.1%}")
            f.write(disp.to_markdown(index=False))
        else:
            f.write("Return data not available.")
        f.write("\n\n")
        
        # Group Distribution
        f.write("## 2. Score Group Analysis (6M Horizon)\n")
        
        def get_bucket(score):
            try:
                s = float(score)
                if s >= 8.0: return "High (>8)"
                if s >= 5.0: return "Med (5-8)"
                return "Low (<5)"
            except: return "N/A"
            
        df['Score_Group'] = df['final_score'].apply(get_bucket)
        
        # Ensure numeric
        for h in ['3M', '6M', '1Y', 'MAX']:
            ret_col = f'Return_{h}'
            alpha_col = f'Alpha_{h}'
            if ret_col in df.columns and alpha_col in df.columns:
                df[ret_col] = pd.to_numeric(df[ret_col], errors='coerce')
                df[alpha_col] = pd.to_numeric(df[alpha_col], errors='coerce')

        # Multi-horizon stats
        horizons_stats = []
        for h in ['3M', '6M', '1Y', 'MAX']:
            ret_col = f'Return_{h}'
            if ret_col in df.columns:
                # Calculate Mean and Median
                grp = df.groupby('Score_Group')[ret_col]
                stats = grp.agg(['mean', 'median'])
                stats.columns = [f'Avg {h}', f'Med {h}']
                horizons_stats.append(stats)
        
        if horizons_stats:
            combined_stats = pd.concat(horizons_stats, axis=1)
            # Format
            for col in combined_stats.columns:
                combined_stats[col] = combined_stats[col].apply(lambda x: f"{x:.1%}")
            
            f.write(combined_stats.to_markdown())
        else:
            f.write("Insufficient data for group analysis.")
        f.write("\n\n")

        # Recall Analysis (Within Candidates)
        f.write("## 3. Recall Analysis (Within Candidates)\n")
        f.write("Did the AI correctly identify the best performers in this batch?\n")
        
        if 'Alpha_6M' in df.columns:
            top_performers = df.sort_values('Alpha_6M', ascending=False).head(5)
            f.write("**Top 5 Alpha Generators:**\n")
            disp_top = top_performers[['ticker', 'final_score', 'verdict', 'Alpha_6M']].copy()
            disp_top['Alpha_6M'] = disp_top['Alpha_6M'].apply(lambda x: f"{x:.1%}")
            f.write(disp_top.to_markdown(index=False))
        f.write("\n\n")

        # Correlation
        f.write("## 4. Correlation Matrix (IC)\n")
        from scipy import stats
        
        ic_rows = []
        for h in ['3M', '6M', '1Y', 'MAX']:
            col = f'Alpha_{h}' # Correlation with Alpha is more meaningful
            if col in df.columns and len(df) > 2:
                valid = df.dropna(subset=['final_score', col])
                if len(valid) > 2:
                    corr, p = stats.pearsonr(valid['final_score'], valid[col])
                    sig = "**Yes**" if p < 0.05 else "No"
                    ic_rows.append({'Horizon': h, 'IC (vs Alpha)': f"{corr:.3f}", 'P-Value': f"{p:.3f}", 'Significant': sig})
        
        if ic_rows:
            f.write(pd.DataFrame(ic_rows).to_markdown(index=False))
        else:
            f.write("Insufficient data for correlation analysis.")
        f.write("\n")

    logger.info(f"AI Backtest Report saved to {output_file}")

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--top_n", type=int, default=10)
    args = parser.parse_args()
    
    run_ai_backtest(args.strategy, args.date, args.top_n)
