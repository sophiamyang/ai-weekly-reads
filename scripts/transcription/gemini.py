from __future__ import annotations

import os
import time

from config import Settings

# Google fetches the video server-side, so this path works from datacenter IPs
# where YouTube blocks caption requests and audio downloads.
RETRY_DELAYS_SECONDS = (0, 20, 60)
RETRYABLE_STATUS_CODES = (429, 500, 503)

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

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    for delay in RETRY_DELAYS_SECONDS:
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
                print(f"Gemini transcription failed for {url}: {exc}")
                return None
            print(f"Gemini transcription throttled for {url}: {type(exc).__name__}")
            continue

        text = (getattr(interaction, "output_text", "") or "").strip()
        if text:
            return text
        print(f"Gemini returned no transcript text for {url}")
        return None
    return None


def _is_retryable(exc: Exception) -> bool:
    """Quota and transient server errors are worth waiting out; others are not."""
    code = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    if code in RETRYABLE_STATUS_CODES:
        return True
    return any(str(status) in str(exc) for status in RETRYABLE_STATUS_CODES)
