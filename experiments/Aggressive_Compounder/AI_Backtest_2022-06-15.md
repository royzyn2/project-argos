# AI Backtest Report: Aggressive_Compounder
**Snapshot Date:** 2022-06-15
**Benchmark:** SPX

## 1. AI Score vs Future Alpha (6M)
| ticker   |   final_score | Return_6M   | Alpha_6M   | verdict    |
|:---------|--------------:|:------------|:-----------|:-----------|
| FLNG     |             9 | 38.6%       | 33.2%      | STRONG_BUY |
| TS       |             8 | 14.9%       | 9.5%       | BUY        |
| SLB      |             8 | 21.5%       | 16.0%      | BUY        |
| HAL      |             8 | 2.6%        | -2.8%      | BUY        |
| VNOM     |             6 | -4.3%       | -9.8%      | HOLD       |
| HES      |             5 | 16.2%       | 10.8%      | HOLD       |
| TECK     |             4 | -6.3%       | -11.7%     | HOLD       |
| KRP      |             4 | -7.9%       | -13.3%     | HOLD       |
| DVN      |             4 | -9.6%       | -15.0%     | HOLD       |
| PXD      |             4 | -12.8%      | -18.2%     | HOLD       |
| MGY      |             4 | -14.2%      | -19.6%     | HOLD       |
| WRB      |             4 | 8.9%        | 3.5%       | HOLD       |
| NTR      |             4 | -13.5%      | -19.0%     | HOLD       |
| SBLK     |             4 | -24.6%      | -30.0%     | HOLD       |
| EOG      |             4 | -1.2%       | -6.6%      | HOLD       |
| XOM      |             4 | 12.2%       | 6.8%       | HOLD       |
| MRO      |             4 | -2.1%       | -7.6%      | SELL       |
| CPG      |             4 | -23.7%      | -29.2%     | HOLD       |
| VRTV     |             4 | 2.2%        | -3.3%      | HOLD       |
| SU       |             4 | -19.8%      | -25.2%     | SELL       |
| EQNR     |             4 | 3.4%        | -2.0%      | HOLD       |
| CIVI     |             4 | -19.7%      | -25.1%     | HOLD       |
| WLK      |             3 | 2.7%        | -2.7%      | SELL       |
| MUR      |             3 | 4.8%        | -0.7%      | SELL       |
| ADM      |             3 | 12.8%       | 7.4%       | SELL       |
| MPC      |             3 | 12.2%       | 6.8%       | SELL       |
| STLD     |             3 | 50.8%       | 45.4%      | SELL       |
| TSEM     |             3 | -1.5%       | -6.9%      | SELL       |
| MTDR     |             3 | -4.0%       | -9.4%      | SELL       |
| TMST     |             2 | -15.8%      | -21.2%     | SELL       |

## 2. Score Group Analysis (6M Horizon)
| Score_Group   | Avg Alpha   |   Count | Win Rate   |
|:--------------|:------------|--------:|:-----------|
| High (>8)     | 14.0%       |       4 | 75%        |
| Low (<5)      | -8.2%       |      24 | 21%        |
| Med (5-8)     | 0.5%        |       2 | 50%        |

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
