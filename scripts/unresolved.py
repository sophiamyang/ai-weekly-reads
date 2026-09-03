"""Durable record of items that were discovered but never produced a transcript.

Without this, a failed item exists only in `output/_metadata/last_run.json` —
which is gitignored, overwritten every run, and lost when an ephemeral cloud
container is reclaimed. Once the publication window moves past the item, it is
never rediscovered either, so it disappears with no record that it was ever
wanted. That is the silent drop this pipeline is otherwise careful to avoid.

The ledger lives in the knowledge base so it persists with the rest of the
state, and it feeds two things: retries that ignore the publication window, and
an audit line that makes outstanding failures visible.
"""
from __future__ import annotations

from dataclasses import fields as dataclass_fields
from datetime import date
from pathlib import Path

from project_paths import KNOWLEDGE_BASE
from sources import MediaItem
from utils import read_json, write_json

UNRESOLVED_PATH = KNOWLEDGE_BASE / "unresolved.json"

# Retrying forever would starve new items: YouTube transcription is capped by a
# daily Gemini quota, so every attempt spent on a permanently captionless video
# is one a fresh item does not get. Stop retrying after this many runs, but keep
# the record — abandoned is not the same as forgotten.
MAX_ATTEMPTS = 4

# Retries compete with new content for the same daily Gemini quota, so cap how
# many a single run will take on. Without this, a large backlog of stuck items
# could consume the whole quota and no new item would be transcribed at all.
MAX_RETRIES_PER_RUN = 10

_ITEM_FIELDS = {field.name for field in dataclass_fields(MediaItem)}


def load_unresolved(path: Path = UNRESOLVED_PATH) -> dict[str, dict]:
    entries = read_json(path, {})
    return entries if isinstance(entries, dict) else {}


def record_unavailable(item: MediaItem, reason: str, path: Path = UNRESOLVED_PATH) -> None:
    """Note that an item failed, or bump its attempt count if already known."""
    entries = load_unresolved(path)
    today = date.today().isoformat()
    existing = entries.get(item.id) or {}
    entries[item.id] = {
        # Descriptions are third-party show-note text and are not needed to
        # retry, so they are left out rather than persisted.
        **{k: v for k, v in item.to_dict().items() if k != "description"},
        "reason": reason,
        "attempts": int(existing.get("attempts") or 0) + 1,
        "first_seen": existing.get("first_seen") or today,
        "last_attempt": today,
    }
    write_json(path, entries)


def clear_resolved(item_id: str, path: Path = UNRESOLVED_PATH) -> bool:
    """Drop an item that has since succeeded. Returns whether anything changed."""
    entries = load_unresolved(path)
    if item_id not in entries:
        return False
    entries.pop(item_id)
    write_json(path, entries)
    return True


def retryable_items(path: Path = UNRESOLVED_PATH) -> list[MediaItem]:
    """Previously failed items still worth another attempt.

    These bypass the publication window deliberately: they were in the window
    when first discovered, and the whole point is that the window has since
    moved past them.
    """
    items = []
    for entry in load_unresolved(path).values():
        if int(entry.get("attempts") or 0) >= MAX_ATTEMPTS:
            continue
        kwargs = {k: v for k, v in entry.items() if k in _ITEM_FIELDS}
        if not kwargs.get("id") or not kwargs.get("url"):
            continue
        items.append(MediaItem(**kwargs))
    # Oldest failures first, so nothing waits behind a steady stream of newer
    # ones, then bounded.
    items.sort(key=lambda i: i.published or "")
    return items[:MAX_RETRIES_PER_RUN]


def abandoned_items(path: Path = UNRESOLVED_PATH) -> list[dict]:
    """Items that exhausted their retries — reported, never silently dropped."""
    return [e for e in load_unresolved(path).values() if int(e.get("attempts") or 0) >= MAX_ATTEMPTS]
