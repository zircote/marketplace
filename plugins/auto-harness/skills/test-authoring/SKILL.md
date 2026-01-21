---
name: Test Authoring
description: This skill should be used when the user asks to "write a test", "create test cases", "add test coverage", "define test expectations", "use contains vs regex", "chain dependent tests", or needs guidance on test definition schema, expectation types, variable capture, or test organization best practices.
version: 1.0.0
---

# Test Authoring for Hook-Driven Frameworks

Write effective test definitions for the hook-driven automated test framework.

## Test Definition Schema

Every test requires these fields:

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `id` | Yes | string | Unique identifier (snake_case) |
| `description` | Yes | string | Human-readable explanation |
| `action` | Yes | string | Instruction for Claude to execute |
| `expect` | Yes | array | Validation expectations |
| `category` | No | string | Grouping for filtering |
| `save_as` | No | string | Variable name to capture output |
| `depends_on` | No | string | ID of prerequisite test |
| `tags` | No | array | Labels for filtering |

## Expectation Types

### `contains` - Substring Match

Use for flexible text matching when exact format may vary.

```yaml
expect:
  - contains: "successfully"
  - contains: "Memory created"
```

**When to use:**
- Success messages
- Partial output validation
- UI text that may have surrounding content

### `not_contains` - Negative Match

Ensure unwanted content is absent.

```yaml
expect:
  - not_contains: "error"
  - not_contains: "failed"
  - not_contains: "undefined"
```

**When to use:**
- Error detection
- Ensuring deprecated patterns removed
- Security validation (no sensitive data exposed)

### `regex` - Pattern Match

Use for structured data with predictable patterns.

```yaml
expect:
  - regex: "ID:\\s+([a-f0-9]{12})"
  - regex: "Count:\\s+\\d+"
  - regex: "(success|complete)"
```

**When to use:**
- ID extraction
- Numeric validation
- Multiple acceptable values
- Structured output parsing

**Capture groups:** Use `()` to capture values for `save_as`.

## Variable Capture and Substitution

### Capturing Values

Use `save_as` with a regex capture group:

```yaml
- id: create_item
  action: "Create a new item named 'test'"
  expect:
    - regex: "ID:\\s+([a-f0-9]+)"
  save_as: item_id
```

The first capture group `()` value is stored in the variable.

### Using Captured Values

Reference with `${variable_name}`:

```yaml
- id: retrieve_item
  action: "Retrieve item ${item_id}"
  depends_on: create_item
  expect:
    - contains: "test"
```

### Dependency Chains

Build test sequences:

```yaml
# Test 1: Create
- id: crud_create
  action: "Create memory with content 'test data'"
  expect:
    - regex: "ID:\\s+(\\w+)"
  save_as: memory_id

# Test 2: Read (depends on create)
- id: crud_read
  action: "Retrieve memory ${memory_id}"
  depends_on: crud_create
  expect:
    - contains: "test data"

# Test 3: Update (depends on read)
- id: crud_update
  action: "Update memory ${memory_id} with content 'updated'"
  depends_on: crud_read
  expect:
    - contains: "updated"

# Test 4: Delete (depends on update)
- id: crud_delete
  action: "Delete memory ${memory_id}"
  depends_on: crud_update
  expect:
    - contains: "deleted"
    - not_contains: "error"
```

## Writing Effective Actions

### Be Specific

**Good:**
```yaml
action: "Call subcog_capture with content: 'Test pattern', namespace: 'patterns'"
```

**Avoid:**
```yaml
action: "Create a memory"  # Too vague
```

### Match Tool Names Exactly

For MCP tools, use the full tool name:

```yaml
action: "Call mcp__plugin_subcog_subcog__subcog_capture with content: 'test'"
```

### Include Required Parameters

```yaml
action: "Call subcog_recall with query: 'authentication', limit: 5, mode: 'hybrid'"
```

## Test Organization

### Categories

Group tests by component or functionality:

| Category | Use For |
|----------|---------|
| `initialization` | Setup and init tests |
| `crud` | Create, read, update, delete |
| `search` | Query and filter operations |
| `validation` | Input validation tests |
| `error-handling` | Error condition tests |
| `integration` | Cross-component tests |
| `commands` | Slash command tests |
| `skills` | Skill trigger tests |
| `hooks` | Hook behavior tests |

### Tags

Use tags for filtering test runs:

| Tag | Meaning |
|-----|---------|
| `smoke` | Quick sanity checks |
| `critical` | Must-pass tests |
| `regression` | Bug fix verification |
| `slow` | Long-running tests |
| `flaky` | Known intermittent failures |

### ID Naming Convention

Pattern: `category_component_action_variant`

Examples:
- `init_basic` - Basic initialization
- `crud_memory_create` - Create memory
- `search_semantic_empty` - Semantic search with no results
- `cmd_review_with_args` - Review command with arguments

## Common Patterns

### Smoke Test Pattern

Quick validation that component works:

```yaml
- id: component_smoke
  description: "Basic smoke test for component"
  category: smoke
  action: "Minimal invocation of component"
  expect:
    - not_contains: "error"
  tags: [smoke, critical]
```

### CRUD Test Pattern

Full lifecycle test:

```yaml
- id: entity_create
  action: "Create entity"
  save_as: entity_id
  tags: [crud]

- id: entity_read
  action: "Read entity ${entity_id}"
  depends_on: entity_create

- id: entity_update
  action: "Update entity ${entity_id}"
  depends_on: entity_read

- id: entity_delete
  action: "Delete entity ${entity_id}"
  depends_on: entity_update
```

### Error Handling Pattern

Validate error responses:

```yaml
- id: invalid_input_error
  description: "Verify error on invalid input"
  action: "Call tool with invalid_param: 'not-valid'"
  expect:
    - contains: "error"
    - regex: "(invalid|not found|failed)"
  tags: [error-handling]
```

### Search Results Pattern

Validate search functionality:

```yaml
- id: search_with_results
  action: "Search for 'known term'"
  expect:
    - contains: "results"
    - regex: "found\\s+\\d+"
    - not_contains: "no results"
```

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques:
- **`references/expectation-patterns.md`** - Regex patterns for common outputs
