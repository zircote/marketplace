# Search Patterns: Finding Past Decisions

Reference for searching and recalling architectural decisions using git-adr.

## Natural Language → Query Mapping

When users ask about decisions, map their intent to the appropriate search strategy:

| User Says | Search Strategy |
|-----------|-----------------|
| "What did we decide about caching?" | `git adr search caching` |
| "Show database decisions" | `git adr search database` or `git adr list --tag database` |
| "Any security-related ADRs?" | `git adr list --tag security` |
| "Decisions from last month" | `git adr list --since 2025-11-16` |
| "Active decisions only" | `git adr list --status accepted` |
| "Show me ADR-001" or "20251216-use-postgresql" | `git adr show <id>` (hydration) |

## Search Command Syntax

### Basic Full-Text Search

```bash
# Search all ADR content (title, context, decision, consequences)
git adr search "search terms"

# Case-sensitive search
git adr search "PostgreSQL" --case-sensitive

# Regex patterns
git adr search "postgres|mysql" --regex

# With surrounding context lines
git adr search "database" --context 5
```

### Filtered Search

Combine search with filters for precision:

```bash
# Search within accepted decisions only
git adr search "caching" --status accepted

# Search decisions with specific tag
git adr search "Redis" --tag backend

# Multiple filters (AND logic)
git adr search "performance" --status accepted --tag api
```

## List Command with Filters

For browsing rather than searching:

```bash
# By status
git adr list --status accepted
git adr list --status proposed
git adr list --status deprecated

# By tag
git adr list --tag security
git adr list --tag database

# By date range
git adr list --since 2025-01-01
git adr list --until 2025-06-30
git adr list --since 2025-01-01 --until 2025-03-31

# Output formats for different needs
git adr list --format table    # Human-readable (default)
git adr list --format oneline  # Compact summary
git adr list --format yaml     # Machine-readable (for context loading)
git adr list --format json     # API-style output
```

## Common Search Scenarios

### Scenario 1: Technology Decision Lookup

User: "What database are we using and why?"

```bash
# First try tag-based lookup
git adr list --tag database

# If no results, search content
git adr search "database"

# Once found, hydrate the full decision
git adr show 20251216-use-postgresql
```

### Scenario 2: Finding Related Decisions

User: "What decisions affect the API layer?"

```bash
# Search by tag
git adr list --tag api

# Broaden with content search
git adr search "api"

# Check for REST/GraphQL mentions
git adr search "rest|graphql" --regex
```

### Scenario 3: Recent Team Decisions

User: "What did we decide this quarter?"

```bash
# Date-range filter
git adr list --since 2025-10-01 --status accepted

# Include proposed decisions awaiting approval
git adr list --since 2025-10-01
```

### Scenario 4: Checking for Conflicts

User: "Is there an existing decision about authentication?"

```bash
# Search multiple related terms
git adr search "authentication|auth|login" --regex

# Also check security tag
git adr list --tag security

# Look for OAuth, JWT, etc.
git adr search "oauth|jwt|token" --regex
```

## Search Tips

### Effective Query Construction

1. **Start broad, then narrow**: `git adr search "cache"` → `git adr search "cache" --tag backend`

2. **Use keywords from architectural vocabulary**:
   - Data: database, storage, persistence, cache, queue
   - API: REST, GraphQL, endpoint, authentication, rate-limit
   - Frontend: framework, state, routing, styling
   - Infrastructure: deploy, scale, monitor, logging

3. **Try synonyms**: "logging" vs "observability" vs "monitoring"

4. **Use regex for variations**: `--regex "log(ging|s)?"`

### When Search Returns No Results

1. Check for typos in search term
2. Try broader terms (e.g., "data" instead of "PostgreSQL")
3. Remove status/tag filters temporarily
4. Use `git adr list` to browse all ADRs
5. The decision may not have been documented yet - offer to create it

### Optimizing Context Usage

For Claude sessions, prefer summary formats initially:

```bash
# Quick overview (minimal tokens)
git adr list --format oneline

# Structured for AI context (includes metadata)
git adr list --format yaml --status active

# Full detail only when needed
git adr show <id>
```

## Integration with Machine Memory

### At Session Start

Auto-load active ADR summaries:
```bash
git adr list --format yaml --status active
```

### On-Demand Hydration

When user requests specific decision:
```bash
# By exact ID
git adr show 20251216-use-postgresql

# By partial match (if unambiguous)
git adr show postgresql  # May work if unique
```

### Decision Recall Workflow

1. Parse user's question for keywords
2. Map to search/list command
3. Execute search
4. Present summary of matching ADRs
5. Offer to show full content of specific ADR

Example:
```
User: "What did we decide about the frontend framework?"

Claude: "I found one relevant ADR:
- 20251210-react-frontend: 'Use React for Frontend' (accepted)

Would you like me to show the full decision with context and consequences?"
```

## Status Reference

| Status | Include in Search? | Notes |
|--------|-------------------|-------|
| `accepted` | Always | Active decisions |
| `proposed` | Yes | Pending approval, relevant context |
| `draft` | Sometimes | Work in progress |
| `deprecated` | On request | Historical context |
| `superseded` | On request | Points to replacement |
| `rejected` | On request | Why something was NOT chosen |

Default search/list includes all statuses. Use `--status` to filter.

## Practical Examples

### Finding Why We Made a Choice

```bash
# User: "Why aren't we using MongoDB?"
git adr search "MongoDB"
# → May find ADR explaining PostgreSQL choice with MongoDB as rejected alternative

git adr search "NoSQL"
# → Broader search if MongoDB not mentioned directly
```

### Checking Before Adding New Tech

```bash
# User: "Can we add Redis for caching?"
git adr search "caching|cache|redis" --regex
# → Check if there's existing caching decision

git adr list --tag performance
# → Related performance decisions
```

### Understanding System Architecture

```bash
# Get all accepted architecture decisions
git adr list --status accepted --format table

# Search for system boundary decisions
git adr search "boundary|interface|contract" --regex
```
