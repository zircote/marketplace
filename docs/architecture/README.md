# Marketplace Architecture

This directory contains architecture diagrams and documentation for the Zircote Marketplace.

## Diagrams

### Plugin System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│ Claude Code CLI │
│ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Plugin Loader │ │
│ │ │ │
│ │ ┌───────────────────────────────────────────────────────┐ │ │
│ │ │ marketplace.json │ │ │
│ │ │ │ │ │
│ │ │ plugins: [ │ │ │
│ │ │ { name: "zircote", source: "./plugins/zircote" } │ │ │
│ │ │ { name: "gh", source: "./plugins/gh" } │ │ │
│ │ │ { name: "nsip", source: "./plugins/nsip" } │ │ │
│ │ │ { name: "datadog", source: "./plugins/datadog" } │ │ │
│ │ │ { name: "document-skills", source: "..." } │ │ │
│ │ │ ] │ │ │
│ │ └───────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
 │
 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Plugins │
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ zircote │ │ gh │ │ nsip │ │
│ │ │ │ │ │ │ │
│ │ - 116 agents │ │ - 9 commands │ │ - 10 commands│ │
│ │ - 54 skills │ │ - 1 agent │ │ - 1 agent │ │
│ │ - 4 commands │ │ - 1 skill │ │ - 9 MCP tools│ │
│ └──────────────┘ └──────────────┘ │ - 14 hooks │ │
│ └──────────────┘ │
│ ┌──────────────┐ ┌──────────────┐ │
│ │ datadog │ │ document- │ │
│ │ │ │ skills │ │
│ │ - 2 agents │ │ │ │
│ │ - 3 refs │ │ - 4 skills │ │
│ └──────────────┘ └──────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Plugin Component Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│ Plugin Structure │
│ │
│ plugins/your-plugin/ │
│ │ │
│ ├──.claude-plugin/ │
│ │ └── plugin.json ◄─────── Plugin manifest (required) │
│ │ │
│ ├── agents/ │
│ │ └── *.md ◄─────────────── Specialized AI personas │
│ │ Invoked via Task tool │
│ │ │
│ ├── commands/ │
│ │ └── *.md ◄─────────────── Slash commands │
│ │ Invoked via /plugin:command │
│ │ │
│ ├── skills/ │
│ │ └── skill-name/ │
│ │ └── SKILL.md ◄──────── Reusable capabilities │
│ │ Auto-activated by triggers │
│ │ │
│ ├── hooks/ │
│ │ └── scripts/*.py ◄──────── Event handlers │
│ │ Pre/Post tool, Session, Prompt │
│ │ │
│ ├── references/ │
│ │ └── *.md ◄─────────────── Context documents │
│ │ Loaded by agents/skills │
│ │ │
│ └── README.md ◄────────────── Documentation (required) │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

### Hook Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│ Hook Lifecycle │
│ │
│ SessionStart │
│ │ │
│ ▼ │
│ ┌─────────────────────┐ │
│ │ Session Initializes │ │
│ │ - API health checks │ │
│ │ - Context injection │ │
│ └─────────────────────┘ │
│ │ │
│ ▼ │
│ UserPromptSubmit ◄──────────────────────────────────────────┐ │
│ │ │ │
│ ▼ │ │
│ ┌─────────────────────┐ │ │
│ │ User Sends Message │ │ │
│ │ - ID detection │ │ │
│ │ - Intent analysis │ │ │
│ └─────────────────────┘ │ │
│ │ │ │
│ ▼ │ │
│ PreToolUse │ │
│ │ │ │
│ ▼ │ │
│ ┌─────────────────────┐ │ │
│ │ Before Tool Runs │ │ │
│ │ - Validation │ │ │
│ │ - Context injection │ │ │
│ └─────────────────────┘ │ │
│ │ │ │
│ ▼ │ │
│ ┌─────────────────────┐ │ │
│ │ Tool Execution │ │ │
│ └─────────────────────┘ │ │
│ │ │ │
│ ▼ │ │
│ PostToolUse │ │
│ │ │ │
│ ▼ │ │
│ ┌─────────────────────┐ │ │
│ │ After Tool Runs │ │ │
│ │ - Result caching │ │ │
│ │ - Error handling │ │ │
│ │ - Logging │ │ │
│ │ - Export generation │ │ │
│ └─────────────────────┘ │ │
│ │ │ │
│ └───────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ Stop │
│ │ │
│ ▼ │
│ ┌─────────────────────┐ │
│ │ Session Ends │ │
│ │ - Cleanup │ │
│ │ - Final exports │ │
│ └─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Invocation

```
┌─────────────────────────────────────────────────────────────────────┐
│ Agent Invocation Flow │
│ │
│ User Request │
│ │ │
│ ▼ │
│ ┌─────────────────────┐ │
│ │ Claude Opus 4.5 │ │
│ │ (Main Context) │ │
│ └─────────────────────┘ │
│ │ │
│ │ Task tool call │
│ │ subagent_type="python-pro" │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Task Tool │ │
│ │ │ │
│ │ 1. Match subagent_type to agent file │ │
│ │ 2. Load agent.md file │ │
│ │ 3. Parse frontmatter (tools, model) │ │
│ │ 4. Create subprocess with agent context │ │
│ │ 5. Execute agent with prompt │ │
│ │ 6. Return results to main context │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ │ │
│ │ Parallel agents │
│ │ │
│ ┌────┴────┬────────────┬────────────┐ │
│ ▼ ▼ ▼ ▼ │
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
│ │ A │ │ B │ │ C │ │ D │ │
│ │ g │ │ a │ │ o │ │ a │ │
│ │ e │ │ c │ │ d │ │ t │ │
│ │ n │ │ k │ │ e │ │ a │ │
│ │ t │ │ e │ │ - │ │ - │ │
│ │ │ │ n │ │ r │ │ a │ │
│ │ 1 │ │ d │ │ e │ │ n │ │
│ │ │ │ │ │ v │ │ a │ │
│ └───┘ └───┘ └───┘ └───┘ │
│ │ │ │ │ │
│ └─────────┴───────────┴───────────┘ │
│ │ │
│ ▼ │
│ Results consolidated │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

### Version Management

```
┌─────────────────────────────────────────────────────────────────────┐
│ Version Management │
│ │
│ Makefile │
│ │ │
│ ├── make bump-changed ────┐ │
│ │ ▼ │
│ │ ┌─────────────────────┐ │
│ │ │ smart-bump.py │ │
│ │ │ │ │
│ │ │ 1. Get last tag │ │
│ │ │ 2. Check git diff │ │
│ │ │ 3. Filter changed │ │
│ │ │ 4. Bump each │ │
│ │ └─────────────────────┘ │
│ │ │ │
│ │ ▼ │
│ │ ┌─────────────────────┐ │
│ ├─────────────►│ bump-my-version │ │
│ │ │ │ │
│ │ │ Uses per-plugin │ │
│ │ │.bumpversion.toml │ │
│ │ └─────────────────────┘ │
│ │ │ │
│ │ ▼ │
│ │ ┌─────────────────────┐ │
│ │ │ Files Updated │ │
│ │ │ │ │
│ │ │ - plugin.json │ │
│ │ │ - README.md │ │
│ │ │ - CHANGELOG.md │ │
│ │ └─────────────────────┘ │
│ │ │ │
│ │ ▼ │
│ └── make release ──► ┌─────────────────────┐ │
│ │ Git Operations │ │
│ │ │ │
│ │ - Commit changes │ │
│ │ - Create tag │ │
│ │ plugin-v1.2.3 │ │
│ │ - Push with tags │ │
│ └─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

## File Formats

### plugin.json Schema

```json
{
 "name": "string (required, kebab-case)",
 "version": "string (required, semver)",
 "description": "string (required)",
 "author": {
 "name": "string (required)",
 "email": "string (required)",
 "url": "string (required)"
 },
 "license": "string (required)",
 "keywords": ["array", "of", "strings"],
 "agents": ["glob patterns to agent.md files"],
 "commands": ["glob patterns to command.md files"],
 "skills": ["glob patterns to SKILL.md files"],
 "hooks": { "/* hook configuration */" },
 "references": ["glob patterns to reference.md files"],
 "mcpServers": { "/* MCP server configuration */" }
}
```

### Agent Frontmatter

```yaml
---
name: agent-name
description: >
 When to use. Include PROACTIVELY for auto-invoke.
model: inherit
tools: Read, Write, Bash, Glob, Grep
---
```

### Command Frontmatter

```yaml
---
description: One-line description
argument-hint: "[arg1] [arg2]"
---
```

### Skill Frontmatter

```yaml
---
name: skill-name
description: Detailed description with trigger conditions.
---
```

## See Also

- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines
- [Plugin Documentation](https://docs.anthropic.com/en/docs/claude-code) - Official Claude Code docs
