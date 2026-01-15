---
name: adr-setup
description: Interactive setup for ADR configuration in this project
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
---

# ADR Setup

Interactive configuration wizard for setting up ADR management in the current project.

## Process

1. **Check for existing configuration**
2. **Gather preferences** through interactive questions
3. **Create configuration file** (`.claude/adr.local.md`)
4. **Create ADR directory** if needed
5. **Initialize README.md index**
6. **Create first ADR** (optional)

## Existing Configuration Check

Check for:
- `.claude/adr.local.md` - Plugin configuration
- `docs/adr/` or other ADR directories
- Existing ADRs

If found, ask:
- Update existing configuration?
- Keep current settings and just fill gaps?

## Configuration Questions

Use AskUserQuestion for structured input:

### ADR Directory
"Where should ADRs be stored?"
- docs/adr/ (recommended)
- docs/decisions/
- architecture/decisions/
- Custom path

### Template Format
"Which ADR template format?"
- MADR (recommended)
- Structured MADR (comprehensive with frontmatter and audit sections)
- Nygard
- Y-Statement
- Alexandrian
- Business Case
- Tyree-Akerman

### MADR Variant (if MADR selected, not applicable for Structured MADR)
"Which MADR template variant?"
- Full (recommended)
- Minimal
- Bare
- Bare-minimal

### Numbering
"How should ADRs be numbered?"
- 4-digit sequential (recommended): 0001, 0002
- 3-digit sequential: 001, 002
- Date-based: 20250115
- Custom pattern

### Status Workflow
"Which status workflow?"
- Standard: proposed → accepted → deprecated → superseded
- Simple: draft → accepted → superseded
- Extended: include rejected, implemented
- Custom

### Git Integration
"Enable git integration?"
- Yes - track changes, suggest commits
- No - manual git management

## Create Configuration

Generate `.claude/adr.local.md`:

```markdown
---
adr_paths:
  - {chosen_path}

default_format: {format}
madr_variant: {variant}

numbering:
  pattern: "{pattern}"
  start_from: 1

statuses:
  workflow:
    - proposed
    - accepted
    - deprecated
    - superseded
  allow_rejected: true

git:
  enabled: {true/false}
  auto_commit: false
  commit_template: "docs(adr): {action} ADR-{id} {title}"
---

# Project ADR Context

{Project name} Architecture Decision Records

## Decision Process

- ADRs are proposed via pull request
- Team review required before acceptance
- Architecture lead has final approval
```

## Create ADR Directory

If directory doesn't exist:
```bash
mkdir -p {adr_path}
```

## Initialize Index

Create README.md with:
- Project header
- Empty ADR table
- Status legend
- Usage instructions

Use template from `${CLAUDE_PLUGIN_ROOT}/templates/README-index.md`

## First ADR (Optional)

"Would you like to create your first ADR?"

If yes, guide through creating ADR-0001:
- Suggest: "Use MADR for Architectural Decision Records"
- Or custom title from user

## Output

Report setup complete:
- Configuration file: `.claude/adr.local.md`
- ADR directory: `{adr_path}/`
- Index file: `{adr_path}/README.md`
- First ADR: `{path}` (if created)

## Next Steps

Suggest next steps:
- Run `/adr-new` to create your first ADR
- Review configuration in `.claude/adr.local.md`
- Add `.claude/adr.local.md` to `.gitignore` if needed
