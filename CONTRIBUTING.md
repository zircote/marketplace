# Contributing to Zircote Marketplace

Thank you for your interest in contributing! This guide explains how to add new plugins, agents, skills, and commands to the marketplace.

## Quick Start

1. Fork and clone the repository
2. Create your plugin in `plugins/your-plugin/`
3. Register it in `.claude-plugin/marketplace.json`
4. Submit a pull request

## Plugin Structure

Every plugin must follow this structure:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── README.md                 # Required: Documentation
├── agents/                   # Optional: Agent definitions
│   └── *.md
├── commands/                 # Optional: Slash commands
│   └── *.md
├── skills/                   # Optional: Skills
│   └── skill-name/
│       └── SKILL.md
├── hooks/                    # Optional: Event hooks
│   └── *.sh or *.py
└── references/               # Optional: Reference materials
    └── *.md
```

## Required Files

### plugin.json

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Brief description of what the plugin does",
  "author": {
    "name": "Your Name",
    "email": "your@email.com",
    "url": "https://github.com/username"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "agents": ["./agents/*.md"],
  "commands": ["./commands/*.md"],
  "skills": ["./skills/*/SKILL.md"]
}
```

**Required fields:**
- `name`: Kebab-case identifier (e.g., `my-awesome-plugin`)
- `version`: Semantic version (e.g., `1.0.0`)
- `description`: One-line description
- `author`: Object with `name`, `email`, and `url`
- `license`: License identifier (MIT recommended)

**Optional fields:**
- `keywords`: Array of search terms
- `agents`, `commands`, `skills`, `hooks`: Glob patterns to component files
- `references`, `scripts`: Additional resources

### Custom Fields

The marketplace supports additional custom fields beyond the standard Claude plugin schema:

#### mcpServers

Define MCP (Model Context Protocol) servers that the plugin provides:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/org/repo.git", "server-command"],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

**Fields:**
- `command`: Executable to run (e.g., `uvx`, `npx`, `python`)
- `args`: Array of command-line arguments
- `env`: Environment variables for the server

#### references

Reference materials for agents and skills to access during execution:

```json
{
  "references": ["./references/*.md"]
}
```

Reference files should contain domain knowledge, query patterns, templates, or examples that agents can use for contextual help.

#### Component Arrays

All component arrays support glob patterns:

```json
{
  "agents": ["./agents/*.md"],
  "commands": ["./commands/*.md"],
  "skills": ["./skills/*/SKILL.md"],
  "hooks": ["./hooks/**/*.sh", "./hooks/**/*.py"],
  "references": ["./references/**/*.md"]
}
```

### README.md

Every plugin needs a README with:

1. **Title and description** - What the plugin does
2. **Installation** - How to install
3. **Usage** - How to use each component
4. **Troubleshooting** - Common issues and solutions
5. **Version** - Current version number

## Component Guidelines

### Agents

Agents are specialized AI personas. Create as `.md` files with YAML frontmatter:

```markdown
---
name: your-agent
description: >
  When to use this agent. Include PROACTIVELY if it should be auto-invoked.
model: inherit
tools: Read, Write, Bash, Glob, Grep
---

# Agent Name

[Agent instructions and capabilities]
```

**Best practices:**
- Include "Use PROACTIVELY when..." in description if auto-invocation desired
- List only needed tools
- Add anti-hallucination rules for domain-specific advice
- Include trigger phrases for discoverability

### Commands

Commands are slash-invocable actions. Create as `.md` files:

```markdown
---
description: One-line description
argument-hint: "[arg1] [arg2]"
---

## Variables

- **ARG1**: Description, defaults to X
- **ARG2**: Description, defaults to Y

## Pre-flight Checks

[Validation steps before executing]

## Workflow

[Step-by-step execution instructions]

## Error Handling

| Error | Response |
|-------|----------|
| Error type | User-friendly message with remediation |

## Notes

[Additional context]
```

**Best practices:**
- Always include pre-flight checks
- Provide error handling table
- Use consistent variable naming

### Skills

Skills are reusable capabilities. Create in `skills/skill-name/SKILL.md`:

```markdown
---
name: skill-name
description: Detailed description of the skill and when to use it.
---

# Skill Name

## Trigger Phrases

Activate when user says:
- "phrase 1", "phrase 2"
- "phrase 3", "phrase 4"

[Skill content and instructions]
```

**Best practices:**
- Include trigger phrases section
- Reference materials go in `references/` subdirectory
- Keep SKILL.md focused; use references for details

### Hooks

Hooks respond to Claude Code events. Create as `.sh` or `.py` files:

```bash
#!/bin/bash
# Hook: PreToolUse
# Description: What this hook does

read -r input
# Process JSON input from stdin
# Output JSON to stdout
echo '{"allow": true}'
```

**Supported events:**
- `SessionStart` - Session begins
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- `UserPromptSubmit` - User sends message
- `Stop` - Session ends

## Registration

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "your-plugin",
      "source": "./plugins/your-plugin",
      "description": "Brief description"
    }
  ]
}
```

For external plugins:

```json
{
  "name": "external-plugin",
  "source": {
    "source": "github",
    "repo": "username/repo-name"
  }
}
```

## Style Guidelines

### Markdown

- Use ATX headers (`#`, `##`, `###`)
- Include code blocks with language hints
- Use tables for structured data
- End files with single newline

### JSON

- 2-space indentation
- Double quotes for strings
- Trailing commas not allowed

### Naming

- Plugin names: `kebab-case`
- Agent/skill names: `kebab-case`
- Commands: `/plugin:command` format

## Testing Your Plugin

Before submitting:

1. **Validate JSON**: Ensure all `.json` files are valid
2. **Check paths**: Verify all referenced files exist
3. **Test commands**: Run each command manually
4. **Test agents**: Invoke agents and verify behavior
5. **Review output**: Check for helpful error messages

## Pull Request Process

1. **Create a feature branch**: `git checkout -b add-your-plugin`
2. **Make changes**: Add your plugin following the guidelines
3. **Test thoroughly**: Verify all components work
4. **Update README**: Add your plugin to the marketplace README if appropriate
5. **Submit PR**: Include:
   - Description of the plugin
   - Use cases and examples
   - Any dependencies or prerequisites

## Questions?

- Open an issue for questions or suggestions
- Check existing internal plugins for examples (`datadog`, `document-skills`)
- See external plugin repositories (e.g., [zircote/nsip](https://github.com/zircote/nsip), [zircote/adr](https://github.com/zircote/adr)) for comprehensive examples with hooks and MCP servers
- See [Claude Code Plugin Documentation](https://docs.anthropic.com/en/docs/claude-code) for protocol details

## License

All contributions must be compatible with the MIT license.
