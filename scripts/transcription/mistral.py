from __future__ import annotations

import os
import signal
import time
from contextlib import contextmanager
from pathlib import Path

from config import Settings

TRANSCRIPTION_HARD_TIMEOUT_SECONDS = 5 * 60


class TranscriptionTimeoutError(TimeoutError):
    pass


def can_transcribe(settings: Settings) -> bool:
    if settings.transcription_provider == "mistral":
        return bool(os.environ.get("MISTRAL_API_KEY"))
    return False


def transcription_method(settings: Settings) -> str:
    return f"{settings.transcription_provider}_transcribe"


def transcribe_audio_url(audio_url: str, settings: Settings) -> str | None:
    if not os.environ.get("MISTRAL_API_KEY"):
        return None
    from mistralai.client import Mistral

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    for delay in (0, 30, 90):
        if delay:
            print(f"Mistral transcription backoff: waiting {delay}s")
            time.sleep(delay)
        try:
            with _hard_timeout(TRANSCRIPTION_HARD_TIMEOUT_SECONDS):
                result = client.audio.transcriptions.complete(
                    model=settings.transcription_model,
                    file_url=audio_url,
                    timeout_ms=1000 * 60 * 30,
                )
            return _transcription_text(result)
        except Exception as exc:
            if _should_retry(exc):
                continue
            print(f"Mistral transcription failed for audio URL: {exc}")
            return None
    print(f"Mistral transcription rate-limited for audio URL after retries: {audio_url}")
    return None


def transcribe_media_file(media_path: Path | None, settings: Settings) -> str | None:
    if not media_path or not media_path.exists() or not os.environ.get("MISTRAL_API_KEY"):
        return None
    from mistralai.client import Mistral

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    for delay in (0, 30, 90):
        if delay:
            print(f"Mistral transcription backoff: waiting {delay}s")
            time.sleep(delay)
        try:
            with media_path.open("rb") as media_file:
                with _hard_timeout(TRANSCRIPTION_HARD_TIMEOUT_SECONDS):
                    result = client.audio.transcriptions.complete(
                        model=settings.transcription_model,
                        file={
                            "content": media_file,
                            "file_name": media_path.name,
                        },
                        timeout_ms=1000 * 60 * 30,
                    )
            return _transcription_text(result)
        except Exception as exc:
            if _should_retry(exc):
                continue
            print(f"Mistral transcription failed for {media_path.name}: {exc}")
            return None
    print(f"Mistral transcription rate-limited for {media_path.name} after retries")
    return None


def _transcription_text(result: object) -> str | None:
    text = getattr(result, "text", None)
    if text:
        return str(text).strip()
    if isinstance(result, dict) and result.get("text"):
        return str(result["text"]).strip()
    return None


def _should_retry(exc: Exception) -> bool:
    message = str(exc).lower()
    return "status 429" in message or "rate limit" in message or "rate_limited" in message


@contextmanager
def _hard_timeout(seconds: int):
    if seconds <= 0 or not hasattr(signal, "SIGALRM"):
        yield
        return

    def _raise_timeout(signum, frame):
        raise TranscriptionTimeoutError(f"Timed out after {seconds}s waiting for transcription response.")

    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)
    signal.signal(signal.SIGALRM, _raise_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_timer != (0.0, 0.0):
            signal.setitimer(signal.ITIMER_REAL, *previous_timer)
