---
name: adr-search
description: Search ADRs by content, status, tags, or date
argument-hint: "<query> [--status=<status>] [--since=<date>]"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Search ADRs

Search Architectural Decision Records by content, status, tags, or date range.

## Process

1. **Parse search arguments**
2. **Build search criteria**
3. **Search ADR files**
4. **Rank and filter results**
5. **Display matches with context**

## Argument Parsing

Supported arguments:
- `<query>`: Text to search for in ADR content
- `--status=<status>`: Filter by status
- `--since=<date>`: ADRs created/modified since date
- `--until=<date>`: ADRs created/modified until date
- `--tag=<tag>`: Filter by tag (if tags are used)
- `--format=<format>`: Output format (default, verbose, json)

## Search Modes

### Full-Text Search

Search across all ADR content:
- Title
- Context
- Decision
- Consequences
- Options (if present)

Use Grep to find matches, then parse files for context.

### Status Filter

Filter by decision status:
```
/adr-search --status=accepted
/adr-search --status=proposed
```

### Date Range

Filter by date:
```
/adr-search --since=2024-01-01  # Or relative: --since=30d
/adr-search --since=30d  # Last 30 days
```

### Combined Search

Combine criteria:
```
/adr-search "postgresql" --status=accepted --since=90d
```

## Search Output

### Default Format

Show matches with context:
```
Found 3 ADRs matching "database":

ADR-0001: Use PostgreSQL for Primary Storage [accepted]
  ...we chose PostgreSQL as our primary **database**...
  File: docs/adr/0001-use-postgresql.md

ADR-0007: Database Connection Pooling [accepted]
  ...the **database** connection pooling strategy...
  File: docs/adr/0007-database-connection-pooling.md

ADR-0012: Database Migration Strategy [proposed]
  ...approach for **database** schema migrations...
  File: docs/adr/0012-database-migration-strategy.md
```

### Verbose Format

Include more context per match:
- Full title
- Status and date
- All matching excerpts
- Related ADRs

### JSON Format

Structured output for tooling:
```json
{
  "query": "database",
  "filters": {"status": "accepted"},
  "results": [
    {
      "id": "0001",
      "title": "Use PostgreSQL for Primary Storage",
      "status": "accepted",
      "file": "docs/adr/0001-use-postgresql.md",
      "matches": [
        {"section": "Context", "excerpt": "...primary database..."}
      ]
    }
  ],
  "total": 3
}
```

## Ranking

Order results by relevance:
1. Title matches (highest)
2. Decision section matches
3. Context matches
4. Other section matches

Within same relevance, order by:
- Accepted > Proposed > Deprecated > Superseded
- More recent first

## Search Tips

Display helpful search tips:
- Use quotes for exact phrases
- Combine with status for focused results
- Use date filters to find recent decisions

## Error Handling

- If no results found, suggest broader search
- If query too short, require minimum length
- If date format invalid, show expected format
