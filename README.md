# Workspace Memory Starter

A simple file-based memory system for Codex, Claude Code, or any local AI workflow.

If you want the shortest possible instruction:

1. Open `Start_Here.md`
2. Create or choose a project
3. Keep your memory files updated as you work

**Quick Start**

1. Open `Start_Here.md`
2. Run `make new-project NAME=my-project` when you are ready to start your own work
   This is a wrapper around `scripts/new_project.sh`.
3. Replace or delete `projects/example-project` once you have your own real project
4. Use `make checkpoint-memory ...` at meaningful milestones
   A checkpoint is a single saved summary of what changed, what you decided, and what should happen next.

Start with [Start_Here.md](./Start_Here.md).

## Why This Exists

Most AI workflows lose useful context between sessions.

This starter gives you a simple way to keep:
- durable workspace knowledge
- project-specific handoff state
- a short rolling memory of recent work

It stays readable because everything is just files on disk.

## Setup

This starter works as plain files on disk.

If you want the helper scripts:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
```

If you do not use a virtual environment, the scripts also work with system `python3`.

## What You Get

This repo gives you:
- a clear session entrypoint
- shared workspace memory
- project-level memory and handoff files
- a lightweight project index
- a repeatable checkpoint habit
- optional Git tracking for code and context together
- one placeholder `example-project` so the structure is visible immediately

## Who This Is For

Use this if you want:
- continuity across AI sessions without a database
- files you can read, diff, and edit directly
- a memory system that works with or without GitHub

## First Five Minutes

1. Read `Start_Here.md`
2. Look at `projects/project_index.json`
3. Decide whether `example-project` is enough to learn from or if you want to create a real project immediately
4. If you want a real project, run `make new-project NAME=my-project`
5. Start working and checkpoint when you hit a meaningful milestone

## Day-To-Day Workflow

At the start of a session:
- read `Start_Here.md`
- choose the project you are continuing
- read that project’s `meta/` files

During work:
- update project files when decisions or next steps become clear
- checkpoint memory after meaningful progress by appending a short session summary to `memory/recent_chat_memory.md`

At the end of a session:
- make sure the latest milestone is checkpointed
- commit if you are using Git

## Git and GitHub

Git is recommended, not required.

- If you use Git locally, your memory changes stay auditable.
- If you use GitHub, you can sync the repo and share it with other people.
- If you use neither, the system still works as plain files on disk.
- On Windows, you may prefer running the Python scripts directly with `python` instead of `make`.

## File Layout

```text
Start_Here.md
memory/
  global_memory.md
  recent_chat_memory.md
  domain/engineering_memory.md
  people/user_context.md
projects/
  project_index.json
  example-project/
    meta/
      project_brief.md
      work_items.json
      session_state.json
      memory.md
      handoff.md
      progress_log.md
scripts/
  new_project.sh
  update_project_index.py
  trim_recent_memory.py
  validate_memory_state.py
  checkpoint_memory.py
```

## Included Utilities

- `make new-project` is the simplest way to create a project; it calls `scripts/new_project.sh`
- `scripts/new_project.sh`
- `scripts/update_project_index.py`
- `scripts/trim_recent_memory.py`
- `scripts/validate_memory_state.py`
- `scripts/checkpoint_memory.py`
- `Makefile` wrappers for common actions

## What To Replace First

As soon as you start using this seriously:
- replace or delete `projects/example-project`
- update `memory/global_memory.md` with your actual cross-project preferences
- update `memory/people/user_context.md` with your real collaboration context
- start building real checkpoints in `memory/recent_chat_memory.md`

## Core Idea

Keep the system small.

Use a few predictable files, update them at meaningful milestones, and keep memory close to the work instead of hiding it behind another service.
