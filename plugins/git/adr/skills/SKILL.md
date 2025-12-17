---
name: git-adr
version: 1.1.0
description: >
  ADRs as Machine Memory - Manage Architecture Decision Records using git-adr, enabling
  ADRs to serve as persistent project context that survives across Claude sessions.
  Auto-loads ADR summaries at session start, recalls past decisions naturally, and
  captures new decisions from conversation. Also executes all git-adr CLI commands
  (init, new, edit, list, show, search, sync, supersede, link, attach, stats, export),
  generates content in any format (MADR, Nygard, Y-Statement, Alexandrian, Business Case,
  Planguage), and teaches ADR best practices.
triggers:
  - architecture decisions
  - ADR
  - decision record
  - what did we decide
  - project decisions
  - record this decision
  - document this decision
---

# git-adr: ADRs as Machine Memory

Use ADRs as persistent project context - decisions that inform AI assistance across sessions.

## CRITICAL RULES

**NEVER modify user configuration without explicit permission.**

- Do NOT run `git-adr config --set` or `git config adr.*` commands unless the user explicitly asks to change config
- Do NOT "check" config by running set commands - use `git config --get` or `git-adr config --get` only
- Before using AI features, READ the existing config with `git config --local --list | grep adr` - do NOT assume or set values
- If AI config is missing, ASK the user what provider/model they want - do NOT set defaults
- The user's config is sacred - treat it as read-only unless explicitly told otherwise

## Installation

### Install git-adr CLI

```bash
# macOS (Homebrew) - Recommended
brew tap zircote/git-adr && brew install git-adr

# Any platform (pip)
pip install git-adr

# With AI features (suggest, draft, summarize, ask)
pip install 'git-adr[ai]'
```

Verify installation:
```bash
git adr --version
```

### Skill Location

This skill is located at:
```
~/.claude/skills/git-adr/
├── SKILL.md                    # This file (entry point)
├── references/
│   ├── commands.md            # Full command reference
│   ├── configuration.md       # Config options
│   ├── best-practices.md      # ADR writing guidance
│   ├── workflows.md           # Common workflow patterns
│   ├── search-patterns.md     # Search & recall reference
│   └── formats/               # ADR format templates
│       ├── madr.md
│       ├── nygard.md
│       ├── y-statement.md
│       ├── alexandrian.md
│       ├── business-case.md
│       └── planguage.md
└── workflows/
    ├── session-start.md       # Auto-context loading behavior
    ├── decision-capture.md    # Create ADRs from conversation
    └── decision-recall.md     # Find past decisions
```

Claude Code automatically discovers this skill when the trigger phrases are detected.

## Auto-Context Loading

**At session start in any git repository**, automatically check for ADRs and load context:

```bash
# Check if git-adr is available and ADRs exist
if git adr --version &>/dev/null && git notes --ref=adr list &>/dev/null 2>&1; then
  git adr list --format=yaml --status=active 2>/dev/null
fi
```

**Display format** (include in your context, not shown to user):
```yaml
# Project ADRs (N active decisions)
- id: 20251216-use-postgresql
  title: "Use PostgreSQL for Persistence"
  status: accepted
  date: 2025-12-16
  tags: [database, backend]
```

This enables you to:
- Reference ADRs naturally in responses ("As decided in ADR-001, we use PostgreSQL...")
- Suggest code consistent with documented decisions
- Warn when user requests conflict with established decisions

For full context loading behavior, see [workflows/session-start.md](workflows/session-start.md).

## Trigger Phrases

### Context & Memory Operations

| User Says | Action |
|-----------|--------|
| "What did we decide about X?" | Search ADRs, show relevant decisions |
| "Show me the database decision" | Hydrate full ADR content with `git adr show` |
| "Record this decision" | Extract context from conversation, create ADR |
| "What decisions exist?" | List all ADRs with `git adr list` |
| "Any decisions about caching?" | Search with `git adr search caching` |

### Decision Capture

When user says "record this decision" or "create an ADR from this":
1. Summarize the decision from conversation
2. Identify: context, options considered, chosen option, consequences
3. Present draft for review
4. Execute `git adr new "<title>"` with approved content

For guided creation workflow, see [workflows/decision-capture.md](workflows/decision-capture.md).

## What is git-adr?

git-adr is a command-line tool that manages ADRs using **git notes** instead of files:
- **Non-intrusive**: ADRs don't clutter the working tree
- **Portable**: Travel with git history
- **Linkable**: Associate decisions with commits
- **Syncable**: Push/pull like regular git content

## Quick Command Reference

