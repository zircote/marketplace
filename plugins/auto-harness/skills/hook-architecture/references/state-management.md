# State Management Reference

Detailed documentation on test state management in hook-driven testing.

## State File Structure

The test state is persisted in `.claude/test-state.json`:

```json
{
  "mode": "running",
  "test_file": "tests/functional/tests.yaml",
  "format": "yaml",
  "current_index": 3,
  "tests": [
    {
      "id": "smoke_basic",
      "status": "passed",
      "started_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:30:05Z",
      "duration_ms": 5000
    }
  ],
  "variables": {
    "entity_id": "abc123",
    "user_name": "test_user"
  },
  "summary": {
    "total": 10,
    "passed": 3,
    "failed": 0,
    "skipped": 0,
    "pending": 7
  },
  "started_at": "2024-01-15T10:30:00Z"
}
```

## State Fields

### Mode

| Value | Description |
|-------|-------------|
| `idle` | No test run active |
| `running` | Test run in progress |
| `paused` | Test run paused (future feature) |
| `completed` | Test run finished |

### Test Entry

Each test in the `tests` array contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Test identifier |
| `status` | enum | `pending`, `running`, `passed`, `failed`, `skipped` |
| `started_at` | ISO8601 | When test started |
| `completed_at` | ISO8601 | When test completed |
| `duration_ms` | number | Execution time |
| `error` | string | Failure reason (if failed) |
| `response` | string | Captured response (if saved) |

### Variables

Key-value store for captured values:

```json
"variables": {
  "user_id": "uuid-here",
  "api_key": "captured-key",
  "count": "42"
}
```

Variables are:
- Captured via regex with `save_as`
- Substituted in subsequent test actions using `${variable_name}`
- Persisted across test runs until reset

## State Transitions

```
[idle] --init--> [running]
         ↓
    test execution loop:
    [running] --next--> execute test
              --validate--> record result
              --skip--> mark skipped
         ↓
[running] --abort--> [idle]
[running] --complete--> [completed]
[completed] --reset--> [idle]
```

## State Operations

### Initialize

```bash
runner.sh init tests/functional/tests.yaml
```

Creates fresh state with all tests pending.

### Update on Validation

```bash
runner.sh validate "response text"
```

Updates current test status based on expectation matching.

### Reset

```bash
runner.sh reset
```

Clears all state, variables, and results.

## Concurrency Safety

The state file uses atomic writes:

1. Write to temporary file (`.test-state.json.tmp`)
2. Validate JSON structure
3. Atomic rename to final location

This prevents corruption if Claude Code restarts mid-test.

## State Recovery

If a session is interrupted:

1. State file persists on disk
2. Next `/run-tests` detects existing state
3. User can choose to resume or reset

```
Test run in progress detected.
  3/10 tests completed

Options:
  - Type 'resume' to continue from test 4
  - Type 'reset' to start fresh
```

## Variable Scoping

Variables are:
- **Session-scoped**: Persist within a test run
- **Cleared on reset**: Starting new run clears variables
- **String values**: All captured values stored as strings

### Variable Substitution

```yaml
action: "Get entity ${entity_id}"
```

Substitution happens at test execution time, not at load time.

### Missing Variables

If a variable is referenced but not captured:
- Test action contains literal `${variable_name}`
- Test should fail if variable was required
- Use `depends_on` to ensure prerequisite tests run first

## Debugging State

### View Current State

```bash
cat .claude/test-state.json | jq .
```

### Check Variables

In test mode, type `vars` to see captured variables.

### State History

State is overwritten, not versioned. For debugging:

```bash
# Backup before test run
cp .claude/test-state.json .claude/test-state.backup.json
```

## Best Practices

### Gitignore State

Add to `.gitignore`:

```
.claude/test-state.json
```

State is runtime data, not configuration.

### Clean State for CI

```bash
# Always start fresh in CI
rm -f .claude/test-state.json
./tests/functional/runner.sh init tests.yaml
./tests/functional/runner.sh run-all
```

### State Size

Keep test suites reasonable:
- Large suites increase state file size
- Split into multiple test files by category
- Use tags to run subsets
