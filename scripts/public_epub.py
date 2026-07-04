from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from project_paths import PUBLIC_LATEST_EPUB, PUBLIC_WEEKLY, ROOT


PUBLIC_EPUB_PATH = PUBLIC_WEEKLY / "latest.epub"


def public_repo_url(relative_path: str) -> str:
    remote_url = _git_remote_url("origin")
    owner_repo = _github_owner_repo(remote_url)
    if not owner_repo:
        return ""
    return f"https://raw.githubusercontent.com/{owner_repo}/main/{relative_path.lstrip('/')}"


def public_epub_repo_url(relative_path: str = "weekly/latest.epub") -> str:
    return public_repo_url(relative_path)


def public_epub_markdown_url() -> str:
    return "latest.epub"


def publish_public_epub(epub_path: Path, public_epub_path: Path = PUBLIC_EPUB_PATH, *, update_root_latest: bool = True) -> str:
    if epub_path.suffix.lower() != ".epub" or not epub_path.exists():
        return "Public EPUB skipped: latest Kindle output is not an EPUB."
    public_epub_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(epub_path, public_epub_path)
    if update_root_latest:
        shutil.copy2(epub_path, PUBLIC_LATEST_EPUB)
    return f"Public EPUB written: {public_epub_path}"


def _git_remote_url(remote_name: str) -> str:
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, OSError):
        return ""
    return result.stdout.strip()


def _github_owner_repo(remote_url: str) -> str:
    if not remote_url:
        return ""
    if remote_url.startswith("git@github.com:"):
        slug = remote_url.removeprefix("git@github.com:").removesuffix(".git")
        return slug.strip("/")
    parsed = urlparse(remote_url)
    host = parsed.netloc.lower().rsplit("@", 1)[-1].split(":", 1)[0]
    if host != "github.com":
        return ""
    return parsed.path.strip("/").removesuffix(".git")
