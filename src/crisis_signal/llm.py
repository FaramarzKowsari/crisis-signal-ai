"""Provider-neutral utilities for structured LLM classification experiments."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

SYSTEM_INSTRUCTION = """You are a cautious crisis-information classifier.
Return only JSON. Do not invent evidence. When the message is ambiguous, choose
'review'. Allowed labels: disaster, not_disaster, review. Provide a probability
between 0 and 1 and a short evidence phrase copied or paraphrased from the input.
"""


@dataclass(frozen=True)
class StructuredLLMResult:
    label: str
    probability_disaster: float
    evidence: str


def build_prompt(text: str, language: str | None = None) -> list[dict[str, str]]:
    context = f"Language hint: {language}\n" if language else ""
    schema = (
        '{"label":"disaster|not_disaster|review",'
        '"probability_disaster":0.0,"evidence":"..."}'
    )
    return [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {
            "role": "user",
            "content": f"{context}Classify this message:\n{text}\nSchema: {schema}",
        },
    ]


def parse_structured_result(raw: str) -> StructuredLLMResult:
    payload: dict[str, Any] = json.loads(raw)
    label = str(payload["label"])
    if label not in {"disaster", "not_disaster", "review"}:
        raise ValueError(f"invalid label: {label}")
    probability = float(payload["probability_disaster"])
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability_disaster must be between 0 and 1")
    evidence = str(payload.get("evidence", "")).strip()
    return StructuredLLMResult(label, probability, evidence)
