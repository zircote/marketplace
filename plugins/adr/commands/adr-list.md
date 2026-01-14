---
name: adr-list
description: List all ADRs with optional status filtering
argument-hint: "[--status=accepted|proposed|deprecated|superseded]"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# List ADRs

List all Architectural Decision Records with optional filtering by status.

## Process

1. **Read configuration** from `.claude/adr.local.md`
2. **Scan ADR directories** for all `.md` files matching ADR pattern
3. **Parse each ADR** to extract metadata
4. **Apply filters** if specified
5. **Format output** as table

## Argument Parsing

Supported arguments:
- `--status=<status>`: Filter by status (accepted, proposed, deprecated, superseded, rejected)
- `--format=<format>`: Output format (table, json, brief)
- No arguments: List all ADRs

## ADR Discovery

Find ADRs in configured paths:
```
{adr_path}/[0-9]*.md
{adr_path}/[0-9][0-9][0-9]*.md
```

For each file, extract:
- ID (from filename)
- Title (from H1 heading)
- Status (from Status section)
- Date (if present)
- Superseded by (if applicable)

## Output Format

### Table Format (default)

```
| ID   | Title                           | Status    | Date       |
|------|---------------------------------|-----------|------------|
| 0001 | Use PostgreSQL for Storage      | accepted  | {date}     |
| 0002 | Adopt Event-Driven Architecture | accepted  | {date}     |
| 0003 | Use Redis for Caching           | proposed  | {date}     |
```

### Brief Format

```
0001: Use PostgreSQL for Storage [accepted]
0002: Adopt Event-Driven Architecture [accepted]
0003: Use Redis for Caching [proposed]
```

### JSON Format

```json
{
  "adrs": [
    {"id": "0001", "title": "...", "status": "accepted", "date": "2025-01-10"},
    ...
  ],
  "total": 3,
  "filtered": 3
}
```

## Statistics Summary

After listing, include summary:
```
Total: 25 ADRs
- Accepted: 20
- Proposed: 3
- Deprecated: 1
- Superseded: 1
```

## Error Handling

- If no ADR directory exists, report and suggest `/adr-setup`
- If no ADRs found, report empty state
- If parsing fails, report file and continue with others
