from __future__ import annotations

import os
import time

from config import Settings

# Google fetches the video server-side, so this path works from datacenter IPs
# where YouTube blocks caption requests and audio downloads.
RETRY_DELAYS_SECONDS = (0, 20, 60)
RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)
# The free tier allows a fixed number of YouTube video-hours per day. Once that
# is spent every remaining video fails the same way, so stop paying the retry
# waits: on a full backlog they would otherwise add ~80s per video for nothing.
QUOTA_FAILURE_STREAK_BEFORE_GIVING_UP_RETRIES = 2

_consecutive_quota_failures = 0

TRANSCRIPT_PROMPT = (
    "Transcribe the spoken audio of this video verbatim as plain text.\n"
    "Rules:\n"
    "- Output only the transcript text, with no preamble, commentary, or headings.\n"
    "- Do not summarize, shorten, or paraphrase; keep the speakers' own words.\n"
    "- Start a new line when the speaker changes or at natural sentence breaks.\n"
    "- Do not include timestamps.\n"
    "- Ignore on-screen text and visuals except when needed to attribute a speaker."
)


def can_transcribe_youtube(settings: Settings) -> bool:
    return bool(settings.youtube_transcription_provider == "gemini" and os.environ.get("GEMINI_API_KEY"))


def youtube_transcription_method(settings: Settings) -> str:
    return f"{settings.youtube_transcription_provider}_youtube_transcribe"


def transcribe_youtube(url: str, settings: Settings) -> str | None:
    """Transcribe a public YouTube video by handing its URL to Gemini."""
    if not can_transcribe_youtube(settings):
        return None

    try:
        from google import genai
    except ImportError:
        print("google-genai is not installed; skipping Gemini YouTube transcription.")
        return None

    global _consecutive_quota_failures

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    delays = RETRY_DELAYS_SECONDS
    if _consecutive_quota_failures >= QUOTA_FAILURE_STREAK_BEFORE_GIVING_UP_RETRIES:
        delays = (0,)

    for delay in delays:
        if delay:
            print(f"Gemini transcription backoff: waiting {delay}s")
            time.sleep(delay)
        try:
            interaction = client.interactions.create(
                model=settings.youtube_transcription_model,
                input=[
                    {"type": "text", "text": TRANSCRIPT_PROMPT},
                    {"type": "video", "uri": url},
                ],
            )
        except Exception as exc:
            if not _is_retryable(exc):
                _consecutive_quota_failures = 0
                print(f"Gemini transcription failed for {url}: {exc}")
                return None
            print(f"Gemini transcription throttled for {url}: {_describe(exc)}")
            continue

        _consecutive_quota_failures = 0
        text = (getattr(interaction, "output_text", "") or "").strip()
        if text:
            return text
        print(f"Gemini returned no transcript text for {url}")
        return None

    _consecutive_quota_failures += 1
    print(f"Gemini transcription gave up for {url}")
    return None


def _is_retryable(exc: Exception) -> bool:
    """Quota and transient server/network errors are worth waiting out; others are not.

    Matches on the SDK's numeric status code rather than the error text, so a
    permanent failure whose message merely contains "429" is not retried.
    """
    code = getattr(exc, "code", None)
    if isinstance(code, int):
        return code in RETRYABLE_STATUS_CODES
    # No status code means the request never got a reply: a timeout or a dropped
    # connection, both of which a retry can still fix.
    return isinstance(exc, (TimeoutError, ConnectionError, OSError))


def _describe(exc: Exception) -> str:
    code = getattr(exc, "code", None)
    return f"{type(exc).__name__} {code}" if isinstance(code, int) else type(exc).__name__
