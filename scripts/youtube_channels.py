from __future__ import annotations

import subprocess
import sys
from typing import Any

from utils import ytdlp_js_runtime_args


def latest_channel_video_urls(channels: list[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    seen_channels: set[str] = set()
    for channel in channels:
        channel_url = str(channel.get("url", "")).strip()
        if not channel_url or channel_url in seen_channels:
            continue
        seen_channels.add(channel_url)
        lookback_count = _lookback_count(channel, default=50)
        urls.extend(_fetch_channel_urls(channel_url, lookback_count))
    return _dedupe(urls)


def _lookback_count(channel: dict[str, Any], default: int) -> int:
    value = channel.get("lookback_count", channel.get("latest_count", default))
    return int(value)


def _fetch_channel_urls(channel_url: str, lookback_count: int) -> list[str]:
    feed_url = _channel_feed_url(channel_url)
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        *ytdlp_js_runtime_args(),
        "--flat-playlist",
        "--playlist-end",
        str(lookback_count),
        "--print",
        "%(url)s",
        feed_url,
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except Exception as exc:
        print(f"Could not fetch YouTube channel {channel_url}: {exc}")
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip().startswith("http")]


def _channel_feed_url(channel_url: str) -> str:
    channel_url = channel_url.rstrip("/")
    explicit_tabs = ("/videos", "/streams", "/shorts", "/playlists", "/featured")
    if "playlist?list=" in channel_url or channel_url.endswith(explicit_tabs):
        return channel_url
    return f"{channel_url}/videos"


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique.append(value)
    return unique
