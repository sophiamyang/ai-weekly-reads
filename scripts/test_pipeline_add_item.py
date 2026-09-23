from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pipeline
from sources import MediaItem


def _item(item_id: str = "id-1", published: str | None = "2026-09-05") -> MediaItem:
    return MediaItem(
        id=item_id,
        url=f"https://example.com/{item_id}",
        source_type="podcast",
        title=f"Episode {item_id}",
        origin="https://feed.example.com/rss",
        published=published,
    )


def _settings(max_items_per_run: int = 0) -> SimpleNamespace:
    return SimpleNamespace(max_items_per_run=max_items_per_run)


def _stats() -> pipeline.RunStats:
    return pipeline.RunStats()


def _add(item, *, cutoff=None, settings=None, items=None, seen=None, **kwargs):
    items = [] if items is None else items
    seen = set() if seen is None else seen
    stats = kwargs.pop("stats", None) or _stats()
    added = pipeline._add_item(
        item,
        settings or _settings(),
        cutoff,
        stats,
        items,
        seen,
        **kwargs,
    )
    return added, items, stats


# --- publication window -----------------------------------------------------

def test_item_inside_the_window_is_kept() -> None:
    added, items, _ = _add(
        _item(published="2026-09-05"),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=True,
    )

    assert added is True
    assert len(items) == 1


def test_item_before_the_cutoff_is_dropped() -> None:
    added, items, stats = _add(
        _item(published="2026-08-20"),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=True,
    )

    assert added is False
    assert items == []
    assert stats.skipped_outside_window == 1


def test_the_cutoff_day_itself_is_inside_the_window() -> None:
    # Boundary: the filter is `published < cutoff`, so an item published exactly
    # on the cutoff belongs to the edition rather than the one before it.
    added, items, _ = _add(
        _item(published="2026-09-01"),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=True,
    )

    assert added is True
    assert len(items) == 1


def test_window_is_not_applied_when_filtering_is_off() -> None:
    added, items, _ = _add(
        _item(published="2020-01-01"),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=False,
    )

    assert added is True
    assert len(items) == 1


def test_no_cutoff_means_no_window_filtering() -> None:
    added, _items, _ = _add(
        _item(published="2020-01-01"),
        cutoff=None,
        filter_by_publication_window=True,
    )

    assert added is True


# --- missing publication dates ----------------------------------------------

def test_undated_item_is_kept_when_a_date_is_not_required() -> None:
    added, items, stats = _add(
        _item(published=None),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=True,
        require_publication_date=False,
    )

    assert added is True
    assert len(items) == 1
    assert stats.skipped_missing_date == 0


def test_undated_item_is_dropped_when_a_date_is_required() -> None:
    # Channel discovery sets require_publication_date, so an item whose date
    # cannot be resolved does not silently join whatever edition is building.
    added, items, stats = _add(
        _item(published=None),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=True,
        require_publication_date=True,
    )

    assert added is False
    assert items == []
    assert stats.skipped_missing_date == 1


def test_unparseable_date_counts_as_missing() -> None:
    added, _items, stats = _add(
        _item(published="sometime last week"),
        cutoff=date(2026, 9, 1),
        filter_by_publication_window=True,
        require_publication_date=True,
    )

    assert added is False
    assert stats.skipped_missing_date == 1


# --- dedup ------------------------------------------------------------------

def test_an_already_seen_id_is_not_added_twice() -> None:
    items: list[MediaItem] = []
    seen: set[str] = set()

    first, items, _ = _add(_item("dup"), items=items, seen=seen, filter_by_publication_window=False)
    second, items, _ = _add(_item("dup"), items=items, seen=seen, filter_by_publication_window=False)

    assert first is True
    assert second is False
    assert len(items) == 1


def test_distinct_ids_are_both_added() -> None:
    items: list[MediaItem] = []
    seen: set[str] = set()

    _add(_item("a"), items=items, seen=seen, filter_by_publication_window=False)
    _add(_item("b"), items=items, seen=seen, filter_by_publication_window=False)

    assert len(items) == 2


# --- per-run limit ----------------------------------------------------------

def test_run_limit_stops_further_items() -> None:
    items: list[MediaItem] = []
    seen: set[str] = set()
    settings = _settings(max_items_per_run=2)

    results = [
        _add(_item(f"i{n}"), settings=settings, items=items, seen=seen,
             filter_by_publication_window=False)[0]
        for n in range(4)
    ]

    assert results == [True, True, False, False]
    assert len(items) == 2


def test_zero_limit_means_unlimited() -> None:
    items: list[MediaItem] = []
    seen: set[str] = set()
    settings = _settings(max_items_per_run=0)

    for n in range(5):
        _add(_item(f"i{n}"), settings=settings, items=items, seen=seen,
             filter_by_publication_window=False)

    assert len(items) == 5
