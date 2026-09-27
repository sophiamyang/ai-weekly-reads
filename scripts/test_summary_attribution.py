import pytest

from project_paths import PROMPTS
from reading_priority import HIGH_SIGNAL_WORDS

SUMMARY_PROMPTS = ["summarize_resource.md", "summarize_podcast.md"]


@pytest.mark.parametrize("name", SUMMARY_PROMPTS)
def test_prompt_requires_attributing_self_reported_numbers(name):
    prompt = (PROMPTS / name).read_text(encoding="utf-8")
    assert '"Our model is 20x faster" must never become "The model is 20x faster"' in prompt


@pytest.mark.parametrize("name", SUMMARY_PROMPTS)
def test_priority_rubric_does_not_invite_evidence_backed(name):
    rubric = (PROMPTS / name).read_text(encoding="utf-8").split("## Reading Priority", 1)[1]
    assert "or evidence-backed" not in rubric
    assert 'Do not call results "evidence-backed"' in rubric


def test_evidence_backed_is_not_a_high_signal():
    # Signals match by substring, so "evidence" alone would still reward "evidence-backed".
    assert not {"evidence", "evidence-backed", "data-backed"} & HIGH_SIGNAL_WORDS
