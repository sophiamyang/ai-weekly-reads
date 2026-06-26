from __future__ import annotations

import re


SPEAKER_HEADING = "## Featured Speakers"
UNKNOWN_SPEAKER_MARKERS = {
    "not clearly identified",
    "no featured speaker",
    "no featured speakers",
    "unknown",
}
NON_NAME_WORDS = {
    "assessment",
    "future",
    "honest",
    "models",
    "plan",
    "research",
    "video",
    "where",
}


def featured_speakers(markdown: str, title: str = "") -> list[str]:
    section = _section_lines(markdown, SPEAKER_HEADING)
    values: list[str] = []
    for line in section:
        value = re.sub(r"^[-*]\s+", "", line.strip())
        value = re.sub(r"^\d+\.\s+", "", value)
        if not value or value.lower().rstrip(".") in UNKNOWN_SPEAKER_MARKERS:
            continue
        values.append(value)
    return normalize_speakers(values, markdown, title)


def normalize_speakers(values: object, markdown: str = "", title: str = "") -> list[str]:
    raw_values = [str(value).strip() for value in values] if isinstance(values, list) else []
    speakers: list[str] = []
    for value in raw_values:
        for speaker in _split_speaker_value(value):
            if speaker not in speakers:
                speakers.append(speaker)
    if speakers:
        return speakers

    inferred = _speakers_from_title(title)
    if inferred:
        return inferred
    return _speakers_from_summary(markdown)


def without_featured_speakers(markdown: str) -> str:
    lines = markdown.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == SPEAKER_HEADING), None)
    if start is None:
        return markdown
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    remaining = lines[:start] + lines[end:]
    return "\n".join(remaining).strip()


def _section_lines(markdown: str, heading: str) -> list[str]:
    lines = markdown.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        return []
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return lines[start + 1 : end]


def _speakers_from_title(title: str) -> list[str]:
    title = title.strip()
    if not title:
        return []

    dash_parts = re.split(r"\s+[—–]\s+", title)
    if len(dash_parts) > 1:
        candidate = dash_parts[-1].strip()
        speakers = _split_speaker_value(candidate)
        if speakers:
            return speakers

    with_match = re.search(r"\bwith\s+(.+)$", title, flags=re.IGNORECASE)
    if with_match:
        candidate = with_match.group(1).strip()
        speakers = _split_speaker_value(candidate)
        if speakers:
            return speakers

    possessive_match = re.search(r":\s+[^:]+['’]s\s+(.+)$", title)
    if possessive_match:
        candidate = possessive_match.group(1).strip()
        if _looks_like_person_name(candidate):
            return [candidate]

    return []


def _speakers_from_summary(markdown: str) -> list[str]:
    summary = "\n".join(_section_lines(markdown, "## Short Summary")).strip()
    match = re.match(r"(?:The guest,\s+)?([^,\n]+),", summary)
    if not match:
        return []
    candidate = match.group(1).strip()
    return [candidate] if _looks_like_person_name(candidate) else []


def _split_speaker_value(value: str) -> list[str]:
    value = value.strip().strip(".")
    if not value:
        return []

    possessive = re.match(r"^[^,]+['’]s\s+(.+)$", value)
    if possessive:
        value = possessive.group(1).strip()

    ampersand = re.match(r"^(.+?),\s*&\s*(.+?),\s*(.+)$", value)
    if ampersand:
        first, second, affiliation = (part.strip() for part in ampersand.groups())
        if _looks_like_person_name(first) and _looks_like_person_name(second):
            return [f"{first}, {affiliation}", f"{second}, {affiliation}"]

    paired = re.match(r"^(.+?)\s+and\s+(.+?)\s+of\s+(.+)$", value)
    if paired:
        first, second, affiliation = (part.strip() for part in paired.groups())
        if _looks_like_person_name(first) and _looks_like_person_name(second):
            return [f"{first}, {affiliation}", f"{second}, {affiliation}"]

    if re.search(r",\s*and\s+|\s+and\s+", value):
        listed = [
            _clean_name_prefix(part)
            for part in re.split(r",\s*(?:and\s+)?|\s+and\s+", value)
        ]
        if len(listed) > 1 and all(_looks_like_person_name(part) for part in listed):
            return listed

    name = value.split(",", 1)[0].strip()
    return [value] if _looks_like_person_name(name) else []


def _clean_name_prefix(value: str) -> str:
    return re.sub(
        r"^(?:co-?founders?|head of [A-Za-zÀ-ÖØ-öø-ÿ]+)\s+",
        "",
        value.strip(),
        flags=re.IGNORECASE,
    ).strip()


def _looks_like_person_name(value: str) -> bool:
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ.'’-]*", value)
    if not 2 <= len(words) <= 4:
        return False
    if any(word.lower() in NON_NAME_WORDS for word in words):
        return False
    return all(word[0].isupper() for word in words if word)
