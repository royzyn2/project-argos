# Kryptonite Test Report: Aggressive_Compounder
**Experiment Tag:** v4_kryptonite

## Scenario Performance (3-Month Window)
Did the strategy survive?

| Scenario        |   ('forward_return', 'mean') |   ('forward_return', 'min') |   ('forward_return', 'count') |   ('max_drawdown', 'mean') |   ('max_drawdown', 'min') |   ('max_drawdown', 'count') |
|:----------------|-----------------------------:|----------------------------:|------------------------------:|---------------------------:|--------------------------:|----------------------------:|
| COVID_CRASH     |                   -0.169449  |                   -0.640696 |                           100 |                  -0.438903 |                 -0.885892 |                         100 |
| INFLATION_SPIKE |                   -0.0963987 |                   -0.412913 |                           100 |                  -0.274394 |                 -0.477671 |                         100 |
| RATE_HIKE_2022  |                   -0.116628  |                   -0.511936 |                           100 |                  -0.257151 |                 -0.620374 |                         100 |

## Worst Drawdowns per Scenario
### COVID_CRASH
| ticker   |   forward_return |   max_drawdown |
|:---------|-----------------:|---------------:|
| EVRI     |        -0.604426 |      -0.885892 |
| SEAS     |        -0.52035  |      -0.789146 |
| VLRS     |        -0.640696 |      -0.770802 |
| HP       |        -0.5872   |      -0.718496 |
| CRMT     |        -0.452583 |      -0.703161 |

### RATE_HIKE_2022
| ticker   |   forward_return |   max_drawdown |
|:---------|-----------------:|---------------:|
| AMBA     |        -0.511936 |      -0.620374 |
| TREX     |        -0.488372 |      -0.51082  |
| VICR     |        -0.405388 |      -0.510461 |
| GT       |        -0.347107 |      -0.50995  |
| CALX     |        -0.454569 |      -0.480051 |

### INFLATION_SPIKE
| ticker   |   forward_return |   max_drawdown |
|:---------|-----------------:|---------------:|
| METC     |       -0.231218  |      -0.477671 |
| TALO     |       -0.0895916 |      -0.472366 |
| EC       |       -0.404734  |      -0.465942 |
| ROCC     |       -0.15423   |      -0.449792 |
| PR       |       -0.0340376 |      -0.443051 |

