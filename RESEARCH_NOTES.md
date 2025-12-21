# Research Notes: Zircote Marketplace

## Marketplace Overview

**Version:** 1.5.0
**Type:** Claude Code Plugin Marketplace
**Structure:** Central registry with local and external plugins

### Plugin Registry (marketplace.json)

| Plugin | Source | Description |
|--------|--------|-------------|
| datadog | Local (`./plugins/datadog`) | DataDog API specialists |
| document-skills | Local (`./plugins/document-skills`) | PDF/DOCX/XLSX/PPTX processing |
| gh | Local (`./plugins/gh`) | GitHub/Git workflow commands |
| nsip | Local (`./plugins/nsip`) | NSIP sheep breeding data (MCP) |
| zircote | Local (`./plugins/zircote`) | Agent library (116 agents, 54 skills) |
| claude-spec | External (zircote/claude-spec) | Project specification lifecycle |
| memory-capture | External (zircote/git-notes-memory-manager) | Git-backed memory system |
| git-adr | External (zircote/git-adr) | Architecture Decision Records |

---

## Plugin Analysis: zircote (z)

**Version:** 1.0.1
**Published Name:** `z`

### Agent Categories (10 directories, 107+ agents)

| Category | Directory | Agent Count |
|----------|-----------|-------------|
| Core Development | 01-core-development | 11 |
| Language Specialists | 02-language-specialists | 23 |
| Infrastructure | 03-infrastructure | 12 |
| Quality & Security | 04-quality-security | 12 |
| Data & AI | 05-data-ai | 12 |
| Developer Experience | 06-developer-experience | 10 |
| Specialized Domains | 07-specialized-domains | 11 |
| Business & Product | 08-business-product | 10 |
| Meta Orchestration | 09-meta-orchestration | 8 |
| Research & Analysis | 10-research-analysis | 6 |
| Templates | templates | 1 (opus-4-5-template) |

### Skills (54 total)

Categories include:
- Anthropic-specific: `anthropic-architect`, `anthropic-prompt-engineer`
- Development: `frontend-development`, `backend-development`, `devops`, `databases`
- AI/Design: `ai-multimodal`, `aesthetic`, `frontend-design`
- Debugging: 5 nested skills under `debugging/`
- Problem-solving: 6 nested skills under `problem-solving/`
- Productivity: `changelog-generator`, `skill-creator`, `mcp-builder`

### Commands (4)

1. `/explore` - Codebase exploration with parallel subagents
2. `/deep-research` - Multi-phase research protocol
3. `/code:review` - Comprehensive code review (6 specialist agents)
4. `/code:review-fix` - Interactive remediation

---

## Plugin Analysis: gh (GitHub Ecosystem)

**Version:** 0.2.0
**Published Name:** `gh`

### Commands (10)

| Command | Purpose |
|---------|---------|
| `/git:cm` | Stage and commit with conventional commits |
| `/git:cp` | Stage, commit, push in one operation |
| `/git:pr` | Create pull request via gh CLI |
| `/git:fr` | Fetch and rebase |
| `/git:sync` | Full sync: fetch, rebase, push |
| `/git:ff` | Fast-forward merge only |
| `/git:prune` | Clean up stale branches |
| `/gh:copilot-onboard` | Generate Copilot config from CLAUDE.md |
| `/gh:onboard` | Onboard new repository |
| `/gh:migrate` | Migration tooling |

### Agents (1)

- `copilot-assistant` - Bridge Claude Code ↔ GitHub Copilot

### Skills (1)

- `ecosystem` - GitHub Actions, templates, CODEOWNERS, Dependabot

### Supporting Files

- `scripts/`: Python utilities for project detection and config generation
- `references/`: Workflow templates (Python, Go, TypeScript)

---

## Plugin Analysis: nsip (NSIP Sheep Breeding)

**Version:** 1.3.1
**Author:** epic pastures

### MCP Server Configuration

```json
{
  "nsip": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/epicpast/nsip-api-client.git", "nsip-mcp-server"]
  }
}
```

### Commands (10)

| Command | Purpose |
|---------|---------|
| `/nsip:consult` | Expert breeding consultation |
| `/nsip:discover` | Discover data patterns |
| `/nsip:health` | API health check |
| `/nsip:lineage` | Pedigree tree |
| `/nsip:lookup` | Animal lookup by LPN ID |
| `/nsip:profile` | Complete animal profile |
| `/nsip:progeny` | Offspring list |
| `/nsip:search` | Search with filters |
| `/nsip:test-api` | Test API connectivity |
| `/nsip:traits` | Trait ranges by breed |

### Agents (1)

- `shepherd` - Expert sheep breeding advisor

