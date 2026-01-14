---
name: Alexandrian ADR Format
description: This skill should be used when the user asks about "Alexandrian format", "Alexandrian ADR", "pattern-based ADR", "forces-based ADR", "Christopher Alexander ADR", or needs guidance on creating ADRs using the Alexandrian pattern format.
version: 1.0.0
---

# Alexandrian ADR Format

The Alexandrian format is inspired by Christopher Alexander's pattern language. It emphasizes the forces influencing decisions and the resulting context after applying a solution.

## About Alexandrian Format

The Alexandrian format is:
- **Pattern-oriented** - Follows pattern language structure
- **Force-focused** - Emphasizes competing forces
- **Context-rich** - Detailed before/after context
- **Relationship-aware** - Links to related patterns/decisions

## Template Structure

```markdown
# {NUMBER}. {TITLE}

Date: {DATE}

## Status

{STATUS}

## Context

{Background and current state}

## Problem

{Clear problem statement}

## Forces

* {Force 1}
* {Force 2}
* {Force 3}

## Solution

{Chosen solution}

## Resulting Context

### Benefits
* {Benefit 1}
* {Benefit 2}

### Drawbacks
* {Drawback 1}
* {Drawback 2}

### Related Patterns/Decisions
* {Related ADR or pattern}
```

## Section Guide

### Context

Describe the background:
- Project state
- Team composition
- Organizational factors
- Technical environment

### Problem

State the problem clearly:
- What issue needs resolution?
- What question needs answering?
- Frame as a specific challenge

### Forces

List forces influencing the decision:
- Technical requirements
- Business constraints
- Team factors
- Organizational pressures

Forces often pull in different directions, creating tension that the decision must resolve.

**Example:**
```markdown
## Forces

* Need for high availability (99.99% uptime SLA)
* Limited budget ($5K/month infrastructure)
* Team expertise in Kubernetes
* Requirement for data residency in EU
* Desire to minimize operational overhead
```

### Solution

Describe the chosen solution:
- What will be done
- How it addresses the forces
- Specific implementation approach

### Resulting Context

Document the state after applying the solution:

**Benefits** - Positive outcomes achieved
**Drawbacks** - Negative consequences accepted
**Related Patterns/Decisions** - Connections to other ADRs or architectural patterns

## When to Use Alexandrian Format

**Best for:**
- Decisions with complex, competing forces
- Pattern-oriented teams
- Decisions requiring detailed context
- Situations with many constraints

**Consider other formats when:**
- Quick documentation needed
- Forces are straightforward
- Team prefers simpler templates

## Alexandrian Best Practices

### Documenting Forces

- List 4-8 forces for most decisions
- Include both technical and non-technical forces
- Note which forces are in tension
- Prioritize or weight forces if helpful

### Resulting Context

- Be honest about drawbacks
- Link to decisions that address drawbacks
- Note conditions that would trigger revisiting

## Additional Resources

### Templates

Template available at:
`${CLAUDE_PLUGIN_ROOT}/templates/alexandrian/adr-template.md`

### External Resources

- "A Pattern Language" by Christopher Alexander
- Pattern-Oriented Software Architecture
