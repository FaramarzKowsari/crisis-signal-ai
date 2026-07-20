"""Artifact loading and risk-aware prediction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from crisis_signal.schemas import PredictionResponse
from crisis_signal.text import normalize_text


class CrisisPredictor:
    def __init__(
        self,
        artifact_path: str | Path,
        decision_threshold: float = 0.5,
        abstain_margin: float | None = None,
    ) -> None:
        artifact: dict[str, Any] = joblib.load(artifact_path)
        if "pipeline" not in artifact or "metadata" not in artifact:
            raise ValueError("invalid model artifact")
        self.pipeline = artifact["pipeline"]
        self.metadata = artifact["metadata"]
        self.decision_threshold = decision_threshold
        self.abstain_margin = (
            float(self.metadata.get("abstain_margin", 0.1))
            if abstain_margin is None
            else abstain_margin
        )
        if not 0 <= self.abstain_margin < 0.5:
            raise ValueError("abstain_margin must be in [0, 0.5)")

    @property
    def model_version(self) -> str:
        return str(self.metadata.get("model_version", "unknown"))

    def predict(self, text: str, source_id: str | None = None) -> PredictionResponse:
        normalized = normalize_text(text)
        probability = float(self.pipeline.predict_proba([normalized])[0, 1])
        abstained = abs(probability - self.decision_threshold) < self.abstain_margin
        if abstained:
            label = "review"
        elif probability >= self.decision_threshold:
            label = "disaster"
        else:
            label = "not_disaster"
        confidence = max(probability, 1.0 - probability)
        return PredictionResponse(
            label=label,
            probability_disaster=probability,
            confidence=confidence,
            abstained=abstained,
            model_version=self.model_version,
            normalized_text=normalized,
            source_id=source_id,
        )
