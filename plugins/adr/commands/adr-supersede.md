---
name: adr-supersede
description: Create a new ADR that supersedes an existing one
argument-hint: "<existing-adr-id> <new-title>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Supersede ADR

Create a new ADR that supersedes an existing one, with proper bidirectional linking.

## Process

1. **Parse arguments** to get existing ADR ID and new title
2. **Verify existing ADR** exists and is supersedable
3. **Gather supersession context** (why superseding)
4. **Create new ADR** with "Supersedes ADR-XXXX"
5. **Update old ADR** status to "superseded" with "Superseded by ADR-YYYY"
6. **Update index** with both changes
7. **Git commit** if configured

## Argument Parsing

Required arguments:
- `<existing-adr-id>`: The ADR being superseded
- `<new-title>`: Title for the new ADR

## Pre-Supersession Checks

Verify the existing ADR:
- Exists
- Is in "accepted" or "deprecated" status
- Is not already superseded

If already superseded, warn and suggest:
- Supersede the current successor instead
- Or proceed with supersession chain

## Context Gathering

Ask for supersession context:
1. **Reason**: "Why is the original ADR being superseded?"
2. **Changes**: "What key changes does the new decision make?"
3. **Migration**: "Is there a migration path from old to new?"

## New ADR Creation

Create new ADR with:
- Next sequential number
- User-provided title
- Status: "proposed" (or "accepted" if immediate)
- Supersedes section linking to old ADR
- Context includes reference to superseded decision

Template addition:
```markdown
## Status

Proposed

Supersedes [ADR-{old_id}](./0001-old-title.md)

## Context and Problem Statement

This decision supersedes ADR-{old_id} because {reason}.

{Additional context}
```

## Old ADR Update

Update the superseded ADR:
```markdown
## Status

Superseded by [ADR-{new_id}](./0002-new-title.md)

**Note**: This ADR has been superseded. See ADR-{new_id} for the current decision.
```

## Index Update

Update README.md:
1. Add new ADR entry
2. Update old ADR status to "superseded"
3. Add supersession relationship in "Related" column if present

## Supersession Chain

If superseding an ADR that itself superseded another:
- Document full chain in new ADR
- Update "More Information" section with history

Example:
```markdown
## More Information

This is the third iteration of our database decision:
- ADR-0001: Original MySQL selection (superseded)
- ADR-0005: Migration to PostgreSQL (superseded by this ADR)
- ADR-0012: This ADR - Move to managed PostgreSQL
```

## Git Integration

If enabled, create commit:
```bash
git add {new_adr} {old_adr} {readme}
git commit -m "docs(adr): ADR-{new_id} supersedes ADR-{old_id}

{new_title}

Supersedes ADR-{old_id}: {old_title}"
```

## Output

Report:
- New ADR created: `{path}` (ADR-{new_id})
- Old ADR updated: `{path}` (ADR-{old_id}) → superseded
- Index updated
- Git commit (if applicable)

## Error Handling

- If existing ADR not found, list available ADRs
- If old ADR is still "proposed", suggest rejection instead
- If bidirectional update fails, report and suggest manual fix
