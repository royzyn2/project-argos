# AI Backtest Report: Aggressive_Compounder
**Snapshot Date:** 2022-06-15
**Benchmark:** SPX

## 1. AI Score vs Future Returns (Multi-Horizon)
| ticker   |   final_score | verdict    | Return_3M   | Return_6M   | Return_1Y   | Return_MAX   |
|:---------|--------------:|:-----------|:------------|:------------|:------------|:-------------|
| FLNG     |             9 | STRONG_BUY | 36.1%       | 38.6%       | 22.9%       | 2.3%         |
| TS       |             8 | BUY        | -5.1%       | 14.9%       | -2.6%       | 7.3%         |
| SLB      |             8 | BUY        | -4.6%       | 21.5%       | 15.1%       | 7.0%         |
| HAL      |             8 | BUY        | -17.4%      | 2.6%        | -8.5%       | -7.5%        |
| VNOM     |             6 | HOLD       | -2.2%       | -4.3%       | -23.9%      | 11.0%        |
| HES      |             5 | HOLD       | 6.6%        | 16.2%       | 15.7%       | 22.3%        |
| TECK     |             4 | HOLD       | -19.6%      | -6.3%       | 4.3%        | 17.9%        |
| KRP      |             4 | HOLD       | 0.5%        | -7.9%       | -14.8%      | -8.4%        |
| DVN      |             4 | HOLD       | 1.5%        | -9.6%       | -27.3%      | -33.3%       |
| PXD      |             4 | HOLD       | -5.4%       | -12.8%      | -19.9%      | 4.4%         |
| MGY      |             4 | HOLD       | -15.2%      | -14.2%      | -23.4%      | -8.8%        |
| WRB      |             4 | HOLD       | 1.1%        | 8.9%        | -11.5%      | 19.7%        |
| NTR      |             4 | HOLD       | 1.0%        | -13.5%      | -31.7%      | -42.0%       |
| SBLK     |             4 | HOLD       | -23.5%      | -24.6%      | -31.4%      | -11.6%       |
| EOG      |             4 | HOLD       | -3.8%       | -1.2%       | -11.0%      | -6.2%        |
| XOM      |             4 | HOLD       | -0.1%       | 12.2%       | 10.8%       | 15.3%        |
| MRO      |             4 | SELL       | -4.5%       | -2.1%       | -16.3%      | -2.7%        |
| CPG      |             4 | HOLD       | -24.3%      | -23.7%      | -26.3%      | -13.0%       |
| VRTV     |             4 | HOLD       | -10.5%      | 2.2%        | -4.2%       | 32.5%        |
| SU       |             4 | SELL       | -19.7%      | -19.8%      | -22.3%      | -4.6%        |
| EQNR     |             4 | HOLD       | -0.6%       | 3.4%        | -16.0%      | -24.0%       |
| CIVI     |             4 | HOLD       | -9.5%       | -19.7%      | -1.4%       | -5.8%        |
| WLK      |             3 | SELL       | -12.5%      | 2.7%        | 6.9%        | 40.8%        |
| MUR      |             3 | SELL       | 0.4%        | 4.8%        | -3.7%       | -3.8%        |
| ADM      |             3 | SELL       | 3.6%        | 12.8%       | -8.3%       | -27.2%       |
| MPC      |             3 | SELL       | -2.8%       | 12.2%       | 14.6%       | 74.4%        |
| STLD     |             3 | SELL       | 5.8%        | 50.8%       | 42.3%       | 73.5%        |
| TSEM     |             3 | SELL       | -3.9%       | -1.5%       | -12.2%      | -15.4%       |
| MTDR     |             3 | SELL       | -2.5%       | -4.0%       | -16.8%      | -5.0%        |
| TMST     |             2 | SELL       | -27.4%      | -15.8%      | -9.9%       | 1.3%         |

## 2. Score Group Analysis (6M Horizon)
| Score_Group   | Avg Return   | Avg Alpha   |   Count | Win Rate   |
|:--------------|:-------------|:------------|--------:|:-----------|
| High (>8)     | 19.4%        | 14.0%       |       4 | 75%        |
| Low (<5)      | -2.8%        | -8.2%       |      24 | 21%        |
| Med (5-8)     | 5.9%         | 0.5%        |       2 | 50%        |

## 3. Recall Analysis (Within Candidates)
Did the AI correctly identify the best performers in this batch?
**Top 5 Alpha Generators:**
| ticker   |   final_score | verdict    | Alpha_6M   |
|:---------|--------------:|:-----------|:-----------|
| STLD     |             3 | SELL       | 45.4%      |
| FLNG     |             9 | STRONG_BUY | 33.2%      |
| SLB      |             8 | BUY        | 16.0%      |
| HES      |             5 | HOLD       | 10.8%      |
| TS       |             8 | BUY        | 9.5%       |

## 4. Correlation Matrix (IC)
| Horizon   |   IC (vs Alpha) |   P-Value | Significant   |
|:----------|----------------:|----------:|:--------------|
| 3M        |           0.331 |     0.074 | No            |
| 6M        |           0.354 |     0.055 | No            |
| 1Y        |           0.199 |     0.291 | No            |
| MAX       |          -0.074 |     0.696 | No            |
