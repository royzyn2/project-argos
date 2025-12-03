# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v6_lite_techrefine
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 484
* **Dates Sampled:** 5
* **Win Rate:** 67.1%
* **Alpha Win Rate:** 47.5%
* **Avg Alpha:** 7.81%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -4.6%       | 6.6%        | 25.0%       | -1.1%      | 9.6%       | 24.3%      | 0.7%                 |
| 6M        | -4.1%       | 14.9%       | 43.7%       | -3.1%      | 14.8%      | 37.6%      | 6.1%                 |
| 1Y        | -4.2%       | 22.3%       | 57.6%       | -4.0%      | 25.3%      | 56.7%      | 0.9%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 13.27%       | 2.89%       | 66.1%      |
| 6M        | 25.68%       | 7.81%       | 67.1%      |
| 1Y        | 45.42%       | 12.97%      | 69.8%      |
| MAX       | 28.83%       | -0.08%      | 57.9%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2020-04-25      |     106 | 25.0%             | 3.3%             |
| 2020-07-25      |     118 | 36.4%             | 16.5%            |
| 2020-10-25      |     127 | 42.1%             | 21.3%            |
| 2023-04-25      |      61 | -6.1%             | -10.5%           |
| 2024-04-25      |      72 | 7.1%              | -8.0%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |              0.016 |    0.7326 | No             |
| 6M        |             -0.047 |    0.3044 | No             |
| 1Y        |             -0.081 |    0.0751 | No             |
| MAX       |             -0.076 |    0.0959 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| growth_score |  0.043 |  0.016 | -0.001 |
| value_score  | -0.013 | -0.004 | -0.023 |
| tech_score   |  0.005 | -0.083 | -0.106 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 30.12%       | 11.59%      |
| Middle 33% | 20.20%       | 3.03%       |
| Top 33%    | 26.72%       | 8.84%       |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| APPS     | 2020-07-25      |     83      | 430.8%      | 410.9%     |
| CELH     | 2020-07-25      |     83      | 350.0%      | 330.1%     |
| DQ       | 2020-07-25      |     83      | 342.8%      | 322.9%     |
| FUTU     | 2020-10-25      |     91.2228 | 341.3%      | 320.5%     |
| FUTU     | 2020-07-25      |     90      | 256.6%      | 236.7%     |
| PLUG     | 2020-04-25      |     90      | 240.0%      | 218.3%     |
| GME      | 2020-04-25      |     83      | 213.4%      | 191.7%     |
| TSLA     | 2020-04-25      |     88      | 193.6%      | 171.9%     |
| SID      | 2020-07-25      |     87      | 172.6%      | 152.7%     |
| CSIQ     | 2020-07-25      |     88.3447 | 166.2%      | 146.3%     |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 127.70%             |
| 6M        | 270.73%             |
| 1Y        | 693.16%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 0.8% (2/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| APPS     | 2020-07-25 | 430.8%      |
| FUTU     | 2020-07-25 | 256.6%      |