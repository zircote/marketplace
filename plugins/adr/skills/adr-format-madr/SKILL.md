---
name: MADR Format
description: This skill should be used when the user asks about "MADR format", "MADR template", "Markdown Architectural Decision Records", "MADR 4.0", "MADR sections", or needs guidance on creating ADRs using the MADR (Markdown Architectural Decision Records) format.
version: 1.0.0
---

# MADR Format

MADR (Markdown Architectural Decision Records) is a lean, developer-friendly ADR format that emphasizes considered options and their pros/cons. It is the default format for the ADR plugin.

## About MADR

MADR is:
- **Lean** - Focuses on essential decision documentation
- **Markdown-native** - Designed for version control
- **Option-focused** - Emphasizes alternatives considered
- **Flexible** - Offers full and minimal variants

Current version: **MADR 4.0.0**

## Template Variants

### Full Template

All sections including optional ones. Use for important decisions requiring comprehensive documentation.

Sections:
1. Title (H1)
2. Status
3. Context and Problem Statement
4. Decision Drivers
5. Considered Options
6. Decision Outcome
7. Consequences (Good/Bad)
8. Confirmation
9. Pros and Cons of the Options
10. More Information

### Minimal Template

Only mandatory sections. Use for simpler decisions or when brevity is preferred.

Sections:
1. Title (H1)
2. Status
3. Context and Problem Statement
4. Decision Outcome

### Bare Templates

Same sections as full/minimal but without explanatory text. For experienced teams who know the format.

## Section Guide

### Title (Required)

Format: `# {Short Title}`

The title should:
- Be a short noun phrase
- Describe the decision topic
- Use title case

**Examples:**
- `# Use PostgreSQL for Primary Storage`
- `# Adopt Event-Driven Architecture`

### Status (Required)

The current status of the decision.

Valid values: `proposed`, `accepted`, `deprecated`, `superseded`

Include metadata if needed:
```markdown
## Status

Accepted

Supersedes ADR-0003
```

### Context and Problem Statement (Required)

Describe the context and the problem requiring a decision.

**Format options:**
1. Free-form prose (2-3 sentences)
2. Illustrative story
3. Question format

**Example:**
```markdown
## Context and Problem Statement

Our order processing system experiences high latency during peak hours.
We need to decouple order submission from order processing to improve
responsiveness. The current synchronous architecture cannot scale to
meet projected growth of 5x order volume.
```

### Decision Drivers (Optional)

Forces and concerns influencing the decision.

**Format:** Bullet list
```markdown
## Decision Drivers

* Need to handle 10x current load
* Team familiarity with technology
* Budget constraints (max $5K/month)
* Must integrate with existing systems
```

### Considered Options (Optional)

List of options seriously considered.

**Format:** Bullet list of option titles
```markdown
## Considered Options

* RabbitMQ
* Apache Kafka
* AWS SQS
* Redis Pub/Sub
```

### Decision Outcome (Required)

State the chosen option and why.

**Format:**
```markdown
## Decision Outcome

Chosen option: "{option title}", because {justification}.
```

**Example:**
```markdown
## Decision Outcome

Chosen option: "Apache Kafka", because it provides the durability and
replay capability we need for order processing, and the team has
existing experience with it.
```

### Consequences (Optional)

Positive and negative outcomes of the decision.

**Format:**
```markdown
### Consequences

* Good, because {positive outcome}
* Good, because {another positive}
* Bad, because {negative outcome}
* Bad, because {another negative}
```

### Confirmation (Optional)

How compliance with the decision will be verified.

**Example:**
```markdown
### Confirmation

The implementation will be verified through:
* Architecture review before deployment
* Load testing against performance requirements
* ArchUnit tests to enforce message-based communication
```

### Pros and Cons of the Options (Optional)

Detailed analysis of each option.

**Format:**
```markdown
## Pros and Cons of the Options

### {Option 1 Title}

{Brief description}

* Good, because {pro}
* Good, because {pro}
* Neutral, because {neutral point}
* Bad, because {con}

### {Option 2 Title}

{Brief description}

* Good, because {pro}
* Bad, because {con}
```

### More Information (Optional)

Additional context, links, or notes.

**Include:**
- Links to related documents
- Team agreement notes
- Implementation timeline
- Conditions for revisiting

## Creating MADR ADRs

### With Full Template

```bash
# Copy full template
cp ${CLAUDE_PLUGIN_ROOT}/templates/madr/adr-template-full.md docs/adr/0001-title.md
```

### With Minimal Template

```bash
# Copy minimal template
cp ${CLAUDE_PLUGIN_ROOT}/templates/madr/adr-template-minimal.md docs/adr/0001-title.md
```

## MADR Best Practices

### Do

- Keep context focused on the problem
- List 2-5 realistic options
- Include both pros and cons for each option
- Be specific about consequences
- Update status when it changes

### Don't

- Include options just to reject them
- List only positive consequences
- Leave placeholder text
- Forget to link related ADRs
- Let status become stale

## MADR vs Other Formats

| Aspect | MADR | Nygard | Y-Statement |
|--------|------|--------|-------------|
| **Focus** | Options comparison | Decision recording | Concise statement |
| **Length** | Medium | Short | Very short |
| **Options** | Detailed | Implicit | Single |
| **Best for** | Tech decisions | Quick records | Simple decisions |

## Additional Resources

### Reference Files

- **`references/madr-examples.md`** - Complete MADR examples

### Templates

Templates available at `${CLAUDE_PLUGIN_ROOT}/templates/madr/`:
- `adr-template-full.md` - All sections with guidance
- `adr-template-minimal.md` - Required sections only
- `adr-template-bare.md` - All sections, no guidance
- `adr-template-bare-minimal.md` - Required sections, no guidance

### Related Skills

- **adr-fundamentals** - ADR basics and lifecycle management
- **adr-decision-drivers** - Identifying and documenting decision drivers
- **adr-quality** - Quality criteria and review process
- **adr-format-structured-madr** - Extended: MADR with frontmatter and audit sections
- **adr-format-nygard** - Alternative: Classic Nygard format
- **adr-format-y-statement** - Alternative: Concise Y-Statement format

### External Resources

- MADR GitHub: https://github.com/adr/madr
- MADR Documentation: https://adr.github.io/madr/
