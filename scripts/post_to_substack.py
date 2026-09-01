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
from contextlib import contextmanager
from pathlib import Path

from config import load_settings
from project_paths import ROOT, ensure_dirs
from substack import latest_substack_post
from utils import load_dotenv


@contextmanager
def _load_substack_api():
    """Yield python-substack's `Api`, not this repo's scripts/substack.py.

    Both are importable as `substack`, and the repo's own module wins because
    scripts/ leads sys.path when a script in it runs. Drop that directory (and
    any cached module) for the duration of the block.

    The swap has to span every call made on the Api, not just the import:
    python-substack defers `from substack.post import Post` and `from substack
    import mdrender` to draft-creation time, and those resolve through
    sys.modules when they run. Restoring the repo module too early makes them
    fail. On exit the repo module is put back, so a later `import substack`
    elsewhere in the pipeline still gets scripts/substack.py.
    """
    script_dir = str(Path(__file__).resolve().parent)
    removed = [p for p in list(sys.path) if p in ("", ".", script_dir)]
    for path in removed:
        sys.path.remove(path)
    shadowed = {name: sys.modules.pop(name) for name in list(sys.modules) if name == "substack" or name.startswith("substack.")}
    try:
        from substack import Api  # noqa: PLC0415 - deliberately late, see docstring

        yield Api
    finally:
        # Evict the library from the module cache, otherwise a later
        # `import substack` elsewhere in the pipeline resolves to it instead of
        # this repo's scripts/substack.py.
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

    post = Path(args.post) if args.post else latest_substack_post()
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

    title, subtitle, body = _split_post(post.read_text(encoding="utf-8"))
    print(f"Creating draft: {title!r} ({len(body)} chars)")

    with _load_substack_api() as api_cls:
        api = api_cls(publication_url=publication_url, cookies_string=f"substack.sid={cookie}")
        # Pass everything by keyword: create_draft_from_markdown takes
        # (title, markdown, ...), so a positional body silently lands in title.
        result = api.create_draft_from_markdown(
            title=title,
            markdown=body,
            subtitle=subtitle,
            publish=False,
        )

    # The draft is returned alongside the tag/prepublish/publish results.
    draft_id = (result.get("draft") or {}).get("id")
    if not draft_id:
        raise RuntimeError(f"Substack accepted the request but returned no draft id: {result}")
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


if __name__ == "__main__":
    sys.exit(main())