### Hook System (14 scripts across 4 lifecycle events)

#### PreToolUse Hooks
| Tool Matcher | Hooks |
|--------------|-------|
| `nsip_get_animal` | lpn_validator, trait_dictionary |
| `nsip_search_by_lpn` | lpn_validator, trait_dictionary |
| `nsip_get_lineage` | lpn_validator |
| `nsip_get_progeny` | lpn_validator |
| `nsip_search_animals` | breed_context_injector, trait_dictionary |
| `nsip_get_trait_ranges` | breed_context_injector, trait_dictionary |

#### PostToolUse Hooks
| Tool Matcher | Hooks |
|--------------|-------|
| `mcp__nsip__.*` (all) | auto_retry, error_notifier |
| `nsip_get_animal` | fallback_cache, query_logger, result_cache, breeding_report |
| `nsip_search_by_lpn` | fallback_cache, query_logger, result_cache, breeding_report |
| `nsip_search_animals` | fallback_cache, query_logger, csv_exporter |
| `nsip_get_lineage` | fallback_cache, query_logger, result_cache, pedigree_visualizer |
| `nsip_get_progeny` | fallback_cache, query_logger, result_cache |

#### SessionStart Hooks
- `api_health_check.py`

#### UserPromptSubmit Hooks
- `smart_search_detector.py`
- `comparative_analyzer.py`

### Test Suite

- Unit tests: session_start, pre_tool_use, post_tool_use, user_prompt_submit
- Integration tests: error_handling, workflows
- Fixtures: mock_api_responses.json, sample_lpn_ids.json, sample_prompts.json

---

## Plugin Analysis: document-skills

**Version:** 1.0.0

### Skills (4)

| Skill | Capabilities |
|-------|-------------|
| pdf | Text extraction, table detection, OCR, metadata, form fields |
| docx | Full text extraction, style preservation, comments, revisions |
| xlsx | Cell/formula reading, named ranges, charts, conditional formatting |
| pptx | Slide content, speaker notes, shapes, animations |

---

## Plugin Analysis: datadog

**Version:** 1.0.0

### Agents (2)

| Agent | Focus |
|-------|-------|
| datadog-pro | DataDog API specialist (v2.45.0+) |
| datadog-api-expert | Monitor/dashboard creation, query syntax |

---

## Patterns Identified

### 1. Plugin Manifest Pattern (plugin.json)

Required fields:
- `name`: Plugin identifier (used for installation)
- `version`: Semver version
- `description`: Brief description
- `author`: Object with `name`, optional `email`, `url`
- `license`: License identifier

Optional arrays:
- `agents`: Paths to agent markdown files
- `skills`: Paths to SKILL.md files
- `commands`: Paths to command markdown files
- `mcpServers`: Paths to MCP configuration files
- `hooks`: Object with lifecycle event configurations
- `references`: Reference documentation
- `scripts`: Supporting scripts

### 2. Agent Definition Pattern

Agents are markdown files with YAML frontmatter:
- Location: `agents/<category>/<name>.md`
- Naming: kebab-case (e.g., `frontend-developer.md`)

### 3. Skill Definition Pattern

Skills use `SKILL.md` as the canonical file:
- Location: `skills/<skill-name>/SKILL.md`
- May include supporting scripts in `scripts/` subdirectory

### 4. Command Definition Pattern

Commands are markdown files:
- Location: `commands/<name>.md` or `commands/<namespace>/<name>.md`
- Invocation: `/<namespace>:<command>` or `/<command>`

### 5. Hook Implementation Pattern (NSIP reference)

- Scripts in `hooks/scripts/*.py`
- Use `${CLAUDE_PLUGIN_ROOT}` for relative paths
- Organize by lifecycle event: PreToolUse, PostToolUse, SessionStart, UserPromptSubmit
- Use matchers for tool-specific hooks

---

## External Dependencies

### GitHub Repositories

1. `zircote/claude-spec` - Project specification lifecycle
2. `zircote/git-notes-memory-manager` - Git-backed memory
3. `zircote/git-adr` - Architecture Decision Records
4. `epicpast/nsip-api-client` - NSIP MCP server

### Runtime Dependencies

- `uv` / `uvx` - Python package manager (for NSIP MCP server)
- `gh` - GitHub CLI (for git plugin commands)
- Various Python libraries in skill scripts

---

## Open Questions

1. How are external plugins (claude-spec, memory-capture, git-adr) versioned in marketplace.json?
2. What is the relationship between `copilot` plugin (deleted) and `gh` plugin (new)?
3. Are there any shared utilities between plugins?

---

*Last Updated: Phase 2 Evidence Gathering*
