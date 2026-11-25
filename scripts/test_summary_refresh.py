from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

import summarize


PLACEHOLDER_MARKERS = [
    "AI summary is not enabled yet",
    "Not generated in local fallback mode",
    "Transcript excerpt:",
    "Mistral summary failed",
]


@pytest.fixture
def settings() -> SimpleNamespace:
    return SimpleNamespace()


def _summary(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "item.md"
    path.write_text(body, encoding="utf-8")
    return path


# --- should_refresh_summary: the decision that spends (or saves) API calls ---

def test_missing_summary_is_always_refreshed(tmp_path, settings, monkeypatch) -> None:
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)

    assert summarize.should_refresh_summary(tmp_path / "absent.md", settings) is True


@pytest.mark.parametrize("marker", PLACEHOLDER_MARKERS)
def test_placeholder_summary_is_refreshed_when_a_key_is_available(
    tmp_path, settings, monkeypatch, marker
) -> None:
    monkeypatch.setenv("MISTRAL_API_KEY", "test-key")
    path = _summary(tmp_path, f"# Episode\n\n{marker}\n")

    assert summarize.should_refresh_summary(path, settings) is True


@pytest.mark.parametrize("marker", PLACEHOLDER_MARKERS)
def test_placeholder_summary_is_kept_without_a_key(tmp_path, settings, monkeypatch, marker) -> None:
    # Without a key a refresh can only produce another placeholder, so the
    # run should not redo the work.
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    path = _summary(tmp_path, f"# Episode\n\n{marker}\n")

    assert summarize.should_refresh_summary(path, settings) is False


def test_real_summary_is_never_refreshed(tmp_path, settings, monkeypatch) -> None:
    monkeypatch.setenv("MISTRAL_API_KEY", "test-key")
    path = _summary(tmp_path, "# Episode\n\n## Short Summary\n\nA real summary.\n")

    assert summarize.should_refresh_summary(path, settings) is False


# --- placeholder / transcript detection --------------------------------------

@pytest.mark.parametrize(
    "text",
    [
        "AI summary is not enabled yet",
        "Not generated in local fallback mode",
        "Mistral summary failed: timeout",
        "AI summary failed",
    ],
)
def test_is_placeholder_summary_flags_fallback_output(text) -> None:
    assert summarize.is_placeholder_summary(f"# Title\n\n{text}\n") is True


def test_is_placeholder_summary_accepts_a_real_summary() -> None:
    assert summarize.is_placeholder_summary("# Title\n\n## Short Summary\n\nFine.\n") is False


@pytest.mark.parametrize("marker", ["Transcript unavailable", "TRANSCRIPTION FAILED"])
def test_failed_transcripts_are_not_sent_to_the_model(marker) -> None:
    assert summarize._has_real_transcript(f"{marker} for this item") is False


def test_real_transcript_is_sent_to_the_model() -> None:
    assert summarize._has_real_transcript("Speaker 1: Welcome back to the show.") is True
