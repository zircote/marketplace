---
name: Hook Architecture
description: This skill should be used when the user asks about "how hooks work", "UserPromptSubmit", "hook-driven testing", "test wrapper", "prompt interception", "hook JSON format", "state management", or needs to understand the architecture of hook-driven automated testing.
version: 1.0.0
---

# Hook-Driven Test Architecture

Understand the hook system that powers automated testing in Claude Code.

## Architecture Overview

The hook-driven test framework transforms Claude Code's conversational interface into an automated test harness by intercepting user prompts and replacing them with test instructions.

```
┌─────────────────────────────────────────────────────┐
│                 Claude Code Session                  │
├─────────────────────────────────────────────────────┤
│  User: "next"                                       │
│       │                                             │
│       ▼                                             │
│  ┌─────────────────────────────────────────────┐   │
│  │         UserPromptSubmit Hook                │   │
│  │         (test-wrapper.sh)                    │   │
│  │                                              │   │
│  │  1. Check test mode active                   │   │
│  │  2. Intercept command                        │   │
│  │  3. Call runner.sh                           │   │
│  │  4. Return {"replace": "new prompt"}         │   │
│  └─────────────────────────────────────────────┘   │
│       │                                             │
│       ▼                                             │
│  Claude sees: "Execute test: Call tool X..."        │
│       │                                             │
│       ▼                                             │
│  Claude executes the MCP tool call                  │
└─────────────────────────────────────────────────────┘
```

## Core Components

### 1. UserPromptSubmit Hook

The hook intercepts every user prompt and can:
- **Pass through**: Return unchanged for normal operation
- **Replace**: Substitute with test instruction
- **Block**: Prevent prompt from reaching Claude

Hook registration in `hooks/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/test-wrapper.sh user-prompt-submit"
          }
        ]
      }
    ]
  }
}
```

### 2. Test Wrapper Script

The wrapper (`hooks/test-wrapper.sh`) handles prompt interception:

```bash
#!/usr/bin/env bash

handle_user_prompt_submit() {
  local input=$(cat)
  local prompt=$(echo "$input" | python3 -c "
import json, sys
print(json.load(sys.stdin).get('prompt', ''))
")

  # Check if test mode active
  if is_test_mode; then
    case "$prompt" in
      next|n)
        output=$("$RUNNER" next)
        json_replace "Execute the following test:\n\n$output"
        ;;
      validate*)
        response="${prompt#validate }"
        output=$("$RUNNER" validate "$response")
        json_replace "$output"
        ;;
      # ... other commands
    esac
  else
    # Pass through to normal processing
    echo "$input"
  fi
}
```

### 3. Runner Script

The runner (`tests/functional/runner.sh`) orchestrates test execution:

**Key functions:**
- `cmd_init` - Initialize test state
- `cmd_next` - Return next test action
- `cmd_validate` - Check response against expectations
- `cmd_status` - Report progress
- `cmd_report` - Generate results

### 4. State Management

Persistent state in `.claude/test-state.json`:

```json
{
  "mode": "running",
  "total_tests": 53,
  "current_index": 5,
  "current_test": {
    "id": "test_id",
    "action": "...",
    "expect": [...]
  },
  "results": [
    {"id": "test1", "status": "pass"},
    {"id": "test2", "status": "fail", "failures": ["..."]}
  ],
  "saved_vars": {
    "memory_id": "abc123"
  }
}
```

## Hook Input/Output Format

### Input (JSON via stdin)

```json
{
  "session_id": "abc123",
  "prompt": "user's typed command",
  "cwd": "/project/path"
}
```

### Output (JSON to stdout)

**Replace prompt:**
```json
{
  "replace": "New prompt text for Claude"
}
```

**Pass through:**
```json
{}
```

**Block prompt:**
```json
{
  "continue": false,
  "systemMessage": "Explanation"
}
```

## Critical Implementation Details

### JSON Escaping

Hook output must be valid JSON. Use Python for reliable escaping:

```bash
json_replace() {
  local content="$1"
  python3 -c "
import json, sys
content = sys.stdin.read()
print(json.dumps({'replace': content}))
" <<< "$content"
}
```

**Common pitfall:** Bash string escaping breaks on newlines and special characters.

### State Persistence

Each hook invocation is stateless. State must persist to disk:

```bash
update_state() {
  local field="$1"
  local value="$2"
  python3 -c "
import json
with open('$STATE_FILE', 'r+') as f:
    data = json.load(f)
    data['$field'] = $value
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
"
}
```

### Test Mode Detection

Check state file to determine if tests are running:

```bash
is_test_mode() {
  [[ -f "$STATE_FILE" ]] || return 1
  local mode=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    print(json.load(f).get('mode', ''))
")
  [[ "$mode" == "running" ]]
}
```

## Test Execution Flow

```
1. User: /run-tests
   └─> Initializes state, sets mode=running

2. User: "next"
   └─> Hook intercepts
   └─> Runner returns test action
   └─> Hook replaces prompt with action
   └─> Claude executes test

3. User: "validate <response>"
   └─> Hook intercepts
   └─> Runner validates against expectations
   └─> Records PASS/FAIL
   └─> Advances to next test

4. Repeat steps 2-3 until all tests complete

5. User: "report"
   └─> Runner generates summary
```

## Extension Points

### Adding New Commands

Extend the wrapper to handle new commands:

```bash
case "$prompt" in
  retry)
    # Re-run current test
    output=$("$RUNNER" retry)
    json_replace "$output"
    ;;
esac
```

### Custom Validation

Add validation types in runner:

```python
if 'json_path' in exp:
    # JSONPath validation
    import jsonpath_ng
    matches = jsonpath_ng.parse(exp['json_path']).find(response)
    if not matches:
        failures.append(f"JSONPath not found: {exp['json_path']}")
```

### Pre/Post Test Hooks

Add lifecycle hooks in runner:

```bash
run_pre_test_hook() {
  if [[ -x "$HOOKS_DIR/pre-test.sh" ]]; then
    "$HOOKS_DIR/pre-test.sh" "$current_test_id"
  fi
}
```

## Additional Resources

### Reference Files

- **`references/state-management.md`** - Test state file schema and management
