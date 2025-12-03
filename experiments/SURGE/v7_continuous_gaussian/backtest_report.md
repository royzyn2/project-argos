# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v7_continuous_gaussian
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 1813
* **Dates Sampled:** 5
* **Win Rate:** 48.7%
* **Alpha Win Rate:** 40.9%
* **Avg Alpha:** -3.73%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -5.9%       | 3.5%        | 14.5%       | -7.6%      | 2.1%       | 12.7%      | 1.7%                 |
| 6M        | -15.3%      | -0.7%       | 12.9%       | -18.4%     | -1.9%      | 9.7%       | 3.2%                 |
| 1Y        | -26.4%      | -2.9%       | 20.2%       | -32.8%     | -9.3%      | 12.4%      | 7.8%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 5.20%        | -0.04%      | 60.7%      |
| 6M        | -0.03%       | -3.73%      | 48.7%      |
| 1Y        | 0.85%        | -10.21%     | 46.1%      |
| MAX       | 27.52%       | -10.71%     | 62.5%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-04-25      |     388 | -0.8%             | -3.5%            |
| 2019-07-25      |     265 | 3.5%              | -6.2%            |
| 2022-10-25      |     390 | 2.2%              | -5.0%            |
| 2023-04-25      |     412 | 1.0%              | -3.3%            |
| 2024-10-25      |     358 | -5.3%             | -1.2%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.068 |    0.0037 | **Yes**        |
| 6M        |              0.052 |    0.0263 | **Yes**        |
| 1Y        |             -0.051 |    0.0298 | **Yes**        |
| MAX       |              0.002 |    0.9203 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| growth_score | -0.041 | -0.041 | -0.004 |
| value_score  |  0.045 |  0.101 | -0.022 |
| tech_score   | -0.081 |  0.037 | -0.047 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | -0.41%       | -4.03%      |
| Middle 33% | -0.78%       | -4.17%      |
| Top 33%    | 1.12%        | -2.99%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| SMCI     | 2023-04-25      |     89.7838 | 181.5%      | 177.1%     |
| DAVE     | 2024-10-25      |     86.0531 | 144.8%      | 148.9%     |
| PLTR     | 2023-04-25      |     86.9398 | 115.0%      | 110.7%     |
| ELF      | 2022-10-25      |     86.0989 | 114.1%      | 107.0%     |
| ARWR     | 2019-04-25      |     92.9836 | 108.1%      | 105.5%     |
| MOD      | 2023-04-25      |     83.1472 | 101.9%      | 97.6%      |
| ACLS     | 2022-10-25      |     84.6521 | 101.2%      | 94.0%      |
| TGLS     | 2022-10-25      |     89.5833 | 99.3%       | 92.1%      |
| IAS      | 2022-10-25      |     92.8918 | 98.8%       | 91.6%      |
| VNET     | 2024-10-25      |     91.0544 | 86.6%       | 90.8%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 118.72%             |
| 6M        | 115.13%             |
| 1Y        | 318.56%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 10.4% (26/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| ZYME     | 2019-04-25 | 77.8%       |
| PODD     | 2019-04-25 | 76.1%       |
| MDC      | 2019-04-25 | 49.2%       |
| DHT      | 2019-04-25 | 49.0%       |
| SKY      | 2019-04-25 | 48.6%       |
| MTH      | 2019-04-25 | 46.2%       |
| ARMK     | 2019-04-25 | 43.9%       |
| RGEN     | 2019-04-25 | 39.3%       |
| IBP      | 2019-04-25 | 38.3%       |
| ELF      | 2022-10-25 | 114.1%      |
| ACLS     | 2022-10-25 | 101.2%      |
| TGLS     | 2022-10-25 | 99.3%       |
| GE       | 2022-10-25 | 72.2%       |
| GRBK     | 2022-10-25 | 64.2%       |
| CNR      | 2023-04-25 | 80.1%       |
| MNSO     | 2023-04-25 | 73.3%       |
| MMYT     | 2023-04-25 | 70.8%       |
| YELP     | 2023-04-25 | 50.4%       |
| UBER     | 2023-04-25 | 49.3%       |
| OII      | 2023-04-25 | 45.5%       |
| NFLX     | 2024-10-25 | 50.0%       |
| ATGE     | 2024-10-25 | 47.3%       |
| BYRN     | 2024-10-25 | 45.1%       |
| KGC      | 2024-10-25 | 40.2%       |
| CHWY     | 2024-10-25 | 39.1%       |
| COMP     | 2024-10-25 | 36.9%       |