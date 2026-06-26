from __future__ import annotations

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
    publisher_transcript = _publisher_transcript(item)
    if transcript_path and transcript_path.exists():
        cached_text = read_transcript_text(transcript_path)
        if cached_text.lower().startswith("transcript unavailable"):
            if publisher_transcript:
                write_raw_transcript(item, publisher_transcript, transcript_path)
                return transcript_path, "publisher_transcript"
            transcribed = _transcribe_available_audio(item, settings)
            if transcribed:
                write_raw_transcript(item, transcribed, transcript_path)
                return transcript_path, transcription_method(settings)
            return transcript_path, "unavailable"
        return transcript_path, "cached"

    text = publisher_transcript or _existing_text_transcript(item)
    method = "publisher_transcript" if publisher_transcript else _existing_text_method(item)

    if not text and item.source_type == "youtube":
        text = fetch_youtube_captions(item.url)
        method = "youtube_captions"

    if not text:
        text = _transcribe_available_audio(item, settings)
        if text:
            method = transcription_method(settings)

    if not text and item.source_type == "youtube" and can_transcribe(settings):
        media_path = download_youtube_audio(item.url, item.id)
        if media_path:
            text = _transcribe_media_file(media_path, settings)
            method = transcription_method(settings)

    if not text:
        return None, "unavailable"

    transcript_path = write_raw_transcript(item, text, transcript_path)
    return transcript_path, method


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
    lowered = description.lower()
    marker_index = lowered.find("transcript")
    if marker_index == -1:
        return None
    transcript = description[marker_index:]
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
