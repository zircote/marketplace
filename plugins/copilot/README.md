# copilot Plugin

GitHub Copilot coding agent onboarding tools for configuring repositories with `copilot-instructions.md` and setup workflows.

## Installation

```bash
claude /plugin install ./plugins/copilot
```

## Purpose

This plugin helps bridge Claude Code and GitHub Copilot by:

1. Analyzing existing Claude Code configuration (CLAUDE.md, .claude/)
2. Generating Copilot-compatible configuration files
3. Ensuring both AI agents follow the same project standards
4. Setting up environment workflows for Copilot coding agent

## Contents

### Agents

- **copilot-onboard**: Analyzes repositories and creates Copilot configuration aligned with Claude Code settings

### Commands

- `/onboard [repository-path]`: Run the onboarding process for a repository

## Generated Files

The onboard agent creates:

### `.github/copilot-instructions.md`
Repository-wide instructions including:
- Project summary and tech stack
- Dependency installation commands
- Test and lint commands
- Code style requirements
- Architectural patterns

### `.github/workflows/copilot-setup-steps.yml`
Environment setup workflow with:
- Language runtime installation
- Package manager setup (uv, npm, cargo, etc.)
- Dependency installation
- Tool verification

### `.github/instructions/*.instructions.md`
Scoped instructions for specific file patterns:
- `python.instructions.md` for `**/*.py`
- `tests.instructions.md` for test files
- `frontend.instructions.md` for React/TypeScript

## Usage

```bash
# Onboard current repository
claude /onboard

# Onboard specific path
claude /onboard /path/to/repository
```

## Python Projects

For Python projects, the generated workflow uses:
- `astral-sh/setup-uv@v4` for uv package manager
- `uv sync --all-extras --dev` for dependencies
- `uv run ruff check .` and `uv run pytest` for quality gates

## Cross-Reference

The onboard agent:
- Reads existing CLAUDE.md if present
- Extracts relevant configuration without duplication
- References shared docs rather than copying content
- Adds notes that Copilot also reads CLAUDE.md
