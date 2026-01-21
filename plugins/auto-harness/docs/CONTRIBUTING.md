---
title: Contributing Guide
description: Development setup, code style, and contribution guidelines for auto-harness
---

# Contributing Guide

## Development Setup

### Prerequisites

- Bash 4.0+
- Python 3.8+ (for JSON/YAML processing)
- PyYAML (`pip install pyyaml`) for YAML test files
- Claude Code CLI installed

### Clone and Install

```bash
git clone <repository-url>
cd auto-harness

# Verify plugin structure
ls -la plugin.json
ls -la commands/
```

### Running Meta-Tests

auto-harness tests itself using its own framework:

```bash
# Initialize test run
./tests/functional/runner.sh init

# Execute tests
./tests/functional/runner.sh next
# ... execute the displayed action ...
./tests/functional/runner.sh validate "your response"

# Continue until complete
./tests/functional/runner.sh report
```

Or use the `/run-tests` command within Claude Code.

## Project Structure

```
auto-harness/
├── .claude/
│   ├── commands/           # Local command overrides (optional)
│   ├── hooks/              # Hook configurations
│   └── test-state.json     # Runtime state (gitignored)
├── commands/               # Slash commands (plugin root)
│   ├── init.md
│   └── validate.md
├── agents/                 # Agent definitions
│   ├── test-generator.md
│   └── setup-validator.md
├── skills/                 # Skill definitions
│   ├── test-authoring/
│   ├── hook-architecture/
│   └── validation-strategies/
├── templates/
│   ├── runner/
│   │   └── runner.sh       # Runner template
│   ├── hooks/
│   │   └── hooks.json      # Hook template
│   ├── tests/
│   │   └── tests.yaml      # Test template
│   └── wrapper/
│       └── test-wrapper.sh # Wrapper template
├── tests/
│   └── functional/
│       ├── runner.sh       # Active runner
│       ├── tests.yaml      # Meta-tests
│       ├── tests.json      # JSON version
│       └── reports/        # Generated reports
├── docs/
│   ├── api-reference.md
│   ├── architecture.md
│   └── CONTRIBUTING.md
└── plugin.json             # Plugin manifest
```

## Making Changes

### Adding a New Command

1. Create command file in `commands/`:

```markdown
---
name: my-command
description: Brief description
---

Command instructions for Claude...
```

2. Update plugin.json if needed
3. Add tests for the command

### Modifying the Runner

1. Edit `tests/functional/runner.sh`
2. Run meta-tests to verify changes
3. If changes are generic, sync to template:
   - Copy to `templates/runner/runner.sh`
   - Restore `{{TEST_FORMAT}}` placeholder on line 22
4. Verify template with: `diff tests/functional/runner.sh templates/runner/runner.sh`

### Adding Tests

Add new tests to `tests/functional/tests.yaml`:

```yaml
- id: my_new_test
  description: What this test verifies
  category: smoke|runner|templates|structure|meta
  action: |
    Run: <concrete command>
    Report the results.
  expect:
    - contains: "expected output"
    - not_contains: "error"
  tags: [relevant, tags]
```

### Test Categories

| Category | Purpose |
|----------|---------|
| `smoke` | Basic functionality checks |
| `runner` | Runner command tests |
| `templates` | Template file validation |
| `structure` | Plugin structure verification |
| `meta` | Self-testing framework tests |

## Code Style

### Bash

- Use `set -euo pipefail` for strict mode
- Quote all variables: `"$VAR"` not `$VAR`
- Use functions for reusable logic
- Prefer `[[` over `[` for conditionals

### Python (embedded)

- Use for JSON/YAML processing
- Keep inline scripts focused
- Handle errors gracefully
- Use stdin pipes instead of heredocs for complex JSON

### Markdown

- Use ATX headers (`#` style)
- Include code fence language identifiers
- Keep lines under 100 characters
- Use reference links for repeated URLs

## Testing Guidelines

### Write Concrete Actions

Tests should specify exact commands:

```yaml
# Good
action: |
  Run: grep -c "function" src/utils.js
  Report the count of functions found.

# Avoid
action: Check how many functions exist
```

### Use Appropriate Expectations

```yaml
# Exact match when output is predictable
expect:
  - contains: "SUCCESS"

# Regex when format varies
expect:
  - regex: "version=[0-9]+\\.[0-9]+"

# Negative check for errors
expect:
  - not_contains: "ERROR"
  - not_contains: "No such file"
```

### Tag Tests Appropriately

```yaml
tags: [smoke, critical]      # Essential functionality
tags: [runner, init]         # Specific feature
tags: [templates, hooks]     # Component category
```

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Follow code style guidelines
   - Add/update tests as needed
   - Update documentation

3. **Run Meta-Tests**
   ```bash
   ./tests/functional/runner.sh init --reset
   # Complete all tests
   ./tests/functional/runner.sh report
   ```

4. **Commit with Clear Message**
   ```bash
   git commit -m "Add feature: description of changes"
   ```

5. **Push and Create PR**
   - Describe what changed and why
   - Reference any related issues
   - Include test results summary

## Release Process

1. Update version in `.claude-plugin/plugin.json`
2. Run full test suite
3. Update CHANGELOG if maintained
4. Tag release: `git tag v1.x.x`
5. Push tags: `git push --tags`

## Getting Help

- Review existing tests for examples
- Check architecture.md for design context
- Open an issue for questions or bugs
