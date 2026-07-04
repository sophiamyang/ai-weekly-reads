from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from config import Settings
from public_epub import public_epub_markdown_url, public_epub_repo_url
from project_paths import SUBSTACK_OUTPUT
from utils import read_text, slugify, split_frontmatter, strip_graph_only_sections, write_text


DEFAULT_INTRO = (
    "A weekly reading packet from the past week, with source dates, channel or publication names, "
    "speakers when available, and concise reading notes."
)
PLAYLIST_INTRO = (
    "A one-shot reading packet from this playlist, with source dates, channel names, speakers when "
    "available, and concise reading notes."
)


def build_substack_post(digest_path: Path, settings: Settings, *, force: bool = False) -> Path | None:
    substack = settings.substack
    if not force and not substack.get("enabled"):
        return None

    fields, body = split_frontmatter(read_text(digest_path))
    title = str(fields.get("title") or _title_from_body(body) or settings.digest_title).strip()
    created = str(fields.get("created") or "").strip()
    is_playlist = _looks_like_playlist_digest(digest_path, title)
    intro = str(substack.get("intro") or (PLAYLIST_INTRO if is_playlist else DEFAULT_INTRO)).strip()

    body = _prepare_body(body, title, intro, is_playlist=is_playlist)
    body = _replace_public_epub_link(body, public_epub_repo_url(_public_epub_relative_path(is_playlist)))
    output_path = _output_path(title, created)
    write_text(output_path, body)

    latest_path = SUBSTACK_OUTPUT / "latest.md"
    write_text(latest_path, body)
    return output_path


def _prepare_body(markdown: str, title: str, intro: str, *, is_playlist: bool) -> str:
    body = strip_graph_only_sections(markdown.strip())
    body = _strip_obsidian_links(body)
    body = _remove_obsidian_lines(body)
    body = _remove_duplicate_item_headings(body)
    body = _remove_internal_horizontal_rules(body)
    body = _remove_placeholder_citations(body)
    if is_playlist:
        body = _remove_week_of_line(body)
    body = _collapse_blank_lines(body)
    body = _replace_first_h1(body, title)
    lines = body.splitlines()

    if intro:
        insert_at = 1 if lines and lines[0].startswith("# ") else 0
        while insert_at < len(lines) and not lines[insert_at].strip():
            lines.pop(insert_at)
        lines[insert_at:insert_at] = ["", intro, ""]

    return "\n".join(lines).strip() + "\n"


def _replace_public_epub_link(markdown: str, absolute_url: str) -> str:
    relative_target = f"]({public_epub_markdown_url()})"
    if absolute_url:
        return markdown.replace(relative_target, f"]({absolute_url})")
    # Without an absolute URL the relative link would be dead on Substack;
    # drop the download line entirely.
    return "\n".join(line for line in markdown.splitlines() if relative_target not in line)


def _public_epub_relative_path(is_playlist: bool) -> str:
    if is_playlist:
        return "one-shot/latest.epub"
    return "weekly/latest.epub"


def _strip_obsidian_links(markdown: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        if "|" in target:
            return target.rsplit("|", 1)[1]
        return Path(target).stem.replace("-", " ")

    return re.sub(r"\[\[([^\]]+)\]\]", replace, markdown)


def _remove_obsidian_lines(markdown: str) -> str:
    removed_prefixes = (
        "Resource note:",
        "Raw transcript:",
        "Source note:",
        "Topic note:",
        "People note:",
        "**Source type:**",
        "**URL:**",
        "**Published:**",
        "Source type:",
        "URL:",
        "Published:",
    )
    lines = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in removed_prefixes):
            continue
        lines.append(line)
    return "\n".join(lines)


def _remove_duplicate_item_headings(markdown: str) -> str:
    lines = []
    current_title = ""
    for line in markdown.splitlines():
        if line.startswith("# "):
            current_title = _normalized_heading(line.removeprefix("# "))
            lines.append(line)
            continue
        if line.startswith("## ") and _is_duplicate_subheading(current_title, line.removeprefix("## ")):
            continue
        lines.append(line)
    return "\n".join(lines)


def _remove_internal_horizontal_rules(markdown: str) -> str:
    lines = markdown.splitlines()
    kept: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() == "***" and _next_nonblank(lines, index).startswith("## "):
            continue
        kept.append(line)
    return "\n".join(kept)


def _remove_placeholder_citations(markdown: str) -> str:
    return re.sub(r"\s+\(example URL format\)", "", markdown)


def _remove_week_of_line(markdown: str) -> str:
    return "\n".join(line for line in markdown.splitlines() if not re.match(r"^Week of \d{4}-\d{2}-\d{2}$", line.strip()))


def _collapse_blank_lines(markdown: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", markdown)


def _replace_first_h1(markdown: str, title: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines[index] = f"# {title}"
            return "\n".join(lines)
    return f"# {title}\n\n{markdown.strip()}"


def _title_from_body(markdown: str) -> str | None:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return None


def _normalized_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def _is_duplicate_subheading(current_title: str, subheading: str) -> bool:
    normalized = _normalized_heading(subheading)
    if not normalized:
        return False
    if normalized == current_title:
        return True
    # Treat only long fragments as repeats of the item title, so a short
    # section heading like "Main Ideas" is never stripped just because the
    # item title happens to contain those words.
    return len(normalized) >= 25 and normalized in current_title


def _next_nonblank(lines: list[str], index: int) -> str:
    for line in lines[index + 1 :]:
        if line.strip():
            return line
    return ""


def _output_path(title: str, created: str) -> Path:
    base = slugify(title, fallback="ai-weekly-reads")
    if created and created not in base:
        base = f"{base}-{slugify(created, fallback='date')}"
    return SUBSTACK_OUTPUT / f"{base}.md"


def _looks_like_playlist_digest(digest_path: Path, title: str) -> bool:
    return digest_path.name.startswith("playlist-") or "playlist" in title.lower() or "@" in title


def substack_status(path: Path | None) -> str:
    if path is None:
        return "Substack export disabled."
    return f"Substack post written: {path}"
