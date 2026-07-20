from crisis_signal.text import normalize_text, normalized_group_key


def test_normalize_social_tokens() -> None:
    value = normalize_text("Flood! https://example.com @responder #Need_Help")
    assert "<URL>" in value
    assert "<USER>" in value
    assert "Need Help" in value


def test_group_key_collapses_punctuation_and_case() -> None:
    assert normalized_group_key("FLOOD!!!") == normalized_group_key("flood")