| Command | Description |
|---------|-------------|
| `git adr init` | Initialize ADR tracking |
| `git adr new "<title>"` | Create new ADR |
| `git adr list` | List all ADRs |
| `git adr show <id>` | Display an ADR |
| `git adr edit <id>` | Edit an ADR |
| `git adr search "<query>"` | Search ADRs |
| `git adr supersede <old-id> "<title>"` | Supersede a decision |
| `git adr link <id> <commit>` | Link ADR to commit |
| `git adr sync push` | Push ADRs to remote |
| `git adr sync pull` | Pull ADRs from remote |
| `git adr stats` | Show statistics |
| `git adr export` | Export to files |
| `git adr config list` | Show configuration |

For full command documentation, see [references/commands.md](references/commands.md).

## Execution Patterns

### Before Executing Commands

Always verify the environment:

```bash
# 1. Check git-adr is installed
git adr --version

# 2. Verify in a git repository
git rev-parse --is-inside-work-tree

# 3. For most commands, check if initialized
git notes --ref=adr list 2>/dev/null || echo "Not initialized"
```

### Error Handling

#### git-adr Not Installed

Detection:
```bash
git adr --version &>/dev/null || echo "NOT_INSTALLED"
```

Response:
```
git-adr is not installed. Install with:

  # macOS (Homebrew) - Recommended
  brew tap zircote/git-adr && brew install git-adr

  # Any platform (pip)
  pip install git-adr

  # With AI features
  pip install 'git-adr[ai]'

After installation, verify with: git adr --version
```

#### Not in a Git Repository

Detection:
```bash
git rev-parse --is-inside-work-tree 2>/dev/null || echo "NOT_GIT_REPO"
```

Response:
```
git-adr requires a git repository.

If this is a new project:
  git init
  git adr init

If you expected to be in a repo, check your current directory:
  pwd
  ls -la
```

#### ADRs Not Initialized

Detection:
```bash
git notes --ref=adr list 2>/dev/null || echo "NOT_INITIALIZED"
```

Response:
```
ADR tracking not initialized in this repository.

Initialize with:
  git adr init

This creates the git notes reference for storing ADRs.
```

#### ADR Not Found

Detection: `git adr show <id>` returns error

Response:
```
ADR not found: "<id>"

This could mean:
- Typo in the ID (format: YYYYMMDD-slug-from-title)
- ADR was deleted or never existed
- ADR exists on remote but not locally

Try:
- List all ADRs: git adr list
- Search by keyword: git adr search "<keyword>"
- Pull from remote: git adr sync pull
```

#### Permission Denied (Git Notes)

Detection: Write operation fails with permission error

Response:
```
Permission denied when writing to git notes.

Possible causes:
- Repository is read-only or on a read-only filesystem
- Git hooks preventing modification
- Repository corruption

Try:
- Check repository permissions: ls -la .git/
- Verify git config: git config --list
- Check hooks: ls .git/hooks/
```

#### AI Commands Without Config

Detection:
```bash
git config --get adr.ai.provider || echo "NO_AI_CONFIG"
```

Response:
```
AI features require configuration.

Current AI config:
  git config --local --list | grep adr.ai

To configure (example with Anthropic):
  git adr config adr.ai.provider anthropic
  git adr config adr.ai.model claude-3-5-sonnet-20241022

Supported providers: openai, anthropic, google, ollama

Note: AI features require the [ai] extras:
  pip install 'git-adr[ai]'
```

#### Sync Conflicts

Detection: `git adr sync` reports merge conflict

Response:
```
ADR sync conflict detected.

Options:
1. Keep local version:
   git adr sync pull --force

2. Keep remote version:
   git notes --ref=adr merge --strategy=theirs origin/refs/notes/adr

3. Manual resolution:
   - Export conflicting ADR: git adr show <id> > local.md
   - Pull remote: git adr sync pull --force
   - Compare and manually merge content

After resolution, push:
  git adr sync push
```

#### No ADRs Found (Empty Repository)

Detection: `git adr list` returns empty

Response:
```
No ADRs found in this repository.

Create your first decision record:
  git adr new "Your First Decision"

Or import existing ADRs from files:
  git adr import ./docs/decisions/

For onboarding to ADR best practices:
  git adr onboard --quick
```

## Format Selection

### Reading Project Configuration

Always check the project's configured template before generating content:

```bash
# Get configured template (defaults to madr if not set)
TEMPLATE=$(git config --get adr.template 2>/dev/null || echo "madr")
echo "Using template: $TEMPLATE"
```

### Available Formats

