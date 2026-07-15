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


def test_deterministic_cleanup_keeps_wrapped_lines_with_same_speaker() -> None:
    raw = """Speaker_1: first thought here
this line wraps the same speaker and should stay attributed.

Speaker_2: response starts here
and continues on the next line too."""

    cleaned = transcript_sanitizer.deterministic_cleanup(raw)

    assert "**Speaker 1:** first thought here this line wraps the same speaker and should stay attributed." in cleaned
    assert "**Speaker 2:** response starts here and continues on the next line too." in cleaned


def test_rewrite_flag_does_not_depend_on_summary_provider() -> None:
    original_rewrite = transcript_sanitizer._cached_mistral_rewrite
    original_key = os.environ.get("MISTRAL_API_KEY")
    os.environ["MISTRAL_API_KEY"] = "test-key"
    transcript_sanitizer._cached_mistral_rewrite = lambda cleaned, _settings: f"rewritten::{cleaned}"
    try:
        result = transcript_sanitizer.transcript_for_reading(
            "Speaker_1: raw words here.",
            SimpleNamespace(
                rewrite_full_transcripts=True,
                summary_provider="local",
                transcript_rewrite_model="mistral-small-latest",
            ),
        )
    finally:
        transcript_sanitizer._cached_mistral_rewrite = original_rewrite
        if original_key is None:
            os.environ.pop("MISTRAL_API_KEY", None)
        else:
            os.environ["MISTRAL_API_KEY"] = original_key

    assert result.startswith("rewritten::")
    assert "**Speaker 1:** raw words here." in result


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
    test_deterministic_cleanup_keeps_wrapped_lines_with_same_speaker()
    test_rewrite_flag_does_not_depend_on_summary_provider()
    test_mistral_prompt_targets_spoken_word_artifacts()


if __name__ == "__main__":
    main()
