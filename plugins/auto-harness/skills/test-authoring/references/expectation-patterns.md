---
title: Expectation Patterns Reference
description: Comprehensive patterns for test expectations in hook-driven testing
---

# Expectation Patterns Reference

Comprehensive patterns for test expectations in hook-driven testing.

## Basic Expectations

### Contains

Check for substring presence in response:

```yaml
expect:
  - contains: "success"
  - contains: "completed"
```

**Best practices:**
- Use distinctive text unlikely to appear accidentally
- Prefer semantic indicators over generic words
- Combine multiple contains for robustness

### Not Contains

Ensure text does NOT appear:

```yaml
expect:
  - not_contains: "error"
  - not_contains: "failed"
  - not_contains: "exception"
```

**Common patterns:**
- Error indicators: `error`, `failed`, `exception`, `fatal`
- Warning indicators: `warning`, `deprecated`
- Status indicators: `pending`, `timeout`

### Regex Patterns

Pattern matching with optional capture:

```yaml
expect:
  - regex: "ID:\\s+([a-f0-9-]+)"
save_as: entity_id
```

## Advanced Regex Patterns

### UUID Capture

```yaml
regex: "([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
```

### Numeric Value Capture

```yaml
# Integer
regex: "count:\\s+(\\d+)"

# Decimal
regex: "value:\\s+([0-9]+\\.?[0-9]*)"

# Negative numbers
regex: "balance:\\s+(-?\\d+)"
```

### Timestamp Patterns

```yaml
# ISO 8601
regex: "(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})"

# Unix timestamp
regex: "timestamp:\\s+(\\d{10,13})"
```

### Status Extraction

```yaml
# Word status
regex: "status:\\s+(\\w+)"

# Quoted string
regex: "message:\\s+\"([^\"]+)\""

# Multi-word with quotes
regex: "description:\\s+[\"']([^\"']+)[\"']"
```

### Path Capture

```yaml
# File path
regex: "file:\\s+(/[^\\s]+)"

# Relative path
regex: "path:\\s+(\\.?/?[\\w/.-]+)"
```

## Combining Expectations

### Strict Validation

Require all conditions:

```yaml
expect:
  - contains: "created successfully"
  - contains: "id:"
  - not_contains: "error"
  - not_contains: "warning"
  - regex: "id:\\s+([a-f0-9]+)"
```

### Flexible Validation

Accept alternative success indicators:

```yaml
# Test passes if ANY of these conditions match
expect:
  - contains: "success"
# OR add separate test for alternative:
- id: alternative_check
  action: "Same action"
  expect:
    - contains: "completed"
```

## MCP Tool Response Patterns

### Tool Success

```yaml
expect:
  - contains: "Tool executed"
  - not_contains: "error"
  - regex: "result:\\s+(.+)"
```

### Tool Error Handling

```yaml
# Expect specific error
expect:
  - contains: "error"
  - contains: "invalid parameter"

# Expect graceful failure
expect:
  - contains: "failed"
  - not_contains: "exception"
  - not_contains: "stack trace"
```

### Tool Output Parsing

```yaml
# JSON-like output
expect:
  - regex: "\"status\":\\s*\"(\\w+)\""
  - regex: "\"count\":\\s*(\\d+)"

# Structured output
expect:
  - contains: "Result:"
  - regex: "- name:\\s+(.+)"
  - regex: "- value:\\s+(\\d+)"
```

## Command Response Patterns

### Slash Command Success

```yaml
expect:
  - contains: "Command executed"
  - not_contains: "usage:"  # Would indicate help/error
```

### Help Output Validation

```yaml
expect:
  - contains: "Usage:"
  - contains: "--help"
  - regex: "Options:\\s*\\n"
```

## Variable Substitution Patterns

### Chained Operations

```yaml
# Step 1: Create
- id: create_item
  action: "Create item named 'test'"
  expect:
    - regex: "ID:\\s+([\\w-]+)"
  save_as: item_id

# Step 2: Read
- id: read_item
  action: "Get item ${item_id}"
  depends_on: create_item
  expect:
    - contains: "test"
    - contains: "${item_id}"

# Step 3: Update
- id: update_item
  action: "Update item ${item_id} with name 'updated'"
  depends_on: read_item
  expect:
    - contains: "updated"

# Step 4: Delete
- id: delete_item
  action: "Delete item ${item_id}"
  depends_on: update_item
  expect:
    - contains: "deleted"
```

### Multiple Variable Capture

```yaml
- id: create_parent
  action: "Create parent entity"
  expect:
    - regex: "parent_id:\\s+(\\w+)"
  save_as: parent_id

- id: create_child
  action: "Create child under parent ${parent_id}"
  depends_on: create_parent
  expect:
    - regex: "child_id:\\s+(\\w+)"
  save_as: child_id

- id: verify_relationship
  action: "Verify ${child_id} belongs to ${parent_id}"
  depends_on: create_child
  expect:
    - contains: "relationship confirmed"
```

## Edge Case Patterns

### Empty Response

```yaml
expect:
  - not_contains: "error"
  # Response may be empty for some operations
```

### Large Output

```yaml
expect:
  - contains: "items found"
  - regex: "showing (\\d+) of (\\d+)"
```

### Multiline Response

```yaml
# Match across lines
expect:
  - contains: "Step 1"
  - contains: "Step 2"
  - contains: "Complete"
```

### Special Characters

```yaml
# Escape special regex chars
expect:
  - regex: "path:\\s+\\./config\\.json"
  - regex: "price:\\s+\\$([0-9.]+)"
```

## Debugging Patterns

When tests fail, use these diagnostic patterns:

### Capture Full Response

```yaml
- id: debug_capture
  action: "Execute problematic operation"
  expect:
    - regex: "([\\s\\S]*)"  # Capture everything
  save_as: full_response
```

### Partial Match Debug

```yaml
# If "success" isn't found, try broader match
expect:
  - regex: "(succ|complete|done|finish)"
```

### Case-Insensitive Match

Regex flags aren't directly supported, but patterns can handle it:

```yaml
# Match Success, success, SUCCESS
expect:
  - regex: "[Ss][Uu][Cc][Cc][Ee][Ss][Ss]"
```
