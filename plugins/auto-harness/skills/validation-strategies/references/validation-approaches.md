# Validation Approaches Reference

Strategies for effective test validation in hook-driven testing.

## Validation Philosophy

### Testing Claude's Behavior

Hook-driven tests validate that Claude:
1. Understands the action instruction
2. Executes the intended operation
3. Returns appropriate responses
4. Handles edge cases gracefully

### What to Validate

| Validate | Don't Validate |
|----------|----------------|
| Response contains expected data | Exact response wording |
| Operation completed | Response length |
| Error handling works | Formatting details |
| State changes occurred | Timestamp precision |

## Validation Strategies by Component Type

### MCP Tool Testing

**Strategy**: Validate tool execution and result structure

```yaml
- id: mcp_tool_basic
  action: "Call mcp__server__create with name: 'test'"
  expect:
    - contains: "created"
    - regex: "id:\\s+([\\w-]+)"
    - not_contains: "error"
  save_as: created_id
```

**Key patterns:**
- Check for success indicators
- Capture returned identifiers
- Verify error absence
- Test both success and error paths

### Command Testing

**Strategy**: Validate command understood and executed

```yaml
- id: command_execution
  action: "Run the /my-command with --flag"
  expect:
    - contains: "executed"
    - not_contains: "unknown command"
    - not_contains: "usage:"
```

**Key patterns:**
- Distinguish success from help output
- Verify flag handling
- Test argument parsing

### Skill Testing

**Strategy**: Validate skill activated and provided guidance

```yaml
- id: skill_activation
  action: "Help me write a test for the API endpoint"
  expect:
    - contains: "test"
    - regex: "(endpoint|API|request)"
```

**Key patterns:**
- Skills provide guidance, not exact outputs
- Use broad semantic matching
- Validate domain relevance

### Hook Testing

**Strategy**: Validate hook modified behavior as expected

```yaml
- id: hook_interception
  action: "Write to protected file"
  expect:
    - contains: "blocked"
    - contains: "permission denied"
```

**Key patterns:**
- Test that hook intercepts correctly
- Verify hook output format
- Test bypass conditions

## Validation Techniques

### Positive Validation

Confirm expected behavior occurred:

```yaml
expect:
  - contains: "success"
  - contains: "completed"
  - regex: "result:\\s+\\w+"
```

### Negative Validation

Confirm unwanted behavior did NOT occur:

```yaml
expect:
  - not_contains: "error"
  - not_contains: "failed"
  - not_contains: "exception"
```

### Structural Validation

Confirm response has expected structure:

```yaml
expect:
  - contains: "{"
  - contains: "}"
  - regex: "\"status\":\\s*\""
```

### Semantic Validation

Confirm meaning without exact match:

```yaml
# Accept any of: created, made, generated, built
expect:
  - regex: "(created|made|generated|built)"
```

## Edge Case Strategies

### Empty Responses

```yaml
- id: empty_list
  action: "List items (when none exist)"
  expect:
    - regex: "(no items|empty|0 results)"
    - not_contains: "error"
```

### Large Responses

```yaml
- id: pagination
  action: "List all 1000 items"
  expect:
    - contains: "showing"
    - regex: "page \\d+ of \\d+"
    - regex: "total:\\s+(\\d+)"
```

### Error Responses

```yaml
- id: invalid_input
  action: "Create with invalid data"
  expect:
    - contains: "error"
    - contains: "validation"
    - not_contains: "exception"  # Should be handled gracefully
```

### Timeout Scenarios

```yaml
- id: long_operation
  action: "Process large dataset"
  expect:
    # Either completes or times out gracefully
    - regex: "(completed|timeout|still processing)"
```

## Multi-Step Validation

### Setup-Execute-Verify Pattern

```yaml
# Setup
- id: setup_data
  action: "Create test user"
  expect:
    - regex: "user_id:\\s+(\\w+)"
  save_as: test_user

# Execute
- id: execute_operation
  action: "Grant admin to ${test_user}"
  depends_on: setup_data
  expect:
    - contains: "granted"

# Verify
- id: verify_result
  action: "Check permissions for ${test_user}"
  depends_on: execute_operation
  expect:
    - contains: "admin"
```

### Cleanup Consideration

Tests should be idempotent. Options:

1. **Unique test data**: Use timestamps/UUIDs
2. **Cleanup tests**: Delete created resources
3. **Reset between runs**: Clear test data externally

## Validation Debugging

### When Validation Fails

1. **Check expectation specificity**
   - Too specific? Broaden the match
   - Too broad? Add distinguishing text

2. **Examine actual response**
   - Use debug test to capture full output
   - Look for unexpected formatting

3. **Verify regex syntax**
   - Test regex separately
   - Check escape characters

### Debug Test Pattern

```yaml
- id: debug_operation
  action: "Execute the failing operation"
  expect:
    - regex: "([\\s\\S]*)"  # Capture everything
  save_as: debug_output
```

Then check `debug_output` variable.

## Validation Anti-Patterns

### Over-Specific Expectations

```yaml
# BAD: Too brittle
expect:
  - contains: "Successfully created entity with ID abc123 at 2024-01-15T10:30:00Z"

# GOOD: Flexible
expect:
  - contains: "created"
  - regex: "ID\\s+([\\w-]+)"
```

### Under-Specific Expectations

```yaml
# BAD: Too permissive
expect:
  - regex: ".*"

# GOOD: Meaningful validation
expect:
  - contains: "success"
  - not_contains: "error"
```

### Ignoring Error Paths

```yaml
# BAD: Only testing happy path
- id: create_success
  action: "Create valid entity"
  expect: [...]

# GOOD: Also test error handling
- id: create_invalid
  action: "Create with missing required field"
  expect:
    - contains: "error"
    - contains: "required"
```

## Performance Validation

### Response Time (Implicit)

Tests track duration automatically. Review in reports:

```json
{
  "id": "slow_operation",
  "duration_ms": 5000
}
```

### Resource Usage

Not directly validated, but can check indicators:

```yaml
expect:
  - not_contains: "memory limit"
  - not_contains: "timeout"
```

## Cross-Platform Considerations

### Path Separators

```yaml
# Works on both Windows and Unix
expect:
  - regex: "path[:/\\\\]config"
```

### Line Endings

Hook scripts normalize line endings. Expectations should be line-ending agnostic.

### Case Sensitivity

Some systems are case-insensitive. Use regex for flexibility:

```yaml
expect:
  - regex: "(?i)success"  # Case-insensitive (if supported)
  # Or explicit alternatives:
  - regex: "[Ss]uccess"
```
