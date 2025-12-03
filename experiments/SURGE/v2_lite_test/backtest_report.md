# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v2_lite_test
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 250
* **Dates Sampled:** 5
* **Win Rate:** 72.4%
* **Alpha Win Rate:** 40.0%
* **Avg Alpha:** 2.21%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -6.0%       | 1.7%        | 13.1%       | 712.6%     | 1603.0%    | 4650.4%    | -4637.3%             |
| 6M        | -1.2%       | 9.2%        | 24.7%       | 708.6%     | 1676.6%    | 4752.6%    | -4727.9%             |
| 1Y        | -15.9%      | 8.8%        | 32.9%       | 602.2%     | 1374.3%    | 4157.2%    | -4124.3%             |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 4.85%        | -1.58%      | 56.0%      |
| 6M        | 17.08%       | 2.21%       | 72.4%      |
| 1Y        | 12.96%       | -4.78%      | 57.6%      |
| MAX       | 14.16%       | -7.74%      | 56.8%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-07-25      |      50 | 3.0%              | -6.7%            |
| 2020-07-25      |      50 | 26.7%             | 6.8%             |
| 2020-10-25      |      50 | 43.9%             | 23.1%            |
| 2021-04-25      |      50 | 4.3%              | -4.5%            |
| 2024-04-25      |      50 | 7.4%              | -7.7%            |

## 5. Predictive Power Analysis (6M)
* **IC:** 0.063 (p=0.3208)

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | 8.78%        | -5.90%      |
| Middle 33% | 24.71%       | 8.41%       |
| Top 33%    | 17.84%       | 4.21%       |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| FUTU     | 2020-10-25      |     96.2228 | 341.3%      | 320.5%     |
| FUTU     | 2020-07-25      |    100      | 256.6%      | 236.7%     |
| OCUL     | 2020-07-25      |     95      | 143.9%      | 124.0%     |
| JFIN     | 2020-10-25      |     96      | 143.5%      | 122.7%     |
| QFIN     | 2020-10-25      |     96      | 116.7%      | 95.9%      |
| ZLAB     | 2020-10-25      |     95      | 103.2%      | 82.4%      |
| IVZ      | 2020-07-25      |    100      | 101.5%      | 81.6%      |
| CASH     | 2020-07-25      |    100      | 100.2%      | 80.3%      |
| CRS      | 2024-04-25      |     93      | 88.8%       | 73.7%      |
| UMC      | 2020-10-25      |     99.8547 | 93.9%       | 73.1%      |