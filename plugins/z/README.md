# z Plugin

Comprehensive agent library featuring 116 specialized Opus 4.5 agents organized by domain, 54 development skills, and powerful exploration and code review commands for enhanced Claude Code workflows.

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

### Skills (54 total)

Development skills in `skills/`:

| Category | Skills |
|----------|--------|
| **AI/Prompting** | anthropic-prompt-engineer, anthropic-architect, claude-code, prompt-engineer |
| **Frontend** | frontend-development, frontend-design, aesthetic, ui-styling, canvas-design, web-artifacts-builder, web-frameworks, artifacts-builder |
| **Backend** | backend-development, databases, devops |
| **Code Quality** | code-review, debugging (5 sub-skills), problem-solving (6 sub-skills) |
| **Tools & Utilities** | mcp-builder, changelog-generator, skill-creator, engineer-skill-creator, template-skill, skill-share, repomix, sequential-thinking |
| **Media** | ai-multimodal, image-enhancer, video-downloader, slack-gif-creator, chrome-devtools |
| **Business** | brand-guidelines, competitive-ads-extractor, content-research-writer, internal-comms, lead-research-assistant, shopify |
| **Specialized** | better-auth, datadog-entity-generator, invoice-organizer, file-organizer, python-deprecation-fixer, python-project-skel, raffle-winner-picker, theme-factory, webapp-testing |

### Commands (4 total)

Located in `commands/`:

| Command | Description |
|---------|-------------|
| `/explore <path\|pattern\|question>` | Exhaustive codebase exploration with parallel subagents and anti-hallucination enforcement |
| `/deep-research <topic\|url>` | Multi-phase research protocol with structured deliverables and quality gates |
| `/code:review [path\|--focus=security\|performance\|maintainability]` | Comprehensive code review using 6 parallel specialist agents |
| `/code:review-fix [CODE_REVIEW.md\|--quick\|--severity=critical]` | Interactive remediation of code review findings |

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

### /code:review

Comprehensive code review using 6 parallel specialist agents.

**Specialist Agents:**
- Security Analyst - OWASP Top 10, auth, secrets, vulnerabilities
- Performance Engineer - N+1 queries, caching, algorithms
- Architecture Reviewer - SOLID, patterns, dependencies
- Code Quality Analyst - DRY, complexity, naming
- Test Coverage Analyst - Missing tests, edge cases
- Documentation Reviewer - Docstrings, README, API docs

**Output Artifacts:**
- `CODE_REVIEW.md` - Full review report with health scores
- `REVIEW_SUMMARY.md` - Executive summary
- `REMEDIATION_TASKS.md` - Actionable checklist by priority

**Focus Modes:**
```bash
claude /code:review                        # Full review
claude /code:review src/                   # Review specific path
claude /code:review --focus=security       # Security-focused review
claude /code:review --focus=performance    # Performance-focused review
claude /code:review --focus=maintainability # Maintainability-focused review
```

### /code:review-fix

Interactive remediation of code review findings with verification.

**Features:**
- User input at key decision points (severity filter, categories, verification depth)
- `--quick` mode for automated defaults
- Routes findings to appropriate specialist agents
- Verification with pr-review-toolkit agents

**Modes:**
```bash
claude /code:review-fix                    # Interactive mode
claude /code:review-fix --quick            # Quick mode with defaults
claude /code:review-fix --severity=critical # Only critical issues
claude /code:review-fix --category=security # Only security fixes
```

**Interactive Decision Points:**
1. Severity filter (Critical/High/Medium/Low)
2. Category selection (Security/Performance/Architecture/Quality)
3. Conflict resolution for overlapping fixes
4. Verification depth (Full/Quick/Tests only/Skip)
5. Commit strategy (Review first/Single commit/Separate commits)

## Templates

Agent templates in `agents/templates/` provide starting points for creating new agents following Opus 4.5 conventions.

## Integration with Other Plugins

The z plugin agents integrate with other marketplace plugins:

- **git plugin**: Use `code-reviewer` before `/git:pr`
- **datadog plugin**: Combine `sre-engineer` with DataDog agents for monitoring setup
- **document-skills**: Use `technical-writer` for documentation processing workflows

## Version

**Plugin:** 1.0.1
**Agents:** 116
**Skills:** 54
**Commands:** 4
