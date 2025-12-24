# Zircote Claude Marketplace Makefile
#
# Provides targets for version management and plugin operations.

.PHONY: help version bump-changed bump-all release release-minor release-major
.PHONY: bump-zircote bump-gh bump-nsip bump-datadog bump-document-skills
.PHONY: validate validate-json validate-fields validate-version validate-readme
.PHONY: validate-commands validate-agents validate-skills
.PHONY: ci quality lint demos demo-clean

PYTHON := python3
SCRIPTS := scripts

# ============================================================================
# Help
# ============================================================================

help:  ## Show this help message
	@echo "Zircote Claude Marketplace"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Version Management:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E 'bump|release|version' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'
	@echo ""
	@echo "Per-Plugin Bumps:"
	@grep -E '^bump-[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'
	@echo ""
	@echo "Other:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -vE 'bump|release|version' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'

# ============================================================================
# Version Management
# ============================================================================

version:  ## Show current versions of all plugins
	@echo "Plugin Versions:"
	@echo ""
	@for plugin in zircote gh nsip datadog document-skills; do \
		version=$$(grep -o '"version": "[^"]*"' plugins/$$plugin/.claude-plugin/plugin.json | cut -d'"' -f4); \
		printf "  %-20s v%s\n" "$$plugin" "$$version"; \
	done

bump-changed:  ## Bump patch version for plugins with changes since last release
	$(PYTHON) $(SCRIPTS)/smart-bump.py patch

bump-changed-minor:  ## Bump minor version for plugins with changes
	$(PYTHON) $(SCRIPTS)/smart-bump.py minor

bump-all:  ## Bump patch version for ALL plugins
	$(PYTHON) $(SCRIPTS)/smart-bump.py --all patch

bump-dry:  ## Preview what would be bumped (dry run)
	$(PYTHON) $(SCRIPTS)/smart-bump.py --dry-run patch

release:  ## Bump changed plugins (patch) and push tags
	$(PYTHON) $(SCRIPTS)/smart-bump.py patch
	git push --follow-tags

release-patch: release  ## Alias for 'release' (bump patch and push tags)

release-minor:  ## Bump changed plugins (minor) and push tags
	$(PYTHON) $(SCRIPTS)/smart-bump.py minor
	git push --follow-tags

release-major:  ## Bump changed plugins (major) and push tags
	$(PYTHON) $(SCRIPTS)/smart-bump.py major
	git push --follow-tags

# ============================================================================
# Per-Plugin Bumps
# ============================================================================

bump-zircote:  ## Bump zircote plugin patch version
	cd plugins/zircote && bump-my-version bump patch

bump-zircote-minor:  ## Bump zircote plugin minor version
	cd plugins/zircote && bump-my-version bump minor

bump-gh:  ## Bump gh plugin patch version
	cd plugins/gh && bump-my-version bump patch

bump-gh-minor:  ## Bump gh plugin minor version
	cd plugins/gh && bump-my-version bump minor

bump-nsip:  ## Bump nsip plugin patch version
	cd plugins/nsip && bump-my-version bump patch

bump-nsip-minor:  ## Bump nsip plugin minor version
	cd plugins/nsip && bump-my-version bump minor

bump-datadog:  ## Bump datadog plugin patch version
	cd plugins/datadog && bump-my-version bump patch

bump-datadog-minor:  ## Bump datadog plugin minor version
	cd plugins/datadog && bump-my-version bump minor

bump-document-skills:  ## Bump document-skills plugin patch version
	cd plugins/document-skills && bump-my-version bump patch

bump-document-skills-minor:  ## Bump document-skills plugin minor version
	cd plugins/document-skills && bump-my-version bump minor

# ============================================================================
# CI & Quality (matches .github/workflows/ci.yml)
# ============================================================================

ci: validate  ## Run all CI checks (same as GitHub Actions)

quality: ci  ## Alias for ci

lint: validate-readme  ## Run linting checks

# ============================================================================
# Validation
# ============================================================================

validate:  ## Run all plugin validations
	@$(PYTHON) $(SCRIPTS)/validate.py

validate-json:  ## Validate JSON syntax only
	@$(PYTHON) $(SCRIPTS)/validate.py --check json

validate-fields:  ## Check required fields only
	@$(PYTHON) $(SCRIPTS)/validate.py --check fields

validate-version:  ## Validate semantic versions only
	@$(PYTHON) $(SCRIPTS)/validate.py --check version

validate-readme:  ## Check README files exist
	@$(PYTHON) $(SCRIPTS)/validate.py --check readme

validate-commands:  ## Validate command file references
	@$(PYTHON) $(SCRIPTS)/validate.py --check commands

validate-agents:  ## Validate agent file references
	@$(PYTHON) $(SCRIPTS)/validate.py --check agents

validate-skills:  ## Validate skill file references
	@$(PYTHON) $(SCRIPTS)/validate.py --check skills

# ============================================================================
# Demo Generation
# ============================================================================

demos:  ## Generate all demo GIFs using vhs
	@echo "Generating demo GIFs..."
	@which vhs > /dev/null || { echo "Error: vhs not installed. Run: brew install vhs"; exit 1; }
	@cd demos && for tape in *.tape; do \
		echo "  Generating $$tape..."; \
		vhs "$$tape" || echo "  Warning: $$tape failed"; \
	done
	@echo "Done. GIFs saved to demos/"

demo-clean:  ## Remove generated demo GIFs
	@rm -f demos/*.gif
	@echo "Removed demo GIFs"
