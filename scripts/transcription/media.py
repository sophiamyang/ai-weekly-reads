from __future__ import annotations

from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover - depends on local environment
    requests = None


def download_direct_media(url: str, item_id: str, directory: Path) -> Path | None:
    if requests is None:
        return None
    suffix = Path(url.split("?", 1)[0]).suffix or ".mp3"
    media_path = directory / f"{item_id}{suffix}"
    try:
        response = requests.get(url, timeout=120, stream=True, headers={"User-Agent": "AIWeeklyReads/0.1"})
        response.raise_for_status()
        with media_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 512):
                if chunk:
                    handle.write(chunk)
        return media_path
    except Exception as exc:
        print(f"Could not download audio fallback: {exc}")
        return None
