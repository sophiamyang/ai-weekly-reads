from __future__ import annotations

import sys

from config import load_settings
from pipeline import build_weekly_book, deliver_to_kindle, print_run_summary, update_knowledge_base
from project_paths import ROOT, ensure_dirs
from utils import load_dotenv


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    stats = update_knowledge_base(settings)
    built = build_weekly_book(settings)
    if not built:
        print_run_summary(stats, 0)
        return
    _digest_path, kindle_path, weekly_resource_count = built
    print(deliver_to_kindle(kindle_path, settings))
    print_run_summary(stats, weekly_resource_count)


if __name__ == "__main__":
    main()
