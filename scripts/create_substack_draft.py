from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin

from config import Settings, load_settings
from project_paths import OUTPUT, ROOT, ensure_dirs
from utils import load_dotenv, read_text


MIN_DRAFT_CHARS = 1200
REQUIRED_MARKERS = ("## Contents", "## Reading Notes")
# Every digest item carries one of these date labels; resources without a
# publication date use "Added" instead of "Published".
DATE_MARKERS = ("- **Published:**", "- **Added:**")


@dataclass(frozen=True)
class DraftPost:
    title: str
    subtitle: str
    markdown: str
    html: str


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Create a Substack draft from the latest Substack-ready post.")
    parser.add_argument("post", nargs="?", help="Substack Markdown path. Defaults to output/substack/latest.md.")
    parser.add_argument("--setup", action="store_true", help="Open the browser so you can log into Substack, then save the session.")
    parser.add_argument("--headless", action="store_true", help="Run without a visible browser window. Default is headed so you can handle login challenges.")
    # Deprecated no-op kept so existing invocations that passed the old
    # default flag keep working.
    parser.add_argument("--headed", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--publish", action="store_true", help="Publish after filling the draft. Requires an explicit flag.")
    args = parser.parse_args()

    ensure_dirs()
    load_dotenv(ROOT / ".env")
    settings = load_settings()
    substack = settings.substack
    if str(substack.get("delivery_method") or "browser_draft") != "browser_draft":
        raise SystemExit("Substack browser draft delivery is disabled. Set substack.delivery_method to browser_draft.")
    publication_url = str(substack.get("publication_url") or "").strip()
    if not publication_url:
        raise SystemExit("Missing substack.publication_url in config/settings.json.")

    post_path = Path(args.post) if args.post else OUTPUT / "substack" / "latest.md"
    if not post_path.exists():
        raise SystemExit(f"Substack post not found: {post_path}. Run scripts/build_substack_post.py first.")

    draft = _load_draft(post_path)
    _create_browser_draft(draft, settings, setup_only=args.setup, publish=args.publish, headless=args.headless)


def _load_draft(path: Path) -> DraftPost:
    markdown = read_text(path).strip()
    _validate_markdown(markdown, path)
    title = _title_from_markdown(markdown)
    subtitle = _subtitle_from_markdown(markdown)
    body = _without_first_h1(markdown)
    return DraftPost(title=title, subtitle=subtitle, markdown=body, html=_markdown_to_html(body))


def _validate_markdown(markdown: str, path: Path) -> None:
    missing = [marker for marker in REQUIRED_MARKERS if marker not in markdown]
    if not any(marker in markdown for marker in DATE_MARKERS):
        missing.append(" or ".join(DATE_MARKERS))
    if missing:
        raise SystemExit(f"{path} does not look like a weekly Substack draft. Missing: {', '.join(missing)}")
    if len(markdown) < MIN_DRAFT_CHARS:
        raise SystemExit(f"{path} is only {len(markdown)} characters; refusing to create a suspiciously short draft.")
    if not markdown.startswith("# "):
        raise SystemExit(f"{path} must start with an H1 title.")


def _title_from_markdown(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return "AI Weekly Reads"


def _without_first_h1(markdown: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[index + 1 :]).strip() + "\n"
    return markdown


def _subtitle_from_markdown(markdown: str) -> str:
    titles = [_subtitle_item(title) for title in _contents_titles(markdown)[:3]]
    titles = [title for title in titles if title]
    if not titles:
        return "The best AI videos and podcasts from the past week."
    if len(titles) == 1:
        return _shorten(f"This week: {titles[0]}.", 180)
    if len(titles) == 2:
        return _shorten(f"{titles[0]} and {titles[1]} from this week's AI reading queue.", 180)
    return _shorten(f"{titles[0]}, {titles[1]}, and {titles[2]} from this week's AI reading queue.", 180)


def _contents_titles(markdown: str) -> list[str]:
    titles: list[str] = []
    in_contents = False
    for line in markdown.splitlines():
        if line.strip() == "## Contents":
            in_contents = True
            continue
        if in_contents and line.startswith("## "):
            break
        if not in_contents:
            continue
        match = re.match(r"^\d+\.\s+(?:\[[^\]]+\]\s+)?(?:\d{4}-\d{2}-\d{2}\s+-\s+)?(.+)$", line.strip())
        if match:
            titles.append(match.group(1).strip())
    return titles


def _subtitle_item(title: str) -> str:
    title = re.split(r"\s+[—-]\s+", title, maxsplit=1)[0]
    title = re.sub(r"\s+", " ", title).strip()
    return _shorten(title, 52).rstrip(".")


def _shorten(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    shortened = value[: max_chars - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return f"{shortened}…"


def _markdown_to_html(markdown: str) -> str:
    try:
        import markdown as markdown_lib
    except ImportError:
        escaped = (
            markdown.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        return f"<pre>{escaped}</pre>"
    return markdown_lib.markdown(markdown, extensions=["extra", "sane_lists"])


def _create_browser_draft(draft: DraftPost, settings: Settings, *, setup_only: bool, publish: bool, headless: bool = False) -> None:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "Playwright is not installed. Run `python3 -m venv .venv-substack`, "
            "`.venv-substack/bin/pip install -r requirements-substack.txt`, and then "
            "`PLAYWRIGHT_BROWSERS_PATH=.venv-substack/ms-playwright "
            ".venv-substack/bin/playwright install chromium`."
        ) from exc

    substack = settings.substack
    publication_url = _normalized_url(str(substack.get("publication_url") or ""))
    compose_url = str(substack.get("compose_url") or "").strip() or urljoin(publication_url, "publish/post")
    user_data_dir = ROOT / str(substack.get("browser_user_data_dir") or "config/private/substack/browser")
    user_data_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            str(user_data_dir),
            headless=headless and not setup_only,
            viewport={"width": 1440, "height": 1000},
        )
        page = context.pages[0] if context.pages else context.new_page()
        for origin in {publication_url.rstrip("/"), "https://substack.com"}:
            try:
                context.grant_permissions(["clipboard-read", "clipboard-write"], origin=origin)
            except Exception:
                pass

        page.goto(compose_url, wait_until="domcontentloaded", timeout=60_000)
        if setup_only:
            print("Log into Substack in the browser window, then press Enter here to save the session.")
            input()
            context.close()
            print(f"Substack browser session saved under {user_data_dir}.")
            return

        _maybe_wait_for_login(page, compose_url, PlaywrightTimeoutError)
        _fill_title(page, draft.title, PlaywrightTimeoutError)
        _fill_subtitle(page, draft.subtitle, PlaywrightTimeoutError)
        _paste_body(page, draft, PlaywrightTimeoutError)
        if publish:
            _publish_post(page, PlaywrightTimeoutError)
            context.close()
            print("Substack post published.")
            return
        print("Substack draft filled in the browser. Review it there, then save/publish manually.")
        print(f"Browser session: {user_data_dir}")
        input("Press Enter here when you are done reviewing the draft...")
        context.close()


def _maybe_wait_for_login(page, compose_url: str, timeout_error_type) -> None:
    if _editor_is_visible(page, timeout_error_type, timeout=5_000):
        return
    if not _looks_like_login_gate(page):
        return

    print("Substack needs you to log in or confirm this browser session.")
    print("Complete that in the browser, then press Enter here.")
    input()
    page.goto(compose_url, wait_until="domcontentloaded", timeout=60_000)
    if not _editor_is_visible(page, timeout_error_type, timeout=15_000) and _looks_like_login_gate(page):
        print("Substack still looks signed out. Complete the login, then press Enter here.")
        input()
        page.goto(compose_url, wait_until="domcontentloaded", timeout=60_000)


def _fill_title(page, title: str, timeout_error_type) -> None:
    selectors = (
        "[data-testid='post-title']",
        "textarea[placeholder*='Title']",
        "input[placeholder*='Title']",
        "[contenteditable='true'][data-placeholder*='Title']",
        "[contenteditable='true'][aria-label*='Title']",
        "[aria-label*='Title']",
    )
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=8_000)
            locator.click()
            _select_all(page)
            page.keyboard.type(title)
            return
        except timeout_error_type:
            continue
        except Exception:
            continue
    print("I could not find the title field automatically.")
    print(f"Title to paste manually: {title}")
    input("Click the Substack title field, paste/type the title, then press Enter here...")


def _fill_subtitle(page, subtitle: str, timeout_error_type) -> None:
    selectors = (
        "textarea[placeholder*='subtitle']",
        "textarea[placeholder*='Subtitle']",
        "input[placeholder*='Subtitle']",
        "[contenteditable='true'][data-placeholder*='Subtitle']",
        "[contenteditable='true'][aria-label*='Subtitle']",
        "textarea[placeholder*='subheading']",
        "input[placeholder*='subheading']",
    )
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=4_000)
            locator.click()
            _select_all(page)
            page.keyboard.type(subtitle)
            return
        except timeout_error_type:
            continue
        except Exception:
            continue
    print(f"Subtitle suggestion: {subtitle}")


def _paste_body(page, draft: DraftPost, timeout_error_type) -> None:
    _put_rich_text_on_clipboard(page, draft)
    selectors = (
        "[data-testid='editor']",
        "[placeholder*='Start writing']",
        "[contenteditable='true'][data-placeholder*='Write']",
        "[contenteditable='true'][aria-label*='Body']",
        ".ProseMirror[contenteditable='true']",
        ".tiptap.ProseMirror",
        "[contenteditable='true']",
    )
    for selector in selectors:
        locator = page.locator(selector).last
        try:
            locator.wait_for(state="visible", timeout=8_000)
            locator.click()
            page.keyboard.press("Meta+V" if sys.platform == "darwin" else "Control+V")
            return
        except timeout_error_type:
            continue
        except Exception:
            continue
    print("Substack did not expose a stable body editor selector, but the full post is on the browser clipboard.")
    input("Click the Substack body editor, paste, then press Enter here...")


def _publish_post(page, timeout_error_type) -> None:
    _click_first_matching_button(
        page,
        timeout_error_type,
        selectors=("[data-testid='publish-button']",),
        names=("Continue", "Publish", "Publish now"),
        label="publish/continue",
        timeout=20_000,
    )
    page.wait_for_timeout(2_500)

    for _step in range(4):
        if _click_first_matching_button(
            page,
            timeout_error_type,
            selectors=(),
            names=("Publish now", "Publish", "Send now", "Send", "Confirm", "Continue"),
            label="publish confirmation",
            timeout=6_000,
            required=False,
        ):
            page.wait_for_timeout(2_500)
            if _looks_published(page):
                return
            continue
        if _looks_published(page):
            return
        break

    buttons = _visible_button_text(page)
    raise SystemExit(
        "Could not confidently complete Substack publish flow. "
        f"Visible buttons: {', '.join(buttons[:20]) or 'none'}"
    )


def _click_first_matching_button(
    page,
    timeout_error_type,
    *,
    selectors: tuple[str, ...],
    names: tuple[str, ...],
    label: str,
    timeout: int,
    required: bool = True,
) -> bool:
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            return True
        except timeout_error_type:
            continue
        except Exception:
            continue

    for name in names:
        for exact in (True, False):
            locator = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I) if exact else re.compile(re.escape(name), re.I)).first
            try:
                locator.wait_for(state="visible", timeout=timeout)
                locator.click()
                return True
            except timeout_error_type:
                continue
            except Exception:
                continue

    if required:
        buttons = _visible_button_text(page)
        raise SystemExit(f"Could not find Substack {label} button. Visible buttons: {', '.join(buttons[:20]) or 'none'}")
    return False


