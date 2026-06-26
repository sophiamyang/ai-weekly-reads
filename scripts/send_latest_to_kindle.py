from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config import load_settings
from project_paths import OUTPUT, ROOT
from send_to_kindle import maybe_send_to_kindle
from utils import load_dotenv


def main() -> None:
    args = _parse_args()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    kindle_file = _latest_kindle_file()
    if not kindle_file:
        print("No Kindle digest found under output/. Run scripts/build_weekly_digest.py first.")
        sys.exit(1)
    print(maybe_send_to_kindle(kindle_file, settings, force=args.force))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send the latest generated Kindle digest.")
    parser.add_argument("--force", action="store_true", help="resend even if this exact digest was already sent")
    return parser.parse_args()


def _latest_kindle_file() -> Path | None:
    candidates = [*OUTPUT.glob("kindle-digest-*.epub"), *OUTPUT.glob("kindle-digest-*.md")]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


if __name__ == "__main__":
    main()
