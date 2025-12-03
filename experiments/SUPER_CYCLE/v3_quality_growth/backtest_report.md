# Strategy Report Card: SUPER_CYCLE (CALENDAR)
**Experiment Tag:** v3_quality_growth
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 1071
* **Dates Sampled:** 20
* **Win Rate:** 59.3%
* **Alpha Win Rate:** 44.7%
* **Avg Alpha:** -1.34%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -6.0%       | 2.5%        | 12.8%       | -9.0%      | 1.1%       | 11.4%      | 1.4%                 |
| 6M        | -9.1%       | 5.1%        | 17.9%       | -13.9%     | 2.0%       | 16.8%      | 1.2%                 |
| 1Y        | -16.3%      | 3.8%        | 27.4%       | -24.1%     | 0.5%       | 22.4%      | 5.0%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 4.04%        | -0.64%      | 58.7%      |
| 6M        | 5.36%        | -1.34%      | 59.3%      |
| 1Y        | 7.06%        | -7.52%      | 54.2%      |
| MAX       | 4.95%        | -12.82%     | 48.1%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2021-01-05      |     100 | 13.6%             | -3.3%            |
| 2021-03-25      |     100 | 8.7%              | -5.1%            |
| 2021-03-29      |     100 | 7.9%              | -3.9%            |
| 2021-06-08      |     100 | 3.6%              | -5.0%            |
| 2021-07-27      |     100 | -4.9%             | -3.8%            |
| 2022-05-06      |      71 | -5.3%             | 3.3%             |
| 2023-06-16      |     100 | 10.0%             | 3.0%             |
| 2023-08-30      |     100 | 15.4%             | 1.6%             |
| 2023-09-18      |     100 | 16.6%             | 0.3%             |
| 2024-10-09      |     100 | -9.4%             | -2.0%            |
| 2024-11-05      |     100 | -0.3%             | 1.8%             |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.005 |    0.8586 | No             |
| 6M        |              0.005 |    0.8668 | No             |
| 1Y        |             -0.031 |    0.3129 | No             |
| MAX       |             -0.026 |    0.3959 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component     |     3M |     6M |     1Y |
|:--------------|-------:|-------:|-------:|
| growth_score  |  0.013 | -0.024 | -0.085 |
| quality_score |  0.057 |  0.025 |  0.011 |
| value_score   | -0.082 |  0.012 |  0.041 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 5.03%        | -0.82%      |
| Middle 33% | 5.64%        | -1.51%      |
| Top 33%    | 5.40%        | -1.68%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| SMCI     | 2023-09-18      |    100      | 272.9%      | 256.6%     |
| SMCI     | 2023-08-30      |    100      | 238.0%      | 224.2%     |
| HIMS     | 2024-11-05      |    100      | 151.7%      | 153.9%     |
| CELH     | 2021-03-25      |     84      | 115.8%      | 102.0%     |
| TPL      | 2022-05-06      |     82      | 80.2%       | 88.8%      |
| NVDA     | 2023-09-18      |     95.8167 | 103.3%      | 87.0%      |
| IMGN     | 2023-09-18      |     90      | 98.8%       | 82.5%      |
| IMGN     | 2023-08-30      |     90      | 96.0%       | 82.3%      |
| TGTX     | 2024-10-09      |    100      | 67.6%       | 75.0%      |
| IBP      | 2023-09-18      |     95.3642 | 88.4%       | 72.2%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 75.10%              |
| 6M        | 133.14%             |
| 1Y        | 167.13%             |

### Recall Analysis (The Munger Metric)
Of the Top 1000 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 1.3% (13/1000)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| CELH     | 2021-03-25 | 115.8%      |
| NVDA     | 2021-03-29 | 67.3%       |
| NVDA     | 2021-06-08 | 72.1%       |
| WTFC     | 2021-07-27 | 38.8%       |
| TPL      | 2022-05-06 | 80.2%       |
| CEIX     | 2023-06-16 | 49.9%       |
| NVDA     | 2023-09-18 | 103.3%      |
| IBP      | 2023-09-18 | 88.4%       |
| BPMC     | 2023-09-18 | 68.6%       |
| AGI      | 2024-10-09 | 52.4%       |
| AEM      | 2024-10-09 | 50.5%       |
| NET      | 2024-11-05 | 50.9%       |
| KGC      | 2024-11-05 | 50.1%       |