# Strategy Report Card: SURGE (EVENT_LITE)
**Experiment Tag:** v3_lite_fixed
**Benchmark:** SPX

## 1. Executive Summary (6M Horizon)
* **Total Candidates:** 2160
* **Dates Sampled:** 5
* **Win Rate:** 45.2%
* **Alpha Win Rate:** 39.1%
* **Avg Alpha:** -3.00%

## 2. Distribution Analysis: Strategy vs Universe
Comparison of return percentiles (25th, Median, 75th) across horizons.
| Horizon   | Strat 25%   | Strat Med   | Strat 75%   | Univ 25%   | Univ Med   | Univ 75%   | Top Quartile Alpha   |
|:----------|:------------|:------------|:------------|:-----------|:-----------|:-----------|:---------------------|
| 3M        | -11.7%      | -0.4%       | 10.4%       | -11.3%     | -0.6%      | 10.0%      | 0.3%                 |
| 6M        | -20.0%      | -2.9%       | 13.8%       | -19.2%     | -1.1%      | 15.5%      | -1.7%                |
| 1Y        | -24.8%      | 0.1%        | 27.7%       | -26.6%     | -0.3%      | 25.2%      | 2.5%                 |

## 3. Multi-Horizon Performance
| Horizon   | Avg Return   | Avg Alpha   | Win Rate   |
|:----------|:-------------|:------------|:-----------|
| 3M        | 0.78%        | -1.56%      | 49.0%      |
| 6M        | 0.10%        | -3.00%      | 45.2%      |
| 1Y        | 8.32%        | -6.96%      | 50.2%      |
| MAX       | 30.22%       | -3.82%      | 61.9%      |

## 4. Period Breakdown
| snapshot_date   |   Count | Avg Return (6M)   | Avg Alpha (6M)   |
|:----------------|--------:|:------------------|:-----------------|
| 2019-04-25      |     491 | -2.0%             | -4.6%            |
| 2019-10-25      |     376 | -15.0%            | -9.8%            |
| 2020-07-25      |     313 | 31.3%             | 11.5%            |
| 2023-07-25      |     482 | 0.3%              | -6.3%            |
| 2024-10-25      |     498 | -6.2%             | -2.1%            |

## 5. Predictive Power Analysis (6M)
* **IC:** -0.001 (p=0.9592)

### Score Bucket Performance
| bucket     | Avg Return   | Avg Alpha   |
|:-----------|:-------------|:------------|
| Bottom 33% | -0.20%       | -2.20%      |
| Middle 33% | -1.91%       | -4.91%      |
| Top 33%    | 2.41%        | -1.89%      |

## 6. Top Winners (Alpha Leaders - 6M)
| ticker   | snapshot_date   |   raw_score | Return_6M   | Alpha_6M   |
|:---------|:----------------|------------:|:------------|:-----------|
| FCEL     | 2019-10-25      |     73.078  | 577.2%      | 582.5%     |
| EXPI     | 2020-07-25      |     71.1271 | 486.8%      | 466.9%     |
| APPS     | 2020-07-25      |     93      | 430.8%      | 410.9%     |
| CELH     | 2020-07-25      |     85      | 350.0%      | 330.1%     |
| DQ       | 2020-07-25      |     85      | 342.8%      | 322.9%     |
| ROOT     | 2024-10-25      |     81.7187 | 269.4%      | 273.5%     |
| FUTU     | 2020-07-25      |    100      | 256.6%      | 236.7%     |
| ALT      | 2023-07-25      |     85      | 211.7%      | 205.1%     |
| PLTR     | 2024-10-25      |     93      | 164.0%      | 168.1%     |
| SID      | 2020-07-25      |     93      | 172.6%      | 152.7%     |