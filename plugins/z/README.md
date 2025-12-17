# z Plugin

Comprehensive agent library featuring 100+ specialized Opus 4.5 agents organized by domain, plus development skills and commands for enhanced Claude Code workflows.

## Installation

```bash
claude /plugin install ./plugins/z
```

## Contents

### Agents (100+)

Organized by domain in `agents/`:

| Category | Directory | Examples |
|----------|-----------|----------|
| Core Development | `01-core-development/` | frontend-developer, backend-developer, fullstack-developer, api-designer |
| Language Specialists | `02-language-specialists/` | python-pro, typescript-pro, golang-pro, rust-engineer, java-architect |
| Infrastructure | `03-infrastructure/` | devops-engineer, sre-engineer, kubernetes-specialist, terraform-engineer |
| Quality & Security | `04-quality-security/` | code-reviewer, security-auditor, penetration-tester, test-automator |
| Data & AI | `05-data-ai/` | data-scientist, data-engineer, ml-engineer, llm-architect, postgres-pro |
| Developer Experience | `06-developer-experience/` | documentation-engineer, cli-developer, build-engineer, mcp-developer |
| Specialized Domains | `07-specialized-domains/` | fintech-engineer, blockchain-developer, game-developer, iot-engineer |
| Business & Product | `08-business-product/` | product-manager, technical-writer, ux-researcher, scrum-master |
| Meta Orchestration | `09-meta-orchestration/` | multi-agent-coordinator, workflow-orchestrator, task-distributor |
| Research & Analysis | `10-research-analysis/` | research-analyst, competitive-analyst, market-researcher |

### Skills

Located in `skills/`:

- **claude-code**: Claude Code expert guidance
- **anthropic-prompt-engineer**: Prompt engineering best practices
- **aesthetic**: UI/UX design principles
- **frontend-development**: React/TypeScript patterns
- **backend-development**: Server-side development
- **databases**: MongoDB and PostgreSQL expertise
- **devops**: Cloud infrastructure and deployment
- **docs-seeker**: Documentation retrieval via llms.txt
- And many more...

### Commands

Located in `commands/`:

- `/explore`: Exhaustive codebase exploration with parallel subagents
- `/deep-research`: Multi-phase research protocol

## Agent Format

All agents follow Opus 4.5 best practices:

```yaml
---
name: agent-name
description: >
  [Role] specialist for [domain]. Use PROACTIVELY when [trigger conditions].
  [Key capabilities and integration points].
model: inherit
tools: Read, Write, Bash, Glob, Grep, [additional-tools]
---
```

## Usage

Agents are invoked via the Task tool with `subagent_type`:

```
Task(subagent_type="frontend-developer", prompt="Build a React component...")
```

Or referenced in CLAUDE.md for automatic routing.

## Templates

Agent templates are available in `agents/templates/` for creating new agents following Opus 4.5 conventions.
