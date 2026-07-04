from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from config import Settings
from digest import build_digest
from ebook import build_kindle_file
from follow_builders_feed import follow_builders_items
from mistral_batch import SummaryBatchItem, summarize_with_mistral_batch
from project_paths import INBOX, METADATA
from public_epub import publish_public_epub
from resources import find_resource, is_summarized_resource, list_resources, write_resource
from send_to_kindle import maybe_send_to_kindle
from source_registry import RegistryLink, load_source_registry, registry_links, registry_youtube_channels
from sources import MediaItem, read_inbox, resolve_link
from substack import build_substack_post, substack_status
from summarize import get_or_create_summary, is_placeholder_summary, should_refresh_summary, summary_path_for
from transcripts import get_or_create_transcript
from utils import parse_date, read_text, write_json
from youtube_channels import latest_channel_video_urls


@dataclass
class RunStats:
    resolved_items: int = 0
    reused_resources: int = 0
    unavailable_transcripts: int = 0
    batch_summaries: int = 0
    direct_summaries: int = 0
    resources_written: int = 0
    placeholder_summaries: int = 0
    skipped_outside_window: int = 0
    skipped_missing_date: int = 0


@dataclass(frozen=True)
class BuildArtifacts:
    digest_path: Path
    kindle_path: Path
    substack_path: Path | None
    weekly_resource_count: int


def update_knowledge_base(settings: Settings) -> RunStats:
    publication_cutoff = publication_cutoff_for(settings)
    stats = RunStats()
    items = discover_items(settings, publication_cutoff, stats)
    stats.resolved_items = len(items)

    metadata = []
    ready_items = []
    batch_items: list[SummaryBatchItem] = []

    for item in items:
        print(f"Processing: {item.title}")
        transcript_path, transcript_method = get_or_create_transcript(item, settings)
        row = item.to_dict()
        row["transcript_method"] = transcript_method
        row["transcript_path"] = str(transcript_path) if transcript_path else ""
        if transcript_method == "unavailable":
            row["summary_path"] = ""
            row["resource_path"] = ""
            metadata.append(row)
            print(f"Skipping resource without transcript: {item.title}")
            stats.unavailable_transcripts += 1
            continue

        existing_resource = find_resource(item.id)
        if existing_resource and is_summarized_resource(existing_resource):
            row["summary_path"] = ""
            row["resource_path"] = str(existing_resource)
            metadata.append(row)
            stats.reused_resources += 1
            continue

        summary_path = summary_path_for(item)
        summary_needs_refresh = should_refresh_summary(summary_path, settings)
        if summary_needs_refresh and _batch_summaries_enabled(settings):
            ready_items.append((item, transcript_path, transcript_method, row))
            batch_items.append(SummaryBatchItem(item=item, transcript_path=transcript_path))
            stats.batch_summaries += 1
            continue

        if summary_needs_refresh:
            stats.direct_summaries += 1
        summary_path = get_or_create_summary(item, transcript_path, settings)
        _write_resource_metadata(item, summary_path, transcript_path, transcript_method, row, metadata, stats)

    if batch_items:
        try:
            summarize_with_mistral_batch(batch_items, settings)
        except Exception as exc:
            print(f"Mistral batch summary failed, falling back to direct summaries: {exc}")
            for batch_item in batch_items:
                get_or_create_summary(batch_item.item, batch_item.transcript_path, settings)
                stats.direct_summaries += 1

    for item, transcript_path, transcript_method, row in ready_items:
        summary_path = summary_path_for(item)
        _write_resource_metadata(item, summary_path, transcript_path, transcript_method, row, metadata, stats)

    write_json(METADATA / "last_run.json", metadata)
    return stats


def discover_items(settings: Settings, publication_cutoff: date | None, stats: RunStats) -> list[MediaItem]:
    registry = load_source_registry()
    queued_links = [RegistryLink(url=link) for link in read_inbox(INBOX / "links.txt", settings.feeds)]
    queued_links.extend(registry_links(registry))
    channels = [*settings.youtube_channels, *registry_youtube_channels(registry)]
    for channel in channels:
        source_name = str(channel.get("name") or "").strip() or None
        content_type = str(channel.get("content_type") or "").strip() or None
        queued_links.extend(
            RegistryLink(
                url=url,
                source_name=source_name,
                content_type=content_type,
                filter_by_publication_window=True,
                require_publication_date=True,
            )
            for url in latest_channel_video_urls([channel])
        )
    queued_links = _dedupe_links(queued_links)

    items: list[MediaItem] = []
    seen_item_ids: set[str] = set()
    for item in follow_builders_items(settings):
        _add_item(item, settings, publication_cutoff, stats, items, seen_item_ids, filter_by_publication_window=True)

    for link in queued_links:
        print(f"Resolving: {link.url}")
        for item in resolve_link(link.url, feed_limit=link.lookback_count or 10):
            if link.source_name and not item.source_name:
                item.source_name = link.source_name
            if link.content_type and not item.content_type:
                item.content_type = link.content_type
            _add_item(
                item,
                settings,
                publication_cutoff,
                stats,
                items,
                seen_item_ids,
                filter_by_publication_window=link.filter_by_publication_window,
                require_publication_date=link.require_publication_date,
            )
            if _run_limit_reached(len(items), settings.max_items_per_run):
                break
        if _run_limit_reached(len(items), settings.max_items_per_run):
            break
    return items


