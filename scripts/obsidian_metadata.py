from __future__ import annotations

import re
from typing import Any

from utils import yaml_value


TOPICS_HEADING = "## Topics"
TOPIC_RULES: dict[str, tuple[str, ...]] = {
    "ai-agents": ("ai agent", "agents", "agentic", "multi-agent", "agency"),
    "coding-agents": ("coding agent", "code agent", "claude code", "codex", "code generation"),
    "model-evaluation": ("model evaluation", "evals", "benchmark", "benchmarking", "evaluation"),
    "model-training": (
        "model training",
        "training",
        "data curation",
        "fine-tuning",
        "finetuning",
        "reinforcement learning",
        "rlhf",
    ),
    "model-inference": (
        "inference",
        "sampling",
        "denoising",
        "distillation",
        "guidance",
        "quantization",
        "serving",
        "latency",
        "diffusion steps",
    ),
    "foundation-models": (
        "foundation model",
        "language model",
        "large model",
        "model capabilities",
        "model weights",
        "llm",
        "gpt-3",
        "transformer",
        "transformers",
        "model architecture",
    ),
    "multimodal-ai": ("multimodal", "vision-language", "video input", "audio model", "speech model"),
    "generative-media": ("video generation", "video model", "image generation", "diffusion", "generative video"),
    "retrieval": ("retrieval-augmented", "retrieval augmented", "rag", "vector database", "embeddings"),
    "ai-infrastructure": ("gpu", "compute", "deployment", "cloud infrastructure", "inference stack"),
    "developer-tools": (
        "developer tool",
        "ide",
        "mcp",
        "webmcp",
        "api",
        "software development",
        "ai engineering",
        "coding assistant",
        "compiler",
        "demo",
        "demos",
        "codebase",
        "code review",
        "repository",
        "testing",
        "workflow",
        "workflows",
        "tooling",
        "toolkit",
        "toolkits",
        "schema",
        "schemas",
        "maintainability",
        "developer ecosystem",
    ),
    "enterprise-ai": (
        "enterprise ai",
        "enterprise",
        "saas",
        "business workflow",
        "workplace",
        "customer",
        "customers",
        "commercial",
        "revenue",
        "arr",
        "willingness to pay",
        "adoption",
        "market",
        "government",
        "erp",
    ),
    "open-source-ai": ("open-source", "open source", "open model", "sovereign ai"),
    "ai-safety": (
        "ai safety",
        "alignment",
        "guardrail",
        "deception",
        "existential risk",
        "cybersecurity",
        "ransomware",
        "security risk",
        "threat detection",
        "regulation",
    ),
    "ai-research": ("ai research", "research productivity", "scientific discovery", "researcher", "experiments"),
    "ai-for-science": ("ai for science", "biology", "protein", "drug discovery", "mathematics", "theorem"),
    "robotics": ("robotics", "robot", "autonomous system", "physical ai"),
    "human-ai-interaction": (
        "human-ai",
        "human computer",
        "simulated humans",
        "virtual people",
        "brand voice",
        "tone",
        "persona",
        "identity",
        "empathy",
        "user trust",
        "emotionally sensitive",
    ),
    "product-development": (
        "product development",
        "product management",
        "product signals",
        "figma",
        "design workflow",
        "distribution",
        "backlog",
        "prd",
        "sprint",
        "behavior change",
        "vision",
        "commercial value",
    ),
    "web-platform": ("web platform", "browser", "iframe", "web app", "web standard"),
    "synthetic-data": ("synthetic data", "data generation", "simulation data"),
}
TOPIC_ALIASES = {
    "agents": "ai-agents",
    "agentic-ai": "ai-agents",
    "code-agents": "coding-agents",
    "coding": "coding-agents",
    "evals": "model-evaluation",
    "evaluation": "model-evaluation",
    "training": "model-training",
    "inference": "model-inference",
    "llms": "foundation-models",
    "large-language-models": "foundation-models",
    "multimodal": "multimodal-ai",
    "generative-ai": "generative-media",
    "rag": "retrieval",
    "infrastructure": "ai-infrastructure",
    "enterprise": "enterprise-ai",
    "open-source": "open-source-ai",
    "safety": "ai-safety",
    "research": "ai-research",
    "science": "ai-for-science",
    "developer-experience": "developer-tools",
    "product": "product-development",
}
OPERATIONAL_TAG_PREFIXES = ("ai-weekly-reads",)
LEGACY_GENERATED_TAGS = {
    "chinese",
    "direct_media",
    "podcast",
    "raw-transcript",
    "resource",
    "web",
    "web_transcript",
    "weekly-book",
    "youtube",
}


def yaml_list_block(key: str, values: list[str]) -> str:
    unique_values = _unique(values)
    if not unique_values:
        return f"{key}: []"
    lines = [f"{key}:"]
    for value in unique_values:
        lines.append(f"  - {yaml_value(value)}")
    return "\n".join(lines)


def obsidian_aliases(*values: object) -> list[str]:
    return _unique(str(value).strip() for value in values if str(value or "").strip())


