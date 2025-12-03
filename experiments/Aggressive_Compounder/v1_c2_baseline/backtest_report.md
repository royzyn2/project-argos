# Strategy Report Card: Aggressive_Compounder (EVENT_LITE)
**Experiment Tag:** v1_c2_baseline
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 1555
* **Dates Sampled:** 5
* **Win Rate:** 59.4%
* **Alpha Win Rate:** 41.5%
* **Avg Alpha:** -3.28%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -7.4%       | 1.9%        | 10.6%       | -11.6%     | -1.4%      | 8.2%       | 2.4%                 |
| 6M        | -9.8%       | 4.5%        | 17.8%       | -17.8%     | -2.4%      | 11.5%      | 6.3%                 |
| 1Y        | -21.0%      | -0.5%       | 20.5%       | -32.5%     | -6.5%      | 15.1%      | 5.4%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 2.11%        | -2.21%      | 56.1%      |
| 6M        | 5.24%        | -3.28%      | 59.4%      |
| 1Y        | 3.21%        | -5.62%      | 49.4%      |
| MAX       | 24.70%       | -5.17%      | 60.1%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-07-25      |     289 | 6.3%              | -3.4%            |
| 2019-10-25      |     237 | -10.1%            | -4.8%            |
| 2021-04-25      |     386 | 4.1%              | -4.8%            |
| 2023-07-25      |     168 | 3.6%              | -2.9%            |
| 2024-04-25      |     475 | 13.7%             | -1.4%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |              0.002 |    0.9242 | No             |
| 6M        |              0.128 |    0      | **Yes**        |
| 1Y        |              0.091 |    0.0003 | **Yes**        |
| MAX       |              0.026 |    0.3116 | No             |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 2.00%        | -4.92%      |
| Middle 33% | 4.64%        | -3.54%      |
| Top 33%    | 9.08%        | -1.37%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| SMR      | 2024-04-25      |     24.1308 | 212.2%      | 197.1%     |
| PCT      | 2024-04-25      |     43.1245 | 183.2%      | 168.1%     |
| TDOC     | 2019-10-25      |     36.8192 | 159.8%      | 165.1%     |
| TSLA     | 2019-10-25      |     34.1949 | 134.3%      | 139.6%     |
| ADMA     | 2024-04-25      |     82.695  | 147.8%      | 132.7%     |
| APLS     | 2023-07-25      |     37.6741 | 120.1%      | 113.5%     |
| ZETA     | 2024-04-25      |     71.3364 | 109.9%      | 94.8%      |
| CRWD     | 2023-07-25      |     77.6273 | 98.9%       | 92.3%      |
| ZYME     | 2019-07-25      |     68.9357 | 95.5%       | 85.8%      |
| PLTR     | 2024-04-25      |     72.6873 | 100.6%      | 85.6%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 88.47%              |
| 6M        | 136.63%             |
| 1Y        | 279.43%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 5.2% (13/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| PODD     | 2019-07-25 | 56.1%       |
| CACC     | 2021-04-25 | 63.7%       |
| VICR     | 2021-04-25 | 59.9%       |
| CAMT     | 2023-07-25 | 79.2%       |
| PCT      | 2024-04-25 | 183.2%      |
| ADMA     | 2024-04-25 | 147.8%      |
| ZETA     | 2024-04-25 | 109.9%      |
| AGX      | 2024-04-25 | 99.4%       |
| PTGX     | 2024-04-25 | 90.4%       |
| MSTR     | 2024-04-25 | 90.2%       |
| VST      | 2024-04-25 | 73.3%       |
| TGTX     | 2024-04-25 | 66.9%       |
| IESC     | 2024-04-25 | 64.8%       |