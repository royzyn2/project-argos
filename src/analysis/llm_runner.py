"""
LLMRunner (The AI Engine)
==========================
Orchestrates the AI Analysis phase.

Logic:
1. Scans data/results/*.csv for strategy outputs.
2. Loads the corresponding AI Prompt (prompts/{Strategy}.js).
3. Loads the deep context from data/warehouse/{ticker}/{date}_context.json.
   - Crucial: Respects TIME TRAVEL. Only loads context for the specific snapshot date.
4. Sends payload to Gemini API.
   - Uses google.genai SDK (v2) for better stability with newer models.
   - Retries on failure.
   - Fallbacks to older models if primary fails.
5. Saves analysis to data/reports/{Strategy}/{ticker}_{date}.json.
"""

import os
import pandas as pd
import json
import time
from pathlib import Path
from src.utils.logger import logger
from config.secrets_loader import get_secret

# Use the new SDK
try:
    from google import genai
    from google.genai import types
    SDK_AVAILABLE = True
except ImportError:
    import google.generativeai as genai_old
    SDK_AVAILABLE = False
    logger.warning("google.genai SDK not found, falling back to google.generativeai (Legacy)")

class LLMRunner:
    def __init__(self):
        self.results_dir = Path("data/results")
        self.warehouse_dir = Path("data/warehouse")
        self.reports_dir = Path("data/reports")
        self.prompts_dir = Path("prompts")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        
        if self.api_key:
            if SDK_AVAILABLE:
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini API Configured (google.genai SDK)")
            else:
                genai_old.configure(api_key=self.api_key)
                self.client = "LEGACY"
                logger.info("Gemini API Configured (Legacy SDK)")
                
            # Model Priority List - Updated for Production Efficiency
            # User requested: Gemini 2.5 Flash first, then Gemini 2.0 Flash
            self.model_priority = ['gemini-2.0-flash', 'gemini-2.0-flash-exp', 'gemini-2.5-pro', 'gemini-1.5-pro']
        else:
            logger.warning("GEMINI_API_KEY not found. Running in MOCK mode.")
        
    def run(self, target_strategy: str = None):
        logger.info("Starting AI Analysis Cycle...")
        
        logger.info(f"Scanning {self.results_dir} for results...")
        csv_files = list(self.results_dir.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files.")
        
        for csv_file in csv_files:
            strategy_name = csv_file.stem
            
            if target_strategy and strategy_name != target_strategy:
                continue
                
            logger.info(f"Processing Strategy: {strategy_name} from {csv_file}")
            self._process_strategy(strategy_name, csv_file)
            
        logger.info("AI Analysis Cycle Complete.")

    def _process_strategy(self, strategy_name: str, csv_path: Path):
        # Load Strategy Prompt
        prompt_path = self.prompts_dir / f"{strategy_name}.js"
        # Try removing suffix if present (e.g. _AI_TEST) to find original prompt
        if not prompt_path.exists():
            if "_AI_TEST" in strategy_name:
                original_strat = strategy_name.replace("_AI_TEST", "")
                prompt_path = self.prompts_dir / f"{original_strat}.js"
            elif "_PRODUCTION" in strategy_name:
                original_strat = strategy_name.replace("_PRODUCTION", "")
                prompt_path = self.prompts_dir / f"{original_strat}.js"

        if not prompt_path.exists():
            logger.warning(f"No prompt found for {strategy_name}, skipping AI analysis.")
            return
            
            with open(prompt_path, "r") as f:
            try:
                strategy_prompt = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in {prompt_path}")
                return

        # Load Candidates (Process ALL)
        try:
            df = pd.read_csv(csv_path)
            if df.empty: return
            
            # Process ALL candidates without artificial limits
            # Sorting by raw_score helps process higher quality candidates first in logs
            if 'raw_score' in df.columns:
                top_candidates = df.sort_values('raw_score', ascending=False)
            else:
                top_candidates = df
                
            # Create Output Directory
            strategy_report_dir = self.reports_dir / strategy_name
            strategy_report_dir.mkdir(exist_ok=True)
            
            for _, row in top_candidates.iterrows():
                self._analyze_candidate(row, strategy_name, strategy_prompt, strategy_report_dir)
                
        except Exception as e:
            logger.error(f"Error processing {strategy_name}: {e}")

    def _analyze_candidate(self, row: pd.Series, strategy_name: str, prompt: dict, output_dir: Path):
        ticker = row['ticker']
        date_str = row['date']
        
        # Check for cached report
        report_path = output_dir / f"{ticker}_{date_str}.json"
        if report_path.exists():
            return

        # Load Warehouse Context
        context_path = self.warehouse_dir / ticker / f"{date_str}_context.json"
        if not context_path.exists():
            logger.warning(f"No context found for {ticker} @ {date_str}, skipping.")
            return
            
        with open(context_path, "r") as f:
            context_data = json.load(f)
            
        ai_response = None
        
        # --- REAL LLM CALL ---
        if self.client:
            try:
                logger.info(f"[{ticker}] Constructing prompt...")
                full_prompt = self._construct_prompt(prompt, context_data)
                
                logger.info(f"[{ticker}] Sending request to Gemini...")
                
                # Retry Logic with Fallback
                ai_response = self._call_gemini_with_retry(full_prompt, ticker)
                
                if ai_response:
                    # Ensure metadata
                    ai_response['ticker'] = ticker
                    ai_response['date'] = date_str
                    ai_response['strategy'] = strategy_name
                    # Add risk_flags if missing
                    if 'risk_flags' not in ai_response:
                         ai_response['risk_flags'] = []
                
            except Exception as e:
                logger.error(f"Gemini Error for {ticker}: {e}. Falling back to mock.")
                ai_response = None

        # --- MOCK FALLBACK (DISABLED FOR PRODUCTION ACCURACY) ---
        if ai_response is None:
            logger.error(f"[{ticker}] AI Analysis failed. Skipping mock generation to ensure data integrity.")
            return
            
        # Save Report
        with open(report_path, "w") as f:
            json.dump(ai_response, f, indent=2)

    def _call_gemini_with_retry(self, prompt_text, ticker):
        """
        Calls Gemini with retries and model fallback using the new SDK.
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            for model_name in self.model_priority:
                try:
                    logger.info(f"[{ticker}] Attempt {attempt+1}/{max_retries} using {model_name}...")
                    
                    text = ""
                    if SDK_AVAILABLE and self.client != "LEGACY":
                        # New SDK
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt_text
                        )
                        text = response.text
                    else:
                        # Legacy SDK
                        model = genai_old.GenerativeModel(model_name)
                        response = model.generate_content(prompt_text)
                        text = response.text

                    logger.info(f"[{ticker}] Received response from {model_name}.")
                    
                    # Clean JSON markdown
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0]
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0]
                    
                    logger.info(f"[{ticker}] Parsing JSON...")
                    return json.loads(text)
                    
                except Exception as e:
                    logger.warning(f"[{ticker}] Error with {model_name}: {e}")
                    # Continue to next model
                    
            # Exponential backoff after trying all models for this attempt
            time.sleep(2 * (attempt + 1))
                    
        logger.error(f"[{ticker}] All retries failed.")
        return None

    def _construct_prompt(self, prompt_config: dict, context_data: dict) -> str:
        """Constructs the final prompt string."""
        p = f"PERSONA: {prompt_config.get('persona', '')}\n\n"
        p += f"GUIDING PRINCIPLES: {json.dumps(prompt_config.get('guidingPrinciples', []))}\n\n"
        p += f"TASK: {prompt_config.get('task_instructions', '')}\n\n"
        p += f"CONTEXT DATA (Financials & Metadata): {json.dumps(context_data, indent=2)}\n\n"
        p += f"OUTPUT SCHEMA (Must return valid JSON matching this): {json.dumps(prompt_config.get('output_schema', {}), indent=2)}\n"
        return p

    def _generate_mock_response(self, row, strategy_name, prompt, context_data):
        ticker = row['ticker']
        date_str = row['date']
        raw_score = row.get('raw_score', 50)
        
        # Ensure final_score is an integer 1-10, not float
        final_score = int(min(10, max(1, round(raw_score / 10))))
        
        if raw_score > 80:
            verdict = "STRONG_BUY"
            analysis = f"Excellent {strategy_name} setup. {context_data.get('primary_metric', 'Key metrics')} confirms thesis."
        elif raw_score > 70:
            verdict = "BUY"
            analysis = "Solid setup, but watch for valuation risks."
        else:
            verdict = "HOLD"
            analysis = "Metrics are borderline. Wait for better entry."

        ai_response = {
            "ticker": ticker,
            "date": date_str,
            "strategy": strategy_name,
            "final_score": final_score,
            "verdict": verdict,
            "analysis": analysis,
            "risk_flags": ["Mock Risk 1", "Mock Risk 2"]
        }

        if 'output_schema' in prompt:
            schema = prompt['output_schema']
            for key, value in schema.items():
                if key in ai_response: continue 
                
                if isinstance(value, dict):
                    mock_sub_obj = {}
                    for sub_key, sub_val in value.items():
                        if "score" in sub_key.lower():
                            mock_sub_obj[sub_key] = final_score
                        elif "verdict" in sub_key.lower():
                            mock_sub_obj[sub_key] = verdict
                        elif "logic" in sub_key.lower() or "rationale" in sub_key.lower():
                            mock_sub_obj[sub_key] = f"Mock logic for {key}"
                        elif "explanation" in sub_key.lower():
                            mock_sub_obj[sub_key] = f"Mock explanation for {key}"
                        elif "ratio" in sub_key.lower():
                            mock_sub_obj[sub_key] = "1.5"
                        else:
                            mock_sub_obj[sub_key] = f"Mock {sub_key}"
                    ai_response[key] = mock_sub_obj
                else:
                    ai_response[key] = f"Mock {key}"
        return ai_response

if __name__ == "__main__":
    runner = LLMRunner()
    runner.run()
