from __future__ import annotations

import os
import sys
from types import ModuleType, SimpleNamespace

import transcript_sanitizer


def test_deterministic_cleanup_structures_transcript() -> None:
    raw = """[00:01] Speaker_1: um this is raw.\n\n00:02:03\nAlice: this has spacing."""

    cleaned = transcript_sanitizer.deterministic_cleanup(raw)

    assert "[00:01]" not in cleaned
    assert "00:02:03" not in cleaned
    assert "**Speaker 1:** um this is raw." in cleaned
    assert "**Alice:** this has spacing." in cleaned


def test_mistral_prompt_targets_spoken_word_artifacts() -> None:
    captured = {}

    class FakeResponse:
        status_code = 200

        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict:
            return {"choices": [{"message": {"content": "**Speaker 1:** This is cleaner."}}]}

    def post(_url: str, *, headers: dict, json: dict, timeout: int) -> FakeResponse:
        captured["payload"] = json
        return FakeResponse()

    original_requests = sys.modules.get("requests")
    original_key = os.environ.get("MISTRAL_API_KEY")
    fake_requests = ModuleType("requests")
    setattr(fake_requests, "post", post)
    sys.modules["requests"] = fake_requests
    os.environ["MISTRAL_API_KEY"] = "test-key"
    try:
        result = transcript_sanitizer._rewrite_chunk("**Speaker 1:** um I I think this matters.", _settings())
    finally:
        if original_requests is None:
            sys.modules.pop("requests", None)
        else:
            sys.modules["requests"] = original_requests
        if original_key is None:
            os.environ.pop("MISTRAL_API_KEY", None)
        else:
            os.environ["MISTRAL_API_KEY"] = original_key

    prompt = "\n".join(message["content"] for message in captured["payload"]["messages"]).lower()
    assert result == "**Speaker 1:** This is cleaner."
    assert "lexical fillers" in prompt
    assert "false starts" in prompt
    assert "repeated words" in prompt


def _settings() -> SimpleNamespace:
    return SimpleNamespace(transcript_rewrite_model="mistral-small-latest")


def main() -> None:
    test_deterministic_cleanup_structures_transcript()
    test_mistral_prompt_targets_spoken_word_artifacts()


if __name__ == "__main__":
    main()
