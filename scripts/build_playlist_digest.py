from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

from config import load_settings
from digest import build_digest
from ebook import build_kindle_file
from public_epub import publish_public_epub
from project_paths import PUBLIC_ONE_SHOT, ROOT, ensure_dirs
from resources import find_resource, is_summarized_resource, write_resource
from send_to_kindle import maybe_send_to_kindle
from sources import MediaItem, resolve_link
from substack import build_substack_post, substack_status
from summarize import get_or_create_summary, is_placeholder_summary, should_refresh_summary, summary_path_for
from transcripts import get_or_create_transcript
from utils import load_dotenv, read_text, slugify, ytdlp_js_runtimes


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Build a one-shot Kindle/Substack/public digest from a YouTube playlist.")
    parser.add_argument("playlist_url", help="YouTube playlist URL")
    parser.add_argument("--title", help="Digest title. Defaults to the YouTube playlist title.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum playlist videos to inspect.")
    parser.add_argument("--send-kindle", action="store_true", help="Send the generated Kindle file.")
    parser.add_argument("--force-kindle", action="store_true", help="Resend to Kindle even if the same file hash was sent before.")
    parser.add_argument("--substack", action="store_true", help="Build a Substack-ready Markdown post.")
    args = parser.parse_args()

    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    playlist_title, video_urls = _playlist_videos(args.playlist_url, args.limit)
    digest_title = args.title or playlist_title or "AI Weekly Reads Playlist"
    if not video_urls:
        raise SystemExit("No videos found in playlist.")

    resource_paths = _process_videos(video_urls, settings)
    if not resource_paths:
        raise SystemExit("No summarized resources were available for this playlist.")

    playlist_settings = replace(settings, digest_title=digest_title)
    output_prefix = f"playlist-{slugify(digest_title, fallback='youtube-playlist')}"
    digest_path = build_digest(
        resource_paths,
        playlist_settings,
        output_prefix=output_prefix,
        public_output_dir=PUBLIC_ONE_SHOT,
        write_weekly_book=False,
        include_title_date=False,
        include_period_label=False,
    )
    kindle_path = build_kindle_file(digest_path, settings)
    print(f"Playlist digest written: {digest_path}")
    if kindle_path != digest_path:
        print(f"Playlist Kindle file written: {kindle_path}")
    public_digest_path = PUBLIC_ONE_SHOT / "latest.md"
    print(f"Public one-shot digest written: {public_digest_path}")
    print(publish_public_epub(kindle_path, PUBLIC_ONE_SHOT / "latest.epub"))

    if args.send_kindle:
        print(maybe_send_to_kindle(kindle_path, settings, force=args.force_kindle))
    if args.substack:
        print(substack_status(build_substack_post(digest_path, settings, force=True)))


def _playlist_videos(playlist_url: str, limit: int) -> tuple[str, list[str]]:
    try:
        import yt_dlp
    except ImportError as exc:
        raise SystemExit("yt-dlp is not installed. Run `.venv/bin/pip install -r requirements.txt`.") from exc

    options: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "playlistend": limit,
        "js_runtimes": ytdlp_js_runtimes(),
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
    title = str(info.get("title") or "").strip()
    urls = []
    for entry in info.get("entries") or []:
        # yt-dlp yields None entries for unavailable/private videos.
        if not entry:
            continue
        url = entry.get("url") or entry.get("webpage_url")
        if not url:
            continue
        if not str(url).startswith("http"):
            url = f"https://www.youtube.com/watch?v={url}"
        urls.append(str(url))
    return title, _dedupe(urls)


def _process_videos(video_urls: list[str], settings) -> list[Path]:
    resource_paths: list[Path] = []
    for index, video_url in enumerate(video_urls, start=1):
        print(f"[{index}/{len(video_urls)}] Resolving: {video_url}")
        for item in resolve_link(video_url, feed_limit=1):
            resource_path = _get_or_create_resource(item, settings)
            if resource_path:
                resource_paths.append(resource_path)
    return _dedupe_paths(resource_paths)


def _get_or_create_resource(item: MediaItem, settings) -> Path | None:
    existing_resource = find_resource(item.id)
    if existing_resource and is_summarized_resource(existing_resource):
        print(f"Reusing summarized resource: {item.title}")
        return existing_resource

    transcript_path, transcript_method = get_or_create_transcript(item, settings)
    if not transcript_path or transcript_method == "unavailable":
        print(f"Skipping resource without transcript: {item.title}")
        return None

    summary_path = summary_path_for(item)
    if should_refresh_summary(summary_path, settings):
        print(f"Summarizing: {item.title}")
    summary_path = get_or_create_summary(item, transcript_path, settings)
    if is_placeholder_summary(read_text(summary_path)):
        print(f"Skipping resource without generated summary: {item.title}")
        return None

    resource_path = write_resource(item, summary_path, transcript_path, transcript_method)
    summary_path.unlink(missing_ok=True)
    print(f"Resource written: {resource_path}")
    return resource_path


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _dedupe_paths(values: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


if __name__ == "__main__":
    main()
