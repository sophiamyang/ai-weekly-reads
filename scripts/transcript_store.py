from __future__ import annotations

from datetime import datetime
from pathlib import Path

from obsidian_metadata import obsidian_aliases, yaml_list_block
from project_paths import RAW_TRANSCRIPTS
from sources import MediaItem
from utils import read_text, slugify, split_frontmatter, write_text, yaml_value


def find_raw_transcript(item_id: str) -> Path | None:
    matches = sorted(RAW_TRANSCRIPTS.glob(f"*-{item_id}.md"))
    if matches:
        return matches[0]
    for path in sorted(RAW_TRANSCRIPTS.glob("*.md")):
        fields, _body = split_frontmatter(read_text(path))
        if str(fields.get("id") or "") == item_id:
            return path
    return None


def write_raw_transcript(item: MediaItem, transcript: str, path: Path | None = None) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d")
    path = path or RAW_TRANSCRIPTS / f"{stamp}-{item.source_type}-{slugify(item.title, item.id)}-{item.id}.md"
    aliases = yaml_list_block(
        "aliases",
        obsidian_aliases(f"{item.title} raw transcript", item.title),
    )
    body = f"""---
id: {yaml_value(item.id)}
title: {yaml_value(f"{item.title} raw transcript")}
{aliases}
source: {yaml_value(item.source_type)}
source_name: {yaml_value(item.source_name or item.source_type)}
content_type: {yaml_value(item.content_type or "")}
url: {yaml_value(item.url)}
origin: {yaml_value(item.origin)}
type: {yaml_value("raw-transcript")}
created: {yaml_value(stamp)}
---

# {item.title} Raw Transcript

{transcript.strip()}
"""
    write_text(path, body)
    return path


def read_transcript_text(path: Path) -> str:
    text = read_text(path).strip()
    if not path.name.endswith(".md") or not text.startswith("---\n"):
        return text
    _fields, text = split_frontmatter(text)
    text = text.strip()
    lines = text.splitlines()
    if lines and lines[0].startswith("# ") and lines[0].endswith(" Raw Transcript"):
        lines = lines[1:]
    return "\n".join(lines).strip()
