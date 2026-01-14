---
name: Tyree-Akerman ADR Format
description: This skill should be used when the user asks about "Tyree-Akerman format", "sophisticated ADR", "comprehensive ADR", "enterprise ADR", "formal ADR template", or needs guidance on creating ADRs using the Tyree-Akerman format for enterprise and formal documentation.
version: 1.0.0
---

# Tyree-Akerman ADR Format

The Tyree-Akerman format, developed by Jeff Tyree and Art Akerman, is a comprehensive template for enterprise-grade architectural decision documentation. It provides extensive traceability to requirements, principles, and related artifacts.

## About Tyree-Akerman Format

The Tyree-Akerman format is:
- **Comprehensive** - Covers all aspects of decision documentation
- **Traceable** - Links to requirements, principles, artifacts
- **Enterprise-ready** - Supports formal governance
- **RACI-aware** - Documents decision makers and stakeholders

## Template Structure

```markdown
# {NUMBER}. {TITLE}

## Metadata

| Attribute | Value |
|-----------|-------|
| Status | {STATUS} |
| Date | {DATE} |
| Decision Makers | {names/roles} |
| Consulted | {names/roles} |
| Informed | {names/roles} |

## Issue

{Architectural question}

## Decision

{Clear decision statement}

## Assumptions

* {Assumption 1}
* {Assumption 2}

## Constraints

* {Constraint 1}
* {Constraint 2}

## Positions

### Position 1: {Title}
{Analysis}

### Position 2: {Title}
{Analysis}

## Argument

{Reasoning for decision}

## Implications

* {Implication 1}
* {Implication 2}

## Related Decisions
## Related Requirements
## Related Artifacts
## Related Principles
## Notes
```

## Section Guide

### Metadata Table

Document decision governance:

| Field | Purpose |
|-------|---------|
| **Status** | Current decision state |
| **Date** | Decision date |
| **Decision Makers** | Those with final authority |
| **Consulted** | Those providing input |
| **Informed** | Those who need to know |

### Issue

State the architectural question clearly:
- What needs to be decided?
- Be precise and unambiguous
- Focus on the architectural aspect

### Decision

State the decision clearly:
- Unambiguous statement
- Specific enough to act upon
- Direct language

### Assumptions

List underlying assumptions:
- What is assumed to be true
- Conditions the decision depends on
- Beliefs about the future

If assumptions prove wrong, the decision may need revisiting.

### Constraints

List fixed constraints:
- Budget limitations
- Technology mandates
- Regulatory requirements
- Timeline restrictions
- Organizational policies

### Positions

Document each option (position) considered:
- Clear description
- Analysis of fit with issue
- Strengths and weaknesses

### Argument

Explain the reasoning:
- Why the chosen position was selected
- Why other positions were rejected
- How the decision addresses the issue

### Implications

List what follows from the decision:
- Required changes
- Follow-up actions
- Dependencies created
- Future constraints

### Traceability Sections

**Related Decisions**: Links to other ADRs
**Related Requirements**: Links to requirements documents
**Related Artifacts**: Links to diagrams, specs, documents
**Related Principles**: Architectural principles supporting decision

### Notes

Additional information:
- Meeting minutes
- Background material
- Future considerations

## When to Use Tyree-Akerman Format

**Best for:**
- Enterprise environments
- Formal governance requirements
- Audit trail needs
- Complex stakeholder environments
- Decisions requiring traceability

**Consider other formats when:**
- Quick documentation needed
- Small team decisions
- Low formality acceptable
- Limited time available

## Tyree-Akerman Best Practices

### Assumptions and Constraints

- Be explicit about assumptions
- Document all constraints, even obvious ones
- Review assumptions periodically
- Note when constraints are lifted

### Traceability

- Link to actual requirement IDs
- Reference specific artifact versions
- Use consistent linking format
- Keep links updated

### Governance

- Complete RACI-style metadata
- Get appropriate sign-off
- Store in accessible location
- Follow change management process

## Comparison with Other Formats

| Aspect | Tyree-Akerman | MADR | Nygard |
|--------|---------------|------|--------|
| Sections | 12+ | 10 | 5 |
| Traceability | Extensive | Limited | None |
| Governance | RACI metadata | Status only | Status |
| Best for | Enterprise | Tech teams | Quick docs |

## Additional Resources

### Templates

Template available at:
`${CLAUDE_PLUGIN_ROOT}/templates/tyree-akerman/adr-template.md`

### External Resources

- "Architecture Decisions: Demystifying Architecture" by Jeff Tyree and Art Akerman
