from __future__ import annotations

import os
import time
from pathlib import Path

import requests

from config import Settings
from project_paths import PROMPTS, SUMMARIES
from sources import MediaItem
from transcript_store import read_transcript_text
from utils import read_text, write_text


SUMMARY_TEMPLATE = """# {title}

Source: {source_type}
Original link: {url}

## One-Paragraph Summary

{overview}

## Main Ideas

{main_ideas}

## Questions And Answers

{qa}

## Notable Details

{details}

## Actionable Takeaways

{takeaways}

## Reading Priority

{priority}
"""


def get_or_create_summary(item: MediaItem, transcript_path: Path, settings: Settings) -> Path:
    summary_path = SUMMARIES / f"{item.id}.md"
    if summary_path.exists() and not should_refresh_summary(summary_path, settings):
        return summary_path

    transcript = read_transcript_text(transcript_path)
    if settings.summary_provider == "mistral" and os.environ.get("MISTRAL_API_KEY") and _has_real_transcript(transcript):
        summary = _mistral_summary(item, transcript, settings)
    else:
        summary = _local_summary(item, transcript, settings)

    write_text(summary_path, summary)
    return summary_path


def summary_path_for(item: MediaItem) -> Path:
    return SUMMARIES / f"{item.id}.md"


def should_refresh_summary(summary_path: Path, settings: Settings) -> bool:
    if not summary_path.exists():
        return True
    summary = read_text(summary_path)
    if os.environ.get("MISTRAL_API_KEY") and "AI summary is not enabled yet" in summary:
        return True
    if os.environ.get("MISTRAL_API_KEY") and "Not generated in local fallback mode" in summary:
        return True
    if os.environ.get("MISTRAL_API_KEY") and "Transcript excerpt:" in summary:
        return True
    if os.environ.get("MISTRAL_API_KEY") and "Mistral summary failed" in summary:
        return True
    return False


def _has_real_transcript(transcript: str) -> bool:
    lowered = transcript.lower()
    return "transcript unavailable" not in lowered and "transcription failed" not in lowered


def is_placeholder_summary(summary: str) -> bool:
    return (
        "AI summary is not enabled yet" in summary
        or "Not generated in local fallback mode" in summary
        or "Mistral summary failed" in summary
        or "AI summary failed" in summary
    )


def has_real_transcript(transcript: str) -> bool:
    return _has_real_transcript(transcript)


def _mistral_summary(item: MediaItem, transcript: str, settings: Settings) -> str:
    try:
        response = _post_mistral_summary(item, transcript, settings)
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        return format_ai_summary(item, content)
    except Exception as exc:
        return _local_summary(item, transcript, settings, note=f"Mistral summary failed: {exc}")


def _post_mistral_summary(item: MediaItem, transcript: str, settings: Settings) -> requests.Response:
    payload = mistral_chat_payload(item, transcript, settings)
    headers = {
        "Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}",
        "Content-Type": "application/json",
    }
    backoffs = [0, 10, 30, 60]
    response: requests.Response | None = None
    for delay in backoffs:
        if delay:
            print(f"Mistral rate limit/backoff: waiting {delay}s before retrying {item.title}")
            time.sleep(delay)
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        if response.status_code != 429:
            return response
    assert response is not None
    return response


def mistral_chat_payload(item: MediaItem, transcript: str, settings: Settings) -> dict:
    return {
        "model": settings.summary_model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": "You create precise, readable Markdown knowledge-base notes from long media transcripts.",
            },
            {
                "role": "user",
                "content": _summary_prompt(item, transcript),
            },
        ],
    }


def format_ai_summary(item: MediaItem, content: str) -> str:
    content = strip_ai_response_wrappers(content)
    return f"# {item.title}\n\nSource: {item.source_type}\nOriginal link: {item.url}\n\n{content.strip()}\n"


def strip_ai_response_wrappers(content: str) -> str:
    stripped = strip_outer_markdown_fence(content).strip()
    fenced = _extract_markdown_fence(stripped)
    if fenced:
        stripped = fenced.strip()
    heading_index = _first_summary_heading_index(stripped)
    if heading_index > 0:
        prefix = stripped[:heading_index].strip().lower()
        if not prefix or "markdown" in prefix or "here is" in prefix or len(prefix.split()) <= 20:
            stripped = stripped[heading_index:]
    return stripped.strip()


def strip_outer_markdown_fence(content: str) -> str:
    stripped = content.strip()
    if not stripped.startswith("```"):
        return content
    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return content


def _extract_markdown_fence(content: str) -> str | None:
    lines = content.splitlines()
    for start, line in enumerate(lines):
        marker = line.strip().lower()
        if marker not in {"```", "```markdown", "```md"}:
            continue
        for end in range(start + 1, len(lines)):
            if lines[end].strip() == "```":
                candidate = "\n".join(lines[start + 1 : end]).strip()
                if "## " in candidate:
                    return candidate
                break
    return None


def _first_summary_heading_index(content: str) -> int:
    heading_markers = [
        "## One-Sentence Takeaway",
        "## Short Summary",
        "## Main Ideas",
    ]
    indexes = [content.find(marker) for marker in heading_markers if content.find(marker) != -1]
    return min(indexes) if indexes else -1


def _summary_prompt(item: MediaItem, transcript: str) -> str:
    prompt_template = read_text(_prompt_path_for(item))
    return f"""
{prompt_template}

Title: {item.title}
URL: {item.url}
Source type: {item.source_type}
Published: {item.published or "unknown"}
Description:
{item.description or ""}

Transcript:
{transcript[:60000]}
"""


def _prompt_path_for(item: MediaItem) -> Path:
    if item.source_type in {"podcast", "youtube"}:
        return PROMPTS / "summarize_podcast.md"
    return PROMPTS / "summarize_resource.md"


def _local_summary(item: MediaItem, transcript: str, settings: Settings, note: str | None = None) -> str:
    words = transcript.split()
    excerpt = " ".join(words[:350])
    if len(words) > 350:
        excerpt += "..."
    if note:
        overview = note
    else:
        overview = "AI summary is not enabled yet. Set MISTRAL_API_KEY to generate structured summaries with Mistral AI."
    return SUMMARY_TEMPLATE.format(
        title=item.title,
        source_type=item.source_type,
        url=item.url,
        overview=overview,
        main_ideas=f"- Transcript excerpt: {excerpt or 'No transcript text available.'}",
        qa="- Not generated in local fallback mode.",
        details="- Not generated in local fallback mode.",
        takeaways="- Not generated in local fallback mode.",
        priority="Medium, pending AI summary.",
    )
