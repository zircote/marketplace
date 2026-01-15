---
name: Structured MADR Format
description: This skill should be used when the user asks about "structured MADR", "structured-madr", "frontmatter ADR", "comprehensive ADR", "auditable ADR", or needs guidance on creating ADRs using the Structured MADR format with YAML frontmatter and audit sections.
version: 1.0.0
---

# Structured MADR Format

Structured MADR is an extension of MADR (Markdown Architectural Decision Records) that adds YAML frontmatter for metadata, comprehensive option analysis, and mandatory audit sections for compliance tracking.

## About Structured MADR

Structured MADR is:
- **Metadata-rich** - YAML frontmatter for structured metadata
- **Comprehensive** - Full option analysis with risk assessments
- **Auditable** - Built-in audit section for compliance tracking
- **MADR-compatible** - Uses standard MADR status values and concepts

## Key Differences from Standard MADR

| Aspect | Standard MADR | Structured MADR |
|--------|--------------|-----------------|
| Frontmatter | None | Required YAML |
| Option Analysis | Pros/cons lists | Full narrative with risk assessment |
| Consequences | Single section | Positive/Negative/Neutral split |
| Audit Trail | None | Required section |
| Metadata | Inline in "More Information" | Structured in frontmatter |
| Decision Drivers | Single list | Primary/Secondary hierarchy |

## Template Structure

### Required YAML Frontmatter

```yaml
---
title: "Decision Title"
description: "Brief description of the decision"
type: adr
category: architecture|api|migration|performance|security|...
tags:
  - relevant-tag
status: proposed|accepted|deprecated|superseded
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: Author Name
project: project-name
technologies:
  - technology-name
audience:
  - developers
  - architects
related:
  - adr_0001.md
---
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Short descriptive title |
| `description` | Yes | One-sentence summary |
| `type` | Yes | Always `adr` |
| `category` | Yes | Decision category (architecture, api, migration, etc.) |
| `tags` | Yes | List of relevant tags |
| `status` | Yes | Current status (proposed, accepted, deprecated, superseded) |
| `created` | Yes | Creation date (YYYY-MM-DD) |
| `updated` | Yes | Last update date (YYYY-MM-DD) |
| `author` | Yes | Decision author |
| `project` | Yes | Project name |
| `technologies` | No | List of technologies involved |
| `audience` | No | Target audience (developers, architects, etc.) |
| `related` | No | List of related ADR filenames |

### Status Values

Structured MADR uses standard MADR status values:

- **proposed** - Decision is under consideration
- **accepted** - Decision has been approved and is in effect
- **deprecated** - Decision is no longer recommended
- **superseded** - Decision has been replaced by another ADR

## Section Guide

### Title (H1)

Format: `# ADR-{NUMBER}: {TITLE}`

The title should match the frontmatter `title` field.

### Status

Repeat the status from frontmatter. Include supersession information if applicable:

```markdown
## Status

Accepted

Supersedes ADR-0003
```

### Context

Split into subsections for clarity:

```markdown
## Context

### Background and Problem Statement

{Describe the situation requiring a decision}

### Current Limitations

{List specific limitations being addressed}
```

### Decision Drivers

Hierarchical organization:

```markdown
## Decision Drivers

### Primary Decision Drivers

1. **Performance**: Must handle 10k requests/second
2. **Reliability**: 99.9% uptime requirement

### Secondary Decision Drivers

1. **Team Familiarity**: Prefer known technologies
2. **Cost**: Budget constraints
```

### Considered Options

Each option gets comprehensive analysis:

```markdown
### Option 1: PostgreSQL

**Description**: Use PostgreSQL as the primary database.

**Technical Characteristics**:
- ACID compliance
- Rich query language
- Mature ecosystem

**Advantages**:
- Strong consistency guarantees
- Excellent tooling support

**Disadvantages**:
- Horizontal scaling requires additional tooling
- Higher operational complexity

**Risk Assessment**:
- **Technical Risk**: Low. Mature and well-documented.
- **Schedule Risk**: Low. Team has existing expertise.
- **Ecosystem Risk**: Low. Large community and vendor support.
```

### Decision

State the decision clearly with implementation details:

```markdown
## Decision

We will use PostgreSQL 15 as the primary database.

The implementation will use:
- **pgBouncer** for connection pooling
- **pg_stat_statements** for query analysis
- **Citus** for horizontal scaling if needed
```

