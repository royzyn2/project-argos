"""
Report Generator (Standalone)
=============================
Generates or regenerates backtest reports from existing AI results.
Usage: python src/engine/report_generator.py --strategy SURGE --date 2022-11-01
"""

import pandas as pd
import argparse
import os
import numpy as np
from pathlib import Path
from scipy import stats
from datetime import timedelta
from src.utils.logger import setup_logger, logger
from src.engine.data_loader import data_loader

def generate_report_only(strategy_name, snapshot_date):
    logger.info(f"Generating Report for {strategy_name} @ {snapshot_date} from cache...")
    
    report_dir = Path(f"data/reports/{strategy_name}_AI_TEST")
    if not report_dir.exists():
        logger.error(f"No report directory found at {report_dir}")
        return

    ai_results = []
    target_dt = pd.to_datetime(snapshot_date)
    
    # Fuzzy Date Matching (Window of +/- 5 days)
    # This handles cases where the candidate date (e.g., Friday) differs slightly from Snapshot (e.g., Saturday)
    
    for json_file in report_dir.glob("*.json"):
        import json
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
                file_date_str = data.get('date')
                if file_date_str:
                    file_dt = pd.to_datetime(file_date_str)
                    if abs((file_dt - target_dt).days) <= 5:
                        ai_results.append(data)
            except: pass

    if not ai_results:
        logger.error(f"No cached AI results found for date window around {snapshot_date}.")
        return
        
    ai_df = pd.DataFrame(ai_results)
    logger.info(f"Loaded {len(ai_df)} records from cache (fuzzy match).")
    
    # Calculate Returns & Sortino
    results_df = _calculate_returns(ai_df, snapshot_date)
    
    # Generate Report
    _generate_ai_report(results_df, strategy_name, snapshot_date)

def _calculate_returns(ai_df, start_date):
    # Reusing the logic from ai_tester.py + Adding Sortino
    start_dt = pd.to_datetime(start_date)
    horizons = {'3M': 63, '6M': 126, '1Y': 252, 'MAX': 504}
    
    bench_df = data_loader.load_ticker_market_data('SPX')
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
        
        # Get Entry Price
        # Use the *actual* date from the AI result if possible, or the snapshot date
        # to be safe, we use the snapshot date as the "Execution Date"
        history = full_df[full_df['date'] <= start_dt]
        if history.empty: 
            start_price = row.get('price', 0) 
            if start_price == 0: continue
        else:
            start_price = history.iloc[-1]['close']
        
        future = full_df[full_df['date'] > start_dt]
        
        row_res = row.to_dict()
        
        for h, days in horizons.items():
            # Stock Return
            period = future.head(days)
            if period.empty:
                stk_ret = 0.0
                sortino = 0.0
            else:
                end_price = period.iloc[-1]['close']
                stk_ret = (end_price / start_price) - 1
                
                # Calculate Daily Returns for Sortino
                daily_rets = period['close'].pct_change().dropna()
                target_return = 0.0 # or Risk Free Rate / 252
                downside_returns = daily_rets[daily_rets < target_return]
                
                if len(downside_returns) > 0:
                    downside_dev = downside_returns.std() * np.sqrt(252)
                    if downside_dev > 0:
                        annualized_mean_ret = daily_rets.mean() * 252
                        sortino = annualized_mean_ret / downside_dev
                    else:
                        sortino = 0.0 # No downside deviation means infinite Sortino theoretically
                else:
                    sortino = 0.0 # Or some high number if returns are all positive
            
            row_res[f'Return_{h}'] = stk_ret
            row_res[f'Sortino_{h}'] = sortino
            
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
    output_dir = Path(f"experiments/{strategy}/AI_Backtests/{date}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "report.md"
    
    with open(output_file, "w") as f:
        f.write(f"# AI Backtest Report: {strategy}\n")
        f.write(f"**Snapshot Date:** {date}\n")
        f.write(f"**Benchmark:** SPX\n\n")
        
        f.write("## 1. AI Score vs Future Returns (Multi-Horizon)\n")
        
        if 'final_score' in df.columns:
            # Extract numeric score from string if necessary (e.g. "8 - Surge")
            df['final_score'] = df['final_score'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
            df['final_score'] = pd.to_numeric(df['final_score'], errors='coerce').fillna(0)
        
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
        
        # Group Distribution (Mean + Median)
        f.write("## 2. Score Group Analysis (Mean vs Median)\n")
        
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
            sortino_col = f'Sortino_{h}'
            if ret_col in df.columns:
                df[ret_col] = pd.to_numeric(df[ret_col], errors='coerce')
            if sortino_col in df.columns:
                df[sortino_col] = pd.to_numeric(df[sortino_col], errors='coerce')

        horizons_stats = []
        for h in ['3M', '6M', '1Y', 'MAX']:
            ret_col = f'Return_{h}'
            sortino_col = f'Sortino_{h}'
            
            if ret_col in df.columns:
                # Calculate Mean and Median
                grp = df.groupby('Score_Group')
                
                # Aggregation dictionary
                agg_dict = {ret_col: ['mean', 'median']}
                if sortino_col in df.columns:
                    agg_dict[sortino_col] = 'mean' # Average Sortino of the group
                
                group_stats = grp.agg(agg_dict)
                
                # Rename columns
                new_cols = [f'Avg {h}', f'Med {h}']
                if sortino_col in df.columns:
                    new_cols.append(f'Sortino {h}')
                
                group_stats.columns = new_cols
                horizons_stats.append(group_stats)
        
        if horizons_stats:
            combined_stats = pd.concat(horizons_stats, axis=1)
            
            # Format columns
            for col in combined_stats.columns:
                if 'Sortino' in col:
                     combined_stats[col] = combined_stats[col].apply(lambda x: f"{x:.2f}")
                else:
                     combined_stats[col] = combined_stats[col].apply(lambda x: f"{x:.1%}")
            
            f.write(combined_stats.to_markdown())
        else:
            f.write("Insufficient data for group analysis.")
        f.write("\n\n")

        # Recall Analysis
        f.write("## 3. Recall Analysis (Within Candidates)\n")
        if 'Alpha_6M' in df.columns:
            top_performers = df.sort_values('Alpha_6M', ascending=False).head(5)
            f.write("**Top 5 Alpha Generators:**\n")
            disp_top = top_performers[['ticker', 'final_score', 'verdict', 'Alpha_6M']].copy()
            disp_top['Alpha_6M'] = disp_top['Alpha_6M'].apply(lambda x: f"{x:.1%}")
            f.write(disp_top.to_markdown(index=False))
        f.write("\n\n")

        # Correlation
        f.write("## 4. Correlation Matrix (IC)\n")
        ic_rows = []
        for h in ['3M', '6M', '1Y', 'MAX']:
            col = f'Alpha_{h}'
            if col in df.columns and len(df) > 2:
                valid = df.dropna(subset=['final_score', col])
                if len(valid) > 2:
                    # stats is already imported from scipy
                    corr, p = stats.pearsonr(valid['final_score'], valid[col])
                    sig = "**Yes**" if p < 0.05 else "No"
                    ic_rows.append({'Horizon': h, 'IC (vs Alpha)': f"{corr:.3f}", 'P-Value': f"{p:.3f}", 'Significant': sig})
        
        if ic_rows:
            f.write(pd.DataFrame(ic_rows).to_markdown(index=False))
        f.write("\n")

    logger.info(f"Report regenerated: {output_file}")

if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    
    generate_report_only(args.strategy, args.date)
