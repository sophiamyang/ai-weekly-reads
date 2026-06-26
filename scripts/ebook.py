from __future__ import annotations

import shutil
import subprocess
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
    subprocess.run(
        [
            pandoc,
            str(markdown_path),
            "--from",
            "markdown+yaml_metadata_block",
            "--to",
            "epub3",
            "--css",
            str(KINDLE_CSS),
            "--toc",
            "--toc-depth=2",
            "--output",
            str(epub_path),
        ],
        check=True,
    )
    return epub_path
