---
name: ADR Fundamentals
description: This skill should be used when the user asks "what is an ADR", "when should I create an ADR", "ADR best practices", "architecture decision records", "ADR lifecycle", "how to document architecture decisions", or needs guidance on ADR fundamentals, when to create ADRs, or ADR lifecycle management.
version: 1.0.0
---

# ADR Fundamentals

Architectural Decision Records (ADRs) capture important architectural decisions along with their context and consequences. This skill provides foundational knowledge for creating, managing, and maintaining ADRs effectively.

## When to Create an ADR

Create an ADR when making decisions that:

- **Have significant impact** - Affect system structure, behavior, or quality attributes
- **Are hard to reverse** - Would require substantial effort to change later
- **Have multiple viable options** - Alternatives were seriously considered
- **Affect multiple components** - Cross-cutting concerns or system-wide patterns
- **Set precedent** - Establish patterns others will follow
- **Involve trade-offs** - Balance competing concerns or constraints

### Common ADR-Worthy Decisions

| Category | Examples |
|----------|----------|
| **Technology Selection** | Programming language, framework, database, cloud provider |
| **Architecture Patterns** | Microservices vs monolith, event-driven, CQRS |
| **API Design** | REST vs GraphQL, versioning strategy, authentication |
| **Data Management** | Storage strategy, caching, replication, backup |
| **Security** | Authentication method, encryption, access control |
| **Integration** | Third-party services, messaging patterns, protocols |
| **Infrastructure** | Container orchestration, deployment strategy, scaling |

### When NOT to Create an ADR

Skip ADRs for:
- Routine implementation choices
- Decisions with obvious answers
- Temporary or experimental changes
- Minor configuration tweaks
- Decisions that can be easily reversed

## ADR Lifecycle

### Status Workflow

```
proposed → accepted → [deprecated] → superseded
              ↓
          rejected
```

| Status | Meaning |
|--------|---------|
| **proposed** | Under consideration, open for discussion |
| **accepted** | Approved and active, guides current development |
| **rejected** | Considered but not adopted (document why) |
| **deprecated** | No longer recommended, pending replacement |
| **superseded** | Replaced by a newer ADR (link to successor) |

### Status Transitions

**proposed → accepted**: Decision reviewed and approved by stakeholders
**proposed → rejected**: Decision not adopted after review
**accepted → deprecated**: Circumstances changed, better alternatives exist
**accepted/deprecated → superseded**: New ADR replaces this one

## Writing Effective ADRs

### Title Guidelines

Use clear, action-oriented titles:
- **Good**: "Use PostgreSQL for primary data storage"
- **Good**: "Adopt event-driven architecture for order processing"
- **Bad**: "Database decision"
- **Bad**: "Architecture stuff"

### Context Best Practices

Provide sufficient background:
- Current state of the system
- Problem being solved
- Constraints and requirements
- Relevant stakeholders

### Decision Drivers

List forces influencing the decision:
- Technical requirements (performance, scalability, reliability)
- Business requirements (cost, time-to-market, compliance)
- Team factors (expertise, capacity, preferences)
- Organizational constraints (existing systems, standards)

### Documenting Options

For each option considered:
- Brief description
- Pros and cons
- Key trade-offs
- Why selected or rejected

### Consequences

Document both positive and negative outcomes:
- Expected benefits
- Known trade-offs accepted
- Risks and mitigations
- Future implications

## ADR Naming Convention

Standard pattern: `{NUMBER}-{slug}.md`

Examples:
- `0001-use-postgresql-for-primary-storage.md`
- `0002-adopt-event-driven-architecture.md`
- `0003-implement-oauth2-authentication.md`

### Number Format Options

| Format | Example | Use Case |
|--------|---------|----------|
| **4-digit** | `0001`, `0042` | Default, supports 9999 ADRs |
| **3-digit** | `001`, `042` | Smaller projects |
| **Date-based** | `20250115` | Chronological emphasis |

## ADR Directory Structure

Standard structure:
```
docs/adr/
├── README.md           # Index and guidelines
├── 0001-first-adr.md
├── 0002-second-adr.md
└── templates/          # Optional: custom templates
```

For large projects, consider module-level ADRs:
```
src/
├── module-a/
│   └── docs/adr/
├── module-b/
│   └── docs/adr/
└── docs/adr/           # Project-wide ADRs
```

## ADR Linking

### Link Types

| Relationship | Meaning |
|-------------|---------|
| **supersedes** | This ADR replaces ADR-XXX |
| **superseded-by** | ADR-XXX replaces this one |
| **relates-to** | Related decision, not a replacement |
| **amends** | Modifies without fully replacing |

### Linking Best Practices

- Always link both directions (supersedes/superseded-by)
- Include reason for supersession
- Keep superseded ADRs for historical context
- Use relates-to for decisions that inform each other

## Common Mistakes

### Avoid These Patterns

1. **Missing context** - Decisions without background are hard to understand later
2. **Vague options** - "Option A vs Option B" without specifics
3. **Missing trade-offs** - Every decision has downsides; document them
4. **Orphaned ADRs** - Not linking superseded decisions
5. **Status neglect** - Forgetting to update status as decisions evolve
6. **Too much detail** - ADRs are summaries, not full specifications

## Integration with Development

### Pull Request Workflow

1. Create ADR in proposed status
2. Open PR for team review
3. Discuss and refine
4. Update status to accepted when merged
5. Reference ADR in related implementation PRs

### Documentation Links

Cross-reference ADRs from:
- Architecture documentation
- README files
- Code comments (for non-obvious patterns)
- Wiki or knowledge base

## Configuration

Read project configuration from `.claude/adr.local.md` for:
- ADR directory location(s)
- Numbering format
- Status workflow
- Template preferences

## Additional Resources

### Reference Files

For detailed guidance on specific topics:
- **`references/decision-criteria.md`** - Comprehensive criteria for ADR-worthy decisions
- **`references/review-checklist.md`** - ADR quality review checklist

### Related Skills

- **adr-format-madr** - MADR template format details (default format)
- **adr-format-nygard** - Classic Nygard format
- **adr-decision-drivers** - Identifying and documenting decision drivers
- **adr-quality** - Quality criteria and review process
- **adr-compliance** - Auditing code against ADRs
- **adr-integration** - CI/CD and tooling integration
