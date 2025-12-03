# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v8_final_validation
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 332
* **Dates Sampled:** 5
* **Win Rate:** 47.6%
* **Alpha Win Rate:** 39.8%
* **Avg Alpha:** -3.07%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -10.8%      | 1.4%        | 13.5%       | -10.0%     | 4.0%       | 14.7%      | -1.2%                |
| 6M        | -20.4%      | -1.5%       | 19.2%       | -14.9%     | 2.1%       | 25.2%      | -6.0%                |
| 1Y        | -25.7%      | -2.5%       | 27.7%       | -26.7%     | 3.0%       | 35.5%      | -7.8%                |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 3.14%        | -1.28%      | 54.2%      |
| 6M        | 2.58%        | -3.07%      | 47.6%      |
| 1Y        | 13.70%       | 5.15%       | 47.6%      |
| MAX       | 25.06%       | -8.37%      | 55.7%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-04-25      |      45 | -6.5%             | -9.2%            |
| 2020-04-25      |      50 | 45.0%             | 23.3%            |
| 2021-10-25      |      99 | -16.5%            | -7.9%            |
| 2022-10-25      |     102 | -2.0%             | -9.1%            |
| 2023-10-25      |      36 | 20.3%             | -1.6%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |              0.064 |    0.2481 | No             |
| 6M        |              0.101 |    0.0669 | No             |
| 1Y        |              0.164 |    0.0028 | **Yes**        |
| MAX       |              0.047 |    0.3927 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component         |     3M |     6M |     1Y |
|:------------------|-------:|-------:|-------:|
| growth_score      |  0.005 | -0.005 |  0.034 |
| improvement_score |  0.076 |  0.102 |  0.14  |
| value_score       |  0.107 |  0.058 | -0.03  |
| tech_score        | -0.022 |  0.031 |  0.111 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 0.25%        | -5.87%      |
| Middle 33% | -3.64%       | -8.89%      |
| Top 33%    | 11.01%       | 5.45%       |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| APPS     | 2020-04-25      |     90.2033 | 498.5%      | 476.8%     |
| SIG      | 2020-04-25      |     92.6556 | 223.1%      | 201.4%     |
| SQ       | 2020-04-25      |     92.8869 | 183.7%      | 162.0%     |
| ALGN     | 2020-04-25      |    100      | 136.1%      | 114.4%     |
| GPRO     | 2020-04-25      |     93      | 123.2%      | 101.5%     |
| TGLS     | 2022-10-25      |     77.7118 | 99.3%       | 92.1%      |
| NVDA     | 2023-10-25      |     79.364  | 110.0%      | 88.2%      |
| ARCH     | 2021-10-25      |     85.3762 | 63.6%       | 72.1%      |
| GES      | 2020-04-25      |     90.7285 | 90.8%       | 69.0%      |
| MERC     | 2021-10-25      |     79.6703 | 51.4%       | 59.9%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 72.99%              |
| 6M        | 162.37%             |
| 1Y        | 414.12%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 1.2% (3/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| APO      | 2019-04-25 | 27.4%       |
| XOM      | 2022-10-25 | 10.3%       |
| LNTH     | 2023-10-25 | -1.2%       |