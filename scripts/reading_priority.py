from __future__ import annotations

import re


PRIORITY_HEADING = "## Reading Priority"
HIGH_SIGNAL_WORDS = {
    "actionable",
    "battle-tested",
    "benchmark",
    "benchmarks",
    "case study",
    "concrete",
    "consequential",
    "cost",
    "cost-saving",
    "data-backed",
    "directly applicable",
    "evidence",
    "evidence-backed",
    "first-person",
    "immediate",
    "materially",
    "measurable",
    "mechanism",
    "mechanisms",
    "novel",
    "pivotal",
    "practical",
    "practicality",
    "production",
    "production-ready",
    "production-tested",
    "rare",
    "reliable",
    "signal",
    "signals",
    "step-change",
    "strategic",
    "tradeoff",
    "tradeoffs",
}
LOW_SIGNAL_WORDS = {
    "announcement",
    "contextual",
    "event",
    "introductory",
    "niche",
    "overview",
    "promotional",
    "recap",
    "repetitive",
    "thin",
}
EVENT_TITLE_PATTERNS = (
    r"\b6 things to know\b",
    r"\bopening keynote\b",
    r"\bworld'?s fair\b",
    r"\bworkshop\b",
    r"\bwalkthrough\b",
    r"\bstate of\b",
)
DEFAULT_REASONS = {
    "High": "Unusually concrete and consequential relative to a typical reading queue.",
    "Medium": "Useful and substantive, but not essential unless this topic is a current priority.",
    "Low": "Mostly contextual, repetitive, or niche relative to the rest of the reading queue.",
}


def normalize_reading_priority(markdown: str, title: str = "") -> str:
    lines = markdown.splitlines()
    start, end = _section_bounds(lines, PRIORITY_HEADING)
    label, reason = _extract_priority(lines, start, end)
    normalized_label = _calibrate_label(markdown, title, label, reason)
    normalized_reason = _normalize_reason(reason, normalized_label)
    block = [PRIORITY_HEADING, "", f"{normalized_label} – {normalized_reason}"]

    if start is None:
        content = markdown.rstrip()
        if content:
            content += "\n\n"
        return content + "\n".join(block) + "\n"

    replaced = lines[:start] + block + lines[end:]
    return "\n".join(replaced).strip() + "\n"


def _extract_priority(lines: list[str], start: int | None, end: int | None) -> tuple[str, str]:
    if start is None or end is None:
        return "", ""
    section_lines = [line.strip() for line in lines[start + 1 : end] if line.strip()]
    if not section_lines:
        return "", ""

    first = _strip_emphasis(section_lines[0])
    match = re.match(r"^(High|Medium|Low)\s*(?:[–—:-]\s*(.*))?$", first, flags=re.IGNORECASE)
    if match:
        label = match.group(1).capitalize()
        reason = (match.group(2) or "").strip()
        if not reason and len(section_lines) > 1:
            reason = " ".join(_strip_emphasis(line) for line in section_lines[1:]).strip()
        return label, _clean_reason(reason)

    joined = " ".join(_strip_emphasis(line) for line in section_lines).strip()
    return "", _clean_reason(joined)


def _section_bounds(lines: list[str], heading: str) -> tuple[int | None, int | None]:
    start = next((index for index, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        return None, None
    end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
    return start, end


def _calibrate_label(markdown: str, title: str, label: str, reason: str) -> str:
    existing = label.lower()
    if existing in {"medium", "low"}:
        return existing.capitalize()

    score = 0
    if _bullet_count(markdown, "## Notable Details") >= 4 or _section_has_digits(markdown, "## Notable Details"):
        score += 1
    if _bullet_count(markdown, "## Actionable Takeaways") >= 3:
        score += 1
    if _has_real_qa(markdown):
        score += 1
    if _contains_signal(reason, HIGH_SIGNAL_WORDS):
        score += 1
    if _contains_signal(_summary_excerpt(markdown), HIGH_SIGNAL_WORDS):
        score += 1
    if _contains_signal(reason, LOW_SIGNAL_WORDS):
        score -= 1
    if _looks_event_like(title):
        score -= 1
    if _is_thin(markdown):
        score -= 1

    if score >= 5:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def _normalize_reason(reason: str, label: str) -> str:
    cleaned = _clean_reason(reason)
    return cleaned or DEFAULT_REASONS[label]


def _clean_reason(reason: str) -> str:
    value = _strip_emphasis(reason).strip()
    value = re.sub(r"^(High|Medium|Low)\s*[–—:-]?\s*", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"^[–—:-]+\s*", "", value).strip()
    value = re.sub(r"\s+", " ", value)
    return value.rstrip(". ") + "." if value else ""


def _summary_excerpt(markdown: str) -> str:
    return " ".join(_section_lines(markdown, "## Short Summary") + _section_lines(markdown, "## Main Ideas"))


def _section_lines(markdown: str, heading: str) -> list[str]:
    lines = markdown.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        return []
    end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
    return [line.strip() for line in lines[start + 1 : end] if line.strip()]


def _bullet_count(markdown: str, heading: str) -> int:
    return sum(1 for line in _section_lines(markdown, heading) if re.match(r"^[-*]\s+|^\d+\.\s+", line))


def _section_has_digits(markdown: str, heading: str) -> bool:
    return any(re.search(r"\d", line) for line in _section_lines(markdown, heading))


def _has_real_qa(markdown: str) -> bool:
    section = " ".join(_section_lines(markdown, "## Questions And Answers")).lower()
    return bool(section) and "no distinct q&a section" not in section


def _is_thin(markdown: str) -> bool:
    return _bullet_count(markdown, "## Notable Details") < 2 and _bullet_count(markdown, "## Actionable Takeaways") < 2 and not _has_real_qa(markdown)


def _contains_signal(text: str, signals: set[str]) -> bool:
    lowered = text.lower()
    return any(signal in lowered for signal in signals)


def _looks_event_like(title: str) -> bool:
    lowered = title.lower()
    return any(re.search(pattern, lowered) for pattern in EVENT_TITLE_PATTERNS)


def _strip_emphasis(value: str) -> str:
    return value.replace("*", "").replace("_", "").strip()