| Format | Config Value | Best For |
|--------|--------------|----------|
| MADR | `madr` | General purpose, option analysis (default) |
| Nygard | `nygard` | Quick, minimal decisions |
| Y-Statement | `y-statement` | Ultra-concise, single sentence |
| Alexandrian | `alexandrian` | Pattern-based, forces analysis |
| Business Case | `business` | Stakeholder approval, ROI |
| Planguage | `planguage` | Measurable quality requirements |

For format templates, see [references/formats/](references/formats/).

## Creating ADRs

### Workflow

1. **Check format**: Read `adr.template` config
2. **Load template**: Read appropriate format from references/formats/
3. **Generate content**: Fill template with user's context
4. **Execute command**: `git adr new "<title>"` with content

### Example: Creating a MADR

```bash
# Create ADR (opens editor with template)
git adr new "Use PostgreSQL for primary database"

# Or with specific format override
git adr new "Use PostgreSQL" --template nygard
```

When generating content, follow the structure in the appropriate format template.

## Common Workflows

### New Project Setup

```bash
git adr init
git adr new "Record architecture decisions"
git adr sync push
```

### Team Collaboration

```bash
git adr sync pull          # Get latest
git adr new "Add caching"  # Create decision
git adr sync push          # Share with team
```

### Linking to Implementation

```bash
# After implementing a decision
git adr link 20250115-use-postgresql abc1234

# View linked commits
git adr show 20250115-use-postgresql
```

### Superseding Decisions

```bash
# When replacing a decision
git adr supersede 20250101-use-mysql "Migrate to PostgreSQL"
```

For more workflows, see [references/workflows.md](references/workflows.md).

## Configuration

Common configuration options:

```bash
# Set default template
git adr config adr.template madr

# Set editor
git adr config --global adr.editor "code --wait"

# Enable auto-sync
git adr config adr.sync.auto_push true
git adr config adr.sync.auto_pull true
```

For all configuration options, see [references/configuration.md](references/configuration.md).

## ADR Best Practices

### When to Write an ADR

Write an ADR for decisions that are:
- **Significant**: Affects architecture or design
- **Structural**: Changes system organization
- **Hard to reverse**: Would require substantial effort to change

### What Makes a Good ADR

- **Clear context**: Explains the situation and constraints
- **Explicit decision**: States what was decided
- **Documented consequences**: Lists positive, negative, and neutral effects
- **Alternatives considered**: Shows options evaluated

### Common Mistakes

- Too detailed (specification, not decision)
- Too brief (no context or rationale)
- Not updating status when decisions change
- Writing long after the decision was made

For complete guidance, see [references/best-practices.md](references/best-practices.md).

## Progressive Loading Guide

Load reference files based on user intent:

| User Intent | Load File |
|-------------|-----------|
| Session start (auto) | `workflows/session-start.md` |
| "Create an ADR" | `references/formats/{template}.md` |
| "Record this decision" | `workflows/decision-capture.md` |
| "What did we decide about X?" | `workflows/decision-recall.md` |
| "What commands are available?" | `references/commands.md` |
| "Configure git-adr" | `references/configuration.md` |
| "What is an ADR?" | `references/best-practices.md` |
| "Set up for my team" | `references/workflows.md` |

## ADR Content Generation

When generating ADR content:

1. **Read the project's configured format**
2. **Load the corresponding template** from references/formats/
3. **Ask clarifying questions** if context is insufficient:
   - What problem are you solving?
   - What alternatives did you consider?
   - What are the constraints?
4. **Fill the template** with the gathered information
5. **Execute the command** to create the ADR

### Content Quality Checklist

Before creating an ADR, ensure:
- [ ] Context explains the situation clearly
- [ ] Decision is explicitly stated
- [ ] Consequences are categorized (positive/negative/neutral)
- [ ] Alternatives were considered (for MADR format)
- [ ] Status is appropriate (proposed/accepted)

## Reference Files

### Machine Memory (workflows/)

| File | Purpose |
|------|---------|
| `workflows/session-start.md` | Auto-context loading behavior |
| `workflows/decision-capture.md` | Guided ADR creation from conversation |
| `workflows/decision-recall.md` | Finding past decisions |

### Command & Config (references/)

| File | Purpose |
|------|---------|
| `references/commands.md` | Full command documentation |
| `references/configuration.md` | All config options |
| `references/best-practices.md` | ADR writing guidance |
| `references/workflows.md` | Common workflow patterns |

### Format Templates (references/formats/)

| File | Purpose |
|------|---------|
| `references/formats/madr.md` | MADR template |
| `references/formats/nygard.md` | Nygard template |
| `references/formats/y-statement.md` | Y-Statement template |
| `references/formats/alexandrian.md` | Alexandrian template |
| `references/formats/business-case.md` | Business Case template |
| `references/formats/planguage.md` | Planguage template |
