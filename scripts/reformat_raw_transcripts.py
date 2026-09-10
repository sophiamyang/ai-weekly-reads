#!/usr/bin/env python3
"""Reflow stored raw transcripts into readable paragraphs.

Transcripts written before `format_for_storage` existed are a single wall of
text — the worst in this vault was one 53,259-word paragraph. This rewrites
them in place, changing no words.

    .venv/bin/python scripts/reformat_raw_transcripts.py --check   # report only
    .venv/bin/python scripts/reformat_raw_transcripts.py

Refuses to write any file whose text is not character-identical once whitespace
is removed, so a formatting bug cannot quietly corrupt the archive.
"""
from __future__ import annotations

import argparse
import re
import sys

from project_paths import RAW_TRANSCRIPTS
from transcript_sanitizer import format_for_storage
from utils import read_text, write_text


def _squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _longest_paragraph(text: str) -> int:
    return max((len(block.split()) for block in text.split("\n\n")), default=0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="Report what would change without writing")
    args = parser.parse_args()

    changed = skipped = 0
    refused: list[str] = []
    worst_before = worst_after = 0

    for path in sorted(RAW_TRANSCRIPTS.glob("*.md")):
        original = read_text(path)
        head, sep, body = original.partition("\n---\n")
        if not sep:  # no frontmatter; treat the whole file as body
            head, body = "", original
        # Keep the "# ... Raw Transcript" heading out of the reflow.
        heading = ""
        stripped = body.lstrip("\n")
        if stripped.startswith("# "):
            heading, _, stripped = stripped.partition("\n")
        formatted = format_for_storage(stripped)

        if _squash(stripped) != _squash(formatted):
            refused.append(path.name)
            continue

        rebuilt = f"{head}{sep}\n{heading}\n\n{formatted}\n" if sep else f"{heading}\n\n{formatted}\n"
        worst_before = max(worst_before, _longest_paragraph(stripped))
        worst_after = max(worst_after, _longest_paragraph(formatted))

        if rebuilt == original:
            skipped += 1
            continue
        changed += 1
        if not args.check:
            write_text(path, rebuilt)

    verb = "would change" if args.check else "reformatted"
    print(f"{verb}: {changed} | already formatted: {skipped} | refused: {len(refused)}")
    print(f"longest paragraph: {worst_before:,} words -> {worst_after:,} words")
    for name in refused:
        print(f"  REFUSED (text would change): {name}", file=sys.stderr)
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
