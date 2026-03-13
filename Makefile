SHELL := /bin/bash
.DEFAULT_GOAL := help

NAME ?=
CHECKPOINT_SUMMARY ?=
CHECKPOINT_PROJECT ?=
CHECKPOINT_DECISIONS ?=
CHECKPOINT_NEXT ?=
CHECKPOINT_ARTIFACTS ?=
CHECKPOINT_FILES ?=
CHECKPOINT_TAGS ?=
RECENT_LIMIT ?=

help:
	@echo "Targets:"
	@echo "  make new-project NAME=project-slug"
	@echo "  make project-index-refresh"
	@echo "  make memory-trim-recent [RECENT_LIMIT=3]"
	@echo "  make memory-validate"
	@echo "  make checkpoint-memory CHECKPOINT_SUMMARY='what changed' [CHECKPOINT_PROJECT=slug] [CHECKPOINT_DECISIONS='a,b'] [CHECKPOINT_NEXT='a,b'] [CHECKPOINT_ARTIFACTS='a,b'] [CHECKPOINT_FILES='a,b'] [CHECKPOINT_TAGS='a,b']"

new-project:
	@test -n "$(NAME)" || (echo "NAME is required" && exit 1)
	@bash scripts/new_project.sh "$(NAME)"

project-index-refresh:
	@python3 scripts/update_project_index.py

memory-trim-recent:
	@python3 scripts/trim_recent_memory.py $(if $(RECENT_LIMIT),--limit "$(RECENT_LIMIT)",)

memory-validate:
	@python3 scripts/validate_memory_state.py

checkpoint-memory:
	@test -n "$(CHECKPOINT_SUMMARY)" || (echo "CHECKPOINT_SUMMARY is required" && exit 1)
	@python3 scripts/checkpoint_memory.py \
		--summary "$(CHECKPOINT_SUMMARY)" \
		$(if $(CHECKPOINT_PROJECT),--project "$(CHECKPOINT_PROJECT)",) \
		$(if $(CHECKPOINT_DECISIONS),--decisions-csv "$(CHECKPOINT_DECISIONS)",) \
		$(if $(CHECKPOINT_NEXT),--next-csv "$(CHECKPOINT_NEXT)",) \
		$(if $(CHECKPOINT_ARTIFACTS),--artifacts-csv "$(CHECKPOINT_ARTIFACTS)",) \
		$(if $(CHECKPOINT_FILES),--files-csv "$(CHECKPOINT_FILES)",) \
		$(if $(CHECKPOINT_TAGS),--tags-csv "$(CHECKPOINT_TAGS)",)
