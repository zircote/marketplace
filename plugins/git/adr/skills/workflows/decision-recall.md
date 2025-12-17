# Decision Recall: Finding Past Decisions

Guide for recalling and presenting past architectural decisions when users ask about them.

## Trigger Detection

Watch for recall-intent phrases:

| Trigger Pattern | User Intent |
|-----------------|-------------|
| "What did we decide about X?" | Find specific decision |
| "Is there an ADR for X?" | Check if documented |
| "Why did we choose X?" | Find rationale |
| "Show me the X decision" | Hydrate specific ADR |
| "Any decisions about X?" | Search for related ADRs |
| "What's our policy on X?" | Find governing decision |

## Recall Workflow

### Step 1: Parse Intent

Extract keywords and intent from user's question:

```
"What did we decide about caching?"
→ Keywords: "caching", "cache"
→ Intent: Find decision
→ Search: git adr search "caching"
```

### Step 2: Search Strategy

Choose the appropriate search approach:

| Situation | Strategy |
|-----------|----------|
| Specific topic | Full-text search |
| Technology category | Tag-based list |
| Date-bounded | Date-filtered list |
| Known ADR ID | Direct show |
| Exploratory | List with format options |

### Step 3: Present Results

Format results based on what was found:

#### Single Match
```
Found: "Use Redis for session caching" (20251210-redis-caching, accepted)

Key points:
- Redis chosen for session data
- 15-minute TTL for sessions
- Cluster mode for high availability

Would you like the full ADR with all context and consequences?
```

#### Multiple Matches
```
Found 3 ADRs related to caching:

1. 20251210-redis-caching: "Use Redis for Session Caching" (accepted)
   Tags: caching, backend, performance

2. 20251205-cdn-caching: "Use CloudFront for Static Assets" (accepted)
   Tags: caching, frontend, infrastructure

3. 20251201-api-cache: "API Response Caching Strategy" (proposed)
   Tags: caching, api, performance

Which would you like to explore in detail?
```

#### No Matches
```
I didn't find any ADRs about "message queuing".

This might mean:
- The decision hasn't been documented yet
- Try different keywords (e.g., "queue", "async", "messaging")
- The decision might be under a different topic

Would you like me to:
- Search with different terms?
- List all ADRs so you can browse?
- Create a new ADR for this topic?
```

### Step 4: Hydrate on Request

When user wants full details:

```bash
git adr show 20251210-redis-caching
```

Present the complete ADR content, formatted for readability.

## Example Recall Scenarios

### Scenario 1: Direct Question

```
User: "What database are we using?"

[Search]: git adr search "database"
[Found]: 20251215-use-postgresql

Claude: "According to ADR 20251215-use-postgresql, we're using PostgreSQL
for the primary database. The decision was made for:
- ACID compliance for financial transactions
- JSON support for flexible schemas
- Team expertise

Want the full ADR with alternatives considered?"
```

### Scenario 2: Rationale Question

```
User: "Why aren't we using GraphQL?"

[Search]: git adr search "graphql|api" --regex
[Found]: 20251201-rest-api

Claude: "ADR 20251201-rest-api explains this. We chose REST over GraphQL because:
- Simpler caching with HTTP standards
- Team more familiar with REST patterns
- Client requirements don't need GraphQL flexibility

GraphQL was considered but rejected due to caching complexity
and learning curve. Full details available if needed."
```

### Scenario 3: Policy Question

```
User: "What's our policy on error handling?"

[Search]: git adr search "error handling"
[Found]: No results

[Search]: git adr list --tag api
[Found]: 20251210-api-standards

Claude: "I found ADR 20251210-api-standards which covers API conventions
including error responses. However, there's no dedicated error handling
ADR. Would you like to:
- See the API standards ADR for error format details?
- Create a specific error handling ADR?"
```

### Scenario 4: Checking Before New Decision

```
User: "Before we add caching, is there an existing decision?"

[Search]: git adr search "caching|cache" --regex
[Search]: git adr list --tag performance

Claude: "Yes, found 2 relevant ADRs:
1. 20251210-redis-caching: Session caching with Redis (accepted)
2. 20251205-cdn-caching: Static asset caching (accepted)

Your new caching decision should align with these. Redis is already
our caching layer for sessions - would new caching fit there, or
does it need a separate decision?"
```

## Presenting ADR Content

When showing full ADR content, structure for readability:

```markdown
## 📋 ADR: Use PostgreSQL for Primary Database
**ID**: 20251215-use-postgresql
**Status**: accepted | **Date**: 2025-12-15
**Tags**: database, backend, infrastructure

### Context
[2-3 sentence summary of the situation]

### Decision
[Clear statement of what was decided]

### Key Consequences
✅ Positive: [main benefits]
⚠️ Tradeoffs: [key tradeoffs accepted]

### Alternatives Considered
- Option A: Rejected because...
- Option B: Rejected because...

---
*Full content: `git adr show 20251215-use-postgresql`*
```

## Related ADR Suggestions

When showing an ADR, check for related decisions:

```bash
# Get tags from current ADR, search for related
git adr list --tag database
git adr list --tag backend
```

```
Related ADRs you might want to review:
- 20251214-database-migrations: Migration strategy
- 20251210-connection-pooling: Connection pool settings
```

## Context Maintenance

### Refresh Triggers

Re-fetch ADR context when:
- User says "reload ADRs" or "refresh decisions"
- Significant time has passed in session
- User mentions creating/modifying an ADR
- User switches git branches

### Context Expiry

If ADR context seems stale:
```
Note: My ADR context was loaded at session start. If decisions
have changed since then, say "reload ADRs" to refresh.
```

## Error Handling

### ADR Not Found by ID

```
I couldn't find an ADR with ID "20251301-foo".

Possible issues:
- Typo in the ID (check format: YYYYMMDD-slug)
- ADR may have been deleted
- Try searching by keyword instead: git adr search "foo"
```

### Search Returns Too Many Results

```
Found 15 ADRs mentioning "api". Let me narrow this down:

By status:
- 8 accepted, 4 proposed, 3 deprecated

By recent activity:
- 3 from this month

Would you like me to:
- Show only accepted decisions?
- Focus on recent decisions?
- Filter by a specific tag?
```

### Conflicting Decisions Found

```
I found potentially conflicting ADRs:

1. 20251201-use-rest: "Use REST for APIs" (accepted)
2. 20251215-graphql-subscriptions: "Use GraphQL for real-time" (proposed)

The second ADR may need to address how it relates to the first.
Would you like to review both to understand the relationship?
```
