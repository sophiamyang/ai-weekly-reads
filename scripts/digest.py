from __future__ import annotations

from pathlib import Path

from config import Settings
from obsidian_metadata import obsidian_aliases, yaml_list_block
from obsidian_graph import weekly_resource_links
from public_epub import public_epub_markdown_url
from project_paths import OUTPUT, PUBLIC_LATEST_MD, PUBLIC_WEEKLY, WEEKLY_BOOKS
from summary_metadata import featured_speakers, without_featured_speakers
from utils import parse_date, read_text, split_frontmatter, strip_graph_only_sections, today_stamp, write_text, yaml_value


def build_digest(
    resource_paths: list[Path],
    settings: Settings,
    *,
    output_prefix: str = "kindle-digest",
    write_public_latest: bool = True,
    public_output_dir: Path = PUBLIC_WEEKLY,
    write_weekly_book: bool = True,
    include_title_date: bool = True,
    include_period_label: bool = True,
) -> Path:
    stamp = today_stamp()
    output_path = OUTPUT / f"{output_prefix}-{stamp}.md"
    weekly_book_path = WEEKLY_BOOKS / output_path.name
    title = f"{settings.digest_title} - {stamp}" if include_title_date else settings.digest_title
    lines: list[str] = [
        "---",
        f"title: {yaml_value(title)}",
        yaml_list_block("aliases", obsidian_aliases(title, f"AI Weekly Reads {stamp}")),
        f"created: {yaml_value(stamp)}",
        f"type: {yaml_value('weekly-book')}",
        f"status: {yaml_value('ready')}",
        f"language: {yaml_value('en')}",
        "---",
        "",
        f"# {settings.digest_title}",
        "",
    ]
    if include_period_label:
        lines.extend([f"Week of {stamp}", ""])
    lines.extend([f"[Download the latest EPUB for Kindle]({public_epub_markdown_url()})", ""])
    lines.extend(["## Contents", ""])
    for index, resource_path in enumerate(resource_paths, start=1):
        lines.append(f"{index}. [{_resource_source(resource_path)}] {_resource_date(resource_path)} - {_resource_title(resource_path)}")
    lines.extend(["", "## Reading Notes", ""])

    for resource_path in resource_paths:
        resource = read_text(resource_path)
        summary = _summary_part(resource)
        lines.append(summary.strip())
        lines.append("")
        lines.append("***")
        lines.append("")

    public_content = "\n".join(lines).strip() + "\n"

    if settings.include_full_transcripts:
        lines.extend(["# Appendix: Full Transcripts", ""])
        for resource_path in resource_paths:
            resource = read_text(resource_path)
            lines.append(f"## {_resource_title(resource_path)} ({_resource_date(resource_path)})")
            lines.append("")
            lines.append(_transcript_part(resource).strip())
            lines.append("")
            lines.append("***")
            lines.append("")

    content = "\n".join(lines).strip() + "\n"
    local_content = content.rstrip() + f"\n\n{weekly_resource_links(resource_paths)}\n"
    write_text(output_path, content)
    if write_weekly_book:
        write_text(weekly_book_path, local_content)
    if write_public_latest:
        write_text(public_output_dir / "latest.md", public_content)
        write_text(PUBLIC_LATEST_MD, public_content)
    return output_path


def _resource_title(resource_path: Path) -> str:
    fields, _body = split_frontmatter(read_text(resource_path))
    title = fields.get("title")
    if title:
        return str(title)
    return resource_path.stem


def _resource_source(resource_path: Path) -> str:
    fields, _body = split_frontmatter(read_text(resource_path))
    source_name = fields.get("source_name") or fields.get("source") or "unknown"
    source_type = _display_source_type(str(fields.get("content_type") or fields.get("source") or ""))
    if source_type and source_type != source_name:
        return f"{source_name} / {source_type}"
    return str(source_name)


def _resource_date(resource_path: Path) -> str:
    fields, _body = split_frontmatter(read_text(resource_path))
    value = str(fields.get("published") or fields.get("created") or "").strip()
    parsed = parse_date(value)
    return parsed.isoformat() if parsed else value or "unknown"


def _display_source_type(source_type: str) -> str:
    labels = {
        "youtube": "YouTube",
        "podcast": "Podcast",
        "video": "Video",
        "livestream": "Livestream",
        "web": "Web",
        "web_transcript": "Web Transcript",
        "direct_media": "Direct Media",
    }
    return labels.get(source_type, source_type or "Unknown")


def _summary_part(resource: str) -> str:
    marker = "\n# Full Transcript\n"
    fields, body = split_frontmatter(resource.split(marker, 1)[0].strip())
    body = strip_graph_only_sections(body)
    summary = _with_resource_metadata(body, fields)
    return "\n".join(_digest_line(line) for line in summary.splitlines() if not line.startswith("Raw transcript: [["))


def _with_resource_metadata(markdown: str, fields: dict) -> str:
    date_value = str(fields.get("published") or fields.get("created") or "").strip()
    parsed = parse_date(date_value)
    if parsed:
        date_value = parsed.isoformat()
    source_name = str(fields.get("source_name") or fields.get("source") or "unknown")
    source_type = _display_source_type(str(fields.get("content_type") or fields.get("source") or ""))
    source_label = source_name
    url = str(fields.get("url") or "").strip()
    speakers_value = fields.get("speakers")
    speakers = [str(value) for value in speakers_value] if isinstance(speakers_value, list) else []
    if not speakers:
        speakers = featured_speakers(markdown, str(fields.get("title") or ""))
    markdown = without_featured_speakers(markdown)
    lines = markdown.strip().splitlines()
    # Drop the bare metadata lines format_ai_summary writes under the H1, but
    # leave later summary content that happens to share those prefixes alone.
    header_end = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
    lines = [
        line
        for index, line in enumerate(lines)
        if index >= header_end or not line.startswith(("Published:", "Added:", "Date:", "Source:", "Original link:"))
    ]
    for index, line in enumerate(lines):
        if not line.startswith("# "):
            continue
        insert_at = index + 1
        while insert_at < len(lines) and not lines[insert_at].strip():
            lines.pop(insert_at)
        metadata = []
        if date_value:
            label = "Published" if fields.get("published") else "Added"
            metadata.append(f"- **{label}:** {date_value}")
        source_kind = source_type if source_type in {"YouTube", "Podcast", "Video", "Livestream"} else "Source"
        source_value = f"[{source_label}]({url})" if url else source_label
        metadata.append(f"- **{source_kind}:** {source_value}")
        if speakers:
            speaker_label = "Speakers" if len(speakers) > 1 else "Speaker"
            metadata.append(f"- **{speaker_label}:** {'; '.join(speakers)}")
        lines[insert_at:insert_at] = ["", *metadata, ""]
        break
    return "\n".join(lines)


def _transcript_part(resource: str) -> str:
    marker = "\n# Full Transcript\n"
    if marker not in resource:
        return ""
    return resource.split(marker, 1)[1].strip()


def _digest_line(line: str) -> str:
    return "***" if line.strip() == "---" else line
