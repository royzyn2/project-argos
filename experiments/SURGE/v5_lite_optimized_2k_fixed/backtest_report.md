# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v5_lite_optimized_2k_fixed
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 839
* **Dates Sampled:** 5
* **Win Rate:** 45.1%
* **Alpha Win Rate:** 33.5%
* **Avg Alpha:** -5.40%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -8.9%       | -0.3%       | 11.5%       | -7.8%      | 2.5%       | 13.9%      | -2.4%                |
| 6M        | -17.0%      | -2.3%       | 13.3%       | -20.3%     | -3.0%      | 14.1%      | -0.7%                |
| 1Y        | -23.8%      | -4.3%       | 16.5%       | -25.0%     | 3.2%       | 30.0%      | -13.4%               |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 2.44%        | -2.53%      | 49.6%      |
| 6M        | 0.56%        | -5.40%      | 45.1%      |
| 1Y        | 9.86%        | 0.59%       | 44.5%      |
| MAX       | 17.23%       | -6.53%      | 45.6%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-10-25      |      94 | -20.1%            | -14.9%           |
| 2020-04-25      |     110 | 24.9%             | 3.1%             |
| 2021-04-25      |     362 | 4.2%              | -4.6%            |
| 2022-04-25      |     109 | -11.7%            | -0.1%            |
| 2022-10-25      |     164 | -3.9%             | -11.0%           |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.009 |    0.7915 | No             |
| 6M        |              0.006 |    0.8626 | No             |
| 1Y        |             -0.024 |    0.4907 | No             |
| MAX       |             -0.029 |    0.4059 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| growth_score |  0.03  |  0.026 | -0.004 |
| value_score  | -0.005 | -0.008 | -0.03  |
| tech_score   | -0.112 | -0.041 | -0.019 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 0.57%        | -5.48%      |
| Middle 33% | -0.13%       | -5.41%      |
| Top 33%    | 0.70%        | -5.27%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| PLUG     | 2020-04-25      |     95      | 240.0%      | 218.3%     |
| GME      | 2020-04-25      |     93      | 213.4%      | 191.7%     |
| TSLA     | 2020-04-25      |     93      | 193.6%      | 171.9%     |
| CALX     | 2020-04-25      |     93      | 161.2%      | 139.4%     |
| VRTV     | 2021-04-25      |     89.506  | 144.8%      | 136.0%     |
| PINS     | 2020-04-25      |     90.0354 | 146.4%      | 124.7%     |
| KPTI     | 2019-10-25      |     95      | 115.4%      | 120.7%     |
| TTD      | 2020-04-25      |     93      | 136.5%      | 114.8%     |
| DDS      | 2021-04-25      |     93      | 119.9%      | 111.0%     |
| TGLS     | 2021-04-25      |     93.1181 | 117.6%      | 108.8%     |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 109.78%             |
| 6M        | 160.07%             |
| 1Y        | 675.43%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 5.6% (14/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| KPTI     | 2019-10-25 | 115.4%      |
| SAFE     | 2019-10-25 | 53.1%       |
| TSLA     | 2020-04-25 | 193.6%      |
| PINS     | 2020-04-25 | 146.4%      |
| TGLS     | 2021-04-25 | 117.6%      |
| INMD     | 2021-04-25 | 91.0%       |
| TRGP     | 2021-04-25 | 64.1%       |
| IT       | 2021-04-25 | 60.4%       |
| CELH     | 2021-04-25 | 59.8%       |
| TH       | 2022-04-25 | 92.3%       |
| PBF      | 2022-04-25 | 68.1%       |
| PARR     | 2022-04-25 | 58.0%       |
| CNR      | 2022-04-25 | 51.7%       |
| ELF      | 2022-10-25 | 114.1%      |