---
name: adr-new
description: Create a new Architectural Decision Record
argument-hint: "<title>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Create New ADR

Create a new Architectural Decision Record with the specified title.

## Process

1. **Read configuration** from `.claude/adr.local.md` if present
2. **Determine next ADR number** by scanning existing ADRs
3. **Ask for format** if not specified in config (default: MADR)
4. **Gather context** through elicitation questions
5. **Create ADR file** using selected template
6. **Update index** (README.md) with new entry

## Configuration Reading

Check for `.claude/adr.local.md`:
- `adr_paths`: Where to create the ADR
- `default_format`: Template format (madr, nygard, y-statement, etc.)
- `numbering.pattern`: How to number (4digit, 3digit, date)
- `madr_variant`: Which MADR variant (full, minimal, bare)

## Numbering Logic

1. Scan existing ADRs in the configured directory
2. Extract highest number
3. Increment by 1
4. Format according to `numbering.pattern`:
   - `4digit`: 0001, 0002, etc.
   - `3digit`: 001, 002, etc.
   - `date`: 20250115, etc.
   - `custom`: Apply custom pattern

## Title Slug Generation

Convert title to slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Truncate if too long

Example: "Use PostgreSQL for Primary Storage" → "use-postgresql-for-primary-storage"

## Elicitation

If argument is just a title, ask clarifying questions:

1. **Context**: "What is the problem or situation requiring this decision?"
2. **Options** (if using MADR): "What alternatives are being considered?"
3. **Decision Drivers**: "What factors are influencing this decision?"

Use AskUserQuestion for structured input when helpful.

## Template Selection

Use template from `${CLAUDE_PLUGIN_ROOT}/templates/{format}/`:
- `madr/adr-template-full.md`
- `madr/adr-template-minimal.md`
- `structured-madr/adr-template.md` (comprehensive with frontmatter and audit)
- `nygard/adr-template.md`
- `y-statement/adr-template.md`
- `alexandrian/adr-template.md`
- `business-case/adr-template.md`
- `tyree-akerman/adr-template.md`

## File Creation

Create file at: `{adr_path}/{number}-{slug}.md`

Replace template placeholders:
- `{TITLE}` → User-provided title
- `{NUMBER}` → Generated number
- `{DATE}` → Current date (YYYY-MM-DD)
- `{STATUS}` → "proposed" (initial status)

## Index Update

After creating ADR, update the README.md index:
1. Read existing README.md
2. Find ADR table
3. Add new entry
4. Write updated README.md

## Output

After creation, report:
- File path created
- ADR number assigned
- Next steps (fill in sections, submit for review)

## Error Handling

- If no ADR directory exists, offer to create it
- If configuration is missing, use defaults
- If title is empty, prompt for it
