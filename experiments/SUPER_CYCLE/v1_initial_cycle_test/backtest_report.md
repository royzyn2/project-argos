# Strategy Report Card: SUPER_CYCLE (EVENT_LITE)
**Experiment Tag:** v1_initial_cycle_test
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 217
* **Dates Sampled:** 5
* **Win Rate:** 44.7%
* **Alpha Win Rate:** 44.7%
* **Avg Alpha:** -1.28%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -17.1%      | -6.8%       | 3.3%        | -12.6%     | 0.9%       | 11.4%      | -8.1%                |
| 6M        | -17.2%      | -2.9%       | 14.0%       | -13.2%     | 4.8%       | 21.5%      | -7.4%                |
| 1Y        | -27.4%      | -0.4%       | 23.7%       | -24.5%     | 0.6%       | 26.8%      | -3.1%                |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | -5.35%       | -3.92%      | 31.8%      |
| 6M        | -1.37%       | -1.28%      | 44.7%      |
| 1Y        | 1.38%        | -3.02%      | 49.3%      |
| MAX       | 9.54%        | -10.11%     | 53.5%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2021-10-25      |     103 | -15.3%            | -6.7%            |
| 2022-07-25      |      79 | 0.7%              | -0.5%            |
| 2023-10-25      |      35 | 34.9%             | 13.1%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.125 |    0.0652 | No             |
| 6M        |             -0.105 |    0.1232 | No             |
| 1Y        |             -0.117 |    0.0851 | No             |
| MAX       |             -0.106 |    0.1201 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component       |     3M |     6M |     1Y |
|:----------------|-------:|-------:|-------:|
| stability_score | -0.126 | -0.195 | -0.212 |
| growth_score    | -0.017 |  0.032 |  0.056 |
| value_score     |  0.041 |  0.147 |  0.127 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | -0.10%       | -0.86%      |
| Middle 33% | 2.34%        | 1.33%       |
| Top 33%    | -6.37%       | -4.32%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| SMCI     | 2023-10-25      |     79.6828 | 237.6%      | 215.7%     |
| AAON     | 2023-10-25      |     72.0576 | 70.9%       | 49.1%      |
| ONTO     | 2023-10-25      |     73.9084 | 70.7%       | 48.9%      |
| WIRE     | 2023-10-25      |     78.4821 | 62.8%       | 40.9%      |
| WIRE     | 2022-07-25      |     73.5545 | 37.8%       | 36.5%      |
| AVGO     | 2023-10-25      |     71.002  | 58.2%       | 36.4%      |
| BCC      | 2023-10-25      |     78.541  | 55.6%       | 33.8%      |
| NEM      | 2021-10-25      |     70.754  | 24.6%       | 33.1%      |
| APD      | 2022-07-25      |     77.9695 | 33.2%       | 32.0%      |
| MLI      | 2023-10-25      |     79.6684 | 53.7%       | 31.8%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 41.20%              |
| 6M        | 73.05%              |
| 1Y        | 95.03%              |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 0.0% (0/250)

*No Top 50 winners were captured by the strategy.*