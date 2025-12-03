# Strategy Report Card: TREND (EVENT_LITE)
**Experiment Tag:** v2_pullback_optimized
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 68
* **Dates Sampled:** 5
* **Win Rate:** 35.3%
* **Alpha Win Rate:** 36.8%
* **Avg Alpha:** -0.18%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -14.1%      | -1.4%       | 11.3%       | -7.9%      | 3.4%       | 15.1%      | -3.9%                |
| 6M        | -25.8%      | -11.1%      | 14.3%       | -16.2%     | 0.8%       | 18.5%      | -4.2%                |
| 1Y        | -18.0%      | 6.5%        | 26.5%       | -23.4%     | 1.5%       | 26.2%      | 0.3%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 1.27%        | 0.25%       | 48.5%      |
| 6M        | -0.39%       | -0.18%      | 35.3%      |
| 1Y        | 15.48%       | 3.12%       | 57.4%      |
| MAX       | 40.03%       | 4.66%       | 67.6%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-10-25      |      22 | -22.0%            | -16.7%           |
| 2020-10-25      |       8 | 64.6%             | 43.8%            |
| 2022-04-25      |      12 | -23.9%            | -12.3%           |
| 2022-07-25      |      23 | 10.3%             | 9.0%             |
| 2024-04-25      |       3 | -3.2%             | -18.3%           |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |              0.064 |    0.6064 | No             |
| 6M        |              0.065 |    0.599  | No             |
| 1Y        |              0.155 |    0.2062 | No             |
| MAX       |              0.115 |    0.3517 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |      3M |      6M |      1Y |
|:-------------|--------:|--------:|--------:|
| tech_score   | nan     | nan     | nan     |
| growth_score |  -0.012 |   0.148 |   0.063 |
| value_score  |   0.069 |  -0.07  |   0.087 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | -5.15%       | -2.68%      |
| Middle 33% | 6.22%        | 4.90%       |
| Top 33%    | -1.45%       | -2.20%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| WAL      | 2020-10-25      |     69.0978 | 156.3%      | 135.5%     |
| EGHT     | 2020-10-25      |     68      | 109.3%      | 88.5%      |
| ACLS     | 2022-07-25      |     74.0952 | 68.6%       | 67.4%      |
| ELF      | 2022-07-25      |     70.5714 | 66.7%       | 65.5%      |
| ABCB     | 2020-10-25      |     74.0952 | 79.0%       | 58.1%      |
| SRPT     | 2022-07-25      |     68      | 54.3%       | 53.0%      |
| GBCI     | 2020-10-25      |     71.2272 | 64.6%       | 43.7%      |
| VRTX     | 2019-10-25      |     71.0476 | 32.1%       | 37.4%      |
| HIMS     | 2022-07-25      |     68      | 30.2%       | 28.9%      |
| SILK     | 2022-07-25      |     67.0476 | 29.5%       | 28.2%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 40.55%              |
| 6M        | 69.41%              |
| 1Y        | 114.03%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 0.8% (2/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| ACLS     | 2022-07-25 | 68.6%       |
| SRPT     | 2022-07-25 | 54.3%       |