"""Lightweight data-drift utilities."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

import numpy as np

from crisis_signal.text import normalize_text


def population_stability_index(
    expected: np.ndarray,
    actual: np.ndarray,
    bins: int = 10,
    epsilon: float = 1e-6,
) -> float:
    expected = np.asarray(expected, dtype=float)
    actual = np.asarray(actual, dtype=float)
    if expected.size == 0 or actual.size == 0:
        raise ValueError("expected and actual arrays must be non-empty")
    quantiles = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    if len(quantiles) < 3:
        return 0.0
    expected_counts, _ = np.histogram(expected, bins=quantiles)
    actual_counts, _ = np.histogram(actual, bins=quantiles)
    expected_pct = expected_counts / max(expected_counts.sum(), 1)
    actual_pct = actual_counts / max(actual_counts.sum(), 1)
    expected_pct = np.clip(expected_pct, epsilon, None)
    actual_pct = np.clip(actual_pct, epsilon, None)
    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))


def token_distribution(texts: Iterable[str], top_k: int = 1000) -> dict[str, float]:
    counter: Counter[str] = Counter()
    for text in texts:
        counter.update(normalize_text(text).casefold().split())
    total = sum(counter.values())
    if total == 0:
        return {}
    return {token: count / total for token, count in counter.most_common(top_k)}


def total_variation_distance(
    reference: dict[str, float], current: dict[str, float]
) -> float:
    vocabulary = set(reference) | set(current)
    return 0.5 * sum(abs(reference.get(t, 0.0) - current.get(t, 0.0)) for t in vocabulary)
