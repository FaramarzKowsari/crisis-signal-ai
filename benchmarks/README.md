# Benchmark evidence registry

`results.csv` is an evidence table, not a marketing leaderboard.

- `historical-not-reproduced` means the number was copied from an archived experiment output.
- `reproduced` means the repository contains a data fingerprint, configuration and artifact metadata for the run.
- Blank metrics are unknown rather than inferred.

Run a reproducible baseline:

```bash
python scripts/run_benchmark.py --data data/train.csv
```

Do not compare rows across different fingerprints as though they used the same data split.
