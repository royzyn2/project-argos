# Kryptonite Test Report: Aggressive_Compounder
**Experiment Tag:** v9_risk_flag
**Benchmark:** SPX

## 1. Scenario Performance (3-Month Window)
Did the strategy survive better than the market?

| Scenario              | Strategy Return   | Benchmark Return   | Alpha   | Avg Drawdown   |
|:----------------------|:------------------|:-------------------|:--------|:---------------|
| COVID_CRASH           | -13.94%           | -11.91%            | -2.03%  | -43.76%        |
| INFLATION_SPIKE       | -8.87%            | -3.57%             | -5.31%  | -28.86%        |
| LIQUIDITY_CRUNCH_2018 | -22.47%           | -15.81%            | -6.66%  | -27.31%        |
| RATE_HIKE_2022        | -10.75%           | -4.46%             | -6.29%  | -25.39%        |

## 2. Detailed Breakdown
### COVID_CRASH
* **Win Rate (vs Bench):** 47.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| EVRI     | -60.4%           | -48.5%  | -88.6%         |
| SEAS     | -52.0%           | -40.1%  | -78.9%         |
| AMRN     | -58.3%           | -46.3%  | -77.7%         |
| VLRS     | -64.1%           | -52.2%  | -77.1%         |
| SNBR     | -47.4%           | -35.4%  | -74.0%         |

### RATE_HIKE_2022
* **Win Rate (vs Bench):** 28.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| AMBA     | -51.2%           | -46.7%  | -62.0%         |
| TREX     | -48.8%           | -44.4%  | -51.1%         |
| VICR     | -40.5%           | -36.1%  | -51.0%         |
| GT       | -34.7%           | -30.3%  | -51.0%         |
| CALX     | -45.5%           | -41.0%  | -48.0%         |

### INFLATION_SPIKE
* **Win Rate (vs Bench):** 31.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| SBOW     | -3.8%            | -0.2%   | -48.6%         |
| METC     | -23.1%           | -19.6%  | -47.8%         |
| EC       | -40.5%           | -36.9%  | -46.6%         |
| ROCC     | -15.4%           | -11.9%  | -45.0%         |
| CIVI     | -16.0%           | -12.4%  | -44.2%         |

### LIQUIDITY_CRUNCH_2018
* **Win Rate (vs Bench):** 21.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| SPPI     | -70.3%           | -54.5%  | -70.3%         |
| ALGN     | -47.9%           | -32.1%  | -49.7%         |
| TPL      | -45.1%           | -29.3%  | -47.2%         |
| RGNX     | -43.1%           | -27.3%  | -46.2%         |
| SQ       | -35.4%           | -19.6%  | -43.5%         |

