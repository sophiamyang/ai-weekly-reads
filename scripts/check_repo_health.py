from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from config import Settings, load_settings
from project_paths import ASSETS, CONFIG, PROMPTS, PUBLIC_LATEST_EPUB, PUBLIC_LATEST_MD, PUBLIC_ONE_SHOT, PUBLIC_WEEKLY, ROOT
from source_registry import load_source_registry, source_lookback_count
from utils import GRAPH_ONLY_HEADINGS, is_url


REQUIRED_SUMMARY_PROMPTS = [
    "summarize_resource.md",
    "summarize_podcast.md",
]
REQUIRED_IGNORES = [
    "config/settings.json",
    "inbox/links.txt",
    "knowledge_base/raw_transcripts/",
    "knowledge_base/resources/",
    "knowledge_base/weekly_books/",
    "knowledge_base/sources/",
    "knowledge_base/people/",
    "knowledge_base/topics/",
    "knowledge_base/indexes/",
    "output/",
    "logs/",
    ".env",
    "config/private/",
    "client_secret_*.json",
]
GENERATED_PATHS = [
    "config/settings.json",
    "inbox/links.txt",
    "knowledge_base/raw_transcripts",
    "knowledge_base/resources",
    "knowledge_base/weekly_books",
    "knowledge_base/sources",
    "knowledge_base/people",
    "knowledge_base/topics",
    "knowledge_base/indexes",
    "output",
    "logs",
    "config/private",
    ".env",
    "client_secret_*.json",
]
PLACEHOLDER_EMAILS = {"yourname_123@kindle.com", "you@example.com"}


