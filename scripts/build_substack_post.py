from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config import load_settings
from project_paths import OUTPUT, ROOT, ensure_dirs
from substack import build_substack_post, substack_status
from utils import load_dotenv


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Build a Substack-ready Markdown post from a generated digest.")
    parser.add_argument("digest", nargs="?", help="Digest Markdown path. Defaults to the latest output/kindle-digest-*.md.")
    parser.add_argument("--force", action="store_true", help="Build even when substack.enabled is false.")
    args = parser.parse_args()

    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    digest_path = Path(args.digest) if args.digest else _latest_digest()
    if not digest_path:
        print("No generated digest found under output/. Run scripts/build_weekly_digest.py first.")
        return

    print(substack_status(build_substack_post(digest_path, settings, force=args.force)))


def _latest_digest() -> Path | None:
    candidates = sorted(OUTPUT.glob("kindle-digest-*.md"))
    return candidates[-1] if candidates else None


if __name__ == "__main__":
    main()
