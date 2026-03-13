#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECENT_MEMORY_PATH = ROOT / "memory" / "recent_chat_memory.md"
HEADER = "# Recent Chat Memory\n\nRolling checkpoints to preserve short-horizon context between sessions.\n\n## Entries\n\n"
CHECKPOINT_MARKER = "### Checkpoint "


def split_checkpoints(text: str) -> list[str]:
    if "## Entries" not in text:
        raise ValueError("recent_chat_memory.md is missing the '## Entries' section.")

    _, entries = text.split("## Entries", 1)
    entries = entries.lstrip("\n")
    if not entries.strip():
        return []

    parts = entries.split(CHECKPOINT_MARKER)
    checkpoints: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        checkpoints.append(f"{CHECKPOINT_MARKER}{part}\n\n")
    return checkpoints


def main() -> int:
    parser = argparse.ArgumentParser(description="Trim recent memory to the newest N checkpoints.")
    parser.add_argument("--limit", type=int, default=3, help="Number of newest checkpoints to keep.")
    args = parser.parse_args()

    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    text = RECENT_MEMORY_PATH.read_text(encoding="utf-8")
    checkpoints = split_checkpoints(text)
    kept = checkpoints[: args.limit]
    RECENT_MEMORY_PATH.write_text(HEADER + "".join(kept).rstrip() + "\n", encoding="utf-8")
    print(f"updated: {RECENT_MEMORY_PATH} (kept {len(kept)} checkpoints)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
