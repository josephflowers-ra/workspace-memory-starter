#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
INDEX_PATH = PROJECTS_DIR / "project_index.json"
REQUIRED_META_FILES = [
    "project_brief.md",
    "work_items.json",
    "session_state.json",
    "memory.md",
    "handoff.md",
    "progress_log.md",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_project_title(project_dir: Path) -> str:
    brief_path = project_dir / "meta" / "project_brief.md"
    if not brief_path.exists():
        return project_dir.name

    lines = brief_path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == "## Project name" and idx + 1 < len(lines):
            title = lines[idx + 1].strip()
            if title:
                return title
    return project_dir.name


def extract_last_session_date(project_dir: Path) -> str:
    session_state_path = project_dir / "meta" / "session_state.json"
    if not session_state_path.exists():
        return ""

    parsed = read_json(session_state_path)
    value = parsed.get("last_session_date", "")
    return value if isinstance(value, str) else ""


def build_entry(project_dir: Path) -> dict:
    meta_dir = project_dir / "meta"
    has_meta = meta_dir.exists()
    missing_meta_files = [
        name for name in REQUIRED_META_FILES if has_meta and not (meta_dir / name).exists()
    ]
    return {
        "slug": project_dir.name,
        "title": extract_project_title(project_dir),
        "path": project_dir.relative_to(ROOT).as_posix(),
        "kind": "project" if has_meta else "collection",
        "status": "active",
        "selectable": has_meta,
        "last_session_date": extract_last_session_date(project_dir),
        "has_meta": has_meta,
        "required_meta_complete": has_meta and not missing_meta_files,
        "missing_meta_files": missing_meta_files,
    }


def main() -> int:
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "required_meta_files": REQUIRED_META_FILES,
        "projects": [
            build_entry(project_dir)
            for project_dir in sorted(PROJECTS_DIR.iterdir())
            if project_dir.is_dir()
        ],
    }
    INDEX_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"updated: {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
