---
title: Architecture Guide
description: Hook-driven testing architecture and design principles for auto-harness
---

# Architecture Guide

## Overview

auto-harness implements a hook-driven testing architecture that enables automated functional testing of Claude Code plugins. The framework intercepts Claude's interactions through `UserPromptSubmit` hooks, allowing tests to be executed as part of normal Claude Code sessions.

## Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code Session                      │
├─────────────────────────────────────────────────────────────┤
│  User Prompt → [UserPromptSubmit Hook] → Claude Response    │
│                        ↓                                     │
│              ┌─────────────────┐                            │
│              │  test-wrapper.sh │                            │
│              └────────┬────────┘                            │
│                       ↓                                      │
│              ┌─────────────────┐                            │
│              │   runner.sh     │                            │
│              └────────┬────────┘                            │
│                       ↓                                      │
│              ┌─────────────────┐                            │
│              │ test-state.json │                            │
│              └─────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## Hook-Driven Testing Model

### Why Hooks?

Traditional test frameworks operate outside the AI context. Hook-driven testing allows:

1. **In-Context Execution** - Tests run within actual Claude sessions
2. **Real Behavior Validation** - Tests verify Claude's actual responses
3. **Conversational Flow** - Tests follow natural interaction patterns
4. **No External Orchestration** - Claude drives its own test execution

### Hook Event Flow

```
1. User types "next" (or test action)
         ↓
2. UserPromptSubmit hook triggers
         ↓
3. test-wrapper.sh receives prompt
         ↓
4. runner.sh processes command
         ↓
5. Returns test instructions OR validates response
         ↓
6. Claude receives modified/original prompt
         ↓
7. Claude executes action, reports result
         ↓
8. Cycle repeats with "validate" call
```

## State Management

### test-state.json

Central state file tracks all test execution data:

```
.claude/
└── test-state.json    # Persisted test state
```

**State Transitions:**

```
[No State] → init → [running] → validate → [running] → ... → [completed]
                        ↓                                         ↓
                      abort                                    report
                        ↓
                   [aborted]
```

### State Fields

| Field | Purpose |
|-------|---------|
| `mode` | Current execution state |
| `current_index` | Position in test sequence |
| `filtered_tests` | IDs of tests matching filters |
| `results` | Array of test outcomes |
| `saved_vars` | Captured variables for substitution |

## Test Execution Lifecycle

### 1. Initialization Phase

```bash
runner.sh init [--category X] [--tag Y]
```

- Loads test definitions from YAML/JSON
- Applies category and tag filters
- Creates initial state file
- Returns test count and first instructions

### 2. Execution Loop

```
┌──────────────────────────────────────┐
│            next                      │
│              ↓                       │
│     [Get current test]               │
│              ↓                       │
│     [Display action]                 │
│              ↓                       │
│     [Claude executes]                │
│              ↓                       │
│     validate "response"              │
│              ↓                       │
│     [Check expectations]             │
│              ↓                       │
│     [Record result]                  │
│              ↓                       │
│     [Advance index]                  │
│              ↓                       │
│     [More tests?] ─Yes─→ Loop        │
│         │                            │
│        No                            │
│         ↓                            │
│     [Complete]                       │
└──────────────────────────────────────┘
```

### 3. Validation Phase

Each test validation evaluates expectations:

```python
for expectation in test.expect:
    if 'contains' in expectation:
        # Literal substring match
        assert expectation['contains'] in response

    if 'not_contains' in expectation:
        # Ensure absence
        assert expectation['not_contains'] not in response

    if 'regex' in expectation:
        # Pattern match with optional capture
        match = re.search(expectation['regex'], response)
        assert match is not None
        if match.groups() and test.save_as:
            captured[test.save_as] = match.group(1)
```

### 4. Completion Phase

```bash
runner.sh report [--format md|json]
```

- Generates summary statistics
- Lists failures with details
- Outputs collapsible passed tests
- Produces machine-readable JSON option

## Plugin Integration

### Template System

auto-harness provides templates for initializing test frameworks in target plugins:

```
templates/
├── runner/
│   └── runner.sh        # Test runner script
├── hooks/
│   └── hooks.json       # Hook configuration
├── tests/
│   └── tests.yaml       # Test definition template
└── wrapper/
    └── test-wrapper.sh  # Hook wrapper script
```

### Initialization Command

The `/init` command copies and configures templates:

1. Creates `tests/functional/` directory
2. Copies runner.sh with format placeholder substitution
3. Configures hooks.json for target project
4. Generates starter tests.yaml

## Design Principles

### 1. Concrete Actions

Tests specify explicit commands Claude should execute:

```yaml
# Good - Concrete action
action: |
  Run: ls -la .claude/
  Report if the directory exists.

# Bad - Vague instruction
action: Check if configuration exists
```

### 2. Observable Expectations

Expectations verify observable outputs, not internal state:

```yaml
# Good - Observable output
expect:
  - contains: "success"
  - regex: "version=[0-9]+"

# Bad - Internal assumption
expect:
  - contains: "internal_flag_set"
```

### 3. Isolation

Each test should be independently executable:

- No implicit dependencies between tests
- Use `save_as` for explicit data passing
- Tests can be filtered and run individually

### 4. Non-Destructive

Tests should not modify production state:

- Use read-only checks where possible
- Clean up any created artifacts
- Avoid tests that require external resources

## Error Handling

### Runner Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| No tests found | Filter too restrictive | Adjust category/tag filters |
| Invalid JSON | Malformed test file | Validate tests.yaml syntax |
| Missing state | init not called | Run `runner.sh init` first |

### Validation Failures

Failures are recorded with specific reasons:

```json
{
  "id": "test_id",
  "status": "fail",
  "failures": [
    "Missing: 'expected string'",
    "Pattern not found: 'regex.*pattern'"
  ]
}
```

## Performance Considerations

### State File I/O

- State is read/written per command
- Python subprocess handles JSON parsing
- No persistent daemon required

### Filter Optimization

- Filters applied at init time
- Only matching tests loaded into state
- Reduces iteration overhead

### Report Generation

- Reports generated on-demand
- No continuous logging overhead
- JSON format enables post-processing
