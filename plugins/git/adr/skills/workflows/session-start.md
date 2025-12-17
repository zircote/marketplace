# Session Start: Auto-Context Loading

Load ADR summaries automatically when starting a Claude Code session in a git repository with ADRs. This provides persistent "machine memory" of architectural decisions.

## Detection Flow

```
Session Start
    │
    ▼
┌─────────────────┐
│ In git repo?    │──No──▶ Skip (not applicable)
└─────────────────┘
    │ Yes
    ▼
┌─────────────────┐
│ git-adr avail?  │──No──▶ Skip (suggest install if user asks about ADRs)
└─────────────────┘
    │ Yes
    ▼
┌─────────────────┐
│ ADRs init?      │──No──▶ Skip (suggest init if user asks about ADRs)
└─────────────────┘
    │ Yes
    ▼
┌─────────────────┐
│ Load summaries  │
│ (active only)   │
└─────────────────┘
```

## Detection Commands

```bash
# Step 1: Check if in git repository
git rev-parse --is-inside-work-tree 2>/dev/null || exit 0

# Step 2: Check if git-adr is installed
git adr --version &>/dev/null || exit 0

# Step 3: Check if ADRs are initialized (any notes exist)
git notes --ref=adr list &>/dev/null 2>&1 || exit 0

# Step 4: Load active ADR summaries
git adr list --format=yaml --status=active 2>/dev/null
```

## Summary Format

Load ADR summaries in this format (for your context, not displayed to user):

```yaml
# Project ADRs (N active decisions)
- id: 20251216-use-postgresql
  title: "Use PostgreSQL for Persistence"
  status: accepted
  date: 2025-12-16
  tags: [database, backend]

- id: 20251215-api-rate-limiting
  title: "API Rate Limiting Strategy"
  status: proposed
  date: 2025-12-15
  tags: [security, api]

- id: 20251210-react-frontend
  title: "Use React for Frontend"
  status: accepted
  date: 2025-12-10
  tags: [frontend, framework]
```

## How to Use Loaded Context

Once ADR summaries are loaded, you can:

### 1. Reference Decisions Naturally

When discussing architecture or making recommendations:
- "As documented in your ADR for PostgreSQL, you've chosen that database..."
- "Your rate limiting decision suggests using token bucket..."
- "Based on the React frontend decision..."

### 2. Align Recommendations

Before suggesting technologies or approaches:
- Check if relevant ADRs exist
- Align suggestions with documented decisions
- Note when suggestions might conflict with existing decisions

### 3. Suggest Related Decisions

When user discusses new architectural choices:
- Note related existing ADRs
- Suggest reviewing relevant decisions
- Offer to create new ADR if decision is significant

## Status Filtering

**By default, load only active decisions:**
- `accepted` - Active, approved decisions
- `proposed` - Pending decisions under consideration

**Exclude from auto-load:**
- `deprecated` - No longer recommended
- `superseded` - Replaced by newer decision
- `draft` - Work in progress

User can request deprecated/superseded ADRs explicitly:
```bash
git adr list --status=deprecated
git adr list --status=superseded
```

## Error Handling

### git-adr Not Installed

If user asks about ADRs but git-adr is not installed:
```
git-adr is not installed. Install with:
  pip install git-adr
  # or
  brew install zircote/tap/git-adr
```

### ADRs Not Initialized

If in a git repo but ADRs not initialized:
```
ADR tracking not initialized in this repository. Initialize with:
  git adr init
```

### No ADRs Found

If initialized but no ADRs exist:
```
No ADRs found in this repository. Create your first with:
  git adr new "Your First Decision"
```

## Token Efficiency

### Large ADR Counts

For repositories with many ADRs (>20), limit auto-load:
```bash
# Load only 20 most recent active ADRs
git adr list --format=yaml --status=active --limit=20
```

Inform user: "Loaded 20 most recent ADRs. Say 'show all ADRs' for complete list."

### Summary vs Full Content

- **Auto-load**: Summary only (id, title, status, date, tags)
- **On request**: Full content via `git adr show <id>`

This keeps initial context load under 1000 tokens for most projects.

## Example Session Start

```
[Session starts in ~/projects/my-app]

[Internal context - not shown to user]:
# Project ADRs (3 active decisions)
- id: 20251216-use-postgresql
  title: "Use PostgreSQL for Persistence"
  status: accepted
  tags: [database, backend]
- id: 20251215-api-rate-limiting
  title: "API Rate Limiting Strategy"
  status: accepted
  tags: [security, api]
- id: 20251210-react-frontend
  title: "Use React for Frontend"
  status: accepted
  tags: [frontend, framework]

[First user message]:
User: "I want to add caching to the API"

[Response uses context]:
"Based on your existing architecture decisions (PostgreSQL backend, React frontend,
rate limiting), I'd suggest Redis for caching. This complements PostgreSQL well
and integrates nicely with your API rate limiting approach. Would you like me to
draft an ADR for this caching decision?"
```

## Refreshing Context

ADR context can become stale if:
- New ADRs created during session
- ADR statuses changed
- User switches to different branch

To refresh: User says "reload ADRs" or "refresh project context"
```bash
git adr list --format=yaml --status=active
```
