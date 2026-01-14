---
name: Nygard ADR Format
description: This skill should be used when the user asks about "Nygard format", "Nygard ADR", "classic ADR format", "simple ADR template", "Michael Nygard ADR", or needs guidance on creating ADRs using the original Nygard format.
version: 1.0.0
---

# Nygard ADR Format

The Nygard format is the original ADR template created by Michael Nygard in 2011. It is simple, focused, and widely adopted as the classic ADR format.

## About Nygard Format

The Nygard format is:
- **Simple** - Five sections only
- **Focused** - Emphasizes context, decision, consequences
- **Value-neutral** - Context describes facts without judgment
- **Concise** - Designed for quick documentation

## Template Structure

```markdown
# {NUMBER}. {TITLE}

Date: {DATE}

## Status

{STATUS}

## Context

{Describe the forces at play}

## Decision

{State what was decided}

## Consequences

{Describe the resulting context}
```

## Section Guide

### Title

Format: `# {NUMBER}. {TITLE}`

Example: `# 4. Use REST for External APIs`

### Date

The date the decision was made or proposed.

Format: `YYYY-MM-DD` or natural date

### Status

What is the status of this decision?

Values: `Proposed`, `Accepted`, `Deprecated`, `Superseded by ADR-XXX`

### Context

Describe the forces at play:
- Technological factors
- Political factors
- Social factors
- Project-specific factors

**Key principle**: Language should be **value-neutral**. Describe facts, not opinions.

**Good example:**
```markdown
## Context

The mobile team needs to integrate with our backend services. They have
expertise in React Native and prefer RESTful APIs. Our current internal
services use gRPC, which would require significant mobile-side changes.
External API traffic is expected to be 10% of total traffic.
```

### Decision

State what was decided:
- Record **what** was decided, not **how** it was reached
- Keep it brief and direct
- Use active voice

**Good example:**
```markdown
## Decision

We will expose external APIs using REST over HTTPS. Internal services
will continue using gRPC. A gateway service will translate between
REST and gRPC for external requests.
```

### Consequences

Describe the resulting context:
- List **all** consequences, not just positive ones
- Include positive, negative, and neutral outcomes
- Consider future implications

**Good example:**
```markdown
## Consequences

External consumers will have a familiar REST interface to work with.
The mobile team can use their existing REST client libraries. We
will need to maintain two API styles (REST external, gRPC internal).
The gateway introduces an additional point of failure and latency.
API versioning will need a clear strategy for the REST endpoints.
```

## When to Use Nygard Format

**Best for:**
- Quick decision documentation
- Straightforward technical choices
- Teams preferring simplicity
- Decisions with clear single option

**Consider other formats when:**
- Multiple options need detailed comparison
- Complex trade-off analysis required
- Detailed pros/cons documentation needed

## Nygard Format Best Practices

### Context Section

- **Do** describe forces objectively
- **Do** include constraints
- **Don't** include opinions or preferences
- **Don't** justify the decision here

### Decision Section

- **Do** state the decision clearly
- **Do** be specific and actionable
- **Don't** explain the reasoning (that's in consequences)
- **Don't** list alternatives

### Consequences Section

- **Do** list all consequences
- **Do** include negatives
- **Don't** only list benefits
- **Don't** hide trade-offs

## Comparison with Other Formats

| Aspect | Nygard | MADR |
|--------|--------|------|
| Sections | 5 | 10 |
| Options documented | Implicit | Explicit |
| Pros/cons | In consequences | Separate section |
| Complexity | Low | Medium |

## Additional Resources

### Templates

Template available at:
`${CLAUDE_PLUGIN_ROOT}/templates/nygard/adr-template.md`

### Related Skills

- **adr-fundamentals** - ADR basics and lifecycle management
- **adr-quality** - Quality criteria and review process
- **adr-format-madr** - Alternative: Feature-rich MADR format
- **adr-format-y-statement** - Alternative: Concise Y-Statement format
- **adr-format-alexandrian** - Alternative: Pattern-based format

### External Resources

- Original blog post: Documenting Architecture Decisions by Michael Nygard (2011)
