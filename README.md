# Zircote Claude Marketplace

A curated collection of Claude Code plugins featuring specialized agents, development workflows, monitoring integrations, and document processing capabilities.

## Overview

This marketplace provides 17 plugins for Claude Code, ranging from domain-specific expert agents to productivity-enhancing workflow tools. Most plugins (15 of 17) are hosted in standalone GitHub repositories for independent versioning and development, while 2 plugins remain internal to this repository. All plugins work identically across Claude Code CLI and VS Code extension.

## Quick Start

```bash
# Add this marketplace to Claude Code
claude /plugin marketplace add zircote/marketplace

# List available plugins
claude /plugin list

# Install plugins (format: plugin-name@marketplace-name)
# Internal plugins (hosted in this repository)
claude /plugin install datadog@zircote              # DataDog monitoring agents
claude /plugin install document-skills@zircote      # PDF/DOCX/XLSX/PPTX processing

# External plugins (hosted in standalone GitHub repositories)
claude /plugin install agents@zircote               # 115 specialized agents + 54 skills
claude /plugin install gh@zircote                   # Git workflow + Copilot onboarding
claude /plugin install documentation-review@zircote # Documentation management
claude /plugin install human-voice@zircote          # AI writing pattern detection
claude /plugin install adr@zircote                  # ADR lifecycle management
claude /plugin install nsip@zircote                 # Sheep breeding data (NSIP)
claude /plugin install aesth@zircote                # Design system management with Subcog
claude /plugin install claude-spec@zircote          # Project specification lifecycle
claude /plugin install subcog@zircote               # Git-backed memory system
claude /plugin install git-adr@zircote              # ADR management via git notes
claude /plugin install github-social@zircote        # Repository presentation optimizer
claude /plugin install sdlc@zircote                  # SDLC quality tools and workflows
claude /plugin install rlm-rs@zircote               # Rust-based RLM plugin
claude /plugin install sigint@zircote               # Market research toolkit
```

## Available Plugins

### Internal Plugins

Plugins hosted directly in this repository.

---

### datadog - DataDog Integration

Expert agents for monitoring setup, dashboard creation, and APM integration.

**Agents:**
- **datadog-pro** - DataDog API specialist for `datadog-api-client` (v2.45.0+)
- **datadog-api-expert** - Monitor/dashboard creation, query syntax, error handling

**Features:**
- Complete code examples with imports and error handling
- v1/v2 API guidance with official documentation citations
- Regional configuration support (US, EU, AP regions)

```bash
claude /plugin install datadog@zircote
```

---

### document-skills - Document Processing

AI-powered document processing for common office formats.

| Skill | Capabilities |
|-------|-------------|
| **PDF** | Text extraction, table detection, OCR, metadata, form fields |
| **DOCX** | Full text extraction, style preservation, comments, revisions |
| **XLSX** | Cell/formula reading, named ranges, charts, conditional formatting |
| **PPTX** | Slide content, speaker notes, shapes, animations |

```bash
claude /plugin install document-skills@zircote

# Usage
claude "Analyze the contents of report.pdf"
claude "Extract data from sales.xlsx"
```

---

### External Plugins

Plugins hosted in standalone GitHub repositories for independent versioning and development.

---

### agents - Agent Library

