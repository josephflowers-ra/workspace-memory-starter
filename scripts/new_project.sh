#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/new_project.sh <project-slug>" >&2
  exit 1
fi

slug="$1"
if [[ ! "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Project slug must match: ^[a-z0-9][a-z0-9-]*$" >&2
  exit 1
fi

base="projects/$slug"
meta="$base/meta"

if [[ -e "$base" ]]; then
  echo "Project already exists: $base" >&2
  exit 1
fi

mkdir -p "$meta"

cat > "$meta/project_brief.md" <<BRIEF
# Project Brief

## Project name
$slug

## Purpose
Describe the project goal.

## Constraints
- Keep tasks small and artifact-based.
- Prefer readable Markdown and JSON files.

## Success criteria
- Define measurable acceptance criteria.

## Current focus
- Define the immediate next milestone.
BRIEF

cat > "$meta/work_items.json" <<WORK
{
  "project": "$slug",
  "last_updated": "",
  "buckets": [
    "Project Management"
  ],
  "items": []
}
WORK

cat > "$meta/session_state.json" <<'STATE'
{
  "last_session_date": "",
  "current_focus": [],
  "next_actions": [],
  "open_questions": [],
  "blocked_items": [],
  "recent_decisions": [],
  "recent_artifacts": [],
  "notes": []
}
STATE

cat > "$meta/memory.md" <<'MEM'
# Project Memory

## Stable Context

- Add durable project assumptions, constraints, and conventions here.

## Session Snapshots
MEM

cat > "$meta/handoff.md" <<HANDOFF
# Handoff: $slug

## Where to start

- Read \`projects/$slug/meta/project_brief.md\`
- Read \`projects/$slug/meta/work_items.json\`
- Read \`projects/$slug/meta/session_state.json\`

## Next actions

- Define the first 3 work items with acceptance criteria.
HANDOFF

cat > "$meta/progress_log.md" <<'LOG'
# Progress Log

## Session Notes
LOG

python3 scripts/update_project_index.py
echo "Created project scaffold: $base"
