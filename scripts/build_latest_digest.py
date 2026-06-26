from __future__ import annotations

import argparse
import sys

from config import load_settings
from pipeline import build_weekly_book, deliver_to_kindle
from project_paths import ROOT, ensure_dirs
from utils import load_dotenv


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Build the latest weekly digest from the local knowledge base.")
    parser.add_argument("--send", action="store_true", help="Send the built digest to Kindle after building.")
    args = parser.parse_args()

    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    built = build_weekly_book(settings)
    if not built:
        return
    _digest_path, kindle_path, _weekly_resource_count = built
    if args.send:
        print(deliver_to_kindle(kindle_path, settings))


if __name__ == "__main__":
    main()
