"""Reproducible training and artifact serialization."""

from __future__ import annotations

import json
import platform
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import sklearn

from crisis_signal.data import grouped_train_test_split, load_dataset
from crisis_signal.evaluation import evaluate_binary_classifier
from crisis_signal.models.classical import build_tfidf_logistic_pipeline


def train_baseline(
    data_path: str | Path,
    output_path: str | Path,
    test_size: float = 0.2,
    random_state: int = 42,
    abstain_margin: float = 0.1,
    min_df: int = 2,
) -> dict[str, Any]:
    frame = load_dataset(data_path)
    split = grouped_train_test_split(
        frame, test_size=test_size, random_state=random_state
    )
    pipeline = build_tfidf_logistic_pipeline(
        random_state=random_state,
        min_df=min_df,
    )
    pipeline.fit(split.train["normalized_text"], split.train["target"])
    probabilities = pipeline.predict_proba(split.test["normalized_text"])[:, 1]
    report = evaluate_binary_classifier(
        split.test["target"].to_numpy(),
        probabilities,
        abstain_margin=abstain_margin,
    )
    metadata: dict[str, Any] = {
        "model_name": "tfidf_logistic_regression",
        "model_version": "0.1.0",
        "created_at": datetime.now(UTC).isoformat(),
        "dataset_fingerprint": split.fingerprint,
        "random_state": random_state,
        "test_size": test_size,
        "abstain_margin": abstain_margin,
        "train_rows": len(split.train),
        "test_rows": len(split.test),
        "python_version": platform.python_version(),
        "sklearn_version": sklearn.__version__,
        "evaluation": report.to_dict(),
    }
    artifact = {"pipeline": pipeline, "metadata": metadata}
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, output)
    output.with_suffix(output.suffix + ".metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    return metadata
