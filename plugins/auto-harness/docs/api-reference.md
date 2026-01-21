---
title: API Reference
description: Complete runner command reference for hook-driven test execution
---

# API Reference

## Runner Commands

The test runner (`runner.sh`) provides the following commands for managing hook-driven test execution.

### init

Initialize or resume a test run.

```bash
./tests/functional/runner.sh init [--category X] [--tag Y] [--reset]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--category X` | Filter tests by category name |
| `--tag Y` | Filter tests by tag |
| `--reset` | Force restart, ignoring existing state |

**Behavior:**
- If a test run is already in progress, displays resume prompt
- Loads tests from `tests.yaml` or `tests.json`
- Applies category and tag filters if specified
- Creates `test-state.json` with initial state

**Exit Codes:**
- `0` - Initialization successful
- `1` - No tests match filters

---

### next

Get the next test action to execute.

```bash
./tests/functional/runner.sh next
```

**Output:**
- Test number and ID
- Category and description
- Action instructions for Claude to execute

**Behavior:**
- Returns current test details without advancing
- Substitutes any `${variable}` references with captured values
- Returns completion message when all tests done

---

### validate

Validate Claude's response against test expectations.

```bash
./tests/functional/runner.sh validate "response text"
```

**Parameters:**

| Parameter | Description |
|-----------|-------------|
| `response` | The text response to validate against expectations |

**Validation Rules:**
- `contains` - Response must include the literal string
- `not_contains` - Response must NOT include the literal string
- `regex` - Response must match the regular expression pattern

**Behavior:**
- Evaluates all expectations for current test
- Records pass/fail result with timestamp
- Advances to next test
- Captures variables if `save_as` defined with regex groups

---

### skip

Skip the current test without validating.

```bash
./tests/functional/runner.sh skip
```

**Behavior:**
- Records test as skipped
- Advances to next test
- Does not affect pass/fail statistics

---

### status

Display current test run progress.

```bash
./tests/functional/runner.sh status
```

**Output:**
- Current mode (running/completed/aborted)
- Progress indicator (current/total)
- Result counts (passed/failed/skipped)
- Active filters if any

---

### report

Generate a test execution report.

```bash
./tests/functional/runner.sh report [--format md|json]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--format md` | Markdown format (default) |
| `--format json` | JSON format for programmatic use |

**Markdown Output:**
- Summary table with counts and percentages
- Failed tests section with failure details
- Collapsible passed tests list
- Skipped tests list

**JSON Output:**
```json
{
  "generated_at": "ISO-8601 timestamp",
  "summary": {
    "total": 15,
    "passed": 14,
    "failed": 1,
    "skipped": 0,
    "pass_rate": 0.933
  },
  "results": [...],
  "filters": {...}
}
```

---

### vars

Display captured variables from test execution.

```bash
./tests/functional/runner.sh vars
```

**Behavior:**
- Shows all variables captured via `save_as` directives
- Variables can be referenced in subsequent tests as `${variable_name}`

---

### abort

Stop the current test run.

```bash
./tests/functional/runner.sh abort
```

**Behavior:**
- Sets mode to "aborted"
- Preserves all recorded results
- Allows generating partial report

---

### reset

Clear all test state and results.

```bash
./tests/functional/runner.sh reset
```

**Behavior:**
- Removes `test-state.json`
- Clears all results and captured variables
- Next `init` starts fresh

---

## Test Definition Format

Tests are defined in YAML or JSON format.

### Test Structure

```yaml
- id: unique_test_identifier
  description: Human-readable test description
  category: smoke|integration|e2e
  action: |
    Run: <command to execute>
    Report the results.
  expect:
    - contains: "expected string"
    - not_contains: "error string"
    - regex: "pattern.*match"
  tags: [tag1, tag2]
  save_as: variable_name  # optional
```

### Expectation Types

| Type | Description | Example |
|------|-------------|---------|
| `contains` | Literal substring match | `contains: "success"` |
| `not_contains` | Literal substring absence | `not_contains: "error"` |
| `regex` | Regular expression match | `regex: "v[0-9]+\\.[0-9]+"` |

### Variable Capture

Use `save_as` with a regex containing capture groups:

```yaml
- id: capture_version
  action: Run: cat package.json | grep version
  expect:
    - regex: '"version":\\s*"([^"]+)"'
  save_as: pkg_version

- id: use_version
  action: Verify version ${pkg_version} is valid
  expect:
    - contains: "${pkg_version}"
```

---

## State File Format

The `test-state.json` file tracks execution state:

```json
{
  "mode": "running|completed|aborted",
  "total_tests": 15,
  "current_index": 5,
  "current_test": {...},
  "filtered_tests": ["test_id_1", "test_id_2"],
  "results": [
    {
      "id": "test_id",
      "status": "pass|fail|skip",
      "failures": [],
      "timestamp": "ISO-8601"
    }
  ],
  "saved_vars": {"var_name": "value"},
  "filter_category": null,
  "filter_tag": null,
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601"
}
```

---

## Hook Integration

The framework integrates with Claude Code via `UserPromptSubmit` hooks.

### hooks.json

```json
{
  "hooks": [
    {
      "name": "test-wrapper",
      "event": "UserPromptSubmit",
      "command": "${CLAUDE_PLUGIN_ROOT}/tests/functional/test-wrapper.sh"
    }
  ]
}
```

### test-wrapper.sh

The wrapper script intercepts user prompts during test runs:
- Reads `$CLAUDE_USER_PROMPT` environment variable
- Passes prompt through runner for validation
- Returns modified prompt or original based on test state
