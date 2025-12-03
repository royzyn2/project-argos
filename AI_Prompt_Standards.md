# **Project Argos: AI Prompt Factory Standards**

**Version:** 1.0
**Purpose:** To ensure all new AI strategy prompts are plug-and-play compatible with the `llm_runner` and `briefing_gen` engines.

---

## **1. The "Factory" Philosophy**

The Argos AI engine is **agnostic**. It does not know what "Growth" or "Value" is. It simply:
1. Reads a Prompt File (`.js`).
2. Executes the LLM instruction.
3. Renders *whatever* JSON structure comes back into the Daily Briefing.

Therefore, the **intelligence** lives entirely in the Prompt File. To create a new strategy analysis, you **do not** need to edit Python code. You only need to create a compliant JSON prompt.

---

## **2. File Location & Naming**

*   **Directory:** `prompts/`
*   **Naming Convention:** `{Strategy_Name}.js`
    *   **CRITICAL:** The filename must match the `strategy_name` column in your CSV results EXACTLY.
    *   *Example:* If your CSV has `strategy_name = 'Super_Cycle'`, your file must be `prompts/Super_Cycle.js`.

---

## **3. The 4-Key Structure (Mandatory)**

Every prompt file must be a valid JSON object containing these four specific keys.

```json
{
    "persona": "...",
    "guidingPrinciples": [...],
    "task_instructions": "...",
    "output_schema": { ... }
}
```

### **A. `persona` (String)**
Who is the AI? Define the lens through which it views data.
*   *Example:* "You are a Distressed Debt Investor looking for bankruptcy remote assets..."

### **B. `guidingPrinciples` (Array of Strings)**
The "Guardrails" and "Mental Models".
*   *Usage:* Instruct the AI on what to prioritize or ignore.
*   *Example:* ["Ignore non-GAAP earnings.", "Focus heavily on free cash flow conversion."]

### **C. `task_instructions` (String or Object)**
The specific questions to answer.
*   *Usage:* Be prescriptive. Don't just say "Analyze this." Say "Calculate the Piotroski F-Score implication."

### **D. `output_schema` (Object) - THE INTERFACE**
This defines what shows up in the Daily Briefing.

---

## **4. Output Schema Standards**

The `briefing_gen.py` engine automatically renders this schema. However, it expects a few **Reserved Keys** for the summary table, while everything else is treated as **Rich Data**.

### **Mandatory Reserved Keys (The Summary Table)**

These MUST exist for the strategy to appear in the "Top Picks" table.

| Key | Type | Description |
| :--- | :--- | :--- |
| **`final_score`** | `Number` (1-10) | The ultimate ranking metric. 10 = Perfect, 1 = Trash. |
| **`verdict`** | `String` | Enum: `STRONG_BUY`, `BUY`, `HOLD`, `SELL`. |
| **`analysis`** | `String` | A one-sentence "Executive Summary" or "One-Liner". |

### **Rich Data Keys (The Deep Dive)**

Any other key you add here will be **automatically rendered** in the "Strategy Deep Dives" section of the Markdown report. Use `camelCase` for keys; the engine will auto-convert them to `Title Case`.

**Supported Structures:**
1.  **String:** Simple text block.
2.  **Object:** Key-Value pairs (ideal for sub-scores).

**Example Schema:**

```json
"output_schema": {
    // --- MANDATORY ---
    "final_score": "Number (1-10)",
    "verdict": "String (BUY/HOLD/SELL)",
    "analysis": "String (One-liner summary)",

    // --- RICH DATA (Customizable per Strategy) ---
    "moatAnalysis": {
        "verdict": "String (Wide/Narrow/None)",
        "score": "Number (1-10)"
    },
    "managementQuality": {
        "capitalAllocation": "String (Good/Bad)",
        "insiderOwnership": "String (High/Low)"
    },
    "catalystWatch": "String (Upcoming events to watch)"
}
```

**How it renders in Markdown:**

> **Moat Analysis:**
> * *Verdict:* Wide
> * *Score:* 9
>
> **Management Quality:**
> * *Capital Allocation:* Good
> * *Insider Ownership:* High
>
> **Catalyst Watch:** Upcoming FDA approval in Q4.

---

## **5. Testing Your Prompt**

1.  Ensure you have generated candidate results (`data/results/{Strategy}.csv`).
2.  Run the LLM Runner: `python src/analysis/llm_runner.py`
3.  Run the Briefing Gen: `python src/analysis/briefing_gen.py`
4.  Check `output/daily_briefings/` to verify your new sections appear correctly.

