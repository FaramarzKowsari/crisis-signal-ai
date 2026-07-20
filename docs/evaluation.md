# Evaluation

Crisis classification is asymmetric: missing a real urgent report can be more costly than reviewing a false alarm. The repository therefore reports a configurable cost-weighted error in addition to standard classification metrics.

## Selective prediction

Messages with probabilities inside an abstention band around the decision threshold are labeled `review`. This creates a coverage–quality trade-off:

- wider abstention band: fewer automatic decisions, usually higher selective accuracy;
- narrower band: more coverage, more risk.

## Required future evaluations

- cross-event generalization;
- cross-language transfer;
- calibration by language and event type;
- robustness to spelling, code-switching and paraphrase;
- latency and memory on target hardware;
- subgroup and geographic error analysis.
