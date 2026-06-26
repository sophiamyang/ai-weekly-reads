from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

try:
    import feedparser
except ImportError:  # pragma: no cover - depends on local environment
    feedparser = None

try:
    import requests
except ImportError:  # pragma: no cover - depends on local environment
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - depends on local environment
    BeautifulSoup = None

from utils import is_url, stable_id, youtube_video_id, ytdlp_js_runtimes


@dataclass
class MediaItem:
    id: str
    url: str
    source_type: str
    title: str
    origin: str
    source_name: str | None = None
    content_type: str | None = None
    audio_url: str | None = None
    published: str | None = None
    description: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def read_inbox(path: Path, configured_feeds: Iterable[str]) -> list[str]:
    links: list[str] = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
    links.extend(configured_feeds)
    seen: set[str] = set()
    unique: list[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique.append(link)
    return unique


def resolve_link(url: str, feed_limit: int = 10) -> list[MediaItem]:
    if not is_url(url):
        return []
    if youtube_video_id(url):
        return [_youtube_item(url)]
    if "spotify.com" in url:
        return [MediaItem(id=stable_id(url), url=url, source_type="spotify", title=url, origin=url)]
    if _looks_like_media_url(url):
        return [
            MediaItem(
                id=stable_id(url),
                url=url,
                source_type="direct_media",
                title=Path(url.split("?", 1)[0]).name or url,
                origin=url,
                audio_url=url,
            )
        ]

    feed_items = _try_parse_feed(url, limit=feed_limit)
    if feed_items:
        return feed_items

    return [_parse_web_page(url)]


def _try_parse_feed(url: str, limit: int = 10) -> list[MediaItem]:
    if feedparser is None:
        return []
    try:
        if requests is not None:
            response = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent": "AIWeeklyReads/0.1",
                    "Accept": "application/rss+xml, application/xml, text/xml, */*",
                },
            )
            response.raise_for_status()
            parsed = feedparser.parse(response.content)
        else:
            parsed = feedparser.parse(url)
    except Exception as exc:
        print(f"Skipping feed that could not be fetched: {url} ({exc})")
        return []
    if not parsed.entries:
        return []
    items: list[MediaItem] = []
    for entry in parsed.entries[:limit]:
        audio_url = _entry_audio_url(entry)
        episode_key = _entry_stable_key(entry, audio_url, url)
        link = entry.get("link") or audio_url or url
        title = entry.get("title") or link
        items.append(
            MediaItem(
                id=stable_id(episode_key),
                url=link,
                source_type="podcast",
                title=title,
                origin=url,
                content_type="podcast",
                audio_url=audio_url,
                published=_entry_published(entry),
                description=_html_to_text(entry.get("summary", "")),
            )
        )
    return items


def _entry_stable_key(entry: dict, audio_url: str | None, feed_url: str) -> str:
    return (
        entry.get("id")
        or entry.get("guid")
        or entry.get("link")
        or audio_url
        or f"{feed_url}:{entry.get('title', '')}:{entry.get('published', '')}"
    )


def _entry_published(entry: dict) -> str | None:
    published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if published_parsed:
        return datetime(*published_parsed[:6], tzinfo=timezone.utc).date().isoformat()
    return entry.get("published") or entry.get("updated")


def _youtube_item(url: str) -> MediaItem:
    title = url
    description = None
    published = None
    source_name = None
    try:
        import yt_dlp

        with yt_dlp.YoutubeDL(
            {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "extract_flat": False,
                "js_runtimes": ytdlp_js_runtimes(),
            }
        ) as ydl:
            info = ydl.extract_info(url, download=False)
        title = info.get("title") or title
        description = info.get("description")
        source_name = info.get("channel") or info.get("uploader")
        upload_date = info.get("upload_date")
        if upload_date and len(upload_date) == 8:
            published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    except Exception:
        pass
    return MediaItem(
        id=stable_id(url),
        url=url,
        source_type="youtube",
        title=title,
        origin=url,
        source_name=source_name,
        published=published,
        description=description,
    )


def _entry_audio_url(entry: dict) -> str | None:
    for enclosure in entry.get("enclosures", []):
        href = enclosure.get("href")
        if href:
            return href
    for link in entry.get("links", []):
        link_type = (link.get("type") or "").lower()
        href = link.get("href")
        if href and (link_type.startswith("audio/") or link_type.startswith("video/")):
            return href
    return None


def _parse_web_page(url: str) -> MediaItem:
    title = url
    description = None
    audio_url = None
    source_type = "web"
    if requests is None or BeautifulSoup is None:
        return MediaItem(
            id=stable_id(url),
            url=url,
            source_type=source_type,
            title=title,
            origin=url,
            description="Install dependencies with `pip install -r requirements.txt` to fetch web pages.",
        )
    try:
        response = requests.get(url, timeout=20, headers={"User-Agent": "AIWeeklyReads/0.1"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        description = _page_text(soup)
        audio = soup.find("audio")
        if audio:
            source = audio.find("source")
            audio_url = audio.get("src") or (source.get("src") if source else None)
            if audio_url:
                audio_url = urljoin(url, audio_url)
        if audio_url:
            source_type = "podcast_page"
        elif _looks_like_transcript(description or ""):
            source_type = "web_transcript"
    except Exception as exc:
        description = f"Could not fetch page yet: {exc}"
    return MediaItem(
        id=stable_id(url),
        url=url,
        source_type=source_type,
        title=title,
        origin=url,
        audio_url=audio_url,
        description=description,
    )


def _page_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    candidates = soup.find_all(["article", "main"])
    root = candidates[0] if candidates else soup.body or soup
    text = root.get_text("\n", strip=True)
    return "\n".join(line for line in text.splitlines() if line.strip())


def _html_to_text(value: str) -> str:
    if BeautifulSoup is None:
        return value or ""
    return BeautifulSoup(value or "", "html.parser").get_text("\n", strip=True)


def _looks_like_transcript(value: str) -> bool:
    lowered = value.lower()
    return "transcript" in lowered and len(value.split()) > 500


def _looks_like_media_url(url: str) -> bool:
    path = url.split("?", 1)[0].lower()
    return path.endswith((".mp3", ".m4a", ".wav", ".aac", ".mp4", ".mov", ".webm"))
