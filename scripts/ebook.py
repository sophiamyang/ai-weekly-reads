from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from config import Settings
from project_paths import ASSETS, OUTPUT


KINDLE_CSS = ASSETS / "kindle.css"


def build_kindle_file(markdown_path: Path, settings: Settings) -> Path:
    output_format = settings.kindle_output_format.lower()
    if output_format in {"md", "markdown"}:
        return markdown_path
    if output_format != "epub":
        print(f"Unknown kindle_output_format={settings.kindle_output_format!r}; sending Markdown.")
        return markdown_path
    return _build_epub(markdown_path)


def _build_epub(markdown_path: Path) -> Path:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        print("Pandoc is not installed; sending Markdown instead of EPUB.")
        return markdown_path

    epub_path = OUTPUT / f"{markdown_path.stem}.epub"
    epub_source = _prepare_epub_source(markdown_path)
    try:
        subprocess.run(
            [
                pandoc,
                str(epub_source),
                "--from",
                "markdown+yaml_metadata_block",
                "--to",
                "epub3",
                "--css",
                str(KINDLE_CSS),
                "--toc",
                "--toc-depth=1",
                "--output",
                str(epub_path),
            ],
            check=True,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        # Never leave a partial EPUB behind: send_latest_to_kindle.py picks
        # the newest output file by modification time.
        epub_path.unlink(missing_ok=True)
        print(f"Pandoc EPUB build failed ({exc}); sending Markdown instead.")
        return markdown_path
    finally:
        if epub_source != markdown_path:
            epub_source.unlink(missing_ok=True)
    return epub_path


def _prepare_epub_source(markdown_path: Path) -> Path:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    frontmatter_end = _frontmatter_end(lines)
    preface_end = next((index for index, line in enumerate(lines[frontmatter_end:], start=frontmatter_end) if line.strip() == "## Reading Notes"), None)
    if preface_end is not None:
        kept_lines = lines[:frontmatter_end]
        kept_lines.extend(["", *lines[preface_end + 1 :]])
        transformed = "\n".join(kept_lines).strip() + "\n"
    else:
        transformed = text
    if transformed == text:
        return markdown_path
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False, dir=OUTPUT) as handle:
        handle.write(transformed)
        return Path(handle.name)


def _frontmatter_end(lines: list[str]) -> int:
    if not lines or lines[0].strip() != "---":
        return 0
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index + 1
    return 0
