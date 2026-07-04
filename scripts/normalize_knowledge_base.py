from __future__ import annotations

from pathlib import Path
from typing import Any

from obsidian_metadata import obsidian_aliases, raw_transcript_tags, resource_tags, weekly_book_tags, without_topics
from obsidian_graph import refresh_all_resource_graphs, refresh_weekly_book_graphs
from project_paths import RAW_TRANSCRIPTS, RESOURCES, WEEKLY_BOOKS
from reading_priority import normalize_reading_priority
from source_registry import load_source_registry
from summary_metadata import normalize_speakers
from summarize import is_placeholder_summary, strip_ai_response_wrappers
from resources import readable_resource_filename
from utils import as_bool, read_text, split_frontmatter, write_text, yaml_value


RESOURCE_FIELDS = [
    "id",
    "title",
    "aliases",
    "type",
    "source",
    "source_name",
    "content_type",
    "speakers",
    "url",
    "origin",
    "published",
    "transcript_method",
    "status",
    "priority",
    "raw_transcript",
    "created",
]

RAW_TRANSCRIPT_FIELDS = [
    "id",
    "title",
    "aliases",
    "source",
    "source_name",
    "content_type",
    "url",
    "origin",
    "type",
    "created",
]

WEEKLY_BOOK_FIELDS = [
    "title",
    "aliases",
    "created",
    "type",
    "status",
    "language",
    "source_digest",
    "source_digest_sha256",
]


def main() -> None:
    changed = 0
    changed += _rename_resource_files()
    changed += _normalize_folder(RESOURCES, "resource")
    changed += _normalize_folder(RAW_TRANSCRIPTS, "raw_transcript")
    changed += _normalize_folder(WEEKLY_BOOKS, "weekly_book")
    changed += refresh_all_resource_graphs()
    changed += refresh_weekly_book_graphs(WEEKLY_BOOKS)
    print(f"Normalized {changed} knowledge-base files.")


def _rename_resource_files() -> int:
    changed = 0
    for path in sorted(RESOURCES.glob("*.md")):
        fields, _body = split_frontmatter(read_text(path))
        item_id = str(fields.get("id") or "").strip()
        title = str(fields.get("title") or "").strip()
        if not item_id or not title:
            continue
        target = path.with_name(readable_resource_filename(title, item_id, path))
        if target != path:
            path.rename(target)
            changed += 1
    return changed


def _normalize_folder(folder: Path, kind: str) -> int:
    changed = 0
    for path in sorted(folder.glob("*.md")):
        text = read_text(path)
        normalized = _normalize_text(text, kind)
        if normalized != text:
            write_text(path, normalized)
            changed += 1
    return changed


def _normalize_text(text: str, kind: str) -> str:
    fields, body = split_frontmatter(text)
    if not fields:
        return text
    if kind in {"resource", "raw_transcript"}:
        fields["source_name"] = fields.get("source_name") or _infer_source_name(fields)

    if kind == "resource":
        fields["tags"] = resource_tags(body, str(fields.get("title") or ""), fields.get("tags"))
        body = without_topics(body)
        body = _strip_embedded_transcript(body)
        body = _clean_embedded_ai_wrapper(body)
        body = normalize_reading_priority(body, str(fields.get("title") or ""))
        fields["type"] = "resource"
        fields["aliases"] = _aliases(fields.get("aliases"), str(fields.get("title") or ""))
        fields["speakers"] = normalize_speakers(
            fields.get("speakers"),
            body,
            str(fields.get("title") or ""),
        )
        if is_placeholder_summary(body):
            fields["status"] = "needs_summary"
        else:
            fields["status"] = "summarized"
        frontmatter = _frontmatter(fields, RESOURCE_FIELDS, tags=_resource_tags(fields, body), omit_empty=True)
    elif kind == "raw_transcript":
        fields["type"] = "raw-transcript"
        title = str(fields.get("title") or "")
        fields["aliases"] = _aliases(fields.get("aliases"), title, title.removesuffix(" raw transcript"))
        frontmatter = _frontmatter(fields, RAW_TRANSCRIPT_FIELDS, tags=_raw_transcript_tags(fields), omit_empty=True)
    else:
        fields["type"] = fields.get("type") or "weekly-book"
        fields["status"] = fields.get("status") or "ready"
        fields["language"] = fields.get("language") or "en"
        fields["aliases"] = _aliases(fields.get("aliases"), str(fields.get("title") or ""))
        frontmatter = _frontmatter(fields, WEEKLY_BOOK_FIELDS, tags=_weekly_book_tags(fields), omit_empty=True)

    return f"{frontmatter}\n\n{body.strip()}\n"


def _frontmatter(
    fields: dict[str, Any],
    ordered_fields: list[str],
    *,
    tags: list[str],
    omit_empty: bool = False,
) -> str:
    lines = ["---"]
    send_to_kindle_line = None
    if "priority" in ordered_fields or "send_to_kindle" in fields:
        send_to_kindle_line = f"send_to_kindle: {yaml_value(as_bool(fields.get('send_to_kindle', True)))}"
    for key in ordered_fields:
        value = fields.get(key, "")
        if omit_empty and (value == "" or value is None or value == []):
            continue
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_value(item)}")
        else:
            lines.append(f"{key}: {yaml_value(value)}")
        if key == "priority" and send_to_kindle_line:
            lines.append(send_to_kindle_line)
            send_to_kindle_line = None
    if send_to_kindle_line:
        lines.append(send_to_kindle_line)
    if tags:
        lines.append("tags:")
        for tag in tags:
            lines.append(f"  - {yaml_value(tag)}")
    lines.append("---")
    return "\n".join(lines)


def _strip_embedded_transcript(body: str) -> str:
    marker = "\n# Full Transcript\n"
    if marker in body:
        return body.split(marker, 1)[0].rstrip()
    return body


def _clean_embedded_ai_wrapper(body: str) -> str:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        lowered = line.strip().lower()
        # Only treat a line as an AI response wrapper when it looks like a
        # preamble ("Here is the markdown summary:"), not prose that merely
        # mentions both words.
        if "markdown" not in lowered or "here is" not in lowered or not lowered.endswith(":"):
            continue
        before = "\n".join(lines[:index]).rstrip()
        cleaned = strip_ai_response_wrappers("\n".join(lines[index:]))
        return f"{before}\n\n{cleaned.strip()}\n"
    return body


def _resource_tags(fields: dict[str, Any], body: str) -> list[str]:
    return resource_tags(body, str(fields.get("title") or ""), fields.get("tags"))


def _raw_transcript_tags(fields: dict[str, Any]) -> list[str]:
    source = str(fields.get("source") or "unknown")
    return raw_transcript_tags(source, fields.get("tags"))


def _weekly_book_tags(fields: dict[str, Any]) -> list[str]:
    status = str(fields.get("status") or "ready")
    language = str(fields.get("language") or "en")
    return weekly_book_tags(status, language, fields.get("tags"))


def _aliases(existing: object, *required: str) -> list[str]:
    values = [str(value) for value in existing] if isinstance(existing, list) else []
    return obsidian_aliases(*values, *required)


def _infer_source_name(fields: dict[str, Any]) -> str:
    registry = load_source_registry()
    origin = str(fields.get("origin") or "")
    source = str(fields.get("source") or "unknown")
    for podcast in registry.get("podcasts", []):
        if origin and origin == podcast.get("rssUrl"):
            return str(podcast.get("name") or source)
    youtube_channels = registry.get("youtube_channels", [])
    if source == "youtube" and len(youtube_channels) == 1:
        return str(youtube_channels[0].get("name") or source)
    return source


if __name__ == "__main__":
    main()
