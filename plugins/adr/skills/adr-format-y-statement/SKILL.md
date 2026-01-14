---
name: Y-Statement ADR Format
description: This skill should be used when the user asks about "Y-statement format", "Y-statement ADR", "concise ADR", "one-sentence ADR", "Olaf Zimmermann ADR", or needs guidance on creating ADRs using the Y-Statement format for concise decision documentation.
version: 1.0.0
---

# Y-Statement ADR Format

The Y-Statement format, developed by Olaf Zimmermann, captures architectural decisions in a single structured sentence. It is the most concise ADR format available.

## About Y-Statement Format

The Y-Statement format is:
- **Concise** - Core decision in one sentence
- **Structured** - Fixed format ensures completeness
- **Traceable** - Connects decision to context and consequences
- **Quick** - Minimal documentation overhead

## The Y-Statement Structure

### Basic Y-Statement

```
In the context of {use case/user story},
facing {concern/non-functional requirement},
we decided for {option}
and against {other options},
to achieve {quality/goal},
accepting {downside/consequence/trade-off}.
```

### Extended Y-Statement

Adds a "because" clause for additional rationale:

```
In the context of {use case/user story},
facing {concern/non-functional requirement},
we decided for {option}
and against {other options},
to achieve {quality/goal},
accepting {downside/consequence/trade-off},
because {additional rationale}.
```

## Template Structure

```markdown
# {NUMBER}. {TITLE}

Date: {DATE}

## Status

{STATUS}

## Decision

In the context of {context},
facing {concern},
we decided for {chosen option}
and against {rejected options},
to achieve {quality goal},
accepting {trade-off}.

## Rationale

{Optional: Expand on the decision with additional context}

## Consequences

{Optional: List specific positive and negative outcomes}
```

## Writing Y-Statements

### Fill-in Guide

| Placeholder | What to Include | Example |
|-------------|----------------|---------|
| `{context}` | Use case or scenario | "building a real-time notification system" |
| `{concern}` | Quality attribute or requirement | "the need for sub-second message delivery" |
| `{option}` | Chosen solution | "WebSockets" |
| `{other options}` | Alternatives rejected | "HTTP polling and Server-Sent Events" |
| `{quality}` | Goal achieved | "low-latency bidirectional communication" |
| `{trade-off}` | Accepted downside | "increased infrastructure complexity" |

### Complete Example

```markdown
# 7. Use WebSockets for Real-Time Notifications

Date: 2025-01-15

## Status

Accepted

## Decision

In the context of building a real-time notification system for our
trading platform, facing the need for sub-second message delivery to
thousands of concurrent users, we decided for WebSockets and against
HTTP long-polling and Server-Sent Events, to achieve low-latency
bidirectional communication with efficient connection management,
accepting increased infrastructure complexity and the need for
WebSocket-aware load balancers.

## Consequences

* Good, because notification latency reduced to <100ms
* Good, because server push eliminates polling overhead
* Bad, because load balancer configuration is more complex
* Bad, because connection state management requires additional code
```

## When to Use Y-Statement Format

**Best for:**
- Quick decision documentation
- Simple, clear-cut decisions
- Decisions with obvious winner
- Teams valuing brevity
- Lightweight ADR processes

**Consider other formats when:**
- Complex multi-option analysis needed
- Detailed pros/cons documentation required
- Multiple stakeholders need extensive context
- Decision reasoning is nuanced

## Y-Statement Best Practices

### Writing Tips

- Keep the statement readable as one (long) sentence
- Be specific in each placeholder
- Name concrete alternatives rejected
- State measurable quality goals
- Be honest about trade-offs

### Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Vague context | "building our system" | "building the payment processing module" |
| Missing alternatives | "other options" | "manual processing and third-party service" |
| Unclear quality | "better performance" | "sub-100ms response time" |
| Hidden trade-offs | "minor issues" | "monthly maintenance overhead of 4 hours" |

## Comparison with Other Formats

| Aspect | Y-Statement | Nygard | MADR |
|--------|-------------|--------|------|
| Length | ~1 sentence | 3-5 paragraphs | 1-2 pages |
| Structure | Fixed format | Flexible | Flexible |
| Options | Named in statement | Implicit | Explicit section |
| Best for | Simple decisions | Quick docs | Complex analysis |

## Additional Resources

### Templates

Template available at:
`${CLAUDE_PLUGIN_ROOT}/templates/y-statement/adr-template.md`

### External Resources

- Y-Statements by Olaf Zimmermann
- Sustainable Architectural Decisions (IEEE Software)
