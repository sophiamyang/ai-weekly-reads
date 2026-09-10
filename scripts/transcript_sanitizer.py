from __future__ import annotations

import hashlib
import os
import re
import time

from config import Settings
from project_paths import SANITIZED_TRANSCRIPTS


CHUNK_SIZE = 12000


def transcript_for_reading(transcript: str, settings: Settings) -> str:
    cleaned = deterministic_cleanup(transcript)
    if not settings.rewrite_full_transcripts:
        return cleaned
    if not os.environ.get("MISTRAL_API_KEY"):
        return cleaned
    return _cached_mistral_rewrite(cleaned, settings)


def deterministic_cleanup(transcript: str) -> str:
    text = transcript.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs: list[str] = []
    pending: list[str] = []
    current_speaker: str | None = None

    def flush_pending() -> None:
        if not pending:
            return
        rendered = _paragraphs_from_text(" ".join(pending))
        if current_speaker:
            paragraphs.extend(f"**{current_speaker}:** {paragraph}" for paragraph in rendered)
        else:
            paragraphs.extend(rendered)
        pending.clear()

    for raw_line in text.splitlines():
        line = _clean_line(raw_line)
        if not line:
            flush_pending()
            current_speaker = None
            continue
        speaker, rest = _speaker_turn(line)
        if speaker:
            flush_pending()
            current_speaker = speaker
            if rest:
                pending.append(rest)
            continue
        pending.append(line)
    flush_pending()
    return "\n\n".join(paragraphs).strip()


STORED_PARAGRAPH_WORDS = 90

# Only unmistakable diarization markers. The general `Name:` heuristic used for
# digest text is far too loose for stored transcripts: measured across the whole
# vault it matched zero real speakers and 36 false ones — mid-sentence colons
# ("My current advice to founders is:") and section headings ("Introduction:").
# Gemini and Mistral both return undiarized prose, so labelling is nearly always
# wrong here; recognise only the explicit forms and otherwise leave text alone.
_EXPLICIT_SPEAKER = re.compile(r"^(speaker[ _-]?\d{1,2})\s*:\s*(.*)$", re.IGNORECASE)


def format_for_storage(transcript: str, target_words: int = STORED_PARAGRAPH_WORDS) -> str:
    """Reflow a transcript into readable paragraphs, changing no words.

    Transcription returns either one unbroken block (Mistral) or one sentence
    per line (Gemini). Markdown renders both as a single wall of text — the
    worst in this vault was a 53,259-word paragraph. This regroups sentences
    into paragraphs and preserves any blank-line structure the source had.
    """
    text = transcript.replace("\r\n", "\n").replace("\r", "\n")
    blocks: list[list[str]] = [[]]
    for raw_line in text.splitlines():
        line = _clean_line(raw_line)
        if not line:
            if blocks[-1]:
                blocks.append([])
            continue
        blocks[-1].append(line)

    out: list[str] = []
    for block in blocks:
        if not block:
            continue
        speaker, first = _EXPLICIT_SPEAKER.match(block[0]).groups() if _EXPLICIT_SPEAKER.match(block[0]) else (None, None)
        if speaker:
            block = [first, *block[1:]] if first else block[1:]
        paragraphs = _paragraphs_from_text(" ".join(block), target_words)
        if speaker and paragraphs:
            paragraphs[0] = f"**{speaker.strip()}:** {paragraphs[0]}"
        out.extend(paragraphs)
    return "\n\n".join(out).strip()


# A leading timestamp is only stripped when it cannot be speech. Bracketed
# forms and zero-padded or hour:minute:second forms are machine-emitted; a bare
# "2:00" with an unpadded hour is how a person says a time, and stripping it
# turned "2:00 a.m. Wow, thanks for being on" into "a.m. Wow, thanks for being
# on". Across 88 stored transcripts there were zero real leading timestamps and
# one spoken time, so the loose rule only ever did damage here.
_LEADING_TIMESTAMP = re.compile(
    r"^(?:"
    r"\[\d{1,2}:\d{2}(?::\d{2})?\]"          # [0:01] or [00:01:02]
    r"|\(\d{1,2}:\d{2}(?::\d{2})?\)"         # (0:01)
    r"|\d{1,2}:\d{2}:\d{2}"                   # 00:01:02
    r"|\d{2}:\d{2}(?!\s*[ap]\.?m\.?\b)"     # 02:30, but not "02:30 pm"
    r")\s*"
)


def _clean_line(line: str) -> str:
    line = re.sub(r"\s+", " ", line).strip()
    while (stripped := _LEADING_TIMESTAMP.sub("", line, count=1)) != line:
        line = stripped
    line = line.strip()
    if re.fullmatch(r"[\[(]?\d{1,2}:\d{2}(?::\d{2})?[\])]?", line):
        return ""
    return line


def _speaker_turn(line: str) -> tuple[str | None, str]:
    match = re.match(
        r"^(?:[-*]\s*)?((?:speaker|SPEAKER)[_ -]?\d{1,2}|[A-Za-z][A-Za-z0-9 ._'-]{0,50})\s*:\s*(.*)$",
        line,
        re.IGNORECASE,
    )
    if not match:
        return None, line
    speaker = re.sub(r"\s+", " ", match.group(1).replace("_", " ")).strip()
    if len(speaker.split()) > 6:
        return None, line
    return speaker, match.group(2).strip()


def _paragraphs_from_text(text: str, target_words: int = 120) -> list[str]:
    if not text.strip():
        return []
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    paragraphs: list[str] = []
    current: list[str] = []
    word_count = 0
    for sentence in sentences:
        words = sentence.split()
        if current and word_count + len(words) > target_words:
            paragraphs.append(" ".join(current))
            current = []
            word_count = 0
        current.append(sentence)
        word_count += len(words)
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def _cached_mistral_rewrite(transcript: str, settings: Settings) -> str:
    SANITIZED_TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(f"{settings.transcript_rewrite_model}\n{transcript}".encode("utf-8")).hexdigest()
    cache_path = SANITIZED_TRANSCRIPTS / f"{key}.md"
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8").strip()
    try:
        rewritten = "\n\n".join(_rewrite_chunk(chunk, settings) for chunk in _chunks(transcript)).strip()
    except Exception as exc:
        print(f"Mistral transcript rewrite failed; using deterministic cleanup: {exc}")
        return transcript
    if rewritten:
        cache_path.write_text(rewritten + "\n", encoding="utf-8")
        return rewritten
    return transcript


def _chunks(text: str) -> list[str]:
    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        addition = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(addition) > CHUNK_SIZE and current:
            chunks.append(current)
            current = paragraph
        else:
            current = addition
    if current:
        chunks.append(current)
    return chunks


def _rewrite_chunk(chunk: str, settings: Settings) -> str:
    import requests

    headers = {
        "Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.transcript_rewrite_model,
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": "Rewrite transcripts into readable Markdown while preserving meaning, speaker turns, names, and factual claims. Remove lexical fillers, smooth false starts, and collapse repeated words only when they do not change meaning. Do not summarize or add information.",
            },
            {
                "role": "user",
                "content": f"Clean this transcript excerpt for reading. Keep speaker labels in bold Markdown when present. Remove lexical fillers such as um, uh, you know, and non-meaningful like. Smooth false starts and repeated words. Preserve technical terms, claims, numbers, caveats, and speaker intent. Return only the cleaned transcript.\n\n{chunk}",
            },
        ],
    }
    response = None
    for delay in (0, 10, 30):
        if delay:
            print(f"Mistral transcript rewrite backoff: waiting {delay}s")
            time.sleep(delay)
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        if response.status_code != 429:
            response.raise_for_status()
            return _strip_markdown_fence(response.json()["choices"][0]["message"]["content"])
    assert response is not None
    response.raise_for_status()
    return ""


def _strip_markdown_fence(content: str) -> str:
    stripped = content.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped


def _demo() -> None:
    raw = """[00:01] Speaker_1: um this is a raw line. it keeps going because transcripts are messy.\n\n00:02:03\nAlice: I think this should read better. You know, without weird spacing."""
    cleaned = deterministic_cleanup(raw)
    assert "[00:01]" not in cleaned
    assert "**Speaker 1:**" in cleaned
    assert "**Alice:**" in cleaned


if __name__ == "__main__":
    _demo()
