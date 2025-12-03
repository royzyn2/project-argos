# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v6_coiled_spring
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 2360
* **Dates Sampled:** 5
* **Win Rate:** 53.2%
* **Alpha Win Rate:** 41.2%
* **Avg Alpha:** -2.37%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -9.0%       | -0.7%       | 9.1%        | -12.3%     | -2.0%      | 8.3%       | 0.8%                 |
| 6M        | -10.2%      | 1.4%        | 14.7%       | -15.0%     | 3.7%       | 18.8%      | -4.0%                |
| 1Y        | -25.0%      | -5.4%       | 13.5%       | -30.9%     | -4.4%      | 19.5%      | -6.0%                |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 0.65%        | -1.85%      | 47.9%      |
| 6M        | 3.64%        | -2.37%      | 53.2%      |
| 1Y        | -2.03%       | -5.91%      | 41.7%      |
| MAX       | 8.96%        | -6.53%      | 49.2%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-04-25      |     381 | -0.1%             | -2.8%            |
| 2020-07-25      |     229 | 27.6%             | 7.7%             |
| 2021-04-25      |     721 | 4.5%              | -4.4%            |
| 2021-07-25      |     657 | -1.1%             | -0.8%            |
| 2023-07-25      |     372 | -0.4%             | -7.0%            |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.005 |    0.7899 | No             |
| 6M        |              0.046 |    0.0242 | **Yes**        |
| 1Y        |              0.022 |    0.2781 | No             |
| MAX       |              0.007 |    0.7427 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| growth_score |  0.018 | -0.008 | -0.008 |
| value_score  |  0.007 |  0.06  |  0.027 |
| tech_score   | -0.035 |  0.032 |  0.022 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 2.93%        | -2.56%      |
| Middle 33% | 3.54%        | -2.45%      |
| Top 33%    | 4.52%        | -2.09%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| SID      | 2020-07-25      |     89      | 172.6%      | 152.7%     |
| CSIQ     | 2020-07-25      |     89.3447 | 166.2%      | 146.3%     |
| MTLS     | 2020-07-25      |     93      | 156.4%      | 136.5%     |
| VRTV     | 2021-04-25      |     85.506  | 144.8%      | 136.0%     |
| SITM     | 2021-04-25      |     93      | 127.2%      | 118.3%     |
| DAR      | 2020-07-25      |     89      | 137.3%      | 117.4%     |
| HIMX     | 2020-07-25      |     93      | 134.3%      | 114.4%     |
| DDS      | 2021-04-25      |     89      | 119.9%      | 111.0%     |
| ARWR     | 2019-04-25      |     93      | 108.1%      | 105.5%     |
| IDT      | 2021-04-25      |     93      | 109.8%      | 101.0%     |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 94.17%              |
| 6M        | 138.26%             |
| 1Y        | 231.63%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 9.2% (23/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| ANIK     | 2019-04-25 | 70.2%       |
| DHT      | 2019-04-25 | 49.0%       |
| SKY      | 2019-04-25 | 48.6%       |
| PFSI     | 2019-04-25 | 44.1%       |
| INSW     | 2019-04-25 | 44.0%       |
| IRT      | 2019-04-25 | 43.6%       |
| CMPR     | 2019-04-25 | 42.1%       |
| RGEN     | 2019-04-25 | 39.3%       |
| RGLD     | 2019-04-25 | 36.5%       |
| BEP      | 2019-04-25 | 35.5%       |
| PRFT     | 2019-04-25 | 33.5%       |
| MTLS     | 2020-07-25 | 156.4%      |
| IDT      | 2021-04-25 | 109.8%      |
| HRI      | 2021-04-25 | 83.5%       |
| VICR     | 2021-04-25 | 59.9%       |
| CELH     | 2021-04-25 | 59.8%       |
| HOLI     | 2021-04-25 | 52.9%       |
| GSKY     | 2021-07-25 | 71.9%       |
| BCTX     | 2021-07-25 | 60.9%       |
| TECK     | 2021-07-25 | 55.1%       |
| TRNS     | 2021-07-25 | 45.9%       |
| BVN      | 2023-07-25 | 85.5%       |
| MOD      | 2023-07-25 | 78.5%       |