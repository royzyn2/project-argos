# Strategy Report Card: TREND (EVENT_LITE)
**Experiment Tag:** v3_risk_adj_mom
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 1321
* **Dates Sampled:** 5
* **Win Rate:** 32.2%
* **Alpha Win Rate:** 42.2%
* **Avg Alpha:** -2.98%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -9.7%       | -0.8%       | 9.2%        | -14.4%     | -2.2%      | 7.3%       | 2.0%                 |
| 6M        | -23.2%      | -9.0%       | 4.9%        | -32.2%     | -12.9%     | 1.7%       | 3.2%                 |
| 1Y        | -25.9%      | -9.6%       | 9.2%        | -38.4%     | -13.4%     | 9.0%       | 0.2%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | -0.41%       | -1.08%      | 47.2%      |
| 6M        | -8.69%       | -2.98%      | 32.2%      |
| 1Y        | -4.03%       | -4.60%      | 36.1%      |
| MAX       | 8.71%        | -5.17%      | 48.0%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-10-25      |     224 | -12.6%            | -7.3%            |
| 2021-07-25      |     261 | -5.9%             | -5.6%            |
| 2021-10-25      |     294 | -17.7%            | -9.1%            |
| 2022-04-25      |     205 | -8.9%             | 2.8%             |
| 2024-10-25      |     337 | -0.4%             | 3.8%             |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.002 |    0.9281 | No             |
| 6M        |              0.055 |    0.047  | **Yes**        |
| 1Y        |              0.006 |    0.8407 | No             |
| MAX       |              0     |    0.9914 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| tech_score   | -0.031 |  0.056 |  0.002 |
| growth_score | -0.009 | -0.016 |  0.008 |
| value_score  |  0.04  |  0.035 | -0.004 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | -10.43%      | -4.72%      |
| Middle 33% | -8.10%       | -2.57%      |
| Top 33%    | -7.54%       | -1.65%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| PLTR     | 2024-10-25      |     90.3542 | 164.0%      | 168.1%     |
| TDOC     | 2019-10-25      |     74.0846 | 159.8%      | 165.1%     |
| TSLA     | 2019-10-25      |     71.7148 | 134.3%      | 139.6%     |
| DXCM     | 2019-10-25      |     72.6917 | 112.7%      | 118.0%     |
| SHOP     | 2019-10-25      |     75.1836 | 99.6%       | 104.9%     |
| HOOD     | 2024-10-25      |     73.5845 | 81.5%       | 85.6%      |
| ITCI     | 2024-10-25      |     72.0892 | 73.9%       | 78.1%      |
| BROS     | 2024-10-25      |     74.0547 | 68.1%       | 72.3%      |
| DINO     | 2022-04-25      |     66.4695 | 60.3%       | 71.9%      |
| TPL      | 2022-04-25      |     67.753  | 58.2%       | 69.8%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 73.96%              |
| 6M        | 101.50%             |
| 1Y        | 284.79%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 5.6% (14/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| VIPS     | 2019-10-25 | 42.5%       |
| MATX     | 2021-07-25 | 39.8%       |
| CF       | 2021-10-25 | 60.7%       |
| CRK      | 2021-10-25 | 52.1%       |
| FHN      | 2021-10-25 | 34.4%       |
| BG       | 2021-10-25 | 30.0%       |
| TRGP     | 2021-10-25 | 29.5%       |
| DINO     | 2022-04-25 | 60.3%       |
| TPL      | 2022-04-25 | 58.2%       |
| PLTR     | 2024-10-25 | 164.0%      |
| RBLX     | 2024-10-25 | 59.1%       |
| LMND     | 2024-10-25 | 58.5%       |
| CORT     | 2024-10-25 | 52.0%       |
| HWM      | 2024-10-25 | 36.7%       |