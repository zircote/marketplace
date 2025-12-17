# copilot Plugin

GitHub Copilot coding agent onboarding tools for configuring repositories with `copilot-instructions.md` and setup workflows.

## Installation

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install copilot
```

## Purpose

This plugin bridges Claude Code and GitHub Copilot by:

1. Analyzing existing Claude Code configuration (CLAUDE.md, .claude/)
2. Generating Copilot-compatible configuration files
3. Ensuring both AI agents follow the same project standards
4. Setting up environment workflows for Copilot coding agent

## Contents

### Agent

- **copilot-onboard**: Analyzes repositories and creates Copilot configuration aligned with Claude Code settings

### Command

- `/copilot:onboard [repository-path]`: Run the onboarding process for a repository

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
claude /copilot:onboard

# Onboard specific path
claude /copilot:onboard /path/to/repository
```

## Example Output

After running `/copilot:onboard` on a Python project:

```
.github/
├── copilot-instructions.md          # Main instructions
├── workflows/
│   └── copilot-setup-steps.yml      # Environment setup
└── instructions/
    ├── python.instructions.md        # Python-specific
    └── tests.instructions.md         # Test-specific
```

## Python Projects

For Python projects, the generated workflow uses:
- `astral-sh/setup-uv@v4` for uv package manager
- `uv sync --all-extras --dev` for dependencies
- `uv run ruff check .` and `uv run pytest` for quality gates

## TypeScript/Node Projects

For Node.js projects, the generated workflow uses:
- Node.js setup with specified version
- `npm ci` or `pnpm install` for dependencies
- `npm run lint` and `npm test` for quality gates

## Cross-Reference with CLAUDE.md

The onboard agent:
- Reads existing CLAUDE.md if present
- Extracts relevant configuration without duplication
- References shared docs rather than copying content
- Adds notes that Copilot also reads CLAUDE.md

## Best Practices

1. **Run after initial project setup**: Onboard once your CLAUDE.md and project structure are established
2. **Keep configs in sync**: When updating CLAUDE.md, re-run onboarding to update Copilot config
3. **Review generated files**: The agent creates sensible defaults but may need project-specific adjustments

## Integration with Other Plugins

- **git plugin**: Commit generated files with `/git:cm`
- **z plugin**: Use `technical-writer` to review generated documentation

## Version

**Plugin:** 1.0.0
