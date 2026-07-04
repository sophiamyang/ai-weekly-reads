from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from config import load_settings
from project_paths import ROOT
from send_to_kindle import GMAIL_SEND_SCOPE, private_path, write_private_file
from utils import load_dotenv


def main() -> None:
    args = _parse_args()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    kindle = settings.kindle
    credentials_path = private_path(
        args.credentials or kindle.get("gmail_credentials_path"),
        "config/private/gmail_credentials.json",
    )
    token_path = private_path(args.token or kindle.get("gmail_token_path"), "config/private/gmail_token.json")

    credentials_path = _resolve_credentials_path(credentials_path, args.credentials)
    if not credentials_path.exists():
        print(f"Missing Gmail OAuth client file: {credentials_path}")
        print("Download a Desktop app OAuth client JSON from Google Cloud and save it there.")
        print("If the file is still named client_secret_*.json, put it in the project root and rerun this command.")
        sys.exit(1)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Missing Gmail OAuth dependencies. Run: .venv/bin/pip install -r requirements.txt")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), [GMAIL_SEND_SCOPE])
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    write_private_file(token_path, creds.to_json())
    print(f"Gmail OAuth token saved: {token_path}")
    print("You can now run: .venv/bin/python scripts/send_latest_to_kindle.py")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Authorize Gmail API send-only access for AI Weekly Reads.")
    parser.add_argument("--credentials", help="path to downloaded Google OAuth desktop client JSON")
    parser.add_argument("--token", help="path where the local Gmail OAuth token should be saved")
    return parser.parse_args()


def _resolve_credentials_path(configured_path: Path, explicit_path: str | None) -> Path:
    if explicit_path or configured_path.exists():
        return configured_path

    candidates = sorted(ROOT.glob("client_secret_*.json"))
    if len(candidates) != 1:
        return configured_path

    source_path = candidates[0]
    configured_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, configured_path)
    configured_path.chmod(0o600)
    print(f"Copied Gmail OAuth client file to private config: {configured_path}")
    print(f"You can delete the downloaded file from the project root: {source_path.name}")
    return configured_path


if __name__ == "__main__":
    main()
