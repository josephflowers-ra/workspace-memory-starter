#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECENT_MEMORY_PATH = ROOT / "memory" / "recent_chat_memory.md"


def csv_to_lines(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def append_checkpoint(args: argparse.Namespace) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    lines: list[str] = []
    lines.append(f"### Checkpoint {timestamp}")
    lines.append(f"- Summary: {args.summary}")
    if args.tags_csv:
        lines.append(f"- Tags: {', '.join(csv_to_lines(args.tags_csv))}")
    lines.append("")

    sections = [
        ("Decisions", csv_to_lines(args.decisions_csv)),
        ("Next Actions", csv_to_lines(args.next_csv)),
        ("Artifacts", csv_to_lines(args.artifacts_csv)),
        ("Files Touched", csv_to_lines(args.files_csv)),
    ]

    for heading, items in sections:
        if not items:
            continue
        lines.append(f"#### {heading}")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    existing = RECENT_MEMORY_PATH.read_text(encoding="utf-8").rstrip() + "\n\n"
    marker = "## Entries\n\n"
    if marker not in existing:
        raise ValueError("recent_chat_memory.md is missing the '## Entries' section.")
    before, after = existing.split(marker, 1)
    updated = before + marker + "\n".join(lines).rstrip() + "\n\n" + after.lstrip("\n")
    RECENT_MEMORY_PATH.write_text(updated.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a checkpoint to recent memory.")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--project")
    parser.add_argument("--decisions-csv", default="")
    parser.add_argument("--next-csv", default="")
    parser.add_argument("--artifacts-csv", default="")
    parser.add_argument("--files-csv", default="")
    parser.add_argument("--tags-csv", default="")
    args = parser.parse_args()

    append_checkpoint(args)
    print(f"updated: {RECENT_MEMORY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
