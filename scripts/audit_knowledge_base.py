from __future__ import annotations

from collections import Counter
from pathlib import Path

from obsidian_metadata import is_operational_tag, resource_tags
from project_paths import INDEXES, METADATA, RAW_TRANSCRIPTS, RESOURCES, WEEKLY_BOOKS
from resources import is_summarized_resource
from transcript_store import read_transcript_text
from utils import read_json, read_text, split_frontmatter


PLACEHOLDER_MARKERS = [
    "AI summary is not enabled yet",
    "Not generated in local fallback mode",
    "Mistral summary failed",
    "AI summary failed",
    "Transcript excerpt:",
]


def main() -> None:
    resource_paths = sorted(RESOURCES.glob("*.md"))
    transcript_paths = sorted(RAW_TRANSCRIPTS.glob("*.md"))
    weekly_books = sorted(WEEKLY_BOOKS.glob("*.md"))
    last_run = read_json(METADATA / "last_run.json", [])

    resource_fields = [_fields(path) for path in resource_paths]
    transcript_fields = [_fields(path) for path in transcript_paths]
    resource_ids = [str(fields.get("id", "")) for fields in resource_fields if fields.get("id")]
    transcript_ids = [str(fields.get("id", "")) for fields in transcript_fields if fields.get("id")]
    resource_keys = [_content_key(fields) for fields in resource_fields]
    transcript_keys = [_content_key(fields) for fields in transcript_fields]

    summarized = [path for path in resource_paths if is_summarized_resource(path)]
    missing_raw = [
        path
        for path, fields in zip(resource_paths, resource_fields, strict=False)
        if fields.get("id") and str(fields.get("id")) not in transcript_ids
    ]
    broken_raw_links = [
        path
        for path, fields in zip(resource_paths, resource_fields, strict=False)
        if fields.get("raw_transcript") and not _raw_transcript_link_exists(str(fields.get("raw_transcript")))
    ]
    placeholders = [path for path in resource_paths if _has_placeholder(path)]
    short_transcripts = [path for path in transcript_paths if len(read_transcript_text(path).split()) < 250]
    metadata_issues = _metadata_issues(resource_paths, transcript_paths, weekly_books)
    graph_issues = _graph_issues(resource_paths, weekly_books)

    print("AI Weekly Reads Audit")
    print("====================")
    print(f"Resources: {len(resource_paths)} total, {len(summarized)} summarized")
    print(f"Raw transcripts: {len(transcript_paths)} total")
    print(f"Weekly books: {len(weekly_books)}")
    print(f"Last run items: {len(last_run) if isinstance(last_run, list) else 0}")
    print("")
    _print_issues("Duplicate resource ids", _duplicates(resource_ids))
    _print_issues("Duplicate transcript ids", _duplicates(transcript_ids))
    _print_issues("Duplicate resource titles", _duplicates(resource_keys))
    _print_issues("Duplicate transcript titles", _duplicates(transcript_keys))
    _print_paths("Resources missing raw transcripts", missing_raw)
    _print_paths("Resources with broken raw transcript links", broken_raw_links)
    _print_paths("Resources with placeholder summaries", placeholders)
    _print_paths("Very short raw transcripts", short_transcripts)
    _print_issues("Obsidian metadata issues", metadata_issues)
    _print_issues("Obsidian graph issues", graph_issues)
    if not any(
        [
            _duplicates(resource_ids),
            _duplicates(transcript_ids),
            _duplicates(resource_keys),
            _duplicates(transcript_keys),
            missing_raw,
            broken_raw_links,
            placeholders,
            short_transcripts,
            metadata_issues,
            graph_issues,
        ]
    ):
        print("No audit issues found.")


def _fields(path: Path) -> dict:
    fields, _body = split_frontmatter(read_text(path))
    return fields


def _has_placeholder(path: Path) -> bool:
    text = read_text(path)
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def _raw_transcript_link_exists(value: str) -> bool:
    path = RAW_TRANSCRIPTS.parent / value
    if path.exists():
        return True
    return (RAW_TRANSCRIPTS / Path(value).name).exists()


