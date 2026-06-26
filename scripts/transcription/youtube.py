from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from project_paths import MEDIA
from utils import youtube_video_id, ytdlp_js_runtime_args


def fetch_youtube_captions(url: str) -> str | None:
    video_id = youtube_video_id(url)
    if not video_id:
        return None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        if hasattr(YouTubeTranscriptApi, "get_transcript"):
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        else:
            transcript = YouTubeTranscriptApi().fetch(video_id)
        return "\n".join(_segment_text(segment) for segment in transcript if _segment_text(segment))
    except Exception:
        return None


def download_youtube_audio(url: str, item_id: str) -> Path | None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    output_template = str(MEDIA / f"{item_id}.%(ext)s")
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        *ytdlp_js_runtime_args(),
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--output",
        output_template,
        url,
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except Exception:
        return None
    matches = list(MEDIA.glob(f"{item_id}.*"))
    return matches[0] if matches else None


def _segment_text(segment: object) -> str:
    if isinstance(segment, dict):
        return str(segment.get("text", ""))
    return str(getattr(segment, "text", ""))
