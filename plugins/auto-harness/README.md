# auto-harness

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/zircote/auto-harness/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-purple.svg)](https://docs.anthropic.com/en/docs/claude-code)

<p align="center">
  <img src=".github/readme-infographic.svg" alt="auto-harness workflow" width="800">
</p>

A Claude Code plugin that automates integration of hook-driven test framework patterns into any project. The plugin scaffolds complete test infrastructure directly into target projects, enabling automated testing of Claude Code plugins, MCP tools, commands, skills, and hooks.

## Overview

auto-harness is a **generator/scaffolding plugin** - it doesn't provide test commands itself, but rather generates test infrastructure INTO your project's `.claude/` directory. This keeps test configuration project-scoped and portable.

### What Gets Generated

When you run `/harness:init`, the plugin creates:

```
your-project/
├── .claude/
│   ├── commands/
│   │   ├── run-tests.md      # /run-tests command
│   │   ├── add-test.md       # /add-test command
│   │   └── test-report.md    # /test-report command
│   ├── hooks/
│   │   ├── hooks.json        # UserPromptSubmit hook config
│   │   └── test-wrapper.sh   # Hook script for test mode
│   └── test-state.json       # Runtime state (gitignored)
└── tests/
    └── functional/
        ├── runner.sh         # Core test orchestration
        ├── tests.yaml        # Test definitions (or .json)
        └── reports/          # Generated reports
```

## Installation

Add to your Claude Code plugins:

```bash
# Via marketplace (when published)
claude plugins add auto-harness

# Or local development
claude --plugin-dir /path/to/auto-harness
```

## Quick Start

1. **Initialize test infrastructure in your project:**
   ```
   /harness:init
   ```

   The setup wizard will guide you through:
   - Project type detection
   - Test format selection (YAML or JSON)
   - Initial test generation
   - Configuration verification

2. **Start a test run:**
   ```
   /run-tests
   ```

   This enters **test mode** where special commands become active.

3. **Execute tests interactively:**
   - Type `next` or `n` to get the next test
   - Claude executes the test action
   - Type `validate <response>` or `v <response>` to check results
   - Repeat until all tests complete

4. **Generate a report:**
   ```
   report
   ```

## Commands

### Plugin Commands

| Command | Description |
|---------|-------------|
| `/harness:init` | Initialize test infrastructure in current project |
| `/harness:validate` | Validate existing test setup |

### Generated Project Commands

After initialization, your project gets these commands:

| Command | Description |
|---------|-------------|
| `/run-tests` | Start test execution mode |
| `/add-test` | Add a new test interactively |
| `/test-report` | Generate test report |

### Test Mode Commands

When test mode is active, these prompts are intercepted:

| Command | Shortcut | Description |
|---------|----------|-------------|
| `next` | `n` | Get next test to execute |
| `skip` | `s` | Skip current test |
| `validate <response>` | `v <response>` | Validate Claude's response |
| `status` | - | Show test progress |
| `report` | - | Generate report |
| `vars` | - | Show captured variables |
| `abort` | `a` | Stop test run |
| `help` | `?` | Show available commands |

## Test Definition Format

### YAML Format

```yaml
---
version: "1.0"
description: "My Project Test Suite"

tests:
  - id: smoke_basic
    description: Basic smoke test
    category: smoke
    action: >
      Confirm the test framework is operational by responding
      with 'Test framework operational'
    expect:
      - contains: "operational"
      - not_contains: "error"
    tags: [smoke, critical]

  - id: mcp_tool_test
    description: Test MCP tool functionality
    category: mcp-tools
    action: "Call mcp__server__tool_name with param: 'test'"
    expect:
      - contains: "success"
      - regex: "result:\\s+(.+)"
    save_as: tool_result
    tags: [mcp, integration]

  - id: dependent_test
    description: Test that uses captured variable
    category: integration
    action: "Process the result: ${tool_result}"
    depends_on: mcp_tool_test
    expect:
      - contains: "processed"
    tags: [integration]
```

### JSON Format (Recommended)

JSON format is recommended as it requires no external dependencies (YAML requires PyYAML which may not be available on all systems).

```json
{
  "version": "1.0",
  "description": "My Project Test Suite",
  "tests": [
    {
      "id": "smoke_basic",
      "description": "Basic smoke test",
      "category": "smoke",
      "action": "Confirm the test framework is operational",
      "expect": [
        { "contains": "operational" },
        { "not_contains": "error" }
      ],
      "tags": ["smoke", "critical"]
    }
  ]
}
```

### Test Schema

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique test identifier |
| `description` | Yes | Human-readable explanation |
| `action` | Yes | Instruction for Claude to execute |
| `expect` | Yes | Array of validation rules |
| `category` | No | Grouping for filtering |
| `tags` | No | Labels for filtering |
| `save_as` | No | Variable name for captured value |
| `depends_on` | No | ID of prerequisite test |

### Expectation Types

| Type | Example | Description |
|------|---------|-------------|
| `contains` | `{"contains": "success"}` | Response must include text |
| `not_contains` | `{"not_contains": "error"}` | Response must not include text |
| `regex` | `{"regex": "ID:\\s+([a-f0-9]+)"}` | Pattern match (capture groups for `save_as`) |

## Architecture

### Hook-Driven Testing

The framework uses Claude Code's `UserPromptSubmit` hook to intercept prompts when test mode is active. This enables:

- **Transparent operation**: Normal prompts pass through unchanged
- **Command interception**: Test commands route to the runner
- **State management**: Test progress persists in `.claude/test-state.json`

### Test Flow

```
User types "next"
     ↓
UserPromptSubmit hook intercepts
     ↓
test-wrapper.sh checks test mode
     ↓
runner.sh returns next test
     ↓
Claude executes test action
     ↓
User types "validate <response>"
     ↓
runner.sh validates expectations
     ↓
Results recorded, proceed to next
```

## Report Formats

Generate reports in multiple formats:

```bash
# Markdown (default)
report

# JSON
report json

# HTML
report html
```

Reports include:
- Test summary (passed/failed/skipped)
- Individual test results with timing
- Captured variables
- Failure details with expected vs actual

## Advanced Usage

### Variable Capture and Substitution

Capture values from test responses and use them in subsequent tests:

```yaml
- id: create_entity
  action: "Create a new user"
  expect:
    - regex: "User ID:\\s+([a-f0-9-]+)"
  save_as: user_id

- id: get_entity
  action: "Get user ${user_id}"
  depends_on: create_entity
  expect:
    - contains: "found"
```

### Filtering Tests

Run specific tests by category or tag:

```bash
# In test mode
/run-tests --category smoke
/run-tests --tag critical
/run-tests --filter "mcp_*"
```

### CI/CD Integration

For automated runs, use the runner directly:

```bash
# Initialize and run all tests
./tests/functional/runner.sh init tests/functional/tests.yaml
./tests/functional/runner.sh run-all

# Get exit code for CI
echo $?  # 0 = all passed, 1 = failures
```

## Troubleshooting

### Test mode not activating

1. Check hook installation: `ls -la .claude/hooks/`
2. Verify hooks.json format
3. Restart Claude Code to reload hooks

### Variables not substituting

1. Ensure `save_as` test passed
2. Check regex has capture group: `([...])`
3. Use `vars` command to inspect captured values

### Validation always failing

1. Check response is passed correctly to validate
2. Try simpler expectation first (just `contains`)
3. For regex, escape special characters

## Development

### Project Structure

```
auto-harness/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/
│   ├── init.md              # /harness:init
│   └── validate.md          # /harness:validate
├── agents/
│   ├── test-generator.md    # Proactive test generation
│   └── setup-validator.md   # Configuration validation
├── skills/
│   ├── test-authoring/      # Test writing guidance
│   ├── hook-architecture/   # Hook system understanding
│   └── validation-strategies/  # Validation approaches
└── templates/               # Generated file templates
    ├── commands/
    ├── hooks/
    ├── runner/
    └── tests/
```

### Meta-Testing

The auto-harness plugin uses its own test framework to test itself. This validates that the framework works correctly.

**Running meta-tests:**

```bash
# Initialize meta-test run
/run-tests --category smoke

# Or run directly
./tests/functional/runner.sh init --category smoke
./tests/functional/runner.sh next
./tests/functional/runner.sh validate "Test framework operational"
./tests/functional/runner.sh report
```

**Meta-test categories:**
- `smoke` - Basic framework verification
- `commands` - Plugin command tests
- `skills` - Skill triggering tests
- `agents` - Agent invocation tests
- `templates` - Template file validation
- `integration` - Full plugin structure tests

### Contributing

1. Fork the repository
2. Create a feature branch
3. Run meta-tests: `/run-tests` to verify framework integrity
4. Test with `/harness:validate` on the plugin itself
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
