from __future__ import annotations

import re
from pathlib import Path

from project_paths import (
    INDEXES,
    OBSIDIAN_CONFIG,
    PEOPLE_NOTES,
    RESOURCES,
    ROOT_OBSIDIAN_CONFIG,
    SOURCE_NOTES,
    TOPIC_NOTES,
)
from source_registry import load_source_registry
from utils import read_text, slugify, split_frontmatter, write_json, write_text, yaml_value


CONNECTIONS_HEADING = "## Connections"
DEFAULT_GRAPH_CONFIG = {
    "collapse-filter": False,
    "search": "-path:raw_transcripts -path:templates -path:people -path:sources -path:indexes -path:weekly_books -file:README -file:Home",
    "showTags": False,
    "showAttachments": False,
    "hideUnresolved": True,
    "showOrphans": False,
    "collapse-color-groups": False,
    "colorGroups": [
        {"query": "path:topics", "color": {"a": 1, "rgb": 16096779}},
        {"query": "path:resources", "color": {"a": 1, "rgb": 6583435}},
    ],
    "collapse-display": False,
    "showArrow": False,
    "textFadeMultiplier": -2,
    "nodeSizeMultiplier": 1,
    "lineSizeMultiplier": 1,
    "collapse-forces": False,
    "centerStrength": 0.45,
    "repelStrength": 20,
    "linkStrength": 1,
    "linkDistance": 220,
    "scale": 0.85,
    "close": True,
}
ROOT_GRAPH_CONFIG = {
    **DEFAULT_GRAPH_CONFIG,
    "search": (
        "-path:.github -path:assets -path:config -path:inbox -path:logs "
        "-path:output -path:prompts -path:scripts -path:skills -path:weekly "
        "-path:knowledge_base/raw_transcripts -path:knowledge_base/templates "
        "-path:knowledge_base/people -path:knowledge_base/sources "
        "-path:knowledge_base/indexes "
        "-path:knowledge_base/weekly_books -file:README -file:Home"
    ),
    "colorGroups": [
        {"query": "path:knowledge_base/topics", "color": {"a": 1, "rgb": 16096779}},
        {"query": "path:knowledge_base/resources", "color": {"a": 1, "rgb": 6583435}},
    ],
}


def refresh_resource_graph(resource_path: Path, *, refresh_indexes: bool = True) -> None:
    fields, body = split_frontmatter(read_text(resource_path))
    if not fields:
        return

    source_name = str(fields.get("source_name") or fields.get("source") or "Unknown").strip()
    source_type = str(fields.get("source") or "unknown").strip()
    source_url = _source_home_url(fields)
    speakers = _string_list(fields.get("speakers"))
    topics = [
        str(tag).removeprefix("topic/").strip()
        for tag in _string_list(fields.get("tags"))
        if str(tag).startswith("topic/")
    ]

    source_link = _ensure_source_note(source_name, source_type, source_url)
    speaker_links = [_ensure_person_note(speaker) for speaker in speakers]
    topic_links = [_ensure_topic_note(topic) for topic in topics]
    body = _replace_connections(body, source_link, speaker_links, topic_links)
    write_text(resource_path, _with_frontmatter(fields, body))
    if refresh_indexes:
        refresh_graph_indexes()


def refresh_all_resource_graphs() -> int:
    ensure_graph_config()
    changed = 0
    for path in sorted(RESOURCES.glob("*.md")):
        before = read_text(path)
        refresh_resource_graph(path, refresh_indexes=False)
        if read_text(path) != before:
            changed += 1
    _prune_orphan_hubs()
    refresh_graph_indexes()
    return changed


def ensure_graph_config() -> None:
    write_json(OBSIDIAN_CONFIG / "graph.json", DEFAULT_GRAPH_CONFIG)
    write_json(ROOT_OBSIDIAN_CONFIG / "graph.json", ROOT_GRAPH_CONFIG)


