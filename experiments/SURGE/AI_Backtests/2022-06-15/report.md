# AI Backtest Report: SURGE
**Snapshot Date:** 2022-06-15
**Benchmark:** SPX

## 1. AI Score vs Future Returns (Multi-Horizon)
| ticker   |   final_score | verdict    | Return_3M   | Return_6M   | Return_1Y   | Return_MAX   |
|:---------|--------------:|:-----------|:------------|:------------|:------------|:-------------|
| DMLP     |             9 | BUY        | -0.1%       | -3.3%       | 1.4%        | 6.8%         |
| HUBG     |             9 | STRONG_BUY | 2.1%        | 10.1%       | 9.1%        | 17.1%        |
| WRB      |             8 | BUY        | 1.1%        | 8.9%        | -11.5%      | 19.7%        |
| ABG      |             8 | BUY        | -8.0%       | 2.6%        | 28.2%       | 34.8%        |
| DLO      |             8 | BUY        | 5.4%        | -43.3%      | -49.5%      | -70.6%       |
| CNM      |             8 | BUY        | 11.5%       | -11.5%      | 27.3%       | 130.5%       |
| RUSHA    |             8 | BUY        | -9.0%       | 0.7%        | 17.7%       | 28.2%        |
| LCII     |             8 | BUY        | -0.3%       | -14.9%      | 8.2%        | -9.7%        |
| KOF      |             8 | BUY        | 10.9%       | 19.8%       | 58.0%       | 53.2%        |
| BCH      |             8 | BUY        | -6.8%       | -2.0%       | 6.9%        | 15.2%        |
| CCU      |             8 | BUY        | -19.9%      | -8.1%       | 21.2%       | -11.3%       |
| DOOR     |             8 | BUY        | -8.3%       | -7.8%       | 21.0%       | 62.8%        |
| UMC      |             8 | BUY        | -24.4%      | -14.0%      | 4.2%        | 6.0%         |
| MGPI     |             8 | BUY        | 18.9%       | 21.5%       | 7.8%        | -23.0%       |
| TECK     |             8 | BUY        | -19.6%      | -6.3%       | 4.3%        | 17.9%        |
| MBUU     |             8 | BUY        | 3.1%        | 4.9%        | 7.5%        | -33.4%       |
| FCNCA    |             8 | BUY        | 34.9%       | 18.2%       | 103.6%      | 160.2%       |
| TTE      |             8 | BUY        | -10.5%      | 8.4%        | 3.7%        | 19.1%        |
| CCEP     |             8 | BUY        | -7.2%       | 7.6%        | 27.9%       | 43.2%        |
| TTC      |             8 | BUY        | 13.4%       | 43.0%       | 22.4%       | 22.6%        |
| CTS      |             8 | BUY        | 16.6%       | 7.2%        | 20.9%       | 38.9%        |
| HUBB     |             8 | BUY        | 21.2%       | 37.0%       | 76.4%       | 113.4%       |
| VIVO     |             8 | BUY        | 18.4%       | 21.4%       | 25.3%       | 25.3%        |
| LFUS     |             8 | BUY        | -14.7%      | -9.0%       | 6.3%        | 2.9%         |
| T        |             7 | HOLD       | -13.8%      | -2.8%       | -17.4%      | -7.2%        |
| ENVX     |             7 | BUY        | 121.7%      | 2.8%        | 37.0%       | 12.9%        |
| BKI      |             7 | HOLD       | 4.7%        | -6.2%       | -11.1%      | 17.4%        |
| OHI      |             6 | HOLD       | 7.5%        | 4.0%        | 9.7%        | 15.5%        |
| NABL     |             0 | BUY        | -4.1%       | 5.3%        | 38.2%       | 35.3%        |
| PGTI     |             0 | BUY        | 14.3%       | 6.1%        | 57.2%       | 137.4%       |

## 2. Score Group Analysis (6M Horizon)
| Score_Group   | Avg Ret 3M   | Avg Ret 6M   | Avg Ret 1Y   | Avg Ret MAX   |
|:--------------|:-------------|:-------------|:-------------|:--------------|
| High (>8)     | 1.2%         | 3.8%         | 18.7%        | 27.9%         |
| Low (<5)      | 5.1%         | 5.7%         | 47.7%        | 86.3%         |
| Med (5-8)     | 30.0%        | -0.6%        | 4.5%         | 9.6%          |

## 3. Recall Analysis (Within Candidates)
Did the AI correctly identify the best performers in this batch?
**Top 5 Alpha Generators:**
| ticker   |   final_score | verdict   | Alpha_6M   |
|:---------|--------------:|:----------|:-----------|
| TTC      |             8 | BUY       | 37.5%      |
| HUBB     |             8 | BUY       | 31.6%      |
| MGPI     |             8 | BUY       | 16.0%      |
| VIVO     |             8 | BUY       | 15.9%      |
| KOF      |             8 | BUY       | 14.4%      |

## 4. Correlation Matrix (IC)
| Horizon   |   IC (vs Alpha) |   P-Value | Significant   |
|:----------|----------------:|----------:|:--------------|
| 3M        |          -0.068 |     0.721 | No            |
| 6M        |          -0.024 |     0.902 | No            |
| 1Y        |          -0.245 |     0.192 | No            |
| MAX       |          -0.284 |     0.129 | No            |