### Consequences

Split into categories:

```markdown
## Consequences

### Positive

1. **Strong Consistency**: ACID guarantees simplify application logic
2. **Query Flexibility**: Complex queries without additional tooling

### Negative

1. **Operational Overhead**: Requires DBA expertise for optimization
2. **Scaling Complexity**: Horizontal scaling needs additional planning

### Neutral

1. **Migration Required**: Existing SQLite data must be migrated
```

### Decision Outcome

Summarize achievements and mitigations:

```markdown
## Decision Outcome

PostgreSQL adoption achieves our primary objectives:
- Handles 10k requests/second with read replicas
- 99.9% uptime via managed service

Mitigations:
- Use managed PostgreSQL to reduce operational overhead
- Document scaling strategy before hitting growth thresholds
```

### Related Decisions

Link to related ADRs:

```markdown
## Related Decisions

- [ADR-0001: Use Rust](adr_0001.md) - Language choice that informed library selection
- [ADR-0005: Event Sourcing](adr_0005.md) - Depends on this storage decision
```

### Links

External resources:

```markdown
## Links

- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Official docs
- [Citus Data](https://www.citusdata.com/) - Horizontal scaling extension
```

### More Information

Metadata section:

```markdown
## More Information

- **Date:** 2025-01-15
- **Source:** SPEC-2025-01-15: Database Selection
- **Related ADRs:** ADR-0001, ADR-0005
```

### Audit (Required)

The audit section tracks compliance:

```markdown
## Audit

### 2025-01-20

**Status:** Compliant

**Findings:**

| Finding | Files | Lines | Assessment |
|---------|-------|-------|------------|
| PostgreSQL connection configured | `src/db/pool.rs` | L15-L45 | compliant |
| pgBouncer deployed | `deploy/k8s/pgbouncer.yaml` | L1-L50 | compliant |

**Summary:** Database implementation follows ADR specifications.

**Action Required:** None
```

## Audit Section Guidelines

### Audit Status Values

- **Pending** - Not yet audited
- **Compliant** - Implementation matches decision
- **Non-Compliant** - Implementation deviates from decision
- **Partial** - Some aspects compliant, others not

### Assessment Values

- **compliant** - Finding confirms adherence
- **non-compliant** - Finding shows deviation
- **partial** - Partially implemented

### When to Audit

- After initial implementation
- After major refactoring
- During periodic compliance reviews
- When related ADRs change

## Creating Structured MADR ADRs

```bash
# Copy template
cp ${CLAUDE_PLUGIN_ROOT}/templates/structured-madr/adr-template.md docs/adr/adr_0001.md
```

## Structured MADR Best Practices

### Do

- Fill all required frontmatter fields
- Provide comprehensive option analysis with risk assessments
- Split consequences into Positive/Negative/Neutral
- Keep audit section updated after implementation
- Link related ADRs bidirectionally

### Don't

- Leave placeholder text in published ADRs
- Skip the audit section (it's required)
- Use non-standard status values
- Forget to update the `updated` date on changes
- Mix MADR and Structured MADR formats in one project

## Comparison with Other Formats

| Aspect | Structured MADR | MADR | Nygard |
|--------|-----------------|------|--------|
| Sections | 12+ | 10 | 5 |
| Frontmatter | Required | None | None |
| Option detail | Full narrative | Pros/cons | Implicit |
| Audit trail | Required | None | None |
| Best for | Regulated/audited projects | Tech decisions | Quick records |

## When to Use Structured MADR

**Best for:**
- Projects requiring compliance auditing
- Complex decisions with multiple stakeholders
- Regulated industries (finance, healthcare)
- Teams wanting comprehensive documentation
- Long-lived projects where decisions need tracking

**Consider other formats when:**
- Quick, simple decisions
- Small teams with informal processes
- Decisions unlikely to need auditing
- Preference for brevity over comprehensiveness

## Additional Resources

### Templates

Template available at:
`${CLAUDE_PLUGIN_ROOT}/templates/structured-madr/adr-template.md`

### Related Skills

- **adr-fundamentals** - ADR basics and lifecycle management
- **adr-quality** - Quality criteria and review process
- **adr-compliance** - Auditing ADRs against code
- **adr-format-madr** - Standard MADR format
- **adr-decision-drivers** - Identifying decision drivers

### Configuration

Enable in `.claude/adr.local.md`:

```yaml
default_format: structured-madr
```
