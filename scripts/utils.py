from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from datetime import date, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


def slugify(value: str, fallback: str = "item") -> str:
    value = value.strip().lower()
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value[:80] or fallback


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, value: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write via a temp file so a crash mid-write can't leave a truncated
    # resource or transcript that later parses as frontmatter-less.
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp_path.write_text(value, encoding="utf-8")
        if mode is not None:
            os.chmod(tmp_path, mode)
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def as_bool(value: object, default: bool = True) -> bool:
    if value is None or value == "":
        return default
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "0", "no", "off"}
    return bool(value)


def yaml_value(value: Any) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(str(value), ensure_ascii=False)


def split_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, markdown
    frontmatter = markdown[4:end]
    body = markdown[end + 5 :]
    return parse_frontmatter(frontmatter), body


def parse_frontmatter(frontmatter: str) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    current_key: str | None = None
    for line in frontmatter.splitlines():
        if line.startswith("  - ") and current_key:
            values = fields.get(current_key)
            if not isinstance(values, list):
                values = []
                fields[current_key] = values
            values.append(_parse_yaml_scalar(line.removeprefix("  - ").strip()))
            continue
        if line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        stripped = value.strip()
        fields[current_key] = "" if stripped == "" else _parse_yaml_scalar(stripped)
    return fields


def _parse_yaml_scalar(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return value


GRAPH_ONLY_HEADINGS = {"connections", "related notes", "obsidian connections"}


def strip_graph_only_sections(markdown: str) -> str:
    lines = markdown.splitlines()
    kept: list[str] = []
    skipping_level: int | None = None
    for line in lines:
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            label = heading.group(2).strip().lower()
            if label in GRAPH_ONLY_HEADINGS:
                skipping_level = level
                continue
            if skipping_level is not None and level <= skipping_level:
                skipping_level = None
        if skipping_level is not None:
            if line.strip() == "***":
                skipping_level = None
                kept.append(line)
            continue
        kept.append(line)
    return "\n".join(kept)


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def today_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    for candidate in (text, text.replace("Z", "+00:00")):
        try:
            return datetime.fromisoformat(candidate).date()
        except ValueError:
            pass
    try:
        return datetime.strptime(text, "%Y%m%d").date()
    except ValueError:
        pass
    try:
        return parsedate_to_datetime(text).date()
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower().rsplit("@", 1)[-1].split(":", 1)[0]
    if host == "youtu.be":
        return parsed.path.strip("/") or None
    if host == "youtube.com" or host.endswith(".youtube.com"):
        query_id = parse_qs(parsed.query).get("v", [None])[0]
        if query_id:
            return query_id
        parts = [part for part in parsed.path.split("/") if part]
        for marker in ("shorts", "embed", "live"):
            if marker in parts:
                index = parts.index(marker)
                if index + 1 < len(parts):
                    return parts[index + 1]
    return None


def ytdlp_js_runtime_args() -> list[str]:
    node_path = shutil.which("node")
    if not node_path:
        return []
    return ["--js-runtimes", f"node:{node_path}"]


def ytdlp_js_runtimes() -> dict[str, dict[str, str]]:
    node_path = shutil.which("node")
    if not node_path:
        return {}
    return {"node": {"path": node_path}}
