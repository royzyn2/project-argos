# Strategy Report Card: SUPER_CYCLE (CALENDAR)
**Experiment Tag:** v2_calendar_robustness
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 686
* **Dates Sampled:** 20
* **Win Rate:** 64.1%
* **Alpha Win Rate:** 47.5%
* **Avg Alpha:** 0.11%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -4.4%       | 3.4%        | 12.1%       | -9.1%      | 1.9%       | 12.5%      | -0.4%                |
| 6M        | -5.6%       | 5.5%        | 17.8%       | -14.9%     | 1.3%       | 17.1%      | 0.7%                 |
| 1Y        | -13.2%      | 2.0%        | 19.5%       | -23.9%     | 1.1%       | 23.2%      | -3.8%                |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 3.86%        | 1.64%       | 59.3%      |
| 6M        | 6.38%        | 0.11%       | 64.1%      |
| 1Y        | 4.52%        | -2.82%      | 54.4%      |
| MAX       | 11.57%       | -8.65%      | 57.4%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2021-02-24      |     100 | 15.8%             | 1.5%             |
| 2021-04-14      |     100 | 8.6%              | 3.1%             |
| 2021-07-15      |      99 | 5.9%              | -2.5%            |
| 2022-04-28      |     100 | -14.1%            | -2.9%            |
| 2022-07-27      |      82 | -0.3%             | -1.2%            |
| 2022-11-29      |      56 | 3.4%              | -3.2%            |
| 2023-06-28      |      41 | 11.4%             | 2.1%             |
| 2024-01-03      |      37 | 23.7%             | 5.4%             |
| 2024-01-09      |      38 | 21.6%             | 4.1%             |
| 2024-04-12      |      33 | 13.2%             | -0.3%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.029 |    0.4483 | No             |
| 6M        |             -0.043 |    0.2606 | No             |
| 1Y        |             -0.102 |    0.0076 | **Yes**        |
| MAX       |             -0.114 |    0.0028 | **Yes**        |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component       |     3M |     6M |     1Y |
|:----------------|-------:|-------:|-------:|
| stability_score | -0.003 |  0.01  | -0.106 |
| growth_score    |  0.025 | -0.018 | -0.024 |
| value_score     | -0.075 | -0.072 |  0.052 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 8.49%        | 1.12%       |
| Middle 33% | 5.61%        | 0.26%       |
| Top 33%    | 5.05%        | -1.03%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| SMCI     | 2024-01-03      |     73.3862 | 201.7%      | 183.4%     |
| SMCI     | 2024-01-09      |     73.4041 | 158.7%      | 141.3%     |
| EPAM     | 2021-02-24      |     87.6866 | 71.5%       | 57.2%      |
| SFM      | 2024-01-03      |     70.5386 | 72.4%       | 54.1%      |
| SPSC     | 2021-04-14      |     72.4099 | 56.7%       | 51.2%      |
| QLYS     | 2023-06-28      |     71.1902 | 60.4%       | 51.2%      |
| SFM      | 2024-01-09      |     70.7997 | 68.0%       | 50.6%      |
| AMD      | 2021-07-15      |     77.5131 | 58.1%       | 49.7%      |
| ONTO     | 2024-01-03      |     74.3998 | 64.6%       | 46.3%      |
| WST      | 2021-02-24      |     82.7189 | 59.9%       | 45.6%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 73.41%              |
| 6M        | 87.63%              |
| 1Y        | 114.31%             |

### Recall Analysis (The Munger Metric)
Of the Top 1000 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 0.1% (1/1000)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| WST      | 2021-02-24 | 59.9%       |