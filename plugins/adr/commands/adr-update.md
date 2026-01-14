---
name: adr-update
description: Update an existing ADR (status, content, or metadata)
argument-hint: "<adr-id> [--status=<status>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Update ADR

Update an existing Architectural Decision Record's status, content, or metadata.

## Process

1. **Parse arguments** to identify ADR and update type
2. **Find ADR file** by ID
3. **Read current content**
4. **Apply updates** based on arguments
5. **Update index** if needed
6. **Git commit** if configured

## Argument Parsing

Supported arguments:
- `<adr-id>`: ADR number (e.g., "0001", "1", "ADR-0001")
- `--status=<status>`: Update status (accepted, rejected, deprecated, superseded)
- `--add-driver=<driver>`: Add a decision driver
- `--add-consequence=<consequence>`: Add a consequence
- No status flag: Open interactive update mode

## ADR Resolution

Find ADR by flexible matching:
- "1" → finds 0001-*.md
- "0001" → finds 0001-*.md
- "ADR-0001" → finds 0001-*.md
- "use-postgresql" → finds *use-postgresql*.md

## Status Update

When updating status:

### To "accepted"
- Update Status section
- Add acceptance date if not present
- Optionally add decision makers

### To "rejected"
- Update Status section
- Prompt for rejection reason
- Add rejection date

### To "deprecated"
- Update Status section
- Prompt for deprecation reason
- Suggest creating successor ADR

### To "superseded"
- Require superseding ADR ID
- Update Status section
- Add "Superseded by ADR-XXXX"
- Update superseding ADR with "Supersedes ADR-YYYY"

## Content Updates

For interactive updates, use AskUserQuestion:
- What section to update?
- What is the new content?
- Any additional changes?

## Index Update

After status change:
1. Read README.md index
2. Update status in ADR table
3. Write updated README.md

## Git Integration

If git integration enabled:
```bash
git add {adr_file}
git commit -m "docs(adr): update ADR-{id} status to {status}"
```

## Output

Report changes made:
- Previous status → New status
- Sections modified
- Related ADRs updated
- Git commit created (if applicable)

## Validation

Before updating:
- Verify ADR exists
- Validate status transition is allowed
- Check for missing required fields
