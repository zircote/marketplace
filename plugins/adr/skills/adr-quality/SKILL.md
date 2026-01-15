---
name: ADR Quality
description: This skill should be used when the user asks about "ADR quality", "review ADR", "ADR checklist", "improve ADR", "ADR validation", "good ADR examples", or needs guidance on evaluating, improving, and maintaining high-quality architectural decision records.
version: 1.0.0
---

# ADR Quality

This skill provides guidance on creating, evaluating, and maintaining high-quality Architectural Decision Records. Quality ADRs are clear, complete, and useful for future readers.

## Quality Criteria

### The 5 C's of ADR Quality

| Criterion | Definition | Questions to Ask |
|-----------|------------|------------------|
| **Clear** | Easy to understand | Can a new team member understand this? |
| **Complete** | All relevant information | Are all sections filled out meaningfully? |
| **Concise** | No unnecessary content | Is every sentence adding value? |
| **Contextual** | Sufficient background | Is the "why" clear? |
| **Current** | Reflects actual state | Is the status accurate? Are links valid? |

## Essential Quality Checks

### Title Quality

Good titles are:
- Specific and searchable
- Action-oriented (verb + noun)
- Not too broad or too narrow

| Quality | Example |
|---------|---------|
| **Good** | "Use PostgreSQL for primary data storage" |
| **Good** | "Adopt event-driven architecture for order processing" |
| **Bad** | "Database" |
| **Bad** | "Technical decision about which database to use for storing user data" |

### Context Quality

Context should answer:
- What problem are we solving?
- What is the current state?
- What constraints exist?
- Who are the stakeholders?

**Good context example:**
```markdown
Our e-commerce platform needs to handle user authentication across
mobile and web applications. Currently, authentication is handled
separately in each app, leading to inconsistent security and duplicate
code. We have 50,000 active users and expect 10x growth in 2 years.
The team has experience with OAuth but not SAML.
```

### Decision Drivers Quality

Drivers should be:
- Specific (not "performance" but "sub-100ms response time")
- Prioritized or weighted
- Traceable to stakeholder needs
- Testable or measurable

### Options Quality

Each option should have:
- Clear description
- Genuine consideration (not straw man)
- Fair pros and cons analysis
- Sufficient detail for comparison

### Decision Quality

The decision should:
- State the choice clearly
- Connect to decision drivers
- Explain why other options were rejected
- Be actionable

### Consequences Quality

Consequences should include:
- Both positive and negative outcomes
- Accepted trade-offs
- Risks and mitigations
- Future implications

## Quality Anti-Patterns

### Common Problems to Avoid

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| **Thin Context** | Just problem statement, no background | Add current state, constraints, stakeholders |
| **Missing Trade-offs** | Only benefits listed | Document negatives of chosen option |
| **Straw Man Options** | Options included just to reject | Only include seriously considered alternatives |
| **Vague Drivers** | Generic terms like "performance" | Add specific, measurable criteria |
| **Orphan ADRs** | No links to related decisions | Add supersedes/relates-to links |
| **Stale Status** | Status doesn't reflect reality | Update status when state changes |
| **Hindsight Bias** | Written long after decision | Create ADRs during decision process |

### Red Flags in ADR Review

- [ ] Only one option considered
- [ ] No cons listed for chosen option
- [ ] Context is single sentence
- [ ] Decision drivers are vague
- [ ] No stakeholders mentioned
- [ ] Status hasn't been updated in months
- [ ] Superseded ADRs not updated

## Quality Review Process

### Self-Review Checklist

Before submitting an ADR:

**Completeness**
- [ ] All sections have meaningful content
- [ ] No placeholder text remaining
- [ ] Links and references work
- [ ] Related ADRs linked

**Clarity**
- [ ] Readable by someone not involved in decision
- [ ] Acronyms defined
- [ ] Technical terms explained
- [ ] Structure aids understanding

**Accuracy**
- [ ] Facts are verifiable
- [ ] Options fairly presented
- [ ] Trade-offs honestly stated
- [ ] Status reflects actual state

### Peer Review Guidelines

When reviewing ADRs:

1. **Read for understanding first** - Can you understand the decision without extra context?
2. **Check decision drivers** - Are they complete and prioritized?
3. **Evaluate options** - Were alternatives seriously considered?
4. **Assess consequences** - Are trade-offs clearly stated?
5. **Consider future readers** - Will this make sense in 6 months?

### Review Questions

Ask these during review:
- "What problem does this solve?"
- "Why was this option chosen over alternatives?"
- "What trade-offs are we accepting?"
- "When should this decision be revisited?"

## Writing Quality Guidelines

### Language and Tone

- Use active voice
- Be specific, not vague
- Avoid unnecessary jargon
- Write for future readers

**Good**: "We chose PostgreSQL for its strong JSON support"
**Bad**: "The database was selected based on various factors"

### Structure and Formatting

- Use consistent heading levels
- Include tables for comparisons
- Use bullet points for lists
- Keep paragraphs focused

### Length Guidelines

| Section | Recommended Length |
|---------|-------------------|
| Title | 5-15 words |
| Context | 100-300 words |
| Decision Drivers | 3-8 items |
| Options | 2-5 options, 50-150 words each |
| Decision | 50-150 words |
| Consequences | 100-300 words |

## Maintaining Quality Over Time

### Regular Audits

Periodically review ADRs for:
- Outdated information
- Incorrect status
- Broken links
- Missing relationships
- Decisions that should be revisited

### Status Hygiene

Keep status current:
- Update to deprecated when appropriate
- Link superseding ADRs
- Remove or archive truly obsolete ADRs

### Documentation Integration

Ensure ADRs connect to:
- Architecture documentation
- README files
- Code comments where relevant
- Onboarding materials

## Quality Metrics

### ADR Health Indicators

| Metric | Good | Concerning | Critical |
|--------|------|------------|----------|
| Sections completed | >90% | 70-90% | <70% |
| Options considered | 2-5 | 1 or >5 | 0 |
| Consequences documented | Both +/- | Only + | None |
| Status currency | Updated monthly | Quarterly | >6 months |
| Links working | 100% | >90% | <90% |

## Additional Resources

### Related Skills

- **adr-fundamentals** - ADR basics and lifecycle
- **adr-decision-drivers** - Identifying and documenting drivers
- **adr-compliance** - Auditing code compliance with ADRs
- **adr-format-madr** - MADR format specifics for quality templates
