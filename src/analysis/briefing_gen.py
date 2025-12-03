"""
Briefing Generator (The Daily Report)
=====================================
Aggregates scattered JSON AI reports into a coherent Markdown briefing.

Logic:
1. Scans data/reports/ for fresh JSONs.
2. Summarizes AI sentiment (Bullish/Bearish).
3. Ranks top picks.
4. Generates a Markdown report in output/daily_briefings/ formatted according to Project Argos Manual Part C.
"""

import os
import json
import pandas as pd
import re
from pathlib import Path
from datetime import datetime
from src.utils.logger import logger

class BriefingGenerator:
    def __init__(self):
        self.reports_dir = Path("data/reports")
        self.warehouse_dir = Path("data/warehouse")
        # Changed output directory structure per user request
        self.output_dir = Path("output/production_results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_sector(self, ticker: str, date: str) -> str:
        """
        Attempts to retrieve the sector from the warehouse context file.
        """
        # Try specific date context first
        context_path = self.warehouse_dir / ticker / f"{date}_context.json"
        if context_path.exists():
            try:
                with open(context_path, 'r') as f:
                    data = json.load(f)
                    return data.get('sector', 'Unknown')
            except:
                pass
        
        # Fallback: Try finding ANY context file
        ticker_dir = self.warehouse_dir / ticker
        if ticker_dir.exists():
            for f in ticker_dir.glob("*_context.json"):
                try:
                    with open(f, 'r') as json_f:
                        data = json.load(json_f)
                        if 'sector' in data:
                            return data['sector']
                except:
                    continue
                    
        return "Unknown"

    def run(self, target_date: str = None, strategy_name: str = None):
        logger.info("Generating Production Results Report...")
        
        # Default to today if no date provided
        if not target_date:
            target_date = datetime.now().strftime("%Y-%m-%d")
            
        # Collect all reports for the specific date
        all_reports = []
        
        strategies = [d for d in self.reports_dir.iterdir() if d.is_dir()]
        
        for strat_dir in strategies:
            # STRICT FILTER: If strategy_name is provided (e.g. Aggressive_Compounder), 
            # ONLY look into that specific folder (or folders starting with it).
            if strategy_name and strategy_name not in strat_dir.name:
                continue
                
            for json_file in strat_dir.glob("*.json"):
                try:
                    with open(json_file, "r") as f:
                        report = json.load(f)
                        # Filter for the target date
                        if report.get('date') == target_date:
                            all_reports.append(report)
                except Exception as e:
                    logger.error(f"Error reading {json_file}: {e}")
        
        if not all_reports:
            logger.warning(f"No reports found for {target_date} to generate briefing.")
            return
            
        df = pd.DataFrame(all_reports)
        
        # Enrich with Sector Data
        df['sector'] = df['ticker'].apply(lambda t: self._get_sector(t, target_date))
        
        # Robust type conversion for final_score
        if 'final_score' in df.columns:
            # Extract numeric score from string if necessary (e.g. "8 - Surge")
            df['final_score'] = df['final_score'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
            df['final_score'] = pd.to_numeric(df['final_score'], errors='coerce').fillna(0)
        
        # Determine final Strategy Name for filename/folder
        # If filtered by strategy, use that. If mixed (shouldn't happen in new flow), use "Combined".
        final_strat_name = strategy_name if strategy_name else "Combined"
        
        # Create Strategy-Specific Output Directory
        strat_output_dir = self.output_dir / final_strat_name
        strat_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Filename: {Strategy}_Production_Run_{Date}.md
        filename = strat_output_dir / f"{final_strat_name}_Production_Run_{target_date}.md"
        
        with open(filename, "w") as f:
            # --- HEADER ---
            f.write(f"# Production Results: {final_strat_name}\n")
            f.write(f"**Date:** {target_date}\n\n")
            
            # --- PART A: MARKET上帝视角 (The Meta-Dashboard) ---
            f.write("## Part A: Market Pulse (The Meta-Dashboard)\n")
            
            # 0. Coverage Stats
            f.write("### 1. Coverage Statistics\n")
            f.write(f"* **Total Companies Analyzed:** {len(df)}\n")
            
            # Sector Breakdown
            if 'sector' in df.columns:
                sector_counts = df['sector'].value_counts()
                f.write("\n**Sector Distribution:**\n")
                for sector, count in sector_counts.items():
                    pct = count / len(df)
                    f.write(f"* **{sector}:** {count} ({pct:.1%})\n")
            f.write("\n")
            
            # 1. Opportunity Spread (Score Distribution)
            f.write("### 2. Opportunity Spread\n")
            if 'final_score' in df.columns:
                scores = df['final_score']
                f.write(f"* **Average Score:** {scores.mean():.1f}/10\n")
                f.write(f"* **Score > 8 (High Conviction):** {(scores >= 8).sum()}\n")
                f.write(f"* **Score < 4 (Avoid):** {(scores <= 3).sum()}\n\n")
            
            # 2. Sentiment (Bullish/Bearish)
            if 'verdict' in df.columns:
                sentiment = df['verdict'].value_counts(normalize=True)
                bullish = sentiment.get('BUY', 0) + sentiment.get('STRONG_BUY', 0)
                f.write(f"### 3. AI Sentiment\n")
                f.write(f"* **Bullish (Buy/Strong Buy):** {bullish:.1%}\n")
                f.write(f"* **Neutral/Bearish:** {1 - bullish:.1%}\n\n")
            
            # --- PART B: 精英榜单 (The Ranked Menu) ---
            f.write("## Part B: The Elite List (Ranked Menu)\n")
            
            for strat in df['strategy'].unique():
                strat_df = df[df['strategy'] == strat].sort_values('final_score', ascending=False)
                
                # Filter for top scores only (e.g. > 6) to keep the menu "Elite"
                elite_df = strat_df[strat_df['final_score'] >= 6]
                
                if elite_df.empty:
                    f.write(f"### 【{strat}】 (No Elite Candidates Found)\n\n")
                    continue
                
                f.write(f"### 【{strat} Selection】\n")
                
                # Prepare table
                table_data = []
                for i, (_, row) in enumerate(elite_df.iterrows(), 1):
                    # One-Liner Extraction
                    one_liner = "N/A"
                    if 'analysis' in row and isinstance(row['analysis'], str):
                        # Take first sentence or first 100 chars
                        one_liner = row['analysis'].split('.')[0] + "."
                    elif 'one_liner' in row and isinstance(row['one_liner'], str):
                         one_liner = row['one_liner']
                    
                    table_data.append({
                        "Rank": i,
                        "Ticker": f"**{row['ticker']}**",
                        "Score": f"**{row.get('final_score', 0)}**",
                        "Verdict": row.get('verdict', 'N/A'),
                        "Sector": row.get('sector', 'N/A'),
                        "AI Commentary": one_liner
                    })
                
                f.write(pd.DataFrame(table_data).to_markdown(index=False))
                f.write("\n\n")
            
            # --- PART C: 深度研报 (The Deep Dives) ---
            f.write("## Part C: Deep Dives\n")
            
            # Group by strategy again
            for strat in df['strategy'].unique():
                strat_df = df[df['strategy'] == strat].sort_values('final_score', ascending=False)
                
                # Logic Change: Iterate through ALL candidates processed
                deep_dive_candidates = strat_df[strat_df['final_score'] > 0]
                
                if deep_dive_candidates.empty:
                    continue
                    
                for _, row in deep_dive_candidates.iterrows():
                    ticker = row['ticker']
                    verdict = row.get('verdict', 'N/A')
                    score = row.get('final_score', 'N/A')
                    sector = row.get('sector', 'N/A')
                    
                    f.write(f"### 🟢 {ticker} ({verdict}) - Score: {score}/10\n")
                    f.write(f"**Sector:** {sector}\n\n")
                    
                    # 1. Core Business
                    if 'coreBusinessModel' in row:
                        f.write(f"**Core Business:** {row['coreBusinessModel']}\n\n")
                    elif 'business_overview' in row:
                        f.write(f"**Core Business:** {row['business_overview']}\n\n")
                    
                    # 2. Moat Analysis
                    if 'moatAnalysis' in row:
                        moat = row['moatAnalysis']
                        if isinstance(moat, dict):
                            f.write(f"**🛡️ Moat Analysis ({moat.get('score', 'N/A')}/10):**\n")
                            f.write(f"{moat.get('verdict', 'N/A')}\n\n")
                    elif 'fundamental_analysis' in row:
                        # Mapping for new SURGE schema
                        fa = row['fundamental_analysis']
                        if isinstance(fa, dict):
                             f.write(f"**🛡️ Competitive Advantage:** {fa.get('competitive_advantage', 'N/A')}\n")
                             f.write(f"**💪 Margin Durability:** {fa.get('margin_durability', 'N/A')}\n\n")

                    # 3. Cycle Analysis (if applicable)
                    if 'cycleAnalysis' in row:
                        cycle = row['cycleAnalysis']
                        if isinstance(cycle, dict):
                            f.write(f"**🔄 Cycle Position:** {cycle.get('position', 'N/A')}\n")
                            f.write(f"*Evidence:* {cycle.get('evidence', 'N/A')}\n\n")
                    elif 'fundamental_analysis' in row:
                         # Mapping for new SURGE schema
                         fa = row['fundamental_analysis']
                         if isinstance(fa, dict):
                             f.write(f"**🔄 Industry Cycle:** {fa.get('industry_cycle', 'N/A')}\n\n")
                            
                    # 4. Valuation
                    if 'valuationAnalysis' in row:
                        val = row['valuationAnalysis']
                        if isinstance(val, dict):
                            f.write(f"**💰 Valuation:** {val.get('verdict', 'N/A')} (Score: {val.get('score', 'N/A')})\n")
                    elif 'cycleAdjustedValuation' in row:
                         val = row['cycleAdjustedValuation']
                         if isinstance(val, dict):
                            f.write(f"**💰 Valuation:** {val.get('verdict', 'N/A')} (Score: {val.get('score', 'N/A')})\n")
                            f.write(f"*Logic:* {val.get('adjustment_logic', 'N/A')}\n\n")
                    elif 'fundamental_analysis' in row:
                         # Mapping for new SURGE schema
                         fa = row['fundamental_analysis']
                         if isinstance(fa, dict):
                             f.write(f"**💰 Valuation Assessment:** {fa.get('valuation_assessment', 'N/A')}\n\n")

                    # 5. Scenarios / Opportunities / Risks
                    if 'marketScenarios' in row:
                        scenarios = row['marketScenarios']
                        if isinstance(scenarios, dict):
                            f.write(f"**🚀 Upside:** {scenarios.get('upside', 'N/A')}\n")
                            f.write(f"**⚠️ Downside:** {scenarios.get('downside', 'N/A')}\n\n")
                    
                    # SURGE New Schema (Arrays)
                    if 'key_opportunities' in row:
                        ops = row['key_opportunities']
                        if isinstance(ops, list):
                            f.write(f"**🚀 Key Opportunities:** {'; '.join(ops)}\n")
                    
                    if 'key_risks' in row:
                        risks = row['key_risks']
                        if isinstance(risks, list):
                            f.write(f"**⚠️ Key Risks:** {'; '.join(risks)}\n\n")
                    
                    # --- SURGE Specific Blocks (Legacy Support) ---
                    if 'catalystAnalysis' in row:
                        f.write(f"**⚡ Catalyst:** {row['catalystAnalysis']}\n\n")
                        
                    if 'earningsQuality' in row:
                        eq = row['earningsQuality']
                        if isinstance(eq, dict):
                            f.write(f"**💎 Earnings Quality:** {eq.get('verdict', 'N/A')}\n")
                            f.write(f"*{eq.get('explanation', 'N/A')}*\n\n")

                    if 'guidanceCheck' in row:
                        gc = row['guidanceCheck']
                        if isinstance(gc, dict):
                            f.write(f"**🔮 Guidance:** {gc.get('tone', 'N/A')}\n")
                            f.write(f"*Drivers:* {gc.get('key_drivers', 'N/A')}\n\n")

                    if 'valuationPEG' in row:
                        vp = row['valuationPEG']
                        if isinstance(vp, dict):
                            f.write(f"**📊 Valuation (PEG):** {vp.get('verdict', 'N/A')} (Ratio: {vp.get('ratio', 'N/A')})\n")
                            f.write(f"*Logic:* {vp.get('logic', 'N/A')}\n\n")

                    if 'sustainabilityVerdict' in row:
                        sv = row['sustainabilityVerdict']
                        if isinstance(sv, dict):
                             f.write(f"**🔋 Sustainability Score:** {sv.get('sustainability_score', sv.get('score', 'N/A'))}/10\n")
                             f.write(f"**⚠️ Risk Factors:** {sv.get('risk_factors', 'N/A')}\n\n")
                    # -----------------------------

                    # 6. Generic Analysis fallback
                    if 'analysis' in row and isinstance(row['analysis'], str):
                         f.write(f"**📝 Synthesis:**\n{row['analysis']}\n\n")
                    elif 'one_liner' in row and isinstance(row['one_liner'], str):
                         f.write(f"**📝 Synthesis:**\n{row['one_liner']}\n\n")
                         
                f.write("---\n\n")
                
        logger.info(f"Briefing generated: {filename}")

if __name__ == "__main__":
    gen = BriefingGenerator()
    # Argument parsing for date
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="YYYY-MM-DD")
    parser.add_argument("--strategy", type=str, help="Filter by strategy name")
    args = parser.parse_args()
    
    gen.run(args.date, args.strategy)
