# Strategy Report Card: TREND (EVENT_LITE)
**Experiment Tag:** v1_trend_baseline
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 1097
* **Dates Sampled:** 5
* **Win Rate:** 46.2%
* **Alpha Win Rate:** 41.7%
* **Avg Alpha:** -2.79%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -9.1%       | 0.7%        | 11.2%       | -8.9%      | 2.8%       | 14.3%      | -3.1%                |
| 6M        | -17.5%      | -2.1%       | 12.2%       | -17.7%     | 2.3%       | 18.4%      | -6.2%                |
| 1Y        | -21.8%      | -3.7%       | 16.2%       | -28.1%     | -0.8%      | 20.2%      | -4.0%                |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 3.21%        | 2.55%       | 51.5%      |
| 6M        | -1.00%       | -2.79%      | 46.2%      |
| 1Y        | -0.33%       | -4.48%      | 45.4%      |
| MAX       | 8.13%        | -13.69%     | 50.0%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2020-10-25      |     168 | 24.5%             | 3.7%             |
| 2021-07-25      |     310 | -10.5%            | -10.2%           |
| 2022-04-25      |     263 | -8.9%             | 2.7%             |
| 2022-07-25      |     158 | 5.8%              | 4.5%             |
| 2022-10-25      |     198 | -2.6%             | -9.8%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.063 |    0.0367 | **Yes**        |
| 6M        |             -0.053 |    0.0809 | No             |
| 1Y        |             -0.02  |    0.4994 | No             |
| MAX       |              0.033 |    0.2738 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| tech_score   | -0.038 | -0.112 | -0.078 |
| growth_score | -0.005 | -0.052 | -0.029 |
| value_score  | -0.074 |  0.048 |  0.05  |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 0.83%        | -1.22%      |
| Middle 33% | -0.23%       | -2.82%      |
| Top 33%    | -3.60%       | -4.33%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| BILI     | 2020-10-25      |     80.4011 | 170.4%      | 149.6%     |
| ELF      | 2022-10-25      |     85.1239 | 114.1%      | 107.0%     |
| APPS     | 2020-10-25      |     79.0752 | 122.0%      | 101.2%     |
| BRKS     | 2020-10-25      |     73.9821 | 116.7%      | 95.9%      |
| DQ       | 2020-10-25      |     80.0038 | 116.1%      | 95.3%      |
| CLF      | 2020-10-25      |     76.6917 | 115.6%      | 94.8%      |
| EGHT     | 2020-10-25      |     78.6589 | 109.3%      | 88.5%      |
| PBF      | 2022-04-25      |     81.0194 | 68.1%       | 79.7%      |
| CVI      | 2022-04-25      |     77.0216 | 63.8%       | 75.5%      |
| UMC      | 2020-10-25      |     73.8862 | 93.9%       | 73.1%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 146.25%             |
| 6M        | 113.94%             |
| 1Y        | 212.18%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 2.0% (5/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| BILI     | 2020-10-25 | 170.4%      |
| SIMO     | 2021-07-25 | 39.7%       |
| CVI      | 2022-04-25 | 63.8%       |
| ELF      | 2022-07-25 | 66.7%       |
| ELF      | 2022-10-25 | 114.1%      |