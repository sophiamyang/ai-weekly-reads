from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from project_paths import CONFIG
from utils import read_json


@dataclass(frozen=True)
class RegistryLink:
    url: str
    lookback_count: int | None = None
    source_name: str | None = None
    content_type: str | None = None
    filter_by_publication_window: bool = False


def load_source_registry(path: Path | None = None) -> dict[str, Any]:
    path = path or CONFIG / "sources.json"
    return read_json(path, {})


def registry_youtube_channels(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [channel for channel in registry.get("youtube_channels", []) if channel.get("url")]


def registry_links(registry: dict[str, Any]) -> list[RegistryLink]:
    links: list[RegistryLink] = []
    for podcast in registry.get("podcasts", []):
        rss_url = podcast.get("rssUrl")
        if rss_url:
            links.append(
                RegistryLink(
                    url=rss_url,
                    lookback_count=source_lookback_count(podcast, default=50),
                    source_name=podcast.get("name"),
                    content_type="podcast",
                    filter_by_publication_window=True,
                )
            )
    return links


def source_lookback_count(source: dict[str, Any], default: int) -> int:
    value = source.get("lookback_count", source.get("latest_count", default))
    return int(value)
