"""FastAPI application for single and batch inference."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException

from crisis_signal import __version__
from crisis_signal.predictor import CrisisPredictor
from crisis_signal.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    PredictionRequest,
    PredictionResponse,
)

app = FastAPI(
    title="CrisisSignal AI",
    version=__version__,
    description="Risk-aware crisis-message classification API",
)


@lru_cache(maxsize=1)
def get_predictor() -> CrisisPredictor:
    path = Path(os.getenv("CRISIS_SIGNAL_MODEL", "artifacts/baseline.joblib"))
    if not path.exists():
        raise FileNotFoundError(
            f"model artifact not found at {path}; train a model or set CRISIS_SIGNAL_MODEL"
        )
    margin = float(os.getenv("CRISIS_SIGNAL_ABSTAIN_MARGIN", "0.10"))
    return CrisisPredictor(path, abstain_margin=margin)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "crisis-signal-ai", "version": __version__}


@app.post("/v1/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        return get_predictor().predict(request.text, source_id=request.source_id)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/v1/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    try:
        predictor = get_predictor()
        return BatchPredictionResponse(
            items=[predictor.predict(item.text, item.source_id) for item in request.items]
        )
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/v1/model-card")
def model_card() -> dict[str, object]:
    try:
        return get_predictor().metadata
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
