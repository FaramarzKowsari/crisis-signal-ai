from crisis_signal.llm import build_prompt, parse_structured_result


def test_prompt_and_parser() -> None:
    prompt = build_prompt("Road blocked by flood", language="en")
    assert prompt[0]["role"] == "system"
    result = parse_structured_result(
        '{"label":"disaster","probability_disaster":0.93,"evidence":"road blocked"}'
    )
    assert result.label == "disaster"
