---
name: harness:init
description: Initialize hook-driven test framework in a project. Guides through configuration and generates complete test infrastructure.
arguments:
  - name: project-path
    description: Path to target project (defaults to current directory)
    required: false
---

# Hook-Driven Test Framework Initialization

This command scaffolds a complete automated test framework into the target project using the hook-driven testing pattern.

## What Gets Generated

The following infrastructure will be created in the target project:

### Commands (`.claude/commands/`)
- `run-tests.md` - Execute test suite with filtering options
- `add-test.md` - Add new test definitions interactively
- `test-report.md` - Generate test reports in various formats

### Test Runner (`tests/functional/`)
- `runner.sh` - Orchestration script handling test execution
- `tests.json` or `tests.yaml` - Test definitions file

### Hooks (`hooks/`)
- `test-wrapper.sh` - UserPromptSubmit hook for test mode
- `hooks.json` - Hook registration configuration

### State Management
- `.claude/test-state.json` - Runtime state (auto-created during test runs)

## Initialization Process

<step name="detect-project">
First, detect the project type and existing infrastructure.

Use Glob and Read tools to check for:
- `.claude-plugin/plugin.json` (Claude plugin project)
- `.mcp.json` (MCP server definitions)
- `hooks/hooks.json` (existing hooks)
- `tests/` directory (existing test structure)
- `.claude/` directory (Claude Code configuration)

Report findings to user before proceeding.
</step>

<step name="gather-requirements">
Use AskUserQuestion to gather configuration:

**Question 1: Test Targets**
Ask what components the user wants to test:
- MCP tools only
- Skills only
- Commands only
- Full plugin testing (all components)
- Custom selection

**Question 2: Test Format**
Ask preferred format for test definitions:
- JSON (structured, precise)
- YAML (readable, comments allowed)
- Both (generate both formats)

**Question 3: Report Formats**
Ask which report formats to support:
- Markdown (default, always included)
- HTML (visual, shareable)
- JSON (machine-readable, CI integration)
- All formats (configurable at runtime)

**Question 4: Hook Integration**
If existing hooks detected, ask:
- Merge with existing hooks
- Create separate test hooks
- Replace existing hooks (with backup)
</step>

<step name="generate-infrastructure">
Based on user choices, generate all infrastructure files using the templates from the auto-harness plugin.

For each file:
1. Read the template from `${CLAUDE_PLUGIN_ROOT}/templates/`
2. Substitute variables based on user configuration
3. Write to target project location
4. Verify file was created successfully

Variable substitutions:
- `{{PROJECT_NAME}}` - Target project name
- `{{TEST_FORMAT}}` - json or yaml
- `{{REPORT_FORMATS}}` - Comma-separated list
- `{{TEST_TARGETS}}` - What components to test
</step>

<step name="create-initial-tests">
If the project is a Claude plugin, offer to generate initial test definitions based on detected components:

For MCP tools:
- Parse `.mcp.json` to find available tools
- Generate basic smoke tests for each tool

For commands:
- Scan `commands/` directory
- Generate invocation tests for each command

For skills:
- Scan `skills/` directory
- Generate trigger tests for each skill

For hooks:
- Parse `hooks/hooks.json`
- Generate event tests for each hook type
</step>

<step name="verify-setup">
Run validation to ensure everything is properly configured:

1. Verify all files exist and are readable
2. Check runner.sh is executable
3. Validate test definitions syntax
4. Verify hooks.json structure
5. Test that hooks can be loaded

Report any issues found and offer to fix them.
</step>

<step name="provide-documentation">
Generate a project-specific README section explaining:
- How to run tests (`/run-tests`)
- How to add new tests (`/add-test`)
- How to generate reports (`/test-report`)
- Test definition schema
- Hook architecture overview

Also reference the full tutorial at:
https://zircote.com/blog/2026/01/hook-driven-automated-test-framework-for-claude-code/
</step>

## Example Session

```
User: /harness:init

Claude: I'll help you set up the hook-driven test framework. Let me first analyze your project...

[Detects plugin with 3 MCP tools, 2 commands, 1 skill]

Claude: I found this is a Claude plugin project with:
- 3 MCP tools defined
- 2 slash commands
- 1 skill

Let me ask a few questions to customize the setup...

[AskUserQuestion: Test targets?]
User: Full plugin testing

[AskUserQuestion: Test format?]
User: YAML

[Generates infrastructure]

Claude: Test framework initialized successfully!

Created files:
✓ .claude/commands/run-tests.md
✓ .claude/commands/add-test.md
✓ .claude/commands/test-report.md
✓ tests/functional/runner.sh
✓ tests/functional/tests.yaml
✓ hooks/test-wrapper.sh
✓ hooks/hooks.json

Generated 12 initial tests:
- 6 MCP tool tests
- 4 command tests
- 2 skill tests

Run /run-tests to execute your test suite!
```

## Error Handling

If any step fails:
1. Report the specific error clearly
2. Suggest remediation steps
3. Offer to retry or skip the problematic step
4. Never leave the project in a broken state - rollback partial changes if needed
