"""Train the baseline and append an evidence-backed benchmark row."""

from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from pathlib import Path

from crisis_signal.training import train_baseline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--artifact", default="artifacts/baseline.joblib")
    parser.add_argument("--results", default="benchmarks/results.csv")
    args = parser.parse_args()

    metadata = train_baseline(args.data, args.artifact)
    evaluation = metadata["evaluation"]
    results_path = Path(args.results)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    exists = results_path.exists()
    fields = [
        "recorded_at",
        "model",
        "dataset_fingerprint",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "macro_f1",
        "ece",
        "status",
        "evidence_source",
    ]
    row = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "model": metadata["model_name"],
        "dataset_fingerprint": metadata["dataset_fingerprint"],
        "accuracy": evaluation["accuracy"],
        "precision": evaluation["precision"],
        "recall": evaluation["recall"],
        "f1": evaluation["f1"],
        "macro_f1": evaluation["macro_f1"],
        "ece": evaluation["expected_calibration_error"],
        "status": "reproduced",
        "evidence_source": str(Path(args.artifact).with_suffix(".joblib.metadata.json")),
    }
    with results_path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
