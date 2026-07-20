"""Typed request and response schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    language: str | None = Field(default=None, max_length=32)
    source_id: str | None = Field(default=None, max_length=256)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must contain non-whitespace characters")
        return value


class PredictionResponse(BaseModel):
    label: Literal["disaster", "not_disaster", "review"]
    probability_disaster: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    abstained: bool
    model_version: str
    normalized_text: str
    source_id: str | None = None


class BatchPredictionRequest(BaseModel):
    items: list[PredictionRequest] = Field(min_length=1, max_length=500)


class BatchPredictionResponse(BaseModel):
    items: list[PredictionResponse]