def refresh_weekly_book_graphs(weekly_books: Path) -> int:
    resources_by_title: dict[str, Path] = {}
    for resource_path in RESOURCES.glob("*.md"):
        fields, _body = split_frontmatter(read_text(resource_path))
        title = str(fields.get("title") or "").strip()
        if title:
            resources_by_title[title] = resource_path

    changed = 0
    for path in sorted(weekly_books.glob("*.md")):
        fields, body = split_frontmatter(read_text(path))
        if str(fields.get("language") or "en").lower() != "en":
            continue
        headings = {line.removeprefix("# ").strip() for line in body.splitlines() if line.startswith("# ")}
        included = [
            resource_path
            for title, resource_path in resources_by_title.items()
            if title in headings
        ]
        if not included:
            continue
        updated_body = _remove_section(body, "## Included Notes").strip()
        updated_body += f"\n\n{weekly_resource_links(included)}\n"
        updated = _with_frontmatter(fields, updated_body)
        if updated != read_text(path):
            write_text(path, updated)
            changed += 1
    return changed


def weekly_resource_links(resource_paths: list[Path]) -> str:
    lines = ["## Included Notes", ""]
    for path in resource_paths:
        fields, _body = split_frontmatter(read_text(path))
        title = str(fields.get("title") or path.stem)
        lines.append(f"- [[resources/{path.stem}|{title}]]")
    return "\n".join(lines).strip()


def refresh_graph_indexes() -> None:
    source_links = _note_links(SOURCE_NOTES)
    people_links = _note_links(PEOPLE_NOTES)
    topic_links = _note_links(TOPIC_NOTES)
    write_text(
        INDEXES / "Sources.md",
        _index_note("Sources", "source-index", source_links),
    )
    write_text(
        INDEXES / "People.md",
        _index_note("People", "people-index", people_links),
    )
    write_text(
        INDEXES / "Topics.md",
        _index_note("Topics", "topic-index", topic_links),
    )


def _ensure_source_note(name: str, source_type: str, url: str) -> str:
    filename = _hub_filename(name, "Unknown Source")
    path = SOURCE_NOTES / f"{filename}.md"
    lines = [
        "---",
        f"title: {yaml_value(name)}",
        f"type: {yaml_value('source')}",
        f"source_type: {yaml_value(source_type)}",
        "---",
        "",
        f"# {name}",
        "",
        f"Type: {source_type}",
    ]
    if url:
        lines.extend(["", f"Website: <{url}>"])
    lines.extend(["", "Resources from this source appear in the backlinks panel.", ""])
    write_text(path, "\n".join(lines))
    return f"[[sources/{filename}|{name}]]"


def _ensure_person_note(speaker: str) -> str:
    name, role = _speaker_parts(speaker)
    slug = slugify(name, "unknown-person")
    path = PEOPLE_NOTES / f"{slug}.md"
    lines = [
        "---",
        f"title: {yaml_value(name)}",
        "aliases:",
        f"  - {yaml_value(speaker)}",
        f"type: {yaml_value('person')}",
        "---",
        "",
        f"# {name}",
    ]
    if role:
        lines.extend(["", f"Role or affiliation: {role}"])
    lines.extend(["", "Appearances and related notes appear in the backlinks panel.", ""])
    write_text(path, "\n".join(lines))
    return f"[[people/{slug}|{name}]]"


def _ensure_topic_note(topic: str) -> str:
    title = _topic_title(topic)
    filename = _hub_filename(title, "Unknown Topic")
    path = TOPIC_NOTES / f"{filename}.md"
    lines = [
        "---",
        f"title: {yaml_value(title)}",
        f"type: {yaml_value('topic')}",
        "---",
        "",
        f"# {title}",
        "",
        "Related resources appear in the backlinks panel.",
        "",
    ]
    write_text(path, "\n".join(lines))
    return f"[[topics/{filename}|{title}]]"


