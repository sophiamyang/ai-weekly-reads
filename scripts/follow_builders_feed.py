from __future__ import annotations

from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - depends on local environment
    requests = None

from config import Settings
from sources import MediaItem
from utils import stable_id


FEED_FILENAMES = {
    "podcasts": "feed-podcasts.json",
}


def follow_builders_items(settings: Settings) -> list[MediaItem]:
    config = settings.follow_builders
    if not config.get("enabled", False):
        return []
    if requests is None:
        print("Skipping follow-builders feed: requests is not installed")
        return []

    items: list[MediaItem] = []
    if config.get("include_podcasts", False):
        feed = _fetch_feed(config, "podcasts")
        _warn_if_short_feed(feed, "podcast", settings)
        items.extend(_podcast_items(feed))
    return items


def _fetch_feed(config: dict[str, Any], key: str) -> dict[str, Any]:
    base_url = str(config.get("base_url") or "").rstrip("/")
    if not base_url:
        return {}
    url = f"{base_url}/{FEED_FILENAMES[key]}"
    try:
        response = requests.get(url, timeout=30, headers={"User-Agent": "AIWeeklyReads/0.1"})
        response.raise_for_status()
        payload = response.json()
        return payload if isinstance(payload, dict) else {}
    except Exception as exc:
        print(f"Could not fetch follow-builders {key} feed: {exc}")
        return {}


def _warn_if_short_feed(feed: dict[str, Any], label: str, settings: Settings) -> None:
    lookback_hours = feed.get("lookbackHours")
    desired_hours = settings.publication_window_days * 24
    if not lookback_hours or desired_hours <= 0:
        return
    try:
        actual_hours = int(lookback_hours)
    except (TypeError, ValueError):
        return
    if actual_hours < desired_hours:
        print(
            f"follow-builders {label} feed covers {actual_hours} hours; "
            f"AI Weekly Reads publication window is {desired_hours} hours."
        )


def _podcast_items(feed: dict[str, Any]) -> list[MediaItem]:
    items: list[MediaItem] = []
    for episode in feed.get("podcasts", []):
        url = str(episode.get("url") or "").strip()
        transcript = str(episode.get("transcript") or "").strip()
        if not url or not transcript:
            continue
        title = str(episode.get("title") or url).strip()
        source_name = str(episode.get("name") or "Podcast").strip()
        stable_key = episode.get("guid") or url
        items.append(
            MediaItem(
                id=stable_id(f"follow-builders:podcast:{stable_key}"),
                url=url,
                source_type="podcast",
                title=title,
                origin="follow-builders:feed-podcasts.json",
                source_name=source_name,
                content_type="podcast",
                published=str(episode.get("publishedAt") or ""),
                description=transcript,
            )
        )
    return items