def resource_tags(markdown: str, title: str = "", existing: object | None = None) -> list[str]:
    section = _section_topics(markdown)
    topics = _existing_topics(existing) or list(section)
    if not topics:
        topics = _infer_topics(markdown, title)
    elif len(topics) < 2:
        # Pad curated-but-short tag lists up to the 2-4 contract from the
        # explicit section first, then keyword inference (the expensive step).
        for topic in [*section, *_infer_topics(markdown, title)]:
            if len(topics) >= 2:
                break
            if topic not in topics:
                topics.append(topic)
    return topics[:4]


def _existing_topics(existing: object) -> list[str]:
    if not isinstance(existing, list):
        return []
    topics: list[str] = []
    for value in existing:
        # Keep only controlled-vocabulary topics so normalization still
        # repairs drift; stored tags are canonical by construction.
        topic = _canonical_topic(str(value))
        if topic and topic not in topics:
            topics.append(topic)
    return topics


def raw_transcript_tags(_source: str = "", _existing: object | None = None) -> list[str]:
    return []


def weekly_book_tags(
    _status: str = "",
    _language: str = "",
    _existing: object | None = None,
) -> list[str]:
    return []


def without_topics(markdown: str) -> str:
    lines = markdown.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == TOPICS_HEADING), None)
    if start is None:
        return markdown
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[:start] + lines[end:]).strip()


def is_operational_tag(tag: str) -> bool:
    clean = tag.strip().lower()
    return clean in LEGACY_GENERATED_TAGS or clean.startswith(OPERATIONAL_TAG_PREFIXES)


def _section_topics(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    start = next((index for index, line in enumerate(lines) if line.strip() == TOPICS_HEADING), None)
    if start is None:
        return []
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    topics: list[str] = []
    for line in lines[start + 1 : end]:
        value = re.sub(r"^[-*]\s+", "", line.strip())
        topic = _canonical_topic(value)
        if topic and topic not in topics:
            topics.append(topic)
    return topics[:5]


def _infer_topics(markdown: str, title: str) -> list[str]:
    title_text = title.lower()
    body_text = _classification_text(markdown).lower()
    scored: list[tuple[int, str]] = []
    for topic, phrases in TOPIC_RULES.items():
        score = sum(4 for phrase in phrases if _contains_phrase(title_text, phrase))
        score += sum(1 for phrase in phrases if _contains_phrase(body_text, phrase))
        if score:
            scored.append((score, topic))
    scored.sort(key=lambda item: (-item[0], item[1]))
    selected = [item for item in scored if item[0] >= 2][:4]
    if len(selected) < 2:
        selected_slugs = {topic for _score, topic in selected}
        selected.extend(item for item in scored if item[1] not in selected_slugs and item not in selected)
    topics = [topic for _score, topic in selected[:4]]
    if len(topics) < 2:
        topics.extend(_fallback_topics(title_text, body_text, topics))
    return [f"topic/{topic}" for topic in topics[:4]]


def _fallback_topics(title_text: str, body_text: str, selected: list[str]) -> list[str]:
    text = f"{title_text}\n{body_text}"
    fallbacks: list[str] = []
    fallback_rules = {
        "developer-tools": ("tool", "tools", "tooling", "workflow", "workflows", "schema", "developer"),
        "ai-infrastructure": ("compute", "gpu", "sandbox", "sandboxing", "observability", "tracing", "runtime", "worker", "workers", "protocol", "session log", "log", "append-only", "event history", "portability"),
        "enterprise-ai": ("customer", "customers", "commercial", "revenue", "arr", "adoption", "market", "government", "erp"),
        "product-development": ("product", "adoption", "vision", "backlog", "prd", "sprint", "behavior change", "commercial value"),
        "human-ai-interaction": ("tone", "voice", "persona", "identity", "empathy", "trust"),
        "ai-safety": ("safety", "security", "ransomware", "cyber", "regulation", "guardrail", "threat"),
    }
    for topic, phrases in fallback_rules.items():
        if topic in selected or topic in fallbacks:
            continue
        if any(_contains_phrase(text, phrase) for phrase in phrases):
            fallbacks.append(topic)
    if len(selected) + len(fallbacks) < 2:
        for default_topic in ("ai-agents", "developer-tools", "enterprise-ai", "product-development"):
            if default_topic not in selected and default_topic not in fallbacks:
                fallbacks.append(default_topic)
            if len(selected) + len(fallbacks) >= 2:
                break
    return fallbacks


def _contains_phrase(text: str, phrase: str) -> bool:
    return bool(re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", text))


def _classification_text(markdown: str) -> str:
    sections = []
    for heading in ("## One-Sentence Takeaway", "## Short Summary", "## Main Ideas"):
        lines = markdown.splitlines()
        start = next((index for index, line in enumerate(lines) if line.strip() == heading), None)
        if start is None:
            continue
        end = next(
            (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
            len(lines),
        )
        sections.extend(lines[start + 1 : end])
    return "\n".join(sections) or markdown


def _canonical_topic(value: str) -> str | None:
    slug = _tag_segment(value.removeprefix("#").removeprefix("topic/"))
    slug = TOPIC_ALIASES.get(slug, slug)
    if slug not in TOPIC_RULES:
        return None
    return f"topic/{slug}"


def _tag_segment(value: object, fallback: str = "unknown") -> str:
    text = str(value or "").strip().lower().replace("_", "-")
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or fallback


def _unique(values: Any) -> list[str]:
    unique_values: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in unique_values:
            unique_values.append(text)
    return unique_values
