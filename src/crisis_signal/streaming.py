"""JSONL stream simulation for repeatable demonstrations."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from crisis_signal.predictor import CrisisPredictor


async def read_jsonl_stream(
    path: str | Path, delay_seconds: float = 0.0
) -> AsyncIterator[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}") from exc
            yield item
            if delay_seconds > 0:
                await asyncio.sleep(delay_seconds)


async def classify_stream(
    path: str | Path,
    predictor: CrisisPredictor,
    delay_seconds: float = 0.0,
) -> AsyncIterator[dict[str, Any]]:
    async for item in read_jsonl_stream(path, delay_seconds):
        if "text" not in item:
            raise ValueError("every stream item must contain a text field")
        result = predictor.predict(str(item["text"]), source_id=item.get("id"))
        yield result.model_dump()
