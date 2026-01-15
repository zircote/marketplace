---
# ADR Plugin Configuration

# ADR directories
adr_paths:
  - docs/adr/

# Default template format - using structured-madr with frontmatter and audit sections
default_format: structured-madr

# Numbering configuration
numbering:
  pattern: "4digit"
  start_from: 1

# Status workflow configuration
statuses:
  workflow:
    - proposed
    - accepted
    - deprecated
    - superseded
  allow_rejected: true

# ADR linking
linking:
  auto_update_superseded: true
  require_supersedes_reason: true

# Index (README.md) configuration
index:
  auto_generate: true
  include_summary: true
  include_status_badge: true

# Git integration
git:
  enabled: true
  auto_commit: false
  commit_template: "docs(adr): {action} ADR-{id} {title}"

# Compliance checking
compliance:
  enabled: true
  check_all_accepted: true
  file_patterns:
    - "**/*.ts"
    - "**/*.js"
    - "**/*.py"
    - "**/*.go"
    - "**/*.md"
  ignore_patterns:
    - "**/node_modules/**"
    - "**/vendor/**"
    - "**/.git/**"
    - "**/dist/**"
    - "**/build/**"

# Export settings
export:
  default_format: html
  include_toc: true
  include_status_badges: true

# Research settings
research:
  include_codebase: true
  include_web: true
  max_web_results: 5
---

# Marketplace ADR Context

This project uses the Structured MADR format for comprehensive architectural decision documentation with YAML frontmatter and audit sections.

## Architecture Principles

- Plugin-based architecture for modularity
- Consistent patterns across all plugins
- Documentation as code

## Decision Making Process

- ADRs capture significant architectural decisions
- All accepted ADRs require compliance audits
- Structured MADR format ensures comprehensive documentation

## Areas of Focus

- Plugin development patterns
- Agent and skill design
- Cross-plugin consistency
