from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from project_paths import MEDIA
from utils import youtube_video_id, ytdlp_js_runtime_args, ytdlp_player_client_args

# YouTube throttles caption requests from datacenter IPs, and the throttling
# tightens the harder it is pushed. Space requests out and retry a blocked one
# a few times rather than hammering: bursts cost more items than they recover.
CAPTION_REQUEST_INTERVAL_SECONDS = 5.0
CAPTION_RETRY_DELAYS_SECONDS = (10, 25, 45)
# Once this many videos in a row exhaust their retries, the IP is blocked for
# more than a moment. Keep trying each video once, but stop paying the retry
# wait: on a full channel backlog that alone would add ~25 minutes per run.
CAPTION_BLOCK_STREAK_BEFORE_GIVING_UP_RETRIES = 3

_last_caption_request_at = 0.0
_consecutive_blocked_videos = 0


def fetch_youtube_captions(url: str) -> str | None:
    global _consecutive_blocked_videos

    video_id = youtube_video_id(url)
    if not video_id:
        return None

    retry_delays = CAPTION_RETRY_DELAYS_SECONDS
    if _consecutive_blocked_videos >= CAPTION_BLOCK_STREAK_BEFORE_GIVING_UP_RETRIES:
        retry_delays = ()

    for attempt, retry_delay in enumerate((*retry_delays, None)):
        _throttle_caption_requests()
        try:
            text = _fetch_caption_text(video_id)
            _consecutive_blocked_videos = 0
            return text
        except Exception as exc:
            if _is_permanent_caption_failure(exc):
                _consecutive_blocked_videos = 0
                return None
            if retry_delay is None:
                _consecutive_blocked_videos += 1
                if attempt:
                    print(f"Captions still blocked after {attempt} retries: {url}")
                else:
                    print(f"Captions blocked (skipping retries while IP is throttled): {url}")
                return None
            print(f"Captions blocked for {video_id}; retrying in {retry_delay}s")
            time.sleep(retry_delay)
    return None


def _fetch_caption_text(video_id: str) -> str:
    from youtube_transcript_api import YouTubeTranscriptApi

    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    else:
        transcript = YouTubeTranscriptApi().fetch(video_id)
    return "\n".join(_segment_text(segment) for segment in transcript if _segment_text(segment))


def _is_permanent_caption_failure(exc: Exception) -> bool:
    """True when retrying cannot help: the video has no captions to fetch."""
    try:
        from youtube_transcript_api import _errors as errors
    except Exception:
        return False
    permanent = tuple(
        getattr(errors, name)
        for name in ("TranscriptsDisabled", "NoTranscriptFound", "InvalidVideoId", "AgeRestricted")
        if hasattr(errors, name)
    )
    return bool(permanent) and isinstance(exc, permanent)


def _throttle_caption_requests() -> None:
    global _last_caption_request_at
    elapsed = time.monotonic() - _last_caption_request_at
    if _last_caption_request_at and elapsed < CAPTION_REQUEST_INTERVAL_SECONDS:
        time.sleep(CAPTION_REQUEST_INTERVAL_SECONDS - elapsed)
    _last_caption_request_at = time.monotonic()


def download_youtube_audio(url: str, item_id: str) -> Path | None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    output_template = str(MEDIA / f"{item_id}.%(ext)s")
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        *ytdlp_js_runtime_args(),
        *ytdlp_player_client_args(),
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
    mp3_path = MEDIA / f"{item_id}.mp3"
    if mp3_path.exists():
        return mp3_path
    matches = sorted(
        path
        for path in MEDIA.glob(f"{item_id}.*")
        # Never pick up truncated yt-dlp intermediates from a crashed run.
        if path.suffix.lower() not in {".part", ".ytdl", ".tmp"}
    )
    return matches[0] if matches else None


def _segment_text(segment: object) -> str:
    if isinstance(segment, dict):
        return str(segment.get("text", ""))
    return str(getattr(segment, "text", ""))