def _looks_published(page) -> bool:
    try:
        text = page.locator("body").inner_text(timeout=5_000)
    except Exception:
        return False
    return bool(re.search(r"\b(published|post is live|view post|share your post)\b", text, re.I))


def _visible_button_text(page) -> list[str]:
    try:
        return page.evaluate(
            """() => Array.from(document.querySelectorAll("button"))
                .filter(el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length))
                .map(el => (el.innerText || el.getAttribute("aria-label") || el.getAttribute("data-testid") || "").trim())
                .filter(Boolean)"""
        )
    except Exception:
        return []


def _editor_is_visible(page, timeout_error_type, *, timeout: int) -> bool:
    selectors = (
        "[data-testid='post-title']",
        "textarea[placeholder*='Title']",
        "input[placeholder*='Title']",
        "[contenteditable='true'][data-placeholder*='Title']",
        "[data-testid='editor']",
        "[placeholder*='Start writing']",
        "[contenteditable='true'][data-placeholder*='Write']",
        ".ProseMirror[contenteditable='true']",
        ".tiptap.ProseMirror",
    )
    for selector in selectors:
        try:
            page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return True
        except timeout_error_type:
            continue
        except Exception:
            continue
    return False


def _looks_like_login_gate(page) -> bool:
    if re.search(r"/(sign-in|login|account|auth)", page.url, re.I):
        return True
    try:
        body_text = page.locator("body").inner_text(timeout=5_000)[:1500]
    except Exception:
        return False
    return bool(re.search(r"\b(log in|sign in|continue with|enter your email|magic link)\b", body_text, re.I))


def _put_rich_text_on_clipboard(page, draft: DraftPost) -> None:
    page.evaluate(
        """async ({ html, text }) => {
            const item = new ClipboardItem({
                "text/html": new Blob([html], { type: "text/html" }),
                "text/plain": new Blob([text], { type: "text/plain" })
            });
            await navigator.clipboard.write([item]);
        }""",
        {"html": draft.html, "text": draft.markdown},
    )


def _select_all(page) -> None:
    page.keyboard.press("Meta+A" if sys.platform == "darwin" else "Control+A")


def _normalized_url(url: str) -> str:
    return url if url.endswith("/") else f"{url}/"


if __name__ == "__main__":
    main()
