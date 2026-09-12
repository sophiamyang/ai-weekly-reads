from __future__ import annotations

import sources


# --- read_inbox -------------------------------------------------------------

def test_read_inbox_skips_comments_and_blank_lines(tmp_path) -> None:
    inbox = tmp_path / "links.txt"
    inbox.write_text(
        "# a comment\n"
        "\n"
        "https://example.com/one\n"
        "   \n"
        "  https://example.com/two  \n"
        "# trailing comment\n",
        encoding="utf-8",
    )

    assert sources.read_inbox(inbox, []) == [
        "https://example.com/one",
        "https://example.com/two",
    ]


def test_read_inbox_tolerates_a_utf8_bom(tmp_path) -> None:
    # Files saved by some Windows editors start with a BOM; without utf-8-sig
    # the first link silently becomes "﻿https://..." and never matches.
    inbox = tmp_path / "links.txt"
    inbox.write_text("https://example.com/one\n", encoding="utf-8-sig")

    assert sources.read_inbox(inbox, []) == ["https://example.com/one"]


def test_read_inbox_appends_configured_feeds_and_dedupes(tmp_path) -> None:
    inbox = tmp_path / "links.txt"
    inbox.write_text("https://example.com/one\nhttps://example.com/two\n", encoding="utf-8")

    links = sources.read_inbox(inbox, ["https://example.com/two", "https://example.com/three"])

    # Order preserved, inbox first, duplicate dropped.
    assert links == [
        "https://example.com/one",
        "https://example.com/two",
        "https://example.com/three",
    ]


def test_read_inbox_handles_a_missing_file(tmp_path) -> None:
    assert sources.read_inbox(tmp_path / "nope.txt", ["https://example.com/feed"]) == [
        "https://example.com/feed"
    ]


# --- _entry_stable_key ------------------------------------------------------

def test_entry_stable_key_prefers_the_feed_guid() -> None:
    entry = {
        "id": "guid-123",
        "link": "https://example.com/ep1?utm_source=rss",
        "title": "Episode 1",
    }

    assert sources._entry_stable_key(entry, "https://cdn.example.com/1.mp3", "https://feed") == "guid-123"


def test_entry_stable_key_survives_a_changing_link() -> None:
    # The point of keying on the guid: a publisher rewriting its URLs must not
    # make every past episode look new.
    before = {"id": "guid-123", "link": "https://old.example.com/ep1"}
    after = {"id": "guid-123", "link": "https://new.example.com/2026/ep1"}

    assert sources._entry_stable_key(before, None, "https://feed") == sources._entry_stable_key(
        after, None, "https://feed"
    )


def test_entry_stable_key_falls_back_through_link_then_audio() -> None:
    link_only = {"link": "https://example.com/ep1"}
    assert sources._entry_stable_key(link_only, "https://cdn/1.mp3", "https://feed") == "https://example.com/ep1"

    audio_only: dict = {}
    assert sources._entry_stable_key(audio_only, "https://cdn/1.mp3", "https://feed") == "https://cdn/1.mp3"


def test_entry_stable_key_last_resort_is_feed_scoped() -> None:
    entry = {"title": "Episode 1", "published": "2026-09-01"}

    key = sources._entry_stable_key(entry, None, "https://feed.example.com/rss")

    # Two shows can both have an "Episode 1"; the feed url keeps them apart.
    assert key.startswith("https://feed.example.com/rss")
    other = sources._entry_stable_key(entry, None, "https://other.example.com/rss")
    assert key != other


# --- _entry_published -------------------------------------------------------

def test_entry_published_prefers_the_parsed_struct() -> None:
    entry = {
        "published_parsed": (2026, 9, 1, 13, 30, 0, 0, 0, 0),
        "published": "whatever the string said",
    }

    assert sources._entry_published(entry) == "2026-09-01"


def test_entry_published_falls_back_to_updated_struct() -> None:
    entry = {"updated_parsed": (2026, 8, 15, 0, 0, 0, 0, 0, 0)}

    assert sources._entry_published(entry) == "2026-08-15"


def test_entry_published_returns_raw_string_when_unparsed() -> None:
    assert sources._entry_published({"published": "Mon, 01 Sep 2026 13:30:00 +0000"}) == (
        "Mon, 01 Sep 2026 13:30:00 +0000"
    )


def test_entry_published_is_none_when_absent() -> None:
    assert sources._entry_published({}) is None


# --- _looks_like_media_url --------------------------------------------------

def test_looks_like_media_url_matches_audio_and_video_extensions() -> None:
    for url in (
        "https://cdn.example.com/ep1.mp3",
        "https://cdn.example.com/ep1.M4A",
        "https://cdn.example.com/clip.mp4",
        "https://cdn.example.com/clip.webm",
    ):
        assert sources._looks_like_media_url(url), url


def test_looks_like_media_url_ignores_query_strings() -> None:
    assert sources._looks_like_media_url("https://cdn.example.com/ep1.mp3?token=abc&t=12")


def test_looks_like_media_url_rejects_pages() -> None:
    for url in (
        "https://example.com/episode",
        "https://example.com/episode.html",
        "https://example.com/mp3",
    ):
        assert not sources._looks_like_media_url(url), url


# --- resolve_link routing ---------------------------------------------------

def test_resolve_link_rejects_non_urls() -> None:
    assert sources.resolve_link("not a url") == []
    assert sources.resolve_link("ftp://example.com/file.mp3") == []


def test_resolve_link_routes_spotify_without_fetching() -> None:
    items = sources.resolve_link("https://open.spotify.com/episode/abc123")

    assert len(items) == 1
    assert items[0].source_type == "spotify"


def test_resolve_link_routes_a_bare_media_url() -> None:
    items = sources.resolve_link("https://cdn.example.com/ep1.mp3?token=abc")

    assert len(items) == 1
    item = items[0]
    assert item.source_type == "direct_media"
    assert item.audio_url == "https://cdn.example.com/ep1.mp3?token=abc"
    # Title comes from the filename, with the query string stripped.
    assert item.title == "ep1.mp3"
