"""Deterministic text normalization for noisy short messages."""

from __future__ import annotations

import html
import re
import unicodedata

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MENTION_RE = re.compile(r"(?<!\w)@[A-Za-z0-9_]+")
HASHTAG_RE = re.compile(r"#([\w-]+)")
WHITESPACE_RE = re.compile(r"\s+")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def normalize_text(text: str) -> str:
    """Normalize a social message while preserving semantically useful words."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    value = html.unescape(text)
    value = unicodedata.normalize("NFKC", value)
    value = CONTROL_RE.sub(" ", value)
    value = URL_RE.sub(" <URL> ", value)
    value = MENTION_RE.sub(" <USER> ", value)
    value = HASHTAG_RE.sub(lambda match: f" {match.group(1).replace('_', ' ')} ", value)
    value = WHITESPACE_RE.sub(" ", value).strip()
    return value


def normalized_group_key(text: str) -> str:
    """Return a conservative key for duplicate-aware splitting."""
    value = normalize_text(text).casefold()
    value = re.sub(r"[^\w<>]+", " ", value, flags=re.UNICODE)
    return WHITESPACE_RE.sub(" ", value).strip()
