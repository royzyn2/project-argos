# Kryptonite Test Report: Aggressive_Compounder
**Experiment Tag:** v5_kryptonite_benchmarked
**Benchmark:** SPX

## 1. Scenario Performance (3-Month Window)
Did the strategy survive better than the market?

| Scenario              | Strategy Return   | Benchmark Return   | Alpha   | Avg Drawdown   |
|:----------------------|:------------------|:-------------------|:--------|:---------------|
| COVID_CRASH           | -16.94%           | -11.91%            | -5.04%  | -43.89%        |
| INFLATION_SPIKE       | -9.64%            | -3.57%             | -6.07%  | -27.44%        |
| LIQUIDITY_CRUNCH_2018 | -22.32%           | -15.81%            | -6.51%  | -26.39%        |
| RATE_HIKE_2022        | -11.66%           | -4.46%             | -7.20%  | -25.72%        |

## 2. Detailed Breakdown
### COVID_CRASH
* **Win Rate (vs Bench):** 44.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| EVRI     | -60.4%           | -48.5%  | -88.6%         |
| SEAS     | -52.0%           | -40.1%  | -78.9%         |
| VLRS     | -64.1%           | -52.2%  | -77.1%         |
| HP       | -58.7%           | -46.8%  | -71.8%         |
| CRMT     | -45.3%           | -33.4%  | -70.3%         |

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
* **Win Rate (vs Bench):** 30.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| METC     | -23.1%           | -19.6%  | -47.8%         |
| TALO     | -9.0%            | -5.4%   | -47.2%         |
| EC       | -40.5%           | -36.9%  | -46.6%         |
| ROCC     | -15.4%           | -11.9%  | -45.0%         |
| PR       | -3.4%            | 0.2%    | -44.3%         |

### LIQUIDITY_CRUNCH_2018
* **Win Rate (vs Bench):** 24.0%
#### Worst Drawdowns
| ticker   | forward_return   | Alpha   | max_drawdown   |
|:---------|:-----------------|:--------|:---------------|
| NVDA     | -49.2%           | -33.4%  | -53.3%         |
| ALGN     | -47.9%           | -32.1%  | -49.7%         |
| MCFT     | -47.7%           | -31.9%  | -47.7%         |
| TPL      | -45.1%           | -29.3%  | -47.2%         |
| RGNX     | -43.1%           | -27.3%  | -46.2%         |

