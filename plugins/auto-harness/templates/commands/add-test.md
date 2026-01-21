---
name: add-test
description: Interactively add a new test definition to the test suite
arguments:
  - name: component
    description: Component type to test (mcp-tool, command, skill, hook)
    required: false
---

# Add Test Definition

Interactively create a new test definition and add it to the test suite.

## Process

<step name="gather-info">
Use AskUserQuestion to gather test information:

**Question 1: Component Type**
If not provided via argument, ask:
- MCP Tool
- Command
- Skill
- Hook
- Other

**Question 2: Test ID**
Ask for a unique test identifier.
Suggest format: `category_component_action` (e.g., `crud_memory_create`)

**Question 3: Description**
Ask for a human-readable description of what the test validates.

**Question 4: Action**
Ask what Claude should do for this test.
Provide examples based on component type:
- MCP Tool: "Call mcp__server__tool with param: 'value'"
- Command: "Run the /command-name command"
- Skill: "Ask: 'trigger phrase'"

**Question 5: Expectations**
Ask what should be validated:
- Text that should appear (contains)
- Text that should NOT appear (not_contains)
- Pattern to match (regex)

**Question 6: Variable Capture**
Ask if any value should be captured for later tests.
If yes, ask for variable name and capture pattern.

**Question 7: Dependencies**
Ask if this test depends on another test running first.

**Question 8: Tags**
Ask for tags to categorize the test:
- smoke, critical, regression, slow, etc.
</step>

<step name="generate-definition">
Generate the test definition based on gathered information.

Example output (YAML):
```yaml
- id: crud_memory_create
  description: Create a new memory and capture its ID
  category: crud
  action: "Call subcog_capture with content: 'Test memory', namespace: 'testing'"
  expect:
    - contains: "captured"
    - not_contains: "error"
    - regex: "ID:\\s+([a-f0-9]+)"
  save_as: test_memory_id
  tags: [crud, smoke]
```

Example output (JSON):
```json
{
  "id": "crud_memory_create",
  "description": "Create a new memory and capture its ID",
  "category": "crud",
  "action": "Call subcog_capture with content: 'Test memory', namespace: 'testing'",
  "expect": [
    {"contains": "captured"},
    {"not_contains": "error"},
    {"regex": "ID:\\s+([a-f0-9]+)"}
  ],
  "save_as": "test_memory_id",
  "tags": ["crud", "smoke"]
}
```
</step>

<step name="validate-definition">
Before adding, validate:
1. ID is unique (not already in tests file)
2. Regex patterns compile without errors
3. Dependencies reference existing test IDs
4. Required fields are present
</step>

<step name="add-to-suite">
Read the existing test file, add the new definition in the appropriate category section, and write back.

Confirm success:
```
✅ Test 'crud_memory_create' added successfully.

To run this test:
  /run-tests --tag smoke

To run only this test:
  Manually set current_index in .claude/test-state.json
```
</step>

## Quick Add Mode

For experienced users, accept inline definition:

```
/add-test --inline '{
  "id": "quick_test",
  "action": "Do something",
  "expect": [{"contains": "success"}]
}'
```

## Generated Test Patterns

Based on component type, suggest appropriate test patterns:

### MCP Tool Pattern
```yaml
- id: tool_name_basic
  action: "Call mcp__server__tool_name with required_param: 'value'"
  expect:
    - not_contains: "error"
  tags: [smoke, mcp]
```

### Command Pattern
```yaml
- id: cmd_name_basic
  action: "Run the /command-name command"
  expect:
    - contains: "expected output"
  tags: [smoke, commands]
```

### Skill Pattern
```yaml
- id: skill_trigger
  action: "Ask: 'trigger phrase from skill description'"
  expect:
    - contains: "skill-specific output"
  tags: [smoke, skills]
```

### Hook Pattern
```yaml
- id: hook_pretooluse
  action: "Trigger a Write tool call to activate hook"
  expect:
    - contains: "hook processed"
  tags: [hooks]
```
