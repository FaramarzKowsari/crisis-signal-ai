import numpy as np

from crisis_signal.evaluation import evaluate_binary_classifier, expected_calibration_error


def test_ece_is_zero_for_perfect_binary_probabilities() -> None:
    y_true = np.array([0, 1, 0, 1])
    probabilities = np.array([0.0, 1.0, 0.0, 1.0])
    assert expected_calibration_error(y_true, probabilities) == 0.0


def test_abstention_reduces_coverage() -> None:
    report = evaluate_binary_classifier(
        np.array([0, 1, 0, 1]),
        np.array([0.1, 0.9, 0.49, 0.51]),
        abstain_margin=0.05,
    )
    assert report.coverage == 0.5
    assert report.selective_accuracy == 1.0
