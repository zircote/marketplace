---
name: Validation Strategies
description: This skill should be used when the user asks about "test validation", "assertion strategies", "regex vs contains", "handling flaky tests", "validation failures", "expected vs actual", or needs guidance on choosing validation approaches and handling edge cases.
version: 1.0.0
---

# Validation Strategies

Choose and implement effective validation strategies for hook-driven tests.

## Validation Approaches

### String Matching (`contains`)

**Strengths:**
- Simple and readable
- Tolerant of formatting changes
- Fast execution

**Weaknesses:**
- May match unintended content
- No structure awareness
- Case-sensitive by default

**Best for:**
- Success/error messages
- UI text validation
- Presence checks

```yaml
expect:
  - contains: "Operation successful"
  - contains: "Created"
```

### Negative Matching (`not_contains`)

**Strengths:**
- Clear failure detection
- Complements positive checks
- Security validation

**Weaknesses:**
- Can't validate what IS present
- May miss variant error messages

**Best for:**
- Error absence verification
- Security checks (no sensitive data)
- Deprecation validation

```yaml
expect:
  - not_contains: "error"
  - not_contains: "exception"
  - not_contains: "password"
```

### Pattern Matching (`regex`)

**Strengths:**
- Precise structure validation
- Value extraction capability
- Multiple value matching

**Weaknesses:**
- Complex to write correctly
- Harder to debug failures
- Performance overhead

**Best for:**
- ID/UUID validation
- Numeric output
- Structured data
- Variable capture

```yaml
expect:
  - regex: "ID:\\s+[a-f0-9]{12}"
  - regex: "Count:\\s+\\d+"
  - regex: "(success|complete|done)"
```

## Choosing the Right Strategy

### Decision Matrix

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Check operation succeeded | `contains` | Flexible message matching |
| Verify no errors | `not_contains` | Catches error variants |
| Extract ID for later use | `regex` with capture | Structured extraction |
| Validate numeric output | `regex` | Pattern precision |
| Check multiple valid responses | `regex` with alternation | `(opt1\|opt2)` |
| Verify exact format | `regex` | Full control |

### Combination Strategies

Use multiple expectations for robust validation:

```yaml
expect:
  # Positive confirmation
  - contains: "Memory created"
  # Negative confirmation
  - not_contains: "error"
  - not_contains: "failed"
  # Structured validation
  - regex: "ID:\\s+([a-f0-9]+)"
```

## Regex Patterns Reference

### Common Patterns

| Pattern | Matches | Use Case |
|---------|---------|----------|
| `\\d+` | One or more digits | Counts, IDs |
| `[a-f0-9]+` | Hex string | UUIDs, hashes |
| `\\w+` | Word characters | Identifiers |
| `.*` | Anything (greedy) | Flexible matching |
| `.*?` | Anything (non-greedy) | Minimal matching |
| `\\s+` | Whitespace | Flexible spacing |
| `(a\|b\|c)` | Alternation | Multiple valid values |

### ID Patterns

```yaml
# UUID v4
regex: "[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

# Short ID (12 hex chars)
regex: "[a-f0-9]{12}"

# Numeric ID
regex: "ID:\\s+(\\d+)"

# Alphanumeric ID
regex: "ID:\\s+([a-zA-Z0-9]+)"
```

### Output Patterns

```yaml
# Success with count
regex: "Found\\s+(\\d+)\\s+results"

# Status messages
regex: "Status:\\s+(active|inactive|pending)"

# Version numbers
regex: "v(\\d+\\.\\d+\\.\\d+)"

# Timestamps
regex: "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}"
```

## Handling Edge Cases

### Empty Results

Validate empty states explicitly:

```yaml
- id: search_no_results
  action: "Search for 'nonexistent_term_xyz'"
  expect:
    - regex: "(no results|0 found|empty)"
    - not_contains: "error"
```

### Variable Output

Handle outputs that may vary:

```yaml
expect:
  # Accept range of counts
  - regex: "Found\\s+[1-9]\\d*\\s+results"
  # Accept multiple success messages
  - regex: "(created|updated|saved)"
```

### Whitespace Sensitivity

Use `\s+` for flexible whitespace:

```yaml
# Rigid (may fail)
- contains: "ID: abc123"

# Flexible (handles formatting)
- regex: "ID:\\s+abc123"
```

### Case Sensitivity

Regex can handle case variations:

```yaml
# Case-insensitive with (?i)
- regex: "(?i)success"

# Explicit alternatives
- regex: "(Success|SUCCESS|success)"
```

## Handling Flaky Tests

### Causes of Flakiness

1. **Timing issues**: Async operations not complete
2. **Order dependence**: Tests affect each other
3. **External dependencies**: Network, services
4. **Non-deterministic output**: Timestamps, random IDs

### Mitigation Strategies

**1. Flexible expectations:**
```yaml
expect:
  # Don't match exact timestamp
  - regex: "Created at: \\d{4}-\\d{2}-\\d{2}"
  # Don't match exact ID
  - regex: "ID:\\s+[a-f0-9]+"
```

**2. Retry logic (in runner):**
```bash
cmd_validate_with_retry() {
  local max_retries=3
  for i in $(seq 1 $max_retries); do
    if cmd_validate "$1"; then
      return 0
    fi
    sleep 1
  done
  return 1
}
```

**3. Tag flaky tests:**
```yaml
- id: external_api_test
  tags: [flaky, external]
```

**4. Isolate stateful tests:**
```yaml
- id: cleanup_before_test
  action: "Reset test state"
  tags: [setup]

- id: actual_test
  depends_on: cleanup_before_test
```

## Debugging Validation Failures

### Reading Failure Messages

```
❌ FAIL: search_basic
Failures:
  - Missing: 'results found'
  - Pattern not found: 'Count:\s+\d+'
```

**Interpretation:**
- `Missing: 'X'` → `contains: X` failed
- `Unexpected: 'X'` → `not_contains: X` failed
- `Pattern not found: 'X'` → `regex: X` failed

### Troubleshooting Steps

1. **Get actual response**: Check what Claude returned
2. **Compare expectations**: Look for typos, case issues
3. **Test regex separately**: Use online regex tester
4. **Simplify expectations**: Start broad, narrow down
5. **Check for invisible chars**: Whitespace, newlines

### Common Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Contains fails on visible text | Case mismatch | Use regex with `(?i)` |
| Regex fails on structured output | Escaping issue | Double-escape special chars |
| Intermittent failures | Timing/async | Add flexible patterns |
| All tests fail | State corruption | Reset with `/run-tests --reset` |

## Additional Resources

### Reference Files

- **`references/validation-approaches.md`** - Validation strategies and patterns
