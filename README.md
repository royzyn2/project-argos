# Project Argos

**Project Argos** is an advanced, AI-driven "factory" for quantitative investment strategies. It combines rigorous quantitative screening with state-of-the-art Large Language Model (LLM) analysis to identify high-conviction investment opportunities in the US equity market.

The system is designed to be modular, allowing for the rapid development, backtesting, and deployment of distinct investment strategies (e.g., Momentum, Quality Compounders, Turnarounds).

## 🚀 Core Architecture

The project follows a strict 5-Phase "Factory Model":

1.  **Phase 1: Quantitative Screening** (`src/strategies/`)
    *   Filters the entire US stock universe (~5000+ stocks) using hard quantitative metrics (Growth, Margins, Price Momentum, Volatility).
    *   Implements specific logic for each strategy (e.g., *SURGE* for earnings acceleration, *Aggressive Compounder* for sustained growth).

2.  **Phase 2: Data Warehouse Assembly** (`src/engine/warehouse_builder.py`)
    *   For passed candidates, the system builds a comprehensive "Dossier" including:
        *   Point-in-Time Financials (Income Statement, Balance Sheet, Cash Flow).
        *   Earnings Call Transcripts (Historical & Recent).
        *   Price Action & Technical Indicators.
        *   Sector & Industry Context.

3.  **Phase 3: AI Analysis** (`src/analysis/llm_runner.py`)
    *   **The "Brain"**: Uses Google Gemini 2.5/2.0 Flash/Pro models to act as a senior equity analyst.
    *   **Prompt Engineering**: Each strategy has a dedicated "Persona" (JSON prompt) that instructs the AI on what to value (e.g., "Scrutinize leverage for SURGE", "Look for moat durability for Compounders").
    *   **Output**: Generates a structured JSON report with Scores (0-10), Verdicts (Buy/Watch/Pass), and detailed qualitative reasoning.

4.  **Phase 4: Backtesting & Validation** (`src/engine/ai_tester.py`)
    *   **Protocol A (Calendar)**: Blind time-travel tests to random past dates to verify predictive power.
    *   **Protocol E (AI Validation)**: Correlates AI scores with actual future returns (3M, 6M, 1Y).
    *   **Reporting**: Generates detailed Markdown reports with Alpha, Win Rates, and Sortino Ratios.

5.  **Phase 5: Production & Reporting** (`src/analysis/briefing_gen.py`)
    *   Runs the pipeline on the latest available data.
    *   Produces a **Daily Briefing**: A comprehensive Markdown report containing:
        *   **Market Pulse**: High-level stats.
        *   **Elite List**: Top-ranked candidates.
        *   **Deep Dives**: Detailed analysis of every candidate.

## 🧠 Implemented Strategies

*   **SURGE**: Captures earnings acceleration and price momentum. Focuses on "Double Engine" growth (Revenue + Profit) with strict risk controls (ROE > 10%, Debt/Equity < 3.0).
*   **Aggressive Compounder**: Identifies long-term multi-baggers with sustained high growth and dominant market positions.
*   **SUPER_CYCLE**: Finds companies with smooth, linear long-term trends resilient to "Black Swan" events.
*   **TREND**: Pure trend-following strategy based on moving averages and risk-adjusted momentum.
*   **Others**: TURNAROUND, SMALL_CAP, DIP, DIVIDEND, CORE_VALUE, CORE_STABLE.

## 🛠️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/project-argos.git
    cd project-argos
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    Create a `.env` file in the root directory (or use `config/secrets_loader.py`) with your API keys:
    ```env
    FMP_API_KEY=your_fmp_key_here
    GEMINI_API_KEY=your_google_gemini_key_here
    ```

## 💻 Usage

The project is controlled via a central CLI `src/main.py`.

### 1. Run a Backtest (Quantitative Only)
```bash
python src/main.py backtest --strategy SURGE --mode CALENDAR
```

### 2. Run an AI Backtest (Time Travel)
Tests the AI's judgment on a specific past date.
```bash
python src/engine/ai_tester.py --strategy SURGE --date 2018-08-15 --top_n 50
```

### 3. Run Production Analysis (Latest Data)
Runs the full pipeline for a strategy on today's data.
```bash
python src/main.py production --strategy SURGE --mode LATEST
```

### 4. Update Data
Updates market prices and fundamental data incrementally.
```bash
python src/engine/data_updater.py --mode market
python src/engine/data_updater.py --mode fundamentals
```

## 📁 Directory Structure

*   `src/`: Source code for engine, strategies, and analysis.
*   `data/`: Storage for market data (Parquet), fundamentals, and generated reports.
*   `prompts/`: JSON-based system prompts defining the AI personas for each strategy.
*   `experiments/`: specialized folders for storing backtest results and research notes.
*   `output/`: Final production reports and Daily Briefings.

## 📄 License

Private & Confidential. Internal Use Only.

