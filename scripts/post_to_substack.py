"""Create a Substack draft over HTTP, without a browser.

Substack sits behind Cloudflare, which challenges headless browsers from
datacenter IPs — GitHub Actions runners included — so browser automation cannot
reach the editor from CI. The JSON API is not challenged, so drafting goes
through it instead.

Authentication is the `substack.sid` session cookie in SUBSTACK_SID. It grants
full account access, so it is read from the environment at run time and never
logged or written to disk.

This creates a DRAFT and never publishes: review and publish from Substack.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from config import load_settings
from project_paths import OUTPUT, ROOT, ensure_dirs
from utils import load_dotenv

SUBSTACK_DIR = OUTPUT / "substack"


def _load_substack_api():
    """Import the python-substack package, not this repo's scripts/substack.py.

    Both are importable as `substack`, and the repo's own module wins because
    scripts/ leads sys.path when a script in it runs. Drop that directory (and
    any cached module) for the duration of the import.
    """
    script_dir = str(Path(__file__).resolve().parent)
    removed = [p for p in list(sys.path) if p in ("", ".", script_dir)]
    for path in removed:
        sys.path.remove(path)
    shadowed = {name: sys.modules.pop(name) for name in list(sys.modules) if name == "substack" or name.startswith("substack.")}
    try:
        from substack import Api  # noqa: PLC0415 - deliberately late, see docstring

        return Api
    finally:
        # Evict the library from the module cache, otherwise a later
        # `import substack` elsewhere in the pipeline resolves to it instead of
        # this repo's scripts/substack.py. The already-imported Api class keeps
        # working regardless.
        for name in [n for n in sys.modules if n == "substack" or n.startswith("substack.")]:
            sys.modules.pop(name, None)
        sys.modules.update(shadowed)
        sys.path[:0] = removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Substack draft from the generated post.")
    parser.add_argument("post", nargs="?", help="Post Markdown path. Defaults to the newest file in output/substack/.")
    parser.add_argument(
        "--no-email-fallback",
        action="store_true",
        help="Do not email the post when drafting fails.",
    )
    args = parser.parse_args()

    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()

    post = Path(args.post) if args.post else _latest_post()
    if not post or not post.exists():
        print("No Substack post found. Build the weekly digest first.", file=sys.stderr)
        return 1

    try:
        url = create_draft(post, settings)
    except Exception as exc:
        print(f"Substack draft failed: {exc}", file=sys.stderr)
        if not args.no_email_fallback:
            _email_fallback(post, settings)
        return 1

    print(f"Substack draft created: {url}")
    return 0


def create_draft(post: Path, settings) -> str:
    cookie = os.environ.get("SUBSTACK_SID", "").strip()
    if not cookie:
        raise RuntimeError("SUBSTACK_SID is not set; cannot authenticate to Substack.")

    publication_url = str((settings.substack or {}).get("publication_url") or "").rstrip("/")
    if not publication_url:
        raise RuntimeError("Missing substack.publication_url in config/settings.json.")

    api_cls = _load_substack_api()
    api = api_cls(publication_url=publication_url, cookies_string=f"substack.sid={cookie}")

    title, subtitle, body = _split_post(post.read_text(encoding="utf-8"))
    print(f"Creating draft: {title!r} ({len(body)} chars)")

    draft = api.create_draft_from_markdown(body, title=title, subtitle=subtitle, publish=False)
    draft_id = draft.get("id")
    if not draft_id:
        raise RuntimeError(f"Substack accepted the request but returned no draft id: {draft}")
    return f"{publication_url}/publish/post/{draft_id}"


def _split_post(text: str) -> tuple[str, str, str]:
    """Split the generated post into title, subtitle, and body.

    Substack stores the title and subtitle as their own fields, so leaving the
    leading heading in the body would duplicate it in the published post.
    """
    lines = text.splitlines()
    title = ""
    subtitle = ""
    start = 0
    for index, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            start = index + 1
            break
    for index in range(start, len(lines)):
        candidate = lines[index].strip()
        if candidate:
            subtitle = candidate
            start = index + 1
            break
    body = "\n".join(lines[start:]).strip()
    return title or "AI Weekly Reads", subtitle, body


def _email_fallback(post: Path, settings) -> None:
    try:
        from email_substack_post import send_substack_post

        print(send_substack_post(post, settings))
    except Exception as exc:
        print(f"Email fallback also failed: {exc}", file=sys.stderr)


def _latest_post() -> Path | None:
    if not SUBSTACK_DIR.exists():
        return None
    posts = [p for p in SUBSTACK_DIR.glob("*.md") if p.name != "latest.md"]
    return max(posts, key=lambda p: p.stat().st_mtime) if posts else None


if __name__ == "__main__":
    sys.exit(main())