def _replace_connections(
    body: str,
    source_link: str,
    speaker_links: list[str],
    topic_links: list[str],
) -> str:
    body = _remove_section(body, CONNECTIONS_HEADING).strip()
    lines = [CONNECTIONS_HEADING, "", f"- Source: {source_link}"]
    if topic_links:
        lines.append(f"- Topics: {', '.join(topic_links)}")
    if speaker_links:
        label = "Speakers" if len(speaker_links) > 1 else "Speaker"
        lines.append(f"- {label}: {', '.join(speaker_links)}")
    return f"{body}\n\n" + "\n".join(lines) + "\n"


def _remove_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        return markdown
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[:start] + lines[end:]).strip()


def _with_frontmatter(fields: dict, body: str) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_value(item)}")
        else:
            lines.append(f"{key}: {yaml_value(value)}")
    lines.extend(["---", "", body.strip(), ""])
    return "\n".join(lines)


def _speaker_parts(value: str) -> tuple[str, str]:
    value = value.strip()
    if " — " in value:
        name, role = value.split(" — ", 1)
        return name.strip(), role.strip()
    if "," in value:
        name, role = value.split(",", 1)
        if len(name.split()) >= 2:
            return name.strip(), role.strip()
    return value, ""


def _string_list(value: object) -> list[str]:
    return [str(item).strip() for item in value] if isinstance(value, list) else []


def _note_links(folder: Path) -> list[str]:
    links: list[str] = []
    for path in sorted(folder.glob("*.md")):
        fields, _body = split_frontmatter(read_text(path))
        title = str(fields.get("title") or path.stem)
        relative = path.relative_to(folder.parent).with_suffix("").as_posix()
        links.append(f"- [[{relative}|{title}]]")
    return links


def _index_note(title: str, note_type: str, links: list[str]) -> str:
    body = "\n".join(links) if links else "_No notes yet._"
    return "\n".join(
        [
            "---",
            f"title: {yaml_value(title)}",
            f"type: {yaml_value(note_type)}",
            "---",
            "",
            f"# {title}",
            "",
            body,
            "",
        ]
    )


def _prune_orphan_hubs() -> None:
    source_slugs: set[str] = set()
    people_slugs: set[str] = set()
    topic_slugs: set[str] = set()
    for resource_path in RESOURCES.glob("*.md"):
        text = read_text(resource_path)
        source_slugs.update(re.findall(r"\[\[sources/([^]|]+)", text))
        people_slugs.update(re.findall(r"\[\[people/([^]|]+)", text))
        topic_slugs.update(re.findall(r"\[\[topics/([^]|]+)", text))
    _prune_folder(SOURCE_NOTES, source_slugs)
    _prune_folder(PEOPLE_NOTES, people_slugs)
    _prune_folder(TOPIC_NOTES, topic_slugs)


def _prune_folder(folder: Path, active_slugs: set[str]) -> None:
    active_names = {name.casefold() for name in active_slugs}
    for path in folder.glob("*.md"):
        if path.stem.casefold() not in active_names:
            path.unlink()


def _hub_filename(value: str, fallback: str) -> str:
    clean = re.sub(r"[/\\:*?\"<>|]+", " - ", value)
    clean = re.sub(r"\s+", " ", clean).strip(" .-")
    return clean or fallback


def _topic_title(topic: str) -> str:
    words = topic.replace("-", " ").split()
    return " ".join("AI" if word.lower() == "ai" else word.title() for word in words)


def _source_home_url(fields: dict) -> str:
    source_name = str(fields.get("source_name") or "").strip()
    registry = load_source_registry()
    for channel in registry.get("youtube_channels", []):
        if source_name and source_name == str(channel.get("name") or "").strip():
            return str(channel.get("url") or "").strip()
    for podcast in registry.get("podcasts", []):
        if source_name and source_name == str(podcast.get("name") or "").strip():
            return str(podcast.get("url") or podcast.get("rssUrl") or "").strip()
    return str(fields.get("origin") or fields.get("url") or "").strip()
