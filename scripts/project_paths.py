from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOT_OBSIDIAN_CONFIG = ROOT / ".obsidian"
ASSETS = ROOT / "assets"
INBOX = ROOT / "inbox"
CONFIG = ROOT / "config"
OUTPUT = ROOT / "output"
SUBSTACK_OUTPUT = OUTPUT / "substack"
PUBLIC_WEEKLY = ROOT / "weekly"
PROMPTS = ROOT / "prompts"
KNOWLEDGE_BASE = ROOT / "knowledge_base"
OBSIDIAN_CONFIG = KNOWLEDGE_BASE / ".obsidian"
RESOURCES = KNOWLEDGE_BASE / "resources"
RAW_TRANSCRIPTS = KNOWLEDGE_BASE / "raw_transcripts"
WEEKLY_BOOKS = KNOWLEDGE_BASE / "weekly_books"
SOURCE_NOTES = KNOWLEDGE_BASE / "sources"
PEOPLE_NOTES = KNOWLEDGE_BASE / "people"
TOPIC_NOTES = KNOWLEDGE_BASE / "topics"
INDEXES = KNOWLEDGE_BASE / "indexes"
TEMPLATES = KNOWLEDGE_BASE / "templates"
SUMMARIES = OUTPUT / "_summaries"
MEDIA = OUTPUT / "_media"
METADATA = OUTPUT / "_metadata"


def ensure_dirs() -> None:
    for path in (
        ASSETS,
        INBOX,
        CONFIG,
        PROMPTS,
        OUTPUT,
        SUBSTACK_OUTPUT,
        PUBLIC_WEEKLY,
        KNOWLEDGE_BASE,
        ROOT_OBSIDIAN_CONFIG,
        OBSIDIAN_CONFIG,
        RESOURCES,
        RAW_TRANSCRIPTS,
        WEEKLY_BOOKS,
        SOURCE_NOTES,
        PEOPLE_NOTES,
        TOPIC_NOTES,
        INDEXES,
        TEMPLATES,
        METADATA,
    ):
        path.mkdir(parents=True, exist_ok=True)
