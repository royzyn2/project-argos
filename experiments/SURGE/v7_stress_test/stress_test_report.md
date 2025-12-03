# Kryptonite Test Report: SURGE
**Experiment Tag:** v7_stress_test
**Benchmark:** SPX

## 1. Scenario Performance (3-Month Survival)
Did the strategy survive better than the market?

| Scenario              | Strategy Return (3M)   | Benchmark Return (3M)   | Alpha (3M)   | Avg Drawdown (3M)   |
|:----------------------|:-----------------------|:------------------------|:-------------|:--------------------|
| COVID_CRASH           | -24.45%                | -11.91%                 | -12.55%      | -46.49%             |
| INFLATION_SPIKE       | -5.08%                 | -3.57%                  | -1.52%       | -18.55%             |
| LIQUIDITY_CRUNCH_2018 | -19.92%                | -15.81%                 | -4.12%       | -23.51%             |
| RATE_HIKE_2022        | -0.87%                 | -4.46%                  | 3.59%        | -17.45%             |

## 2. Detailed Breakdown
### COVID_CRASH
* **Win Rate (vs Bench):** 24.0%
#### Worst Drawdowns (3M)
| ticker   | Return_3M   | Alpha_3M   | MaxDD_3M   |
|:---------|:------------|:-----------|:-----------|
| GTLS     | -42.5%      | -30.6%     | -75.9%     |
| DENN     | -49.1%      | -37.2%     | -75.7%     |
| EBIX     | -40.5%      | -28.6%     | -75.0%     |
| ATI      | -61.3%      | -49.4%     | -74.4%     |
| EPRT     | -52.7%      | -40.8%     | -71.3%     |

### RATE_HIKE_2022
* **Win Rate (vs Bench):** 54.0%
#### Worst Drawdowns (3M)
| ticker   | Return_3M   | Alpha_3M   | MaxDD_3M   |
|:---------|:------------|:-----------|:-----------|
| HHR      | -71.2%      | -66.8%     | -71.3%     |
| PVH      | -27.8%      | -23.3%     | -39.9%     |
| AEO      | -35.2%      | -30.8%     | -37.0%     |
| SLAB     | -26.0%      | -21.5%     | -34.8%     |
| SMTC     | -22.8%      | -18.3%     | -32.3%     |

### INFLATION_SPIKE
* **Win Rate (vs Bench):** 46.0%
#### Worst Drawdowns (3M)
| ticker   | Return_3M   | Alpha_3M   | MaxDD_3M   |
|:---------|:------------|:-----------|:-----------|
| ZIM      | -43.9%      | -40.3%     | -47.3%     |
| TECK     | -20.1%      | -16.5%     | -43.7%     |
| DDS      | -0.5%       | 3.1%       | -41.1%     |
| JWN      | -33.2%      | -29.6%     | -37.8%     |
| BFH      | -29.6%      | -26.0%     | -33.7%     |

### LIQUIDITY_CRUNCH_2018
* **Win Rate (vs Bench):** 34.0%
#### Worst Drawdowns (3M)
| ticker   | Return_3M   | Alpha_3M   | MaxDD_3M   |
|:---------|:------------|:-----------|:-----------|
| PATK     | -54.6%      | -38.7%     | -54.6%     |
| SMCI     | -29.7%      | -13.9%     | -45.6%     |
| BDC      | -41.8%      | -26.0%     | -42.4%     |
| LMAT     | -33.9%      | -18.1%     | -41.5%     |
| GEF      | -41.4%      | -25.6%     | -41.4%     |