**Source:** [zircote/agents](https://github.com/zircote/agents)

**115 specialized Opus 4.5 agents** organized by domain, plus 54 skills.

| Category | Agents | Examples |
|----------|--------|----------|
| Core Development | 11 | frontend-developer, backend-developer, api-designer |
| Language Specialists | 23 | python-pro, typescript-pro, golang-pro, rust-engineer |
| Infrastructure | 12 | devops-engineer, sre-engineer, kubernetes-specialist |
| Quality & Security | 12 | code-reviewer, security-auditor, penetration-tester |
| Data & AI | 12 | data-scientist, ml-engineer, llm-architect, postgres-pro |
| Developer Experience | 10 | documentation-engineer, cli-developer, mcp-developer |
| Specialized Domains | 11 | fintech-engineer, blockchain-developer, game-developer |
| Business & Product | 10 | product-manager, technical-writer, scrum-master |
| Meta Orchestration | 8 | multi-agent-coordinator, workflow-orchestrator |
| Research & Analysis | 6 | research-analyst, competitive-analyst |

**Skills:** 54 specialized skills including `claude-code`, `anthropic-prompt-engineer`, `databases`, `devops`, `debugging`, and more.

```bash
claude /plugin install agents@zircote
```

---

### gh - Git Workflow & GitHub Ecosystem

**Source:** [zircote/gh](https://github.com/zircote/gh)

Streamlined version control operations, GitHub ecosystem integration, and Copilot configuration.

| Command | Description |
|---------|-------------|
| `/git:cm` | Stage all and commit with conventional commit format |
| `/git:cp` | Stage, commit, and push in one operation |
| `/git:pr [to] [from]` | Create pull request via `gh` CLI |
| `/git:fr [remote] [branch]` | Fetch and rebase onto remote branch |
| `/git:sync [remote] [branch]` | Full sync: fetch, rebase, push |
| `/git:ff [remote] [branch]` | Fast-forward merge only |
| `/git:prune [--force]` | Clean up stale local branches |
| `/gh:copilot-onboard [path]` | Generate Copilot config from CLAUDE.md |
| `/gh:migrate [--ci=TYPE]` | Multi-CI to GitHub Actions migration |

**Agent:** `copilot-assistant` - Bridge Claude Code and GitHub Copilot configurations

**Skills:**
- **GitHub Ecosystem** - Actions, templates, CODEOWNERS, Dependabot setup

```bash
claude /plugin install gh@zircote
```

---

### nsip - NSIP Sheep Breeding

**Source:** [zircote/nsip](https://github.com/zircote/nsip)

Access National Sheep Improvement Program breeding data with MCP tools.

**9 MCP Tools:**
- `nsip_get_last_update` - Database update date
- `nsip_list_breeds` - Available breed groups
- `nsip_search_animals` - Search with pagination
- `nsip_get_animal` - Detailed animal information
- `nsip_get_lineage` - Pedigree tree
- `nsip_get_progeny` - Offspring list
- And more...

**10 Commands:**
- `/nsip:consult` - Expert breeding consultation
- `/nsip:lookup` - Animal lookup by LPN ID
- `/nsip:profile` - Complete animal profile
- `/nsip:search` - Search with filters
- `/nsip:traits` - Trait ranges by breed

**Agent:** `shepherd` - Expert sheep breeding advisor

**Hooks:** 14 intelligent hooks for error resilience, caching, and exports

```bash
claude /plugin install nsip@zircote
```

**Prerequisites:** `uv` package manager (https://docs.astral.sh/uv/)

---

### documentation-review - Documentation Management

**Source:** [zircote/documentation-review](https://github.com/zircote/documentation-review)

Comprehensive documentation management with review, creation, update, and maintenance capabilities.

**Agents:**
- **doc-writer** - Generate new documentation from codebase analysis
- **doc-reviewer** - Review documentation for quality, accuracy, and completeness

**Commands:**
- `/doc-review` - Review documentation for quality issues
- `/doc-create` - Generate new documentation from codebase analysis
- `/doc-update` - Update outdated documentation with current information
- `/doc-cleanup` - Identify and report obsolete documentation
- `/doc-setup` - Interactive setup for documentation configuration
- `/changelog` - Manage CHANGELOG.md entries and release documentation

**Skills:**
- **documentation-standards** - Best practices for documentation quality
- **changelog** - Keep a Changelog format and conventions
- **api-documentation** - API specification and documentation patterns

```bash
claude /plugin install documentation-review@zircote
```

---

### human-voice - AI Writing Pattern Detection

**Source:** [zircote/human-voice](https://github.com/zircote/human-voice)

Detect and prevent AI-generated writing patterns to ensure authentic human voice in content.

**Agent:**
- **voice-reviewer** - Proactive content review after writing/editing markdown files

**Commands:**
- `/human-voice:review [path]` - Analyze content for AI patterns (4-tier analysis)
- `/human-voice:fix [path]` - Auto-fix character-level issues (em dashes, smart quotes, emojis)

**Skill:**
- **human-voice** - Multi-tier detection patterns and writing guidelines

**Detection Tiers:**

| Tier | Type | Examples | Fix |
|------|------|----------|-----|
| 1 | Characters | Em dashes, smart quotes, emojis | Automated |
| 2 | Language | "delve", "harness", "it's worth noting" | Manual |
| 3 | Structural | List addiction, rule-of-three overuse | Manual |
| 4 | Voice | Passive voice, generic analogies | Manual |

```bash
claude /plugin install human-voice@zircote
```

---

### adr - ADR Lifecycle Management

**Source:** [zircote/adr](https://github.com/zircote/adr)

Complete lifecycle management for Architectural Decision Records with multi-format support.

**Agents:**
- **adr-compliance** - Audit code against accepted ADRs
- **adr-researcher** - Research context and options for decisions
- **adr-author** - Detect and document architectural decisions

**Commands:**
- `/adr-new` - Create a new ADR
- `/adr-list` - List all ADRs with status filtering
- `/adr-update` - Update an existing ADR
- `/adr-supersede` - Create an ADR that supersedes another
- `/adr-search` - Search ADRs by content, status, or tags
- `/adr-export` - Export ADRs to HTML, JSON, or PDF
- `/adr-setup` - Interactive setup for ADR configuration

**Skills:**
- **adr-fundamentals** - ADR basics and best practices
- **adr-format-madr** - MADR 4.0 template format
- **adr-format-nygard** - Classic Nygard format
- **adr-format-y-statement** - Concise Y-Statement format
- **adr-format-alexandrian** - Pattern-based Alexandrian format
- **adr-format-business-case** - Business case format for executives
- **adr-quality** - ADR quality checklist and validation
- **adr-decision-drivers** - Identifying architectural forces
- **adr-integration** - CI/CD and tooling integration
- **adr-compliance** - Code compliance auditing

**Formats Supported:** MADR, Nygard, Y-Statement, Alexandrian, Tyree-Akerman, Business Case

```bash
claude /plugin install adr@zircote
```

---

### aesth - Design System Management

Craft-focused design system management powered by Subcog memory. Build interfaces with elegance, consistency, and semantic memory.

**Source:** [zircote/aesth](https://github.com/zircote/aesth)

**Commands:**
- `/aesth:init` - Initialize skill and load design system from Subcog
- `/aesth:status` - Display current design system state
- `/aesth:validate` - Validate code against design rules
- `/aesth:capture` - Store patterns and decisions to Subcog
- `/aesth:extract` - Extract patterns from existing code

**Skill:** aesth - Craft principles, Subcog integration, design directions

**Features:**
- Six design directions (Precision & Density, Warmth & Approachability, etc.)
- Memory-first architecture with Subcog MCP
- Validation against spacing grid, colors, depth strategy, typography
- Cross-project craft principles sharing

**Scope:** Dashboards, admin panels, SaaS apps, tools (not marketing sites)

```bash
claude /plugin install aesth@zircote
```

**Prerequisites:** Subcog MCP server configured and running

---

### claude-spec - Project Specification Lifecycle

Strategic project planning, implementation tracking, and retrospectives.

**Source:** [zircote/claude-spec](https://github.com/zircote/claude-spec)

**Commands:**
- `/cs:p <project-idea>` - Strategic project planner with Socratic elicitation
- `/cs:i [project-id]` - Implementation progress tracker with PROGRESS.md
- `/cs:s [project-id]` - Project status and portfolio listing
- `/cs:c <project-path>` - Close project with retrospective generation

**Features:**
- PRD and implementation plan generation
- PROGRESS.md checkpoint system for multi-session work
- Git worktree management for parallel development

```bash
claude /plugin install claude-spec@zircote
```

---

### subcog - Git-Backed Memory System

A Git-backed memory system for Claude Code, capturing decisions, learnings, and context as git notes with semantic search and automatic recall.

**Source:** [zircote/subcog](https://github.com/zircote/subcog)

**Features:**
- Memory capture with namespaces (decisions, patterns, learnings, context)
- Semantic search and automatic recall
- Git notes storage for version control integration
- MCP server integration

```bash
claude /plugin install subcog@zircote
```

---

### git-adr - ADR Management via Git Notes

A command-line tool that integrates Architecture Decision Record management directly into your git workflow using git notes.

**Source:** [zircote/git-adr](https://github.com/zircote/git-adr)

**Features:**
- ADRs stored as git notes (not files)
- Integrated with git workflow
- Searchable decision history

```bash
claude /plugin install git-adr@zircote
```

---

### github-social - Repository Presentation Optimizer

Optimize GitHub repository presentation with social preview images and engaging metadata.

**Source:** [zircote/github-social](https://github.com/zircote/github-social)

**Commands:**

| Command | Description |
|---------|-------------|
| `/social-preview` | Generate a social preview image for the current project |
| `/social-preview:setup` | Interactive setup wizard for configuration |
| `/repo-metadata` | Generate optimized description and topics (use `--apply` to update GitHub) |

**Skills:**
- **social-preview** - Analyze project and generate social preview images
- **repo-metadata** - Generate optimized repository descriptions and topics

**Features:**
- Analyzes project files (README, package.json, CLAUDE.md) to understand purpose
- Generates detailed image prompts for social preview images
- Supports multiple image providers: DALL-E 3, Stable Diffusion, Midjourney, manual
- Outputs images meeting GitHub requirements (1280x640px, <1MB)
- Generates SEO-friendly repository descriptions (max 350 chars)
- Suggests relevant topics for discoverability (max 20 topics)
- Can apply changes via `gh` CLI or output for manual review

```bash
claude /plugin install github-social@zircote
```

---

### sdlc - SDLC Quality Tools

Software development lifecycle quality tools and workflows.

**Source:** [zircote/sdlc-quality](https://github.com/zircote/sdlc-quality)

```bash
claude /plugin install sdlc@zircote
```

---

### rlm-rs - Rust RLM Plugin

Rust-based RLM plugin for Claude Code.

**Source:** [zircote/rlm-rs-plugin](https://github.com/zircote/rlm-rs-plugin)

```bash
claude /plugin install rlm-rs@zircote
```

---

### auto-harness - Test Framework Generator

Hook-driven automated test framework generator for Claude Code projects.

**Source:** [zircote/auto-harness](https://github.com/zircote/auto-harness)

**Commands:**
- `/harness:init` - Scaffold test infrastructure into target project
- `/run-tests` - Execute automated functional test suite

**Features:**
- YAML/JSON test definitions with variable capture
- UserPromptSubmit hook for test interception
- Test filtering by category and tags
- Markdown and JSON report generation

```bash
claude /plugin install auto-harness@zircote
```

---

### sigint - Market Research Toolkit

Comprehensive market research toolkit with iterative workflows, multi-audience reports, and trend-based modeling.

**Source:** [zircote/sigint](https://github.com/zircote/sigint)

**Commands:**

| Command | Description |
|---------|-------------|
| `/sigint:start <topic>` | Begin new research session |
| `/sigint:augment <area>` | Deep-dive into specific area |
| `/sigint:update` | Refresh existing research data |
| `/sigint:report` | Generate comprehensive report |
| `/sigint:issues` | Create GitHub issues from findings |
| `/sigint:resume` | Resume previous research session |
| `/sigint:status` | Show current research state |
| `/sigint:init` | Manually initialize Subcog context |

**Agents:**
- **market-researcher** - Autonomous market research and data gathering
- **issue-architect** - Converts findings to sprint-sized GitHub issues
- **report-synthesizer** - Generates multi-format reports with visualizations

**Skills (Research Methodologies):**
- Competitive Analysis (Porter's 5 Forces)
- Market Sizing (TAM/SAM/SOM)
- Trend Analysis & Modeling (three-valued logic: INC/DEC/CONST)
- Customer Research & Personas
- Tech Assessment & Feasibility
- Financial Analysis & Unit Economics
- Regulatory Review
- Report Writing

**Features:**
- Multi-audience reports (executives, PMs, investors, developers)
- Transitional scenario graphs (Mermaid)
- Subcog memory integration for session persistence
- GitHub issue generation from findings

```bash
claude /plugin install sigint@zircote
```

**Prerequisites:** Subcog MCP server, GitHub CLI (`gh`)

---

## Marketplace Structure

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Central plugin registry (17 plugins total)
├── plugins/                      # Internal plugins (2)
│   ├── datadog/                  # Monitoring integration
│   │   └── agents/               # datadog-pro, datadog-api-expert
│   └── document-skills/          # Document processing
│       ├── pdf/                  # PDF skill
│       ├── docx/                 # Word skill
│       ├── xlsx/                 # Excel skill
│       └── pptx/                 # PowerPoint skill
├── External Plugins (15 GitHub repos)
│   ├── zircote/agents            # Agent library (115 agents, 54 skills)
│   ├── zircote/gh                # Git workflow + Copilot onboarding
│   ├── zircote/nsip              # Sheep breeding data (MCP tools)
│   ├── zircote/documentation-review  # Documentation management
│   ├── zircote/human-voice       # AI writing pattern detection
│   ├── zircote/adr               # ADR lifecycle management
│   ├── zircote/aesth             # Design system management
│   ├── zircote/claude-spec       # Project specification lifecycle
│   ├── zircote/subcog            # Git-backed memory system
│   ├── zircote/git-adr           # ADR management via git notes
│   ├── zircote/github-social     # Repository presentation optimizer
│   ├── zircote/sdlc-quality      # sdlc - SDLC quality tools
│   ├── zircote/rlm-rs-plugin     # rlm-rs - Rust-based RLM plugin
│   ├── zircote/auto-harness      # auto-harness - Test framework generator
│   └── zircote/sigint            # sigint - Market research toolkit
└── README.md                     # This file
```

## Installation Methods

### Method 1: From GitHub (Recommended)

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install <plugin-name>
```

### Method 2: Direct GitHub URL

```bash
claude /plugin marketplace add https://github.com/zircote/marketplace
claude /plugin install <plugin-name>
```

### Method 3: Local Development

```bash
git clone https://github.com/zircote/marketplace.git
cd marketplace
claude /plugin marketplace add ./
claude /plugin install <plugin-name>
```

## Contributing

To add a new plugin:

1. Create a plugin directory under `plugins/`
2. Add required files:
   ```
   plugins/your-plugin/
   ├── .claude-plugin/
   │   └── plugin.json    # Plugin manifest
   ├── README.md          # Documentation
   ├── agents/            # Agent definitions (optional)
   ├── commands/          # Slash commands (optional)
   └── skills/            # Skills (optional)
   ```
3. Register in `.claude-plugin/marketplace.json`
4. Submit a pull request

### plugin.json Structure

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/username"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "agents": ["./agents/*.md"],
  "commands": ["./commands/*.md"],
  "skills": ["./skills/*/SKILL.md"]
}
```

## Troubleshooting

### Marketplace Not Found

```bash
# Verify the URL
claude /plugin marketplace add https://github.com/zircote/marketplace

# Or use shorthand
claude /plugin marketplace add zircote/marketplace
```

### Plugin Installation Fails

1. Ensure marketplace is added first
2. Check internet connectivity
3. For NSIP plugin, verify `uv` is installed: `uv --version`

### MCP Server Issues (NSIP)

```bash
# Test MCP server manually
uvx --from git+https://github.com/epicpast/nsip-api-client.git nsip-mcp-server

# Re-enable plugin
claude /plugin disable nsip
claude /plugin enable nsip
```

## Platform Support

All plugins work identically across:
- Claude Code CLI (terminal)
- Claude Code VS Code extension
- 100% feature parity

## Support

- **Repository:** https://github.com/zircote/marketplace
- **Issues:** https://github.com/zircote/marketplace/issues

## License

MIT License. Individual plugins may have their own licenses - see each plugin's README.

## Version

**Marketplace:** 1.11.0

---

*This marketplace structure follows patterns from [claude-code-templates](https://github.com/davila7/claude-code-templates).*
