# AI Backtest Report: Aggressive_Compounder
**Snapshot Date:** 2022-01-03
**Benchmark:** SPX

## 1. AI Score vs Future Alpha (6M)
| ticker   |   final_score | Return_6M   | Alpha_6M   | verdict    |
|:---------|--------------:|:------------|:-----------|:-----------|
| CLFD     |             9 | -18.5%      | 1.4%       | STRONG_BUY |
| NVEE     |             8 | -16.1%      | 3.8%       | BUY        |
| CALX     |             6 | -54.5%      | -34.7%     | BUY        |
| PIPR     |             4 | -38.7%      | -18.8%     | HOLD       |
| STC      |             4 | -35.6%      | -15.8%     | HOLD       |
| AVGO     |             4 | -27.2%      | -7.4%      | HOLD       |
| AAWW     |             4 | -37.7%      | -17.9%     | HOLD       |
| WIRE     |             4 | -30.2%      | -10.3%     | SELL       |
| HRI      |             4 | -40.9%      | -21.1%     | SELL       |
| LPX      |             4 | -30.1%      | -10.2%     | HOLD       |
| NVMI     |             4 | -43.2%      | -23.4%     | HOLD       |
| COKE     |             4 | -5.5%       | 14.3%      | SELL       |
| MGPI     |             4 | 19.0%       | 38.8%      | HOLD       |
| KLAC     |             4 | -32.7%      | -12.8%     | HOLD       |
| LOB      |             3 | -61.7%      | -41.9%     | SELL       |
| ODFL     |             3 | -23.7%      | -3.9%      | SELL       |
| SAIA     |             3 | -38.0%      | -18.2%     | SELL       |
| ONTO     |             3 | -40.9%      | -21.1%     | SELL       |
| BLDR     |             3 | -29.5%      | -9.7%      | SELL       |
| ATKR     |             3 | -21.7%      | -1.9%      | SELL       |
| NVDA     |             3 | -49.8%      | -29.9%     | SELL       |
| SKY      |             3 | -33.9%      | -14.1%     | SELL       |
| HLIO     |             3 | -38.4%      | -18.6%     | SELL       |
| ACLS     |             3 | -37.2%      | -17.4%     | SELL       |
| MLI      |             2 | -11.9%      | 7.9%       | SELL       |
| TREX     |             2 | -57.2%      | -37.4%     | SELL       |
| SMTC     |             2 | -43.0%      | -23.2%     | SELL       |
| BCPC     |             2 | -21.1%      | -1.3%      | SELL       |
| ENTG     |             2 | -33.4%      | -13.5%     | SELL       |
| SITE     |             2 | -48.6%      | -28.7%     | SELL       |

## 2. Score Group Analysis (6M Horizon)
| Score_Group   | Avg Alpha   |   Count | Win Rate   |
|:--------------|:------------|--------:|:-----------|
| High (>8)     | 2.6%        |       2 | 100%       |
| Low (<5)      | -13.2%      |      27 | 11%        |
| Med (5-8)     | -34.7%      |       1 | 0%         |

## 3. Recall Analysis (Within Candidates)
Did the AI correctly identify the best performers in this batch?
**Top 5 Alpha Generators:**
| ticker   |   final_score | verdict    | Alpha_6M   |
|:---------|--------------:|:-----------|:-----------|
| MGPI     |             4 | HOLD       | 38.8%      |
| COKE     |             4 | SELL       | 14.3%      |
| MLI      |             2 | SELL       | 7.9%       |
| NVEE     |             8 | BUY        | 3.8%       |
| CLFD     |             9 | STRONG_BUY | 1.4%       |

## 4. Correlation Matrix (IC)
| Horizon   |   IC (vs Alpha) |   P-Value | Significant   |
|:----------|----------------:|----------:|:--------------|
| 3M        |           0.189 |     0.317 | No            |
| 6M        |           0.237 |     0.208 | No            |
| 1Y        |           0.513 |     0.004 | **Yes**       |
| MAX       |          -0.208 |     0.271 | No            |
