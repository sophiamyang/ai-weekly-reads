from __future__ import annotations

import sys

from config import load_settings
from pipeline import print_run_summary, update_knowledge_base
from project_paths import ROOT, ensure_dirs
from utils import load_dotenv


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    stats = update_knowledge_base(settings)
    print_run_summary(stats)


if __name__ == "__main__":
    main()
