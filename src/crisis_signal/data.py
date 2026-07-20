"""Dataset loading, validation, fingerprinting and leakage-aware splitting."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from crisis_signal.text import normalize_text, normalized_group_key


@dataclass(frozen=True)
class DatasetSplit:
    train: pd.DataFrame
    test: pd.DataFrame
    fingerprint: str


def load_dataset(
    path: str | Path,
    text_column: str = "text",
    target_column: str = "target",
) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = {text_column, target_column} - set(frame.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    frame = frame.copy()
    frame[text_column] = frame[text_column].fillna("").map(str)
    frame = frame[frame[text_column].str.strip().ne("")]
    frame[target_column] = pd.to_numeric(frame[target_column], errors="raise").astype(int)
    invalid = set(frame[target_column].unique()) - {0, 1}
    if invalid:
        raise ValueError(f"target must contain only 0 and 1; found {sorted(invalid)}")
    frame["normalized_text"] = frame[text_column].map(normalize_text)
    frame["group_key"] = frame[text_column].map(normalized_group_key)
    return frame.reset_index(drop=True)


def dataset_fingerprint(frame: pd.DataFrame) -> str:
    ordered = frame[["normalized_text", "target"]].sort_values(
        ["normalized_text", "target"]
    )
    payload = ordered.to_csv(index=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def grouped_train_test_split(
    frame: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> DatasetSplit:
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    if frame["group_key"].nunique() < 2:
        raise ValueError("at least two unique normalized text groups are required")
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(
        splitter.split(frame, y=frame["target"], groups=frame["group_key"])
    )
    train = frame.iloc[train_idx].reset_index(drop=True)
    test = frame.iloc[test_idx].reset_index(drop=True)
    overlap = set(train["group_key"]) & set(test["group_key"])
    if overlap:
        raise RuntimeError("duplicate-aware split failed: overlapping text groups detected")
    return DatasetSplit(train=train, test=test, fingerprint=dataset_fingerprint(frame))
