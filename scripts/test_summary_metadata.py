from __future__ import annotations

import pytest

from summary_metadata import featured_speakers, normalize_speakers, without_featured_speakers


def _summary(speakers_block: str, short_summary: str = "A summary.") -> str:
    return (
        "# Episode\n\n"
        "## Featured Speakers\n\n"
        f"{speakers_block}\n\n"
        "## Short Summary\n\n"
        f"{short_summary}\n"
    )


# --- featured_speakers ------------------------------------------------------

def test_reads_bulleted_and_numbered_speakers() -> None:
    markdown = _summary("- Jane Doe, Acme\n2. John Smith, Initech")

    assert featured_speakers(markdown) == ["Jane Doe, Acme", "John Smith, Initech"]


@pytest.mark.parametrize("marker", ["Not clearly identified.", "Unknown", "No featured speakers"])
def test_unknown_markers_are_not_speakers(marker) -> None:
    assert featured_speakers(_summary(f"- {marker}")) == []


def test_duplicate_speakers_are_listed_once() -> None:
    markdown = _summary("- Jane Doe, Acme\n- Jane Doe, Acme")

    assert featured_speakers(markdown) == ["Jane Doe, Acme"]


def test_shared_affiliation_is_split_into_two_speakers() -> None:
    markdown = _summary("- Jane Doe and John Smith of Acme")

    assert featured_speakers(markdown) == ["Jane Doe, Acme", "John Smith, Acme"]


def test_non_name_phrases_are_rejected() -> None:
    assert featured_speakers(_summary("- Future Research Plan")) == []


# --- fallbacks when the section is empty ------------------------------------

def test_falls_back_to_the_title_after_a_dash() -> None:
    markdown = _summary("- Unknown")

    assert featured_speakers(markdown, title="Scaling Agents — Jane Doe") == ["Jane Doe"]


def test_falls_back_to_the_title_after_with() -> None:
    assert featured_speakers(_summary("- Unknown"), title="A conversation with Jane Doe") == ["Jane Doe"]


def test_falls_back_to_the_short_summary_lead() -> None:
    markdown = _summary("- Unknown", short_summary="The guest, Jane Doe, explains evals.")

    assert featured_speakers(markdown) == ["Jane Doe"]


def test_title_wins_over_the_summary_lead() -> None:
    markdown = _summary("- Unknown", short_summary="The guest, John Smith, explains evals.")

    assert featured_speakers(markdown, title="Evals — Jane Doe") == ["Jane Doe"]


def test_normalize_speakers_ignores_non_list_input() -> None:
    assert normalize_speakers("Jane Doe") == []


# --- without_featured_speakers ----------------------------------------------

def test_removes_only_the_speaker_section() -> None:
    result = without_featured_speakers(_summary("- Jane Doe, Acme"))

    assert "## Featured Speakers" not in result
    assert "Jane Doe" not in result
    assert "## Short Summary" in result


def test_leaves_markdown_without_the_section_untouched() -> None:
    markdown = "# Episode\n\n## Short Summary\n\nText."

    assert without_featured_speakers(markdown) == markdown
