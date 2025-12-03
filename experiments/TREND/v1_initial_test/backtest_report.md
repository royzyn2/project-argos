# Strategy Report Card: TREND (EVENT_LITE)
**Experiment Tag:** v1_initial_test
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 1325
* **Dates Sampled:** 5
* **Win Rate:** 48.6%
* **Alpha Win Rate:** 38.9%
* **Avg Alpha:** -5.76%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -3.8%       | 4.3%        | 12.3%       | -6.3%      | 2.5%       | 12.7%      | -0.5%                |
| 6M        | -17.2%      | -0.9%       | 15.2%       | -22.4%     | -4.6%      | 9.7%       | 5.5%                 |
| 1Y        | -26.2%      | -5.7%       | 14.6%       | -37.2%     | -9.9%      | 9.9%       | 4.7%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 4.63%        | -1.36%      | 63.1%      |
| 6M        | -0.12%       | -5.76%      | 48.6%      |
| 1Y        | -2.38%       | -5.97%      | 42.3%      |
| MAX       | 14.34%       | -9.18%      | 53.0%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-10-25      |     213 | -10.4%            | -5.2%            |
| 2021-04-25      |     293 | 5.3%              | -3.5%            |
| 2021-07-25      |     310 | -10.5%            | -10.2%           |
| 2022-10-25      |     198 | -2.6%             | -9.8%            |
| 2024-04-25      |     311 | 13.8%             | -1.3%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.022 |    0.4154 | No             |
| 6M        |             -0.016 |    0.5486 | No             |
| 1Y        |             -0.032 |    0.2433 | No             |
| MAX       |             -0.042 |    0.1265 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| tech_score   | -0.01  | -0.045 | -0.089 |
| growth_score |  0.008 |  0.026 | -0.014 |
| value_score  | -0.042 | -0.037 |  0.021 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 0.18%        | -4.93%      |
| Middle 33% | 0.21%        | -5.59%      |
| Top 33%    | -0.73%       | -6.76%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| TDOC     | 2019-10-25      |     83.2701 | 159.8%      | 165.1%     |
| TSLA     | 2019-10-25      |     77.9805 | 134.3%      | 139.6%     |
| ADMA     | 2024-04-25      |     86.2928 | 147.8%      | 132.7%     |
| DXCM     | 2019-10-25      |     79.167  | 112.7%      | 118.0%     |
| ELF      | 2022-10-25      |     85.1239 | 114.1%      | 107.0%     |
| SHOP     | 2019-10-25      |     80.7337 | 99.6%       | 104.9%     |
| ZETA     | 2024-04-25      |     80.5291 | 109.9%      | 94.8%      |
| MRNA     | 2021-04-25      |     82.5657 | 95.6%       | 86.7%      |
| PLTR     | 2024-04-25      |     84.1316 | 100.6%      | 85.6%      |
| PRFT     | 2021-04-25      |     69.7321 | 90.4%       | 81.6%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 77.79%              |
| 6M        | 116.49%             |
| 1Y        | 272.15%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 3.2% (8/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| PRFT     | 2021-04-25 | 90.4%       |
| MDP      | 2021-04-25 | 87.5%       |
| MDB      | 2021-04-25 | 66.4%       |
| CACC     | 2021-04-25 | 63.7%       |
| SIMO     | 2021-07-25 | 39.7%       |
| ELF      | 2022-10-25 | 114.1%      |
| ZETA     | 2024-04-25 | 109.9%      |
| MNDY     | 2024-04-25 | 60.5%       |