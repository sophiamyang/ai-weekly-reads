"""Email the generated Substack post to yourself, ready to paste and publish.

Substack has no publishing API, and browser automation cannot reach the network
from the cloud runner, so the last step stays manual. This delivers the post to
your inbox using the same Gmail credentials as Kindle delivery.
"""
from __future__ import annotations

import argparse
import base64
import sys
from email.message import EmailMessage
from pathlib import Path

from config import load_settings
from project_paths import ROOT, ensure_dirs
from send_to_kindle import _configured_email, _gmail_service
from substack import latest_substack_post
from utils import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(description="Email the latest Substack post to yourself.")
    parser.add_argument("post", nargs="?", help="Post Markdown path. Defaults to the newest file in output/substack/.")
    parser.add_argument("--to", help="Recipient. Defaults to the Kindle sender address.")
    args = parser.parse_args()

    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()

    post = Path(args.post) if args.post else latest_substack_post()
    if not post or not post.exists():
        raise SystemExit("No Substack post found. Build the weekly digest first.")

    print(send_substack_post(post, settings, recipient=args.to))


def send_substack_post(post: Path, settings, *, recipient: str | None = None) -> str:
    kindle = settings.kindle
    sender = _configured_email(kindle, "sender_email")
    if not sender:
        return "Substack email skipped: missing KINDLE_SENDER_EMAIL."
    recipient = recipient or sender

    try:
        service = _gmail_service(kindle)
    except ImportError:
        return "Substack email skipped: install Gmail API dependencies."
    except FileNotFoundError as exc:
        return f"Substack email skipped: {exc}"
    except Exception as exc:
        return f"Substack email skipped: Gmail OAuth failed. {exc}"

    message = _build_message(post, sender, recipient, settings)
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    service.users().messages().send(userId="me", body={"raw": encoded}).execute()
    return f"Emailed {post.name} to {recipient}."


def _build_message(post: Path, sender: str, recipient: str, settings) -> EmailMessage:
    publication = str((settings.substack or {}).get("publication_url") or "").rstrip("/")
    compose = f"{publication}/publish/post" if publication else "your Substack publication"
    title = post.stem.replace("-", " ")

    message = EmailMessage()
    message["Subject"] = f"Substack draft ready: {title}"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        f"This week's Substack post is attached.\n\n"
        f"To publish: open {compose}, paste the attached Markdown, and review before publishing.\n\n"
        f"Substack emails your subscribers automatically once the post goes live."
    )
    message.add_attachment(
        post.read_bytes(),
        maintype="text",
        subtype="markdown",
        filename=post.name,
    )
    return message



if __name__ == "__main__":
    sys.exit(main())
