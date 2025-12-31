# Zircote Claude Marketplace

A curated collection of Claude Code plugins featuring specialized agents, development workflows, monitoring integrations, and document processing capabilities.

## Overview

This marketplace provides 10 plugins for Claude Code, ranging from domain-specific expert agents to productivity-enhancing workflow tools. All plugins work identically across Claude Code CLI and VS Code extension.

## Quick Start

```bash
# Add this marketplace to Claude Code
claude /plugin marketplace add zircote/marketplace

# List available plugins
claude /plugin list

# Install a specific plugin
claude /plugin install zircote    # 116 specialized agents
claude /plugin install gh         # Git workflow + Copilot onboarding
claude /plugin install lsp-tools  # LSP-first code intelligence
claude /plugin install datadog    # DataDog monitoring agents
claude /plugin install document-skills  # PDF/DOCX/XLSX/PPTX processing
claude /plugin install nsip       # Sheep breeding data (NSIP)
claude /plugin install cs         # Project specification lifecycle
claude /plugin install markdown-lsp  # LSP tools + diagnostic hooks for Markdown
claude /plugin install subcog     # Git-backed memory system
claude /plugin install git-adr    # ADR management via git notes
```

## Available Plugins

### z - Agent Library

**116 specialized Opus 4.5 agents** organized by domain, plus 54 skills and powerful commands.

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

**Commands:**
- `/explore <path|pattern|question>` - Exhaustive codebase exploration with parallel subagents
- `/deep-research <topic>` - Multi-phase research protocol with structured deliverables
- `/code:review [path|--focus=security]` - Comprehensive code review with 6 specialist agents
- `/code:review-fix [--quick]` - Interactive remediation of code review findings

**Skills:** 54 specialized skills including `claude-code`, `anthropic-prompt-engineer`, `databases`, `devops`, `debugging`, and more.

```bash
claude /plugin install z
```

---

### gh - Git Workflow & GitHub Ecosystem

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
claude /plugin install gh
```

---

### lsp-tools - LSP-First Code Intelligence

LSP-first code intelligence for Claude Code - enforces Language Server Protocol usage for all code operations.

**Command:**
| Command | Description |
|---------|-------------|
| `/lsp-setup` | Copies language-specific hooks to project's `.claude/hooks.json` |

**Skill:** `lsp-enable` - Enforces the "Three Iron Laws" of LSP-first development:
1. **Never guess** - Always use LSP for definitions, references, and symbols
2. **Never assume** - Verify imports, types, and dependencies via LSP
3. **Never skip** - Run LSP diagnostics before and after every change

**Language Support (12 languages):**
| Language | LSP Server | Key Operations |
|----------|------------|----------------|
| TypeScript/JavaScript | typescript-language-server | Go to definition, find references, rename |
| Python | pylsp, pyright | Type checking, import resolution |
| Go | gopls | Package navigation, interface implementation |
| Rust | rust-analyzer | Trait resolution, macro expansion |
| Java | jdtls | Maven/Gradle integration, refactoring |
| Kotlin | kotlin-language-server | Null safety, coroutine support |
| C# | omnisharp | .NET integration, NuGet packages |
| C/C++ | clangd | Header navigation, compile commands |
| Ruby | solargraph | Gem resolution, YARD documentation |
| PHP | intelephense | Composer packages, PSR standards |
| HTML/CSS | vscode-html-language-server | Class references, selector validation |
| LaTeX | texlab | Citation resolution, reference checking |

**Reference Documentation:**
- LSP Operations Guide
- Enforcement Protocol
- Decision Matrix
- Setup Verification

```bash
claude /plugin install lsp-tools
```

---

### markdown-lsp - Markdown LSP Tools

LSP tools plugin and diagnostic hooks for Markdown files.

**External Source:** [zircote/markdown-lsp](https://github.com/zircote/markdown-lsp)

**Features:**
- LSP-powered Markdown editing and validation
- Diagnostic hooks for Claude Code
- Syntax checking and link validation

```bash
claude /plugin install markdown-lsp
```

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
claude /plugin install datadog
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
claude /plugin install document-skills

# Usage
claude "Analyze the contents of report.pdf"
claude "Extract data from sales.xlsx"
```

---

### nsip - NSIP Sheep Breeding

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
claude /plugin install nsip
```

**Prerequisites:** `uv` package manager (https://docs.astral.sh/uv/)

---

### cs - Project Specification Lifecycle

Strategic project planning, implementation tracking, and retrospectives.

**External Source:** [zircote/claude-spec](https://github.com/zircote/claude-spec)

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
claude /plugin install cs
```

---

## Marketplace Structure

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Central plugin registry
├── plugins/
│   ├── zircote/                  # Agent library (116 agents, 54 skills)
│   │   ├── agents/               # Organized by domain (01-10)
│   │   └── skills/               # Development skills
│   ├── gh/                       # Git workflow + Copilot
│   │   ├── agents/               # copilot-assistant
│   │   ├── commands/             # cm, cp, pr, fr, sync, ff, prune, migrate
│   │   └── skills/               # GitHub ecosystem
│   ├── lsp-tools/                # LSP-first code intelligence
│   │   ├── commands/             # lsp-setup
│   │   └── skills/               # lsp-enable
│   ├── datadog/                  # Monitoring integration
│   │   └── agents/               # datadog-pro, datadog-api-expert
│   ├── document-skills/          # Document processing
│   │   ├── pdf/                  # PDF skill
│   │   ├── docx/                 # Word skill
│   │   ├── xlsx/                 # Excel skill
│   │   └── pptx/                 # PowerPoint skill
│   └── nsip/                     # Sheep breeding data
│       ├── agents/               # shepherd
│       ├── commands/             # 10 commands
│       └── hooks/                # 14 hooks
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

**Marketplace:** 1.6.0

---

*This marketplace structure follows patterns from [claude-code-templates](https://github.com/davila7/claude-code-templates).*
