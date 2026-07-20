"""Safe multimodal building blocks: hashing and duplicate-image detection."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def perceptual_hash(path: str | Path) -> str:
    try:
        import imagehash
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Install multimodal dependencies: pip install -e '.[multimodal]'"
        ) from exc
    with Image.open(path) as image:
        return str(imagehash.phash(image.convert("RGB")))


def hamming_distance(hash_a: str, hash_b: str) -> int:
    if len(hash_a) != len(hash_b):
        raise ValueError("hashes must have equal length")
    return sum(bin(int(a, 16) ^ int(b, 16)).count("1") for a, b in zip(hash_a, hash_b, strict=True))
