# Fimbulwinter - developer task runner
#
# Run `make` (or `make help`) to list targets.
# Pass script flags through ARGS, e.g.:  make deploy-full ARGS='--yes --no-restart'
#
# Note: server-install.sh and server-autoupdate.sh run on the game server via
# the Pelican egg, and scripts/pipeline/ is driven by the mod-maintenance
# workflow (see CLAUDE.md "Maintenance pipeline"); only the parts that are
# useful locally are exposed as targets here.

SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

TOML ?= thunderstore.toml
ARGS ?=
OUT  ?=
# Release tooling. CI installs pinned versions; locally, put them on PATH or
# point these at the binaries.
CHANGIE   ?= changie
GIT_CLIFF ?= git-cliff
PY        ?= python3
PIPE      := scripts/pipeline
# Version bump for release-prep: auto picks it (see release_notes.py level).
BUMP      ?= auto

.PHONY: help version updates profile build deploy-configs deploy-full deploy-reinstall install-mods \
	change changelog-lint keybind-audit release-prep release-notes release-check clean

help: ## Show this help message
	@echo "Fimbulwinter - available targets:"
	@echo
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Variables (append VAR=value to any target):"
	@echo "  ARGS='...'   extra flags passed through to the script"
	@echo "               deploy-*:     --yes  --no-restart"
	@echo "               install-mods: --server-dir DIR --source thunderstore|local --repo-dir . --full"
	@echo "  TOML=path    toml used by 'updates' (default: thunderstore.toml)"
	@echo "  OUT=path     output path for 'profile' (default: dist/)"
	@echo
	@echo "Examples:"
	@echo "  make profile"
	@echo "  make updates"
	@echo "  make deploy-configs ARGS='--yes'"
	@echo "  make deploy-full ARGS='--yes --no-restart'"
	@echo "  make change             (add a player-facing changelog note)"
	@echo "  make release-prep && make release-check"

version: ## Print the current package version from thunderstore.toml
	@grep -Po 'versionNumber = "\K[^"]+' $(TOML)

updates: ## Check Thunderstore for outdated mods (scripts/update-mods.sh)
	bash scripts/update-mods.sh $(TOML)

profile: ## Build the distributable .r2z profile into dist/ (scripts/export-profile.sh)
	bash scripts/export-profile.sh $(OUT)

build: ## Build the Thunderstore package zip with tcli (output in build/)
	tcli build --config-path $(TOML)

deploy-configs: ## Push config/ to the live server and restart (scripts/deploy.sh configs)
	bash scripts/deploy.sh configs $(ARGS)

deploy-full: ## Stage local toml-resolved mods + configs to the server (scripts/deploy.sh full)
	bash scripts/deploy.sh full $(ARGS)

deploy-reinstall: ## Panel reinstall pulling the latest PUBLISHED pack (scripts/deploy.sh reinstall)
	bash scripts/deploy.sh reinstall $(ARGS)

install-mods: ## Run the shared mod resolver/installer (needs ARGS, e.g. ARGS='--server-dir /tmp/x --source local --repo-dir .')
	@if [ -z "$(ARGS)" ]; then \
		echo "install-mods requires ARGS, e.g.:"; \
		echo "  make install-mods ARGS='--server-dir /tmp/stage --source local --repo-dir .'"; \
		exit 1; \
	fi
	bash scripts/install-mods.sh $(ARGS)

change: ## Add a player-facing changelog note (.changes/unreleased/)
	$(CHANGIE) new

changelog-lint: ## Check CHANGELOG.md, .changes/ and notes (ARGS='--base main' in PRs)
	CHANGIE=$(CHANGIE) $(PY) $(PIPE)/changelog_lint.py $(ARGS)

keybind-audit: ## List shared key combinations (ARGS='--base main' fails on new ones)
	$(PY) $(PIPE)/keybind_audit.py audit $(ARGS)

release-prep: ## Batch notes into the next version: CHANGELOG.md and toml version (BUMP=patch|minor|major to override)
	$(PY) $(PIPE)/release_notes.py prep
	$(CHANGIE) batch $$(if [ "$(BUMP)" = auto ]; then $(PY) $(PIPE)/release_notes.py level; else echo "$(BUMP)"; fi) \
		--header-path header.md --footer-path footer.md
	$(CHANGIE) merge
	@echo "Version is now $$(grep -Po 'versionNumber = "\K[^"]+' $(TOML)) -- review, commit, then make release-check"

release-notes: ## Write the GitHub Release body for the current version to build/release-notes.md
	@mkdir -p build
	$(PY) $(PIPE)/release_notes.py github --version $$(grep -Po 'versionNumber = "\K[^"]+' $(TOML)) \
		--cliff $(GIT_CLIFF) --out build/release-notes.md

release-check: ## Verify version, CHANGELOG, tag, and working tree are release-ready
	@CHANGIE=$(CHANGIE) $(PY) $(PIPE)/changelog_lint.py
	@set -e; \
	v=$$(grep -Po 'versionNumber = "\K[^"]+' $(TOML)); \
	echo "toml version:  $$v"; \
	if grep -q "^## \[$$v\]" CHANGELOG.md; then \
		echo "CHANGELOG:     [$$v] section present"; \
	else \
		echo "CHANGELOG:     MISSING [$$v] section"; exit 1; \
	fi; \
	git fetch --tags --quiet 2>/dev/null || true; \
	if git rev-parse "v$$v" >/dev/null 2>&1; then \
		echo "tag v$$v:    ALREADY EXISTS - bump the version before tagging"; exit 1; \
	else \
		echo "tag v$$v:    available"; \
	fi; \
	if [ -n "$$(git status --porcelain)" ]; then \
		echo "working tree:  DIRTY - commit before tagging"; \
	else \
		echo "working tree:  clean"; \
	fi; \
	echo "release-check: OK (tag with: git tag v$$v && git push origin v$$v)"

clean: ## Remove tcli build output (build/)
	rm -rf build/
	@echo "removed build/ (dist/ kept - remove manually if desired)"
