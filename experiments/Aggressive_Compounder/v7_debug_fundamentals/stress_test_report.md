# Kryptonite Test Report: Aggressive_Compounder
**Experiment Tag:** v7_debug_fundamentals
**Benchmark:** SPX

## 1. Scenario Performance (3-Month Window)
Did the strategy survive better than the market?

| Scenario              | Strategy Return   | Benchmark Return   | Alpha   | Avg Drawdown   |
|:----------------------|:------------------|:-------------------|:--------|:---------------|
| COVID_CRASH           | -14.66%           | -11.91%            | -2.76%  | -44.52%        |
| INFLATION_SPIKE       | -9.59%            | -3.57%             | -6.02%  | -30.44%        |
| LIQUIDITY_CRUNCH_2018 | -23.72%           | -15.81%            | -7.91%  | -28.84%        |
| RATE_HIKE_2022        | -9.72%            | -4.46%             | -5.26%  | -26.00%        |

## 2. Detailed Breakdown
### COVID_CRASH
* **Win Rate (vs Bench):** 45.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| EVRI     | -60.4%           | -48.5%  | -88.6%         |
| SEAS     | -52.0%           | -40.1%  | -78.9%         |
| AMRN     | -58.3%           | -46.3%  | -77.7%         |
| VLRS     | -64.1%           | -52.2%  | -77.1%         |
| SNBR     | -47.4%           | -35.4%  | -74.0%         |

### RATE_HIKE_2022
* **Win Rate (vs Bench):** 32.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| AMBA     | -51.2%           | -46.7%  | -62.0%         |
| TREX     | -48.8%           | -44.4%  | -51.1%         |
| GT       | -34.7%           | -30.3%  | -51.0%         |
| CALX     | -45.5%           | -41.0%  | -48.0%         |
| INMD     | -43.1%           | -38.6%  | -47.7%         |

### INFLATION_SPIKE
* **Win Rate (vs Bench):** 29.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| VTNR     | -39.2%           | -35.6%  | -61.2%         |
| ESTE     | -22.5%           | -19.0%  | -49.0%         |
| SBOW     | -3.8%            | -0.2%   | -48.6%         |
| METC     | -23.1%           | -19.6%  | -47.8%         |
| TALO     | -9.0%            | -5.4%   | -47.2%         |

### LIQUIDITY_CRUNCH_2018
* **Win Rate (vs Bench):** 18.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| SPPI     | -70.3%           | -54.5%  | -70.3%         |
| CTLP     | -65.9%           | -50.1%  | -65.9%         |
| CRON     | -19.1%           | -3.2%   | -50.5%         |
| ALGN     | -47.9%           | -32.1%  | -49.7%         |
| AMD      | -42.5%           | -26.7%  | -48.3%         |

