import numpy as np

from crisis_signal.monitoring import population_stability_index, total_variation_distance


def test_psi_is_zero_for_identical_samples() -> None:
    sample = np.arange(100, dtype=float)
    assert population_stability_index(sample, sample) == 0.0


def test_total_variation_distance() -> None:
    assert total_variation_distance({"a": 1.0}, {"b": 1.0}) == 1.0