def build_weekly_artifacts(settings: Settings) -> BuildArtifacts | None:
    publication_cutoff = publication_cutoff_for(settings)
    weekly_resources = list_resources(settings.weekly_resource_limit, since=publication_cutoff)
    if not weekly_resources:
        if publication_cutoff:
            print(f"No summarized resources published or created since {publication_cutoff}.")
        else:
            print("No links or knowledge-base resources found. Add links to inbox/links.txt.")
        return None
    digest_path = build_digest(weekly_resources, settings)
    kindle_path = build_kindle_file(digest_path, settings)
    print(f"Digest written: {digest_path}")
    if kindle_path != digest_path:
        print(f"Kindle file written: {kindle_path}")
    try:
        print(publish_public_epub(kindle_path))
    except Exception as exc:
        print(f"Public EPUB publish failed: {exc}")
    substack_path = build_substack_post(digest_path, settings)
    print(substack_status(substack_path))
    return BuildArtifacts(
        digest_path=digest_path,
        kindle_path=kindle_path,
        substack_path=substack_path,
        weekly_resource_count=len(weekly_resources),
    )


def deliver_to_kindle(kindle_path: Path, settings: Settings, *, force: bool = False) -> str:
    return maybe_send_to_kindle(kindle_path, settings, force=force)


def publication_cutoff_for(settings: Settings) -> date | None:
    if settings.publication_window_days <= 0:
        return None
    try:
        now = datetime.now(ZoneInfo(settings.timezone))
    except ZoneInfoNotFoundError:
        now = datetime.now()
    return now.date() - timedelta(days=settings.publication_window_days)


def print_run_summary(stats: RunStats, weekly_resource_count: int | None = None) -> None:
    print("Run summary:")
    print(f"- resolved items: {stats.resolved_items}")
    print(f"- reused summarized resources: {stats.reused_resources}")
    print(f"- queued batch summaries: {stats.batch_summaries}")
    print(f"- direct fallback summaries: {stats.direct_summaries}")
    print(f"- resources written: {stats.resources_written}")
    print(f"- skipped without transcript: {stats.unavailable_transcripts}")
    print(f"- skipped without generated summary: {stats.placeholder_summaries}")
    print(f"- skipped outside publication window: {stats.skipped_outside_window}")
    if stats.skipped_missing_date:
        print(f"- skipped without resolvable publication date: {stats.skipped_missing_date}")
    if weekly_resource_count is not None:
        print(f"- weekly resources included: {weekly_resource_count}")


def _add_item(
    item: MediaItem,
    settings: Settings,
    publication_cutoff: date | None,
    stats: RunStats,
    items: list[MediaItem],
    seen_item_ids: set[str],
    *,
    filter_by_publication_window: bool,
    require_publication_date: bool = False,
) -> bool:
    if filter_by_publication_window and publication_cutoff is not None:
        published = parse_date(item.published)
        if published is None and require_publication_date:
            print(f"Skipping item without resolvable publication date: {item.title or item.url}")
            stats.skipped_missing_date += 1
            return False
        if published is not None and published < publication_cutoff:
            stats.skipped_outside_window += 1
            return False
    if _run_limit_reached(len(items), settings.max_items_per_run):
        return False
    if item.id in seen_item_ids:
        return False
    items.append(item)
    seen_item_ids.add(item.id)
    return True


def _batch_summaries_enabled(settings) -> bool:
    return (
        settings.summary_provider == "mistral"
        and settings.summary_mode == "batch"
        and bool(os.environ.get("MISTRAL_API_KEY"))
    )


def _run_limit_reached(item_count: int, max_items_per_run: int) -> bool:
    return max_items_per_run > 0 and item_count >= max_items_per_run


def _write_resource_metadata(
    item: MediaItem,
    summary_path,
    transcript_path,
    transcript_method: str,
    row: dict,
    metadata: list[dict],
    stats: RunStats,
) -> None:
    if is_placeholder_summary(read_text(summary_path)):
        summary_path.unlink(missing_ok=True)
        row["summary_path"] = str(summary_path)
        row["resource_path"] = ""
        metadata.append(row)
        print(f"Skipping resource without generated summary: {item.title}")
        stats.placeholder_summaries += 1
        return

    resource_path = write_resource(item, summary_path, transcript_path, transcript_method)
    summary_path.unlink(missing_ok=True)
    row["summary_path"] = str(summary_path)
    row["resource_path"] = str(resource_path)
    metadata.append(row)
    stats.resources_written += 1


def _dedupe_links(links: list[RegistryLink]) -> list[RegistryLink]:
    seen: set[str] = set()
    unique: list[RegistryLink] = []
    for link in links:
        if link.url in seen:
            continue
        seen.add(link.url)
        unique.append(link)
    return unique
