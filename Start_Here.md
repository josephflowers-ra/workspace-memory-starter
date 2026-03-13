# Start Here

This file is the session entrypoint for this workspace.

You can use this system in four ways:
- files only
- files + Git
- files + Python helpers
- files + Git + Python helpers

Files are always the source of truth. Python and Git are optional layers.

## Pick Your Mode

### Files only

- Edit the Markdown and JSON files directly
- Create new projects by copying the example project structure
- Add checkpoints manually to `memory/recent_chat_memory.md`

### Files + Git

- Use the same file-based workflow
- Add commits when you reach meaningful milestones

### Files + Python helpers

- Use `make new-project`, `make checkpoint-memory`, and the other helpers
- The files remain the real source of truth

### Files + Git + Python helpers

- Use the helpers for speed
- Use Git for history and sharing

## Where Memory Lives

- Workspace memory root: `memory/`
- Cross-project memory: `memory/global_memory.md`
- Domain memory: `memory/domain/engineering_memory.md`
- User/context mirror: `memory/people/user_context.md`
- Rolling recent memory: `memory/recent_chat_memory.md`
- Project registry: `projects/project_index.json`
- Project memory: `projects/<project-slug>/meta/memory.md`
- Project handoff state: `projects/<project-slug>/meta/session_state.json`

## Session Start Routine

1. Read `projects/project_index.json`
2. Choose the active project
   - `example-project` is only a placeholder; replace it with your own real project when you start
3. If the work does not fit an existing project, create one:
   - With Python helpers: `make new-project NAME=<project-slug>`
   - Without Python: copy `projects/example-project/` to a new slug and update `projects/project_index.json`
4. Read:
   - `projects/<project-slug>/meta/project_brief.md`
   - `memory/recent_chat_memory.md`
   - `projects/<project-slug>/meta/session_state.json`
   - `projects/<project-slug>/meta/memory.md`
   - `projects/<project-slug>/meta/work_items.json`

## During Work

Checkpoint memory after each meaningful milestone.

A checkpoint is a short saved summary of:
- what changed
- what you decided
- what should happen next

Examples:
- you created a new project
- you finished a draft worth reviewing
- you made an important decision
- you completed a clear implementation step

Checkpoint command:

```bash
make checkpoint-memory \
  CHECKPOINT_SUMMARY="what changed" \
  CHECKPOINT_PROJECT="<project-slug>" \
  CHECKPOINT_DECISIONS="decision 1,decision 2" \
  CHECKPOINT_NEXT="next step 1,next step 2" \
  CHECKPOINT_ARTIFACTS="path/to/artifact1,path/to/artifact2" \
  CHECKPOINT_FILES="file1,file2" \
  CHECKPOINT_TAGS="memory,checkpoint"
```

Without Python, add the checkpoint entry manually to `memory/recent_chat_memory.md`.

Optional maintenance:

```bash
make project-index-refresh
make memory-trim-recent RECENT_LIMIT=3
make memory-validate
```

Without Python, you can still:
- update `projects/project_index.json` by hand
- trim `memory/recent_chat_memory.md` manually
- visually inspect the memory files for consistency

## Session End Routine

Before ending a session:
- make sure the latest milestone is checkpointed
- update the project index if projects changed
- validate memory files if you touched the structure

If you use Git:

```bash
git status
git add -A
git commit -m "checkpoint: <project-slug> <what changed>"
```

If you use GitHub:

```bash
git push origin main
```

## Routing Rule

Before picking a project, ask:
- what are we working on right now?
- should I continue the last thread or start a different project?

If the answer is unclear:
1. Read `memory/recent_chat_memory.md`
2. Summarize the last 3 checkpoints
3. Ask which thread to continue

## Design Rule

Do not try to store everything.

Store only what improves:
- future decisions
- faster resumption
- cleaner handoffs
