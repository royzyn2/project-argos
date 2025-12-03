# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v7_gaussian_tech
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 2798
* **Dates Sampled:** 5
* **Win Rate:** 48.1%
* **Alpha Win Rate:** 45.2%
* **Avg Alpha:** -1.08%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -10.6%      | -1.5%       | 8.9%        | -13.9%     | -2.8%      | 5.5%       | 3.3%                 |
| 6M        | -14.0%      | -1.0%       | 12.2%       | -21.7%     | -4.2%      | 8.3%       | 3.9%                 |
| 1Y        | -27.6%      | -8.6%       | 9.4%        | -39.0%     | -14.1%     | 5.3%       | 4.1%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | -0.52%       | -0.75%      | 45.5%      |
| 6M        | -0.46%       | -1.08%      | 48.1%      |
| 1Y        | -6.53%       | -5.15%      | 37.0%      |
| MAX       | 9.07%        | -6.21%      | 47.9%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-04-25      |     398 | -0.7%             | -3.3%            |
| 2021-04-25      |     741 | 4.3%              | -4.5%            |
| 2021-07-25      |     729 | -1.1%             | -0.8%            |
| 2022-04-25      |     530 | -10.4%            | 1.2%             |
| 2022-07-25      |     400 | 5.2%              | 4.0%             |

## 5. Predictive Power Analysis (Multi-Horizon)
Correlation between Strategy Score and Future Returns (Information Coefficient).
| Horizon   |   IC (Correlation) |   P-Value | Significant?   |
|:----------|-------------------:|----------:|:---------------|
| 3M        |             -0.034 |    0.0725 | No             |
| 6M        |              0.037 |    0.0532 | No             |
| 1Y        |              0.01  |    0.601  | No             |
| MAX       |             -0.005 |    0.7887 | No             |

### Score Component Correlation (Driver Analysis)
Which specific factor drives returns?
| Component    |     3M |     6M |     1Y |
|:-------------|-------:|-------:|-------:|
| growth_score |  0.002 | -0.026 | -0.025 |
| value_score  | -0.006 |  0.05  |  0.027 |
| tech_score   | -0.048 |  0.042 |  0.019 |

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | -1.35%       | -1.18%      |
| Middle 33% | -0.82%       | -1.56%      |
| Top 33%    | 0.80%        | -0.50%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| VIST     | 2022-07-25      |     81.4622 | 147.5%      | 146.2%     |
| VRTV     | 2021-04-25      |     83.195  | 144.8%      | 136.0%     |
| SITM     | 2021-04-25      |     90.7419 | 127.2%      | 118.3%     |
| DDS      | 2021-04-25      |     88.153  | 119.9%      | 111.0%     |
| GGAL     | 2022-07-25      |     85.627  | 109.4%      | 108.2%     |
| CLFD     | 2022-04-25      |     85.6897 | 95.3%       | 106.9%     |
| ARWR     | 2019-04-25      |     92.9907 | 108.1%      | 105.5%     |
| VET      | 2021-07-25      |     82.7009 | 104.4%      | 104.7%     |
| IDT      | 2021-04-25      |     90.7513 | 109.8%      | 101.0%     |
| CVLG     | 2022-04-25      |     85.0248 | 87.2%       | 98.8%      |

### Theoretical Ceiling (Perfect Selection)
If the AI perfectly picked the Top 10 winners from this candidate pool, what would the return be?
| Horizon   | Top 10 Avg Return   |
|:----------|:--------------------|
| 3M        | 94.14%              |
| 6M        | 116.74%             |
| 1Y        | 261.50%             |

### Recall Analysis (The Munger Metric)
Of the Top 250 performers in the Universe Sample, how many did we catch?
* **Recall Rate:** 17.6% (44/250)

#### Caught Winners:
| ticker   | date       | Return_6M   |
|:---------|:-----------|:------------|
| BLDR     | 2019-04-25 | 65.8%       |
| MHO      | 2019-04-25 | 55.5%       |
| DHT      | 2019-04-25 | 49.0%       |
| INSW     | 2019-04-25 | 44.0%       |
| ARMK     | 2019-04-25 | 43.9%       |
| BEP      | 2019-04-25 | 35.5%       |
| BKD      | 2019-04-25 | 33.7%       |
| PRFT     | 2019-04-25 | 33.5%       |
| FRO      | 2019-04-25 | 33.1%       |
| TTWO     | 2019-04-25 | 32.1%       |
| IDT      | 2021-04-25 | 109.8%      |
| MGY      | 2021-04-25 | 91.5%       |
| INMD     | 2021-04-25 | 91.0%       |
| HCI      | 2021-04-25 | 84.4%       |
| VET      | 2021-04-25 | 63.4%       |
| VICR     | 2021-04-25 | 59.9%       |
| CELH     | 2021-04-25 | 59.8%       |
| VET      | 2021-07-25 | 104.4%      |
| MRO      | 2021-07-25 | 57.4%       |
| BLDR     | 2021-07-25 | 47.7%       |
| TSLA     | 2021-07-25 | 46.7%       |
| MGY      | 2021-07-25 | 44.9%       |
| EQNR     | 2021-07-25 | 43.4%       |
| ATLC     | 2021-07-25 | 40.3%       |
| MATX     | 2021-07-25 | 39.8%       |
| CNOB     | 2021-07-25 | 39.4%       |
| EOG      | 2021-07-25 | 38.8%       |
| BCC      | 2021-07-25 | 38.5%       |
| ELF      | 2022-04-25 | 70.9%       |
| TPL      | 2022-04-25 | 58.2%       |
| VIST     | 2022-04-25 | 57.0%       |
| CNR      | 2022-04-25 | 51.7%       |
| TA       | 2022-04-25 | 49.3%       |
| EVOP     | 2022-04-25 | 46.6%       |
| HAE      | 2022-04-25 | 43.4%       |
| DEN      | 2022-04-25 | 41.9%       |
| SLB      | 2022-04-25 | 34.8%       |
| DVN      | 2022-04-25 | 33.9%       |
| MTDR     | 2022-04-25 | 30.6%       |
| DECK     | 2022-04-25 | 29.8%       |
| XOM      | 2022-04-25 | 29.6%       |
| GGAL     | 2022-07-25 | 109.4%      |
| MOD      | 2022-07-25 | 83.2%       |
| TRMD     | 2022-07-25 | 71.6%       |