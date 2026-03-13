#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_META_FILES = [
    "project_brief.md",
    "work_items.json",
    "session_state.json",
    "memory.md",
    "handoff.md",
    "progress_log.md",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def validate_recent_memory(failures: list[str]) -> None:
    path = ROOT / "memory" / "recent_chat_memory.md"
    if not path.exists():
        fail(f"Missing file: {path}", failures)
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# Recent Chat Memory"):
        fail(f"Unexpected header in {path}", failures)
    if "## Entries" not in text:
        fail(f"Missing '## Entries' section in {path}", failures)


def validate_project_index(failures: list[str]) -> None:
    index_path = ROOT / "projects" / "project_index.json"
    if not index_path.exists():
        fail(f"Missing file: {index_path}", failures)
        return

    try:
        parsed = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid JSON: {index_path}: {exc}", failures)
        return

    if parsed.get("schema_version") != 1:
        fail(f"{index_path}: unsupported schema_version", failures)

    projects = parsed.get("projects")
    if not isinstance(projects, list):
        fail(f"{index_path}: 'projects' must be a list", failures)
        return

    project_dirs = {path.name for path in (ROOT / "projects").iterdir() if path.is_dir()}
    indexed_slugs: set[str] = set()

    for entry in projects:
        if not isinstance(entry, dict):
            fail(f"{index_path}: every project entry must be an object", failures)
            continue
        slug = entry.get("slug")
        if not isinstance(slug, str) or not slug:
            fail(f"{index_path}: project entry missing valid slug", failures)
            continue
        indexed_slugs.add(slug)
        if bool(entry.get("has_meta")):
            meta_dir = ROOT / "projects" / slug / "meta"
            for filename in REQUIRED_META_FILES:
                if not (meta_dir / filename).exists():
                    fail(f"Missing required project meta file: {meta_dir / filename}", failures)

    missing_from_index = sorted(project_dirs - indexed_slugs)
    if missing_from_index:
        fail(
            f"{index_path}: missing project entries for {', '.join(missing_from_index)}",
            failures,
        )


def validate_project_session_states(failures: list[str]) -> None:
    for path in sorted((ROOT / "projects").glob("*/meta/session_state.json")):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"Invalid JSON: {path}: {exc}", failures)
            continue

        if not isinstance(parsed, dict):
            fail(f"session_state is not object: {path}", failures)
            continue

        for key in ["current_focus", "next_actions", "open_questions", "blocked_items"]:
            if key in parsed and not isinstance(parsed[key], list):
                fail(f"{path}: '{key}' must be a list when present", failures)


def main() -> int:
    failures: list[str] = []
    validate_recent_memory(failures)
    validate_project_index(failures)
    validate_project_session_states(failures)

    if failures:
        print("Memory/session validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Memory/session validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
