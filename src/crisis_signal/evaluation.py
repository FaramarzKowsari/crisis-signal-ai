"""Risk-aware classification evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


@dataclass(frozen=True)
class EvaluationReport:
    accuracy: float
    precision: float
    recall: float
    f1: float
    macro_f1: float
    brier_score: float
    expected_calibration_error: float
    false_negative_cost: float
    false_positive_cost: float
    weighted_error_cost: float
    confusion_matrix: list[list[int]]
    coverage: float
    selective_accuracy: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def expected_calibration_error(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    n_bins: int = 10,
) -> float:
    if n_bins < 2:
        raise ValueError("n_bins must be at least 2")
    y_true = np.asarray(y_true, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    if len(y_true) != len(probabilities):
        raise ValueError("y_true and probabilities must have equal length")
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    error = 0.0
    for lower, upper in zip(edges[:-1], edges[1:], strict=True):
        include_upper = upper == 1.0
        mask = (probabilities >= lower) & (
            probabilities <= upper if include_upper else probabilities < upper
        )
        if not np.any(mask):
            continue
        confidence = float(np.mean(probabilities[mask]))
        accuracy = float(np.mean(y_true[mask]))
        error += float(np.mean(mask)) * abs(accuracy - confidence)
    return error


def evaluate_binary_classifier(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    threshold: float = 0.5,
    abstain_margin: float = 0.0,
    false_negative_cost: float = 5.0,
    false_positive_cost: float = 1.0,
    calibration_bins: int = 10,
) -> EvaluationReport:
    y_true = np.asarray(y_true, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    predictions = (probabilities >= threshold).astype(int)
    matrix = confusion_matrix(y_true, predictions, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()

    reviewed = np.abs(probabilities - threshold) < abstain_margin
    selected = ~reviewed
    selective_accuracy = (
        float(accuracy_score(y_true[selected], predictions[selected]))
        if np.any(selected)
        else None
    )
    weighted_cost = float(fn * false_negative_cost + fp * false_positive_cost)

    return EvaluationReport(
        accuracy=float(accuracy_score(y_true, predictions)),
        precision=float(precision_score(y_true, predictions, zero_division=0)),
        recall=float(recall_score(y_true, predictions, zero_division=0)),
        f1=float(f1_score(y_true, predictions, zero_division=0)),
        macro_f1=float(f1_score(y_true, predictions, average="macro", zero_division=0)),
        brier_score=float(brier_score_loss(y_true, probabilities)),
        expected_calibration_error=expected_calibration_error(
            y_true, probabilities, n_bins=calibration_bins
        ),
        false_negative_cost=false_negative_cost,
        false_positive_cost=false_positive_cost,
        weighted_error_cost=weighted_cost,
        confusion_matrix=matrix.astype(int).tolist(),
        coverage=float(np.mean(selected)),
        selective_accuracy=selective_accuracy,
    )
