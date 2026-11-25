"""Routing in update_knowledge_base: each item is skipped, reused, or summarized.

A wrong branch here either spends API calls on work that already exists or
silently drops an item from the edition, so the collaborators are stubbed and
only the routing is exercised.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

import pipeline
from sources import MediaItem


def _item(item_id: str) -> MediaItem:
    return MediaItem(
        id=item_id,
        url=f"https://example.com/{item_id}",
        source_type="podcast",
        title=f"Episode {item_id}",
        origin="https://feed.example.com/rss",
        published="2026-09-05",
    )


@pytest.fixture
def run(monkeypatch, tmp_path):
    """Stub pipeline collaborators; return a function that runs one pass."""
    calls: dict[str, list] = {
        "record_unavailable": [],
        "clear_resolved": [],
        "get_or_create_summary": [],
        "write_metadata": [],
        "last_run": [],
    }

    def configure(
        items,
        *,
        transcript_methods=None,
        summarized_resources=(),
        needs_refresh=True,
        batch=False,
    ):
        transcript_methods = transcript_methods or {}

        monkeypatch.setattr(pipeline, "publication_cutoff_for", lambda settings: None)
        monkeypatch.setattr(pipeline, "discover_items", lambda settings, cutoff, stats: list(items))

        def fake_transcript(item, settings):
            method = transcript_methods.get(item.id, "youtube")
            path = None if method == "unavailable" else tmp_path / f"{item.id}.txt"
            return path, method

        monkeypatch.setattr(pipeline, "get_or_create_transcript", fake_transcript)
        monkeypatch.setattr(
            pipeline,
            "record_unavailable",
            lambda item, reason: calls["record_unavailable"].append(item.id),
        )
        monkeypatch.setattr(pipeline, "clear_resolved", lambda item_id: calls["clear_resolved"].append(item_id))
        monkeypatch.setattr(
            pipeline,
            "find_resource",
            lambda item_id: tmp_path / f"{item_id}.resource.md" if item_id in summarized_resources else None,
        )
        monkeypatch.setattr(pipeline, "is_summarized_resource", lambda path: True)
        monkeypatch.setattr(pipeline, "summary_path_for", lambda item: tmp_path / f"{item.id}.summary.md")
        monkeypatch.setattr(pipeline, "should_refresh_summary", lambda path, settings: needs_refresh)
        monkeypatch.setattr(pipeline, "_batch_summaries_enabled", lambda settings: batch)

        def fake_summary(item, transcript_path, settings):
            calls["get_or_create_summary"].append(item.id)
            return tmp_path / f"{item.id}.summary.md"

        monkeypatch.setattr(pipeline, "get_or_create_summary", fake_summary)
        monkeypatch.setattr(pipeline, "summarize_with_mistral_batch", lambda batch_items, settings: None)

        def fake_write_metadata(item, summary_path, transcript_path, transcript_method, row, metadata, stats):
            calls["write_metadata"].append(item.id)
            metadata.append(row)

        monkeypatch.setattr(pipeline, "_write_resource_metadata", fake_write_metadata)
        monkeypatch.setattr(pipeline, "write_json", lambda path, data: calls["last_run"].append(data))

        stats = pipeline.update_knowledge_base(SimpleNamespace())
        return stats, calls

    return configure


def _last_run_ids(calls) -> list[str]:
    return [row["id"] for row in calls["last_run"][-1]]


def test_item_without_transcript_is_recorded_and_not_summarized(run) -> None:
    stats, calls = run([_item("a")], transcript_methods={"a": "unavailable"})

    assert stats.unavailable_transcripts == 1
    assert calls["record_unavailable"] == ["a"]
    assert calls["clear_resolved"] == []
    assert calls["get_or_create_summary"] == []
    # Still listed in last_run.json so the skip is visible, with no paths.
    row = calls["last_run"][-1][0]
    assert row["summary_path"] == "" and row["resource_path"] == ""


def test_already_summarized_resource_is_reused_without_a_model_call(run) -> None:
    stats, calls = run([_item("a")], summarized_resources={"a"})

    assert stats.reused_resources == 1
    assert stats.direct_summaries == 0
    assert calls["get_or_create_summary"] == []
    assert calls["clear_resolved"] == ["a"]
    assert calls["last_run"][-1][0]["resource_path"].endswith("a.resource.md")


def test_item_needing_a_summary_is_summarized_directly(run) -> None:
    stats, calls = run([_item("a")], needs_refresh=True)

    assert stats.direct_summaries == 1
    assert calls["get_or_create_summary"] == ["a"]
    assert calls["write_metadata"] == ["a"]


def test_fresh_summary_is_not_counted_as_new_work(run) -> None:
    stats, calls = run([_item("a")], needs_refresh=False)

    # get_or_create_summary is still called (it returns the cached file),
    # but the run should not report it as a new summary.
    assert stats.direct_summaries == 0
    assert calls["write_metadata"] == ["a"]


def test_batch_mode_defers_summaries_and_still_writes_metadata(run) -> None:
    stats, calls = run([_item("a"), _item("b")], needs_refresh=True, batch=True)

    assert stats.batch_summaries == 2
    assert calls["get_or_create_summary"] == []
    assert calls["write_metadata"] == ["a", "b"]


def test_mixed_run_routes_each_item_once(run) -> None:
    items = [_item("missing"), _item("reused"), _item("new")]
    stats, calls = run(
        items,
        transcript_methods={"missing": "unavailable"},
        summarized_resources={"reused"},
    )

    assert (stats.unavailable_transcripts, stats.reused_resources, stats.direct_summaries) == (1, 1, 1)
    assert calls["get_or_create_summary"] == ["new"]
    assert sorted(_last_run_ids(calls)) == ["missing", "new", "reused"]