def main() -> None:
    errors: list[str] = []
    _check_settings(CONFIG / "settings.example.json", errors)
    if (CONFIG / "settings.json").exists():
        _check_settings(CONFIG / "settings.json", errors)
    _check_sources(errors)
    _check_prompts(errors)
    _check_kindle_css(errors)
    _check_git_hygiene(errors)

    if errors:
        print("AI Weekly Reads repo health check failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("AI Weekly Reads repo health check passed.")


def _check_settings(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing settings file: {path.relative_to(ROOT)}")
        return
    settings = load_settings(path)
    label = path.relative_to(ROOT)
    _check_non_negative_int(label, "publication_window_days", settings.publication_window_days, errors)
    _check_non_negative_int(label, "max_items_per_run", settings.max_items_per_run, errors)
    _check_positive_int(label, "weekly_resource_limit", settings.weekly_resource_limit, errors)

    if settings.summary_mode not in {"batch", "direct"}:
        errors.append(f"{label}: summary_mode must be 'batch' or 'direct'.")
    if settings.summary_provider not in {"mistral", "local"}:
        errors.append(f"{label}: summary_provider must be 'mistral' or 'local'.")
    if settings.transcription_provider not in {"mistral", "none"}:
        errors.append(f"{label}: transcription_provider must be 'mistral' or 'none'.")
    if settings.kindle_output_format.lower() not in {"epub", "markdown", "md"}:
        errors.append(f"{label}: kindle_output_format must be 'epub' or 'markdown'.")
    if settings.follow_builders.get("enabled") and not _is_http_url(settings.follow_builders.get("base_url")):
        errors.append(f"{label}: follow_builders.base_url must be an HTTP(S) URL when enabled.")
    _check_kindle_settings(label, settings, errors)
    _check_substack_settings(label, settings, errors)


def _check_kindle_settings(label: Path, settings: Settings, errors: list[str]) -> None:
    kindle = settings.kindle
    if not kindle.get("enabled"):
        return
    delivery_method = str(kindle.get("delivery_method") or "").strip().lower()
    if delivery_method not in {"gmail_api", "gmail", "google", "smtp", "apple_mail", "mail", "macos_mail"}:
        errors.append(f"{label}: kindle.delivery_method is not recognized.")
    kindle_email = str(kindle.get("kindle_email") or "").strip()
    if not kindle_email or kindle_email in PLACEHOLDER_EMAILS:
        errors.append(f"{label}: kindle.kindle_email must be configured before enabling delivery.")


def _check_substack_settings(label: Path, settings: Settings, errors: list[str]) -> None:
    substack = settings.substack
    if not isinstance(substack.get("enabled"), bool):
        errors.append(f"{label}: substack.enabled must be true or false.")
    delivery_method = str(substack.get("delivery_method") or "").strip().lower()
    if delivery_method not in {"browser_draft", "export"}:
        errors.append(f"{label}: substack.delivery_method must be 'browser_draft' or 'export'.")
    if not isinstance(substack.get("auto_publish"), bool):
        errors.append(f"{label}: substack.auto_publish must be true or false.")
    if substack.get("enabled") and delivery_method == "browser_draft":
        publication_url = str(substack.get("publication_url") or "").strip()
        if not _is_http_url(publication_url):
            errors.append(f"{label}: substack.publication_url must be configured before browser draft delivery.")


def _check_sources(errors: list[str]) -> None:
    registry = load_source_registry()
    _check_list(registry, "youtube_channels", errors)
    _check_list(registry, "podcasts", errors)

    seen_urls: set[str] = set()
    for index, channel in enumerate(registry.get("youtube_channels", []), start=1):
        url = str(channel.get("url") or "").strip()
        _check_url(url, f"youtube_channels[{index}].url", errors)
        _check_unique(url, seen_urls, f"youtube_channels[{index}].url", errors)
        _check_source_lookback(channel, f"youtube_channels[{index}]", errors)
        _check_content_type(channel, f"youtube_channels[{index}]", errors)

    for index, podcast in enumerate(registry.get("podcasts", []), start=1):
        rss_url = str(podcast.get("rssUrl") or "").strip()
        _check_url(rss_url, f"podcasts[{index}].rssUrl", errors)
        _check_unique(rss_url, seen_urls, f"podcasts[{index}].rssUrl", errors)
        _check_source_lookback(podcast, f"podcasts[{index}]", errors)
        _check_content_type(
            {**podcast, "content_type": podcast.get("content_type", "podcast")},
            f"podcasts[{index}]",
            errors,
        )


def _check_prompts(errors: list[str]) -> None:
    for prompt_name in REQUIRED_SUMMARY_PROMPTS:
        path = PROMPTS / prompt_name
        if not path.exists():
            errors.append(f"Missing prompt: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8").strip()
        if len(text.split()) < 50:
            errors.append(f"Prompt is unexpectedly short: {path.relative_to(ROOT)}")
        for heading in (
            "## One-Sentence Takeaway",
            "## Short Summary",
            "## Featured Speakers",
            "## Topics",
            "## Reading Priority",
        ):
            if heading not in text:
                errors.append(f"{path.relative_to(ROOT)} is missing {heading!r}.")


def _check_kindle_css(errors: list[str]) -> None:
    path = ASSETS / "kindle.css"
    if not path.exists():
        errors.append(f"Missing Kindle stylesheet: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for phrase in ("background: #ffffff !important", "color: #000000 !important", "line-height: 1.45"):
        if phrase not in text:
            errors.append(f"{path.relative_to(ROOT)} is missing {phrase!r}.")


def _check_git_hygiene(errors: list[str]) -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    for pattern in REQUIRED_IGNORES:
        if pattern not in gitignore:
            errors.append(f".gitignore should include {pattern!r}.")
    if (ROOT / "data").exists():
        errors.append("Unexpected durable data/ folder exists; use knowledge_base/ and output/ instead.")

    tracked = _git_ls_files(GENERATED_PATHS)
    if tracked:
        joined = ", ".join(tracked[:10])
        suffix = " ..." if len(tracked) > 10 else ""
        errors.append(f"Generated/private paths are tracked by Git: {joined}{suffix}")

    _check_public_dir(PUBLIC_WEEKLY, "weekly", errors, allow_empty=False)
    _check_public_dir(PUBLIC_ONE_SHOT, "one-shot", errors, allow_empty=True)
    _check_root_public_latest(errors)


def _check_public_dir(public_dir: Path, label: str, errors: list[str], *, allow_empty: bool) -> None:
    public_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in public_dir.glob("*")
        if path.is_file() and not path.name.startswith(".")
    )
    expected_md = f"{label}/latest.md"
    expected_epub = f"{label}/latest.epub"
    allowed = [expected_md]
    allowed_with_epub = [expected_epub, expected_md]
    if allow_empty and not public_files:
        return
    if public_files not in (allowed, allowed_with_epub):
        errors.append(f"{label}/ should contain only public latest artifacts: {expected_md} and optional {expected_epub}.")
        return
    latest_md = public_dir / "latest.md"
    if latest_md.exists():
        _check_public_markdown(latest_md, f"{label}/latest.md", errors)


def _check_public_markdown(path: Path, label: str, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if "# Appendix: Full Transcripts" in text:
        errors.append(f"{label} must not contain full transcripts.")
    for marker in ("## Contents", "## Reading Notes"):
        if marker not in text:
            errors.append(f"{label} is missing {marker!r}.")
    graph_headings = [f"## {heading.title()}" for heading in GRAPH_ONLY_HEADINGS]
    if "[[" in text or any(heading in text for heading in graph_headings):
        errors.append(f"{label} must not contain Obsidian-only wikilinks or graph sections.")
    if not re.search(r"^- \*\*(Published|Added):\*\*", text, re.MULTILINE):
        errors.append(f"{label} should include published or added dates in each summary.")
    if not re.search(r"^- \*\*(YouTube|Podcast|Video|Livestream|Source):\*\* \[[^\]]+\]\(https?://", text, re.MULTILINE):
        errors.append(f"{label} should include linked source labels for original items.")


def _check_root_public_latest(errors: list[str]) -> None:
    if not PUBLIC_LATEST_MD.exists():
        errors.append("latest.md should exist at the repository root and track the most recent public edition.")
    else:
        _check_public_markdown(PUBLIC_LATEST_MD, "latest.md", errors)


def _check_list(registry: dict[str, Any], key: str, errors: list[str]) -> None:
    if not isinstance(registry.get(key, []), list):
        errors.append(f"config/sources.json field {key!r} must be a list.")


def _check_source_lookback(source: dict[str, Any], label: str, errors: list[str]) -> None:
    try:
        value = source_lookback_count(source, default=50)
    except (TypeError, ValueError):
        errors.append(f"{label}.lookback_count must be an integer.")
        return
    if value <= 0:
        errors.append(f"{label}.lookback_count must be positive.")


def _check_content_type(source: dict[str, Any], label: str, errors: list[str]) -> None:
    value = str(source.get("content_type") or "").strip()
    if value and value not in {"podcast", "video", "livestream"}:
        errors.append(f"{label}.content_type must be podcast, video, or livestream.")


def _check_positive_int(label: Path, key: str, value: int, errors: list[str]) -> None:
    if value <= 0:
        errors.append(f"{label}: {key} must be positive.")


def _check_non_negative_int(label: Path, key: str, value: int, errors: list[str]) -> None:
    if value < 0:
        errors.append(f"{label}: {key} must be zero or positive.")


def _check_url(value: str, label: str, errors: list[str]) -> None:
    if not _is_http_url(value):
        errors.append(f"{label} must be an HTTP(S) URL.")


def _is_http_url(value: object) -> bool:
    return isinstance(value, str) and is_url(value)


def _check_unique(value: str, seen: set[str], label: str, errors: list[str]) -> None:
    if not value:
        return
    if value in seen:
        errors.append(f"{label} is duplicated: {value}")
    seen.add(value)


def _git_ls_files(paths: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", *paths],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


if __name__ == "__main__":
    main()
