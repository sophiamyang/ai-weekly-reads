from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sources import youtube_item_id  # noqa: E402
from utils import stable_id  # noqa: E402

VIDEO_ID = "dQw4w9WgXcQ"

EQUIVALENT_URLS = [
    f"https://www.youtube.com/watch?v={VIDEO_ID}",
    f"https://youtube.com/watch?v={VIDEO_ID}",
    f"https://m.youtube.com/watch?v={VIDEO_ID}",
    f"https://youtu.be/{VIDEO_ID}",
    f"https://www.youtube.com/watch?v={VIDEO_ID}&t=42s",
    f"https://www.youtube.com/watch?v={VIDEO_ID}&list=PLabc123",
    f"https://www.youtube.com/embed/{VIDEO_ID}",
    f"https://www.youtube.com/shorts/{VIDEO_ID}",
    f"https://www.youtube.com/live/{VIDEO_ID}",
]


def test_equivalent_youtube_urls_share_one_id():
    ids = {youtube_item_id(url) for url in EQUIVALENT_URLS}
    assert len(ids) == 1, f"expected one id, got {len(ids)}: {sorted(ids)}"


def test_share_link_matches_channel_discovery_link():
    # The duplicate people actually hit: a link pasted into inbox/links.txt
    # against the watch?v= URL channel discovery produces for the same video.
    assert youtube_item_id(f"https://youtu.be/{VIDEO_ID}") == youtube_item_id(
        f"https://www.youtube.com/watch?v={VIDEO_ID}"
    )


def test_timestamp_and_playlist_params_do_not_change_identity():
    base = youtube_item_id(f"https://www.youtube.com/watch?v={VIDEO_ID}")
    assert youtube_item_id(f"https://www.youtube.com/watch?v={VIDEO_ID}&t=42s") == base
    assert youtube_item_id(f"https://www.youtube.com/watch?v={VIDEO_ID}&list=PLabc") == base


def test_different_videos_keep_different_ids():
    assert youtube_item_id(f"https://youtu.be/{VIDEO_ID}") != youtube_item_id(
        "https://youtu.be/oHg5SJYRHA0"
    )


def test_non_youtube_url_falls_back_to_url_hash():
    url = "https://example.com/some/episode"
    assert youtube_item_id(url) == stable_id(url)


def test_youtube_id_is_namespaced_against_raw_video_id_hash():
    # Guards against a non-YouTube item whose URL happens to be the bare video id.
    assert youtube_item_id(f"https://youtu.be/{VIDEO_ID}") != stable_id(VIDEO_ID)
