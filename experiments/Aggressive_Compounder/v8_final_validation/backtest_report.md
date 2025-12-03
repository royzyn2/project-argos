# Strategy Report Card: Aggressive_Compounder
**Experiment Tag:** v8_final_validation
**Benchmark:** SPX

## 1. Executive Summary
* **Total Candidates Tested:** 500
* **Dates Sampled:** 5
* **Overall Win Rate (Absolute):** 56.6%
* **Alpha Win Rate (vs Bench):** 49.0%
* **Avg Alpha:** 2.80%

## 2. Predictive Power Analysis
* **Information Coefficient (IC):** -0.051
* **Significance (p-value):** 0.2522 (Not Significant)

### Score Spread Analysis (Aggregate)
| bucket     | ('forward_return', 'mean')   | ('forward_return', 'median')   |   ('forward_return', 'count') | ('Alpha', 'mean')   | ('Alpha', 'median')   |   ('Alpha', 'count') |
|:-----------|:-----------------------------|:-------------------------------|------------------------------:|:--------------------|:----------------------|---------------------:|
| Top 33%    | 5.2%                         | 0.1%                           |                           167 | 3.1%                | -1.8%                 |                  167 |
| Middle 33% | 10.5%                        | 6.2%                           |                           166 | 5.1%                | 1.9%                  |                  166 |
| Bottom 33% | 5.9%                         | 2.6%                           |                           167 | 0.2%                | -2.6%                 |                  167 |

### Score Spread by Period (Stability Check)
| snapshot_date   | Bottom 33% (forward_return)   | Middle 33% (forward_return)   | Top 33% (forward_return)   | Bottom 33% (Alpha)   | Middle 33% (Alpha)   | Top 33% (Alpha)   |
|:----------------|:------------------------------|:------------------------------|:---------------------------|:---------------------|:---------------------|:------------------|
| 2018-02-12      | -                             | 10.9%                         | 3.7%                       | -                    | 4.6%                 | -2.5%             |
| 2020-11-13      | 15.6%                         | 13.2%                         | 19.3%                      | 0.5%                 | -1.9%                | 4.2%              |
| 2020-12-08      | 17.3%                         | 9.2%                          | 19.9%                      | 2.7%                 | -5.3%                | 5.4%              |
| 2022-04-12      | -16.5%                        | -9.4%                         | -12.1%                     | 2.1%                 | 9.2%                 | 6.6%              |
| 2024-08-28      | -2.9%                         | 22.4%                         | 16.0%                      | -7.5%                | 17.8%                | 11.4%             |

## 3. Performance by Snapshot Date
| snapshot_date   | Avg Return   | Win Rate   | Avg Alpha   | Alpha Win Rate   |
|:----------------|:-------------|:-----------|:------------|:-----------------|
| 2018-02-12      | 5.6%         | 54.0%      | -0.6%       | 48.0%            |
| 2020-11-13      | 15.6%        | 73.0%      | 0.4%        | 46.0%            |
| 2020-12-08      | 14.2%        | 74.0%      | -0.3%       | 43.0%            |
| 2022-04-12      | -13.0%       | 22.0%      | 5.6%        | 61.0%            |
| 2024-08-28      | 13.4%        | 60.0%      | 8.8%        | 47.0%            |

## 4. Top Winners (Alpha Leaders)
| ticker   | snapshot_date   |   raw_score | forward_return   | Benchmark_Return   | Alpha   |
|:---------|:----------------|------------:|:-----------------|:-------------------|:--------|
| APP      | 2024-08-28      |        78.7 | 283.3%           | 4.6%               | 278.7%  |
| HIMS     | 2024-08-28      |        83.3 | 177.9%           | 4.6%               | 173.3%  |
| PLTR     | 2024-08-28      |        84   | 174.8%           | 4.6%               | 170.2%  |
| EAT      | 2024-08-28      |        78.8 | 126.6%           | 4.6%               | 122.0%  |
| VSTO     | 2020-12-08      |        69.6 | 113.6%           | 14.5%              | 99.1%   |
| SUPV     | 2024-08-28      |        77.3 | 92.0%            | 4.6%               | 87.4%   |
| CEIX     | 2022-04-12      |        81.6 | 63.5%            | -18.7%             | 82.2%   |
| CNR      | 2022-04-12      |        81.6 | 63.5%            | -18.7%             | 82.2%   |
| CLS      | 2024-08-28      |        78.6 | 85.6%            | 4.6%               | 81.0%   |
| PBF      | 2022-04-12      |        68.1 | 60.0%            | -18.7%             | 78.7%   |