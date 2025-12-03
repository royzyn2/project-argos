# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v4_lite_optimized
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 827
* **Dates Sampled:** 5
* **Win Rate:** 46.6%
* **Alpha Win Rate:** 36.9%
* **Avg Alpha:** -1.33%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -9.5%       | -0.8%       | 10.7%       | -10.1%     | -0.3%      | 9.7%       | 1.0%                 |
| 6M        | -17.1%      | -2.2%       | 14.8%       | -20.2%     | -4.1%      | 12.9%      | 1.9%                 |
| 1Y        | -24.3%      | -3.6%       | 20.0%       | -25.9%     | -0.0%      | 25.0%      | -5.0%                |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 1.93%        | -2.08%      | 48.4%      |
| 6M        | 2.70%        | -1.33%      | 46.6%      |
| 1Y        | 6.62%        | -3.76%      | 45.7%      |
| MAX       | 8.43%        | -4.43%      | 44.3%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-10-25      |      94 | -20.1%            | -14.9%           |
| 2020-07-25      |     124 | 35.7%             | 15.8%            |
| 2021-04-25      |     362 | 4.2%              | -4.6%            |
| 2022-04-25      |     109 | -11.7%            | -0.1%            |
| 2024-10-25      |     138 | -4.1%             | 0.0%             |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.01  |    0.7806 | No             |
| 6M        |              0.004 |    0.8981 | No             |
| 1Y        |             -0.001 |    0.9735 | No             |
| MAX       |             -0.011 |    0.742  | No             |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 2.12%        | -1.29%      |
| Middle 33% | 6.97%        | 2.65%       |
| Top 33%    | 2.97%        | -2.15%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| APPS     | 2020-07-25      |     93      | 430.8%      | 410.9%     |
| CELH     | 2020-07-25      |     85      | 350.0%      | 330.1%     |
| DQ       | 2020-07-25      |     85      | 342.8%      | 322.9%     |
| FUTU     | 2020-07-25      |    100      | 256.6%      | 236.7%     |
| PLTR     | 2024-10-25      |     93      | 164.0%      | 168.1%     |
| SID      | 2020-07-25      |     93      | 172.6%      | 152.7%     |
| CSIQ     | 2020-07-25      |     93.3447 | 166.2%      | 146.3%     |
| MTLS     | 2020-07-25      |     93      | 156.4%      | 136.5%     |
| VRTV     | 2021-04-25      |     89.506  | 144.8%      | 136.0%     |
| QURE     | 2024-10-25      |     95      | 125.7%      | 129.8%     |