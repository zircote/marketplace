---
description: Onboard a repository for GitHub Copilot coding agent with configuration aligned to Claude Code
argument-hint: "[repository-path]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

Analyze this repository and configure it for GitHub Copilot coding agent, ensuring alignment with any existing Claude Code configuration.

## Task

1. **Discover existing configuration**:
   - Check for: `CLAUDE.md`, `.claude/`, `AGENTS.md`, `.github/copilot-instructions.md`
   - Identify: package manager, test runner, linter, formatter
   - Review: `.github/workflows/` for CI patterns

2. **Generate Copilot configuration files**:

### `.github/copilot-instructions.md`
Repository-wide instructions including:
- Project summary and tech stack
- Dependency installation command
- Test command
- Lint/format commands
- Code style requirements
- Key architectural patterns

### `.github/workflows/copilot-setup-steps.yml`
Environment setup with job named `copilot-setup-steps`:
```yaml
name: Copilot Setup Steps
on:
  workflow_dispatch:
  push:
    paths: [.github/workflows/copilot-setup-steps.yml]
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Language runtime setup
      # Package manager setup  
      # Dependency installation
      # Tool verification
```

### `.github/instructions/*.instructions.md` (optional)
Scoped instructions with frontmatter:
```yaml
---
applyTo: "**/*.py"
---
```

3. **For Python projects with uv**, use:
   - `astral-sh/setup-uv@v4` action
   - `uv sync --all-extras --dev` for deps
   - `uv run ruff check .` and `uv run pytest` for quality

4. **Cross-reference with CLAUDE.md**: Don't duplicate—Copilot reads CLAUDE.md too. Add complementary info only.

5. **Output summary**: What was detected, files created, any manual steps needed.

$ARGUMENTS