def _content_key(fields: dict) -> str:
    source_name = str(fields.get("source_name") or fields.get("origin") or fields.get("source") or "")
    title = str(fields.get("title") or "").removesuffix(" raw transcript")
    return f"{source_name}::{title}".strip(":")


def _duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _metadata_issues(resource_paths: list[Path], transcript_paths: list[Path], weekly_books: list[Path]) -> list[str]:
    issues: list[str] = []
    for path in resource_paths:
        fields = _fields(path)
        _fields_unused, body = split_frontmatter(read_text(path))
        expected = resource_tags(body, str(fields.get("title") or ""), fields.get("tags"))
        issues.extend(
            _frontmatter_issues(
                path,
                fields,
                "resource",
                expected,
                require_aliases=True,
                require_topic_tags=True,
            )
        )
    for path in transcript_paths:
        fields = _fields(path)
        issues.extend(_frontmatter_issues(path, fields, "raw-transcript", [], require_aliases=True))
    for path in weekly_books:
        fields = _fields(path)
        issues.extend(_frontmatter_issues(path, fields, "weekly-book", [], require_aliases=True))
    return issues


def _frontmatter_issues(
    path: Path,
    fields: dict,
    expected_type: str,
    expected_tags: list[str],
    *,
    require_aliases: bool,
    require_topic_tags: bool = False,
) -> list[str]:
    issues: list[str] = []
    if fields.get("type") != expected_type:
        issues.append(f"{path}: type should be {expected_type!r}")
    if require_aliases and not fields.get("aliases"):
        issues.append(f"{path}: aliases should not be empty")
    tags = fields.get("tags")
    if require_topic_tags and not isinstance(tags, list):
        issues.append(f"{path}: resource tags should be a YAML list")
        return issues
    if tags == "" or tags is None:
        tags = []
    if not isinstance(tags, list):
        issues.append(f"{path}: tags should be a YAML list when present")
        return issues
    operational = [tag for tag in tags if is_operational_tag(str(tag))]
    if operational:
        issues.append(f"{path}: operational tags should be Properties instead: {', '.join(operational)}")
    invalid_topics = [str(tag) for tag in tags if not str(tag).startswith("topic/")]
    if invalid_topics:
        issues.append(f"{path}: non-topic tags found: {', '.join(invalid_topics)}")
    if require_topic_tags and not 2 <= len(tags) <= 4:
        issues.append(f"{path}: resources should have 2-4 topic tags")
    missing_tags = [tag for tag in expected_tags if tag not in tags]
    if missing_tags:
        issues.append(f"{path}: missing tags {', '.join(missing_tags)}")
    return issues


def _graph_issues(resource_paths: list[Path], weekly_books: list[Path]) -> list[str]:
    issues: list[str] = []
    if not resource_paths and not weekly_books:
        return issues
    for index_name in ("Sources.md", "People.md", "Topics.md"):
        if not (INDEXES / index_name).exists():
            issues.append(f"{INDEXES / index_name}: missing graph index")
    for path in resource_paths:
        text = read_text(path)
        fields = _fields(path)
        if "## Connections" not in text or "[[sources/" not in text:
            issues.append(f"{path}: missing source graph connection")
        speakers = fields.get("speakers")
        if isinstance(speakers, list) and speakers and "[[people/" not in text:
            issues.append(f"{path}: missing speaker graph connection")
        tags = fields.get("tags")
        if isinstance(tags, list) and tags and "[[topics/" not in text:
            issues.append(f"{path}: missing topic graph connection")
    for path in weekly_books:
        fields = _fields(path)
        if str(fields.get("language") or "en").lower() == "en":
            if "## Included Notes" not in read_text(path):
                issues.append(f"{path}: missing included-note links")
    return issues


def _print_issues(label: str, values: list[str]) -> None:
    if not values:
        return
    print(f"{label}:")
    for value in values:
        print(f"  - {value}")


def _print_paths(label: str, paths: list[Path]) -> None:
    if not paths:
        return
    print(f"{label}:")
    for path in paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
