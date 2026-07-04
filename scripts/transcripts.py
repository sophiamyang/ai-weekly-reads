from __future__ import annotations

import re
import tempfile
from pathlib import Path

from config import Settings
from sources import MediaItem
from transcript_store import find_raw_transcript, read_transcript_text, write_raw_transcript
from transcription.media import download_direct_media
from transcription.mistral import can_transcribe, transcribe_audio_url, transcribe_media_file, transcription_method
from transcription.youtube import download_youtube_audio, fetch_youtube_captions


def get_or_create_transcript(item: MediaItem, settings: Settings) -> tuple[Path | None, str]:
    transcript_path = find_raw_transcript(item.id)
    if transcript_path and transcript_path.exists():
        cached_text = read_transcript_text(transcript_path)
        if not cached_text.lower().startswith("transcript unavailable"):
            return transcript_path, "cached"
        # A cached "unavailable" marker is not permanent: retry acquisition so
        # captions or transcripts published later win. Skip the yt-dlp audio
        # download here, though — it already failed to produce a transcript
        # once, and re-downloading full audio every run for a stuck item is
        # expensive.
        text, method = _acquire_transcript(item, settings, include_audio_download=False)
        if not text:
            return transcript_path, "unavailable"
        write_raw_transcript(item, text, transcript_path)
        return transcript_path, method

    text, method = _acquire_transcript(item, settings)
    if not text:
        return None, "unavailable"
    transcript_path = write_raw_transcript(item, text, transcript_path)
    return transcript_path, method


def _acquire_transcript(
    item: MediaItem,
    settings: Settings,
    *,
    include_audio_download: bool = True,
) -> tuple[str | None, str]:
    publisher_transcript = _publisher_transcript(item)
    if publisher_transcript:
        return publisher_transcript, "publisher_transcript"

    text = _existing_text_transcript(item)
    if text:
        return text, _existing_text_method(item)

    if item.source_type == "youtube":
        text = fetch_youtube_captions(item.url)
        if text:
            return text, "youtube_captions"

    text = _transcribe_available_audio(item, settings)
    if text:
        return text, transcription_method(settings)

    if include_audio_download and item.source_type == "youtube" and can_transcribe(settings):
        media_path = download_youtube_audio(item.url, item.id)
        if media_path:
            text = _transcribe_media_file(media_path, settings)
            if text:
                return text, transcription_method(settings)

    return None, "unavailable"


def _existing_text_transcript(item: MediaItem) -> str | None:
    if item.source_type == "web_transcript" and item.description:
        return item.description
    if item.source_type == "podcast" and item.origin.startswith("follow-builders:") and item.description:
        return item.description
    return None


def _existing_text_method(item: MediaItem) -> str:
    if item.origin.startswith("follow-builders:"):
        return "follow_builders_feed"
    return "page_text"


def _publisher_transcript(item: MediaItem) -> str | None:
    if item.source_type != "podcast" or not item.description:
        return None
    description = item.description.strip()
    # Require the "Transcript" marker to start a line — either as a
    # heading-like label ("Transcript", "# Full Transcript", "=== Transcript
    # ===") or with the text following a colon on the same line — so prose
    # such as "a full transcript is available at ..." in show notes is not
    # mistaken for the transcript itself.
    marker = re.search(
        r"(?im)^[#>*=\s-]*(?:full\s+|episode\s+|show\s+)?transcripts?\s*[:*=\s-]*$"
        r"|^(?:full\s+|episode\s+|show\s+)?transcripts?\s*:\s*\S"
        r"|^transcripts?\b[^\n]{0,30}:\s*$",
        description,
    )
    if marker is None:
        return None
    transcript = description[marker.start():]
    # Substack adds this footer after public podcast descriptions.
    footer_index = transcript.lower().find("this is a public episode")
    if footer_index != -1:
        transcript = transcript[:footer_index]
    transcript = transcript.strip()
    if len(transcript.split()) < 500:
        return None
    return transcript


def _transcribe_available_audio(item: MediaItem, settings: Settings) -> str | None:
    if not item.audio_url or not can_transcribe(settings):
        return None
    if settings.transcription_provider == "mistral":
        text = transcribe_audio_url(item.audio_url, settings)
        if text:
            return text
        with tempfile.TemporaryDirectory() as tmpdir:
            media_path = download_direct_media(item.audio_url, item.id, Path(tmpdir))
            return transcribe_media_file(media_path, settings)
    return None


def _transcribe_media_file(media_path: Path | None, settings: Settings) -> str | None:
    if settings.transcription_provider == "mistral":
        return transcribe_media_file(media_path, settings)
    return None
