from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

from project_paths import RESOURCES
from obsidian_metadata import obsidian_aliases, resource_tags, without_topics, yaml_list_block
from obsidian_graph import refresh_resource_graph
from reading_priority import normalize_reading_priority
from sources import MediaItem
from summary_metadata import featured_speakers
from summarize import is_placeholder_summary
from transcript_store import find_raw_transcript, read_transcript_text, write_raw_transcript
from utils import as_bool, parse_date, read_text, split_frontmatter, write_text, yaml_value


def write_resource(
    item: MediaItem,
    summary_path: Path,
    transcript_path: Path,
    transcript_method: str,
) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d")
    existing = find_resource(item.id)
    existing_fields = _resource_fields(existing) if existing else {}
    filename = existing.name if existing else readable_resource_filename(item.title, item.id)
    resource_path = existing or RESOURCES / filename
    summary = read_text(summary_path).strip()
    summary = normalize_reading_priority(summary, item.title).strip()
    transcript = read_transcript_text(transcript_path)
    raw_transcript_path = write_raw_transcript(item, transcript, find_raw_transcript(item.id))
    status = "needs_summary" if is_placeholder_summary(summary) else "summarized"
    priority = "medium"
    aliases = yaml_list_block("aliases", obsidian_aliases(item.title))
    speakers = featured_speakers(summary, item.title)
    speakers_block = f"{yaml_list_block('speakers', speakers)}\n" if speakers else ""
    # A rewrite (e.g. re-summarizing a placeholder) must not clobber curated
    # frontmatter: keep the user's send_to_kindle choice and topic tags.
    send_to_kindle = as_bool(existing_fields.get("send_to_kindle", True))
    tags = yaml_list_block("tags", resource_tags(summary, item.title, existing_fields.get("tags")))
    summary = without_topics(summary)

    body = f"""---
id: {yaml_value(item.id)}
title: {yaml_value(item.title)}
{aliases}
type: {yaml_value("resource")}
source: {yaml_value(item.source_type)}
source_name: {yaml_value(item.source_name or item.source_type)}
content_type: {yaml_value(item.content_type or "")}
{speakers_block}url: {yaml_value(item.url)}
origin: {yaml_value(item.origin)}
published: {yaml_value(item.published or "")}
transcript_method: {yaml_value(transcript_method)}
status: {yaml_value(status)}
priority: {yaml_value(priority)}
send_to_kindle: {yaml_value(send_to_kindle)}
raw_transcript: {yaml_value(f"raw_transcripts/{raw_transcript_path.name}")}
created: {yaml_value(stamp)}
{tags}
---

Raw transcript: [[raw_transcripts/{raw_transcript_path.stem}|{item.title} raw transcript]]

{summary}
"""
    write_text(resource_path, body)
    refresh_resource_graph(resource_path)
    return resource_path


def find_resource(item_id: str) -> Path | None:
    for path in sorted(RESOURCES.glob("*.md")):
        fields, _body = split_frontmatter(read_text(path))
        if str(fields.get("id") or "") == item_id:
            return path
    return None


def readable_resource_filename(title: str, item_id: str, current: Path | None = None) -> str:
    graph_title = re.split(r"\s+[—–]\s+", title, maxsplit=1)[0]
    graph_title = re.sub(r"\s+with\s+.+$", "", graph_title, flags=re.IGNORECASE)
    clean = re.sub(r"[/\\:*?\"<>|]+", " - ", graph_title)
    clean = re.sub(r"\s+", " ", clean).strip(" .-")
    if len(clean) > 90:
        clean = clean[:90].rsplit(" ", 1)[0].rstrip(" .-")
    clean = clean or f"Resource {item_id[:8]}"
    candidate = RESOURCES / f"{clean}.md"
    if candidate == current or not candidate.exists():
        return candidate.name
    fields, _body = split_frontmatter(read_text(candidate))
    if str(fields.get("id") or "") == item_id:
        return candidate.name
    return f"{clean} ({item_id[:8]}).md"


def list_resources(limit: int | None = None, since: date | None = None) -> list[Path]:
    resources: list[tuple[Path, dict]] = []
    for path in RESOURCES.glob("*.md"):
        fields = _resource_fields(path)
        if not as_bool(fields.get("send_to_kindle", True)):
            print(f"Excluding resource marked send_to_kindle: false: {fields.get('title') or path.stem}")
            continue
        if fields.get("status") == "summarized" and _resource_fields_in_window(fields, since):
            resources.append((path, fields))

    resources.sort(key=lambda row: _resource_sort_key(*row), reverse=True)
    paths = [path for path, _fields in resources]
    if limit is not None:
        return paths[:limit]
    return paths


def is_summarized_resource(path: Path) -> bool:
    return _resource_fields(path).get("status") == "summarized"


def _resource_fields(path: Path) -> dict:
    fields, _body = split_frontmatter(read_text(path))
    return fields


def _resource_fields_in_window(fields: dict, since: date | None) -> bool:
    if since is None:
        return True
    resource_date = _resource_date(fields)
    return resource_date is None or resource_date >= since


def _resource_sort_key(path: Path, fields: dict) -> tuple[date, str]:
    return (
        _resource_date(fields) or date.min,
        str(fields.get("title") or path.stem).lower(),
    )


def _resource_date(fields: dict) -> date | None:
    return parse_date(str(fields.get("published") or "")) or parse_date(str(fields.get("created") or ""))
