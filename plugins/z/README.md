# z Plugin

Comprehensive agent library featuring 116 specialized Opus 4.5 agents organized by domain, 46 development skills, and powerful exploration commands for enhanced Claude Code workflows.

## Installation

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install z
```

## Contents

### Agents (116 total)

Specialized agents organized by domain in `agents/`:

| Category | Count | Directory | Examples |
|----------|-------|-----------|----------|
| Core Development | 11 | `01-core-development/` | frontend-developer, backend-developer, fullstack-developer, api-designer, mobile-developer, ui-designer |
| Language Specialists | 23 | `02-language-specialists/` | python-pro, typescript-pro, golang-pro, rust-engineer, java-architect, react-specialist, nextjs-developer, vue-expert |
| Infrastructure | 12 | `03-infrastructure/` | devops-engineer, sre-engineer, kubernetes-specialist, terraform-engineer, cloud-architect, database-administrator |
| Quality & Security | 12 | `04-quality-security/` | code-reviewer, security-auditor, penetration-tester, test-automator, performance-engineer, debugger, qa-expert |
| Data & AI | 12 | `05-data-ai/` | data-scientist, data-engineer, ml-engineer, llm-architect, postgres-pro, prompt-engineer, nlp-engineer |
| Developer Experience | 10 | `06-developer-experience/` | documentation-engineer, cli-developer, build-engineer, refactoring-specialist, mcp-developer, dx-optimizer |
| Specialized Domains | 11 | `07-specialized-domains/` | fintech-engineer, blockchain-developer, game-developer, iot-engineer, payment-integration |
| Business & Product | 10 | `08-business-product/` | product-manager, technical-writer, ux-researcher, scrum-master |
| Meta Orchestration | 8 | `09-meta-orchestration/` | multi-agent-coordinator, workflow-orchestrator, task-distributor |
| Research & Analysis | 6 | `10-research-analysis/` | research-analyst, competitive-analyst, market-researcher, trend-analyst |
| Templates | 1 | `templates/` | Agent creation templates |

### Skills (46 total)

Development skills in `skills/`:

| Category | Skills |
|----------|--------|
| **AI/Prompting** | anthropic-prompt-engineer, anthropic-architect, claude-code, prompt-engineer |
| **Frontend** | frontend-development, frontend-design, aesthetic, ui-styling, canvas-design, web-artifacts-builder, web-frameworks |
| **Backend** | backend-development, databases, devops |
| **Document Processing** | chrome-devtools, repomix |
| **Code Quality** | code-review, debugging, problem-solving |
| **Tools & Utilities** | mcp-builder, changelog-generator, skill-creator, engineer-skill-creator, template-skill |
| **Media** | ai-multimodal, image-enhancer, video-downloader, slack-gif-creator |
| **Business** | brand-guidelines, competitive-ads-extractor, content-research-writer, internal-comms, lead-research-assistant, shopify |
| **Specialized** | better-auth, datadog-entity-generator, invoice-organizer, file-organizer, python-deprecation-fixer, python-project-skel, raffle-winner-picker, sequential-thinking, theme-factory, webapp-testing |

### Commands

Located in `commands/`:

| Command | Description |
|---------|-------------|
| `/explore <path\|pattern\|question>` | Exhaustive codebase exploration with parallel subagents and anti-hallucination enforcement |
| `/deep-research <topic\|url>` | Multi-phase research protocol with structured deliverables and quality gates |

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

[Detailed agent instructions including protocols, execution patterns, and output formats]
```

## Usage

### Via Task Tool (Subagent Delegation)

Agents are invoked via the Task tool with `subagent_type`:

```
Task(subagent_type="frontend-developer", prompt="Build a React component for user authentication")
Task(subagent_type="security-auditor", prompt="Review this codebase for vulnerabilities")
Task(subagent_type="python-pro", prompt="Refactor this module using best practices")
```

### Parallel Execution

Deploy multiple specialists simultaneously for independent tasks:

```
# Parallel: Full-stack feature with security review
Task(subagent_type="frontend-developer", prompt="Build the UI")
Task(subagent_type="backend-developer", prompt="Build the API")
Task(subagent_type="security-auditor", prompt="Review for vulnerabilities")

# Sequential: Research then implement
research = Task(subagent_type="research-analyst", prompt="Research best practices for X")
# Then use findings to guide implementation
Task(subagent_type="python-pro", prompt="Implement based on research: {research}")
```

### CLAUDE.md References

Reference agents in your project's CLAUDE.md for automatic routing:

```markdown
## Agent Preferences

- Use `frontend-developer` for React/TypeScript work
- Use `python-pro` for Python implementation
- Use `code-reviewer` before merging PRs
```

## Commands Detail

### /explore

The `/explore` command conducts exhaustive codebase investigation:

**Features:**
- Parallel subagent deployment for different exploration tracks
- Anti-hallucination enforcement - reads all files before making claims
- Structured deliverables with file inventories
- "Very thorough" exploration level by default

**Example:**
```bash
claude /explore src/auth
claude /explore "How does the payment system work?"
claude /explore "**/*.py"
```

### /deep-research

The `/deep-research` command executes multi-phase research:

**Phases:**
1. Scope Definition - Classify research type and success criteria
2. Evidence Gathering - Systematic information collection
3. Analysis and Synthesis - Cross-reference and evaluate
4. Deliverable Production - Structured report with recommendations

**Example:**
```bash
claude /deep-research "Best practices for GraphQL authentication"
claude /deep-research ./legacy-system
```

## Templates

Agent templates in `agents/templates/` provide starting points for creating new agents following Opus 4.5 conventions.

## Integration with Other Plugins

The z plugin agents integrate with other marketplace plugins:

- **git plugin**: Use `code-reviewer` before `/git:pr`
- **datadog plugin**: Combine `sre-engineer` with DataDog agents for monitoring setup
- **document-skills**: Use `technical-writer` for documentation processing workflows

## Version

**Plugin:** 1.0.0
**Agents:** 116
**Skills:** 46
**Commands:** 2
