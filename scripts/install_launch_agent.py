from __future__ import annotations

import argparse
import plistlib
import subprocess
from pathlib import Path

from project_paths import ROOT


LABEL = "com.ai-weekly-reads.weekly-digest"
LAUNCH_AGENTS = Path.home() / "Library" / "LaunchAgents"
PLIST_PATH = LAUNCH_AGENTS / f"{LABEL}.plist"


def main() -> None:
    parser = argparse.ArgumentParser(description="Install or uninstall the AI Weekly Reads weekly LaunchAgent.")
    parser.add_argument("--uninstall", action="store_true", help="Unload and remove the LaunchAgent.")
    parser.add_argument("--weekday", type=int, default=0, help="0=Sunday, 1=Monday, ..., 6=Saturday. Default: 0.")
    parser.add_argument("--hour", type=int, default=8, help="Run hour in 24-hour time. Default: 8.")
    parser.add_argument("--minute", type=int, default=0, help="Run minute. Default: 0.")
    args = parser.parse_args()

    if args.uninstall:
        uninstall()
        return

    _validate_schedule(parser, args)
    install(args.weekday, args.hour, args.minute)


def _validate_schedule(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    # launchd accepts out-of-range StartCalendarInterval values at load time
    # but the job then never fires, so fail fast here instead.
    if not 0 <= args.weekday <= 7:
        parser.error("--weekday must be between 0 and 7 (launchd treats both 0 and 7 as Sunday).")
    if not 0 <= args.hour <= 23:
        parser.error("--hour must be between 0 and 23.")
    if not 0 <= args.minute <= 59:
        parser.error("--minute must be between 0 and 59.")


def install(weekday: int, hour: int, minute: int) -> None:
    LAUNCH_AGENTS.mkdir(parents=True, exist_ok=True)
    (ROOT / "logs").mkdir(parents=True, exist_ok=True)
    plist = {
        "Label": LABEL,
        "ProgramArguments": [
            str(ROOT / ".venv" / "bin" / "python"),
            str(ROOT / "scripts" / "build_weekly_digest.py"),
        ],
        "WorkingDirectory": str(ROOT),
        "StartCalendarInterval": {
            "Weekday": weekday,
            "Hour": hour,
            "Minute": minute,
        },
        "StandardOutPath": str(ROOT / "logs" / "weekly-digest.out.log"),
        "StandardErrorPath": str(ROOT / "logs" / "weekly-digest.err.log"),
        "RunAtLoad": False,
    }
    with PLIST_PATH.open("wb") as file:
        plistlib.dump(plist, file)
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], check=False)
    subprocess.run(["launchctl", "load", str(PLIST_PATH)], check=True)
    print(f"Installed {LABEL} at {PLIST_PATH}")
    print(f"Schedule: weekday={weekday}, {hour:02d}:{minute:02d}")


def uninstall() -> None:
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], check=False)
    if PLIST_PATH.exists():
        PLIST_PATH.unlink()
    print(f"Removed {LABEL}")


if __name__ == "__main__":
    main()
