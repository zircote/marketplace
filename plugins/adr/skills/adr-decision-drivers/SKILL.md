---
name: ADR Decision Drivers
description: This skill should be used when the user asks about "decision drivers", "architectural forces", "quality attributes", "how to identify trade-offs", "non-functional requirements for ADRs", or needs help identifying, documenting, and weighing the forces that influence architectural decisions.
version: 1.0.0
---

# ADR Decision Drivers

Decision drivers are the forces, concerns, and requirements that influence architectural decisions. Identifying and documenting these drivers clearly is essential for creating ADRs that explain not just what was decided, but why.

## What Are Decision Drivers?

Decision drivers are factors that:
- Constrain the solution space
- Prioritize certain qualities over others
- Represent stakeholder concerns
- Create tension requiring trade-offs

### Categories of Decision Drivers

| Category | Description | Examples |
|----------|-------------|----------|
| **Functional** | What the system must do | Features, capabilities, integrations |
| **Quality Attributes** | How well system must perform | Performance, security, reliability |
| **Constraints** | Fixed limitations | Budget, timeline, technology mandates |
| **Business** | Organizational factors | Cost, time-to-market, compliance |
| **Technical** | Engineering considerations | Maintainability, testability, complexity |
| **Team** | Human factors | Skills, capacity, preferences |

## Identifying Decision Drivers

### Discovery Questions

Ask these questions to uncover drivers:

**Functional Drivers**
- What must this system do?
- What capabilities are essential vs nice-to-have?
- What integrations are required?

**Quality Attribute Drivers**
- What are the performance requirements?
- How critical is availability?
- What are the security requirements?
- How important is scalability?

**Constraint Drivers**
- What is the budget?
- What is the timeline?
- What technologies are mandated?
- What regulations apply?

**Business Drivers**
- What is the cost sensitivity?
- How important is time-to-market?
- What is the risk tolerance?
- What competitive factors matter?

**Technical Drivers**
- How complex can the solution be?
- What is the expected maintenance burden?
- How important is extensibility?
- What testing requirements exist?

**Team Drivers**
- What skills does the team have?
- What capacity is available?
- What are team preferences?
- What training would be needed?

## Quality Attributes (The "-ilities")

### Core Quality Attributes

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Performance** | Response time, throughput | Latency (ms), requests/sec |
| **Scalability** | Handle increased load | Concurrent users, data volume |
| **Availability** | System uptime | Percentage uptime, MTBF |
| **Reliability** | Correct operation | Error rate, MTTR |
| **Security** | Protection from threats | Vulnerabilities, compliance |
| **Maintainability** | Ease of changes | Change effort, code complexity |
| **Testability** | Ease of testing | Test coverage, test time |
| **Usability** | User experience | Task completion time, errors |

### Extended Quality Attributes

| Attribute | Definition | Measures |
|-----------|------------|----------|
| **Portability** | Run on different platforms | Platform support, migration effort |
| **Interoperability** | Work with other systems | Integration points, standards |
| **Modifiability** | Support changes | Change impact, coupling |
| **Observability** | Monitor system state | Metrics, logs, traces |
| **Deployability** | Ease of deployment | Deployment frequency, time |
| **Recoverability** | Recovery from failure | RTO, RPO |

## Documenting Decision Drivers

### Format for Driver Documentation

```markdown
## Decision Drivers

* **{Driver Name}** - {Brief description of the driver and why it matters}
* **{Driver Name}** - {Brief description}
```

### Good Driver Documentation

```markdown
## Decision Drivers

* **High availability required** - System must maintain 99.9% uptime as per SLA
* **Limited budget** - Total solution cost must not exceed $50K/year
* **Team lacks Kubernetes expertise** - Any container orchestration must be learnable quickly
* **Compliance with GDPR** - User data must be stored in EU region
* **Sub-100ms response time** - API latency critical for user experience
```

### Poor Driver Documentation

```markdown
## Decision Drivers

* Performance
* Cost
* Easy to use
```

Problems: Too vague, no specifics, no prioritization

## Prioritizing Drivers

### MoSCoW Method

| Priority | Meaning | Treatment |
|----------|---------|-----------|
| **Must** | Non-negotiable | Solution must satisfy |
| **Should** | Important | Satisfy if possible |
| **Could** | Nice to have | Include if easy |
| **Won't** | Out of scope | Explicitly excluded |

### Ranking Approach

List drivers in order of importance:
1. {Most critical driver}
2. {Second most important}
3. {Third priority}
...

### Weighted Scoring

Assign weights to drivers:
| Driver | Weight (1-5) |
|--------|-------------|
| Availability | 5 |
| Performance | 4 |
| Cost | 3 |
| Maintainability | 2 |

## Trade-off Analysis

### Identifying Trade-offs

Common quality attribute trade-offs:

| Trade-off | Description |
|-----------|-------------|
| **Performance vs Maintainability** | Optimized code harder to maintain |
| **Security vs Usability** | More security often means more friction |
| **Scalability vs Cost** | Scaling often increases infrastructure cost |
| **Flexibility vs Simplicity** | Configurable systems are more complex |
| **Speed vs Quality** | Faster delivery may reduce quality |

### Documenting Trade-offs

```markdown
### Trade-offs Accepted

We accept:
- **Higher infrastructure cost** for improved availability
- **Increased complexity** for better extensibility
- **Longer initial development** for lower maintenance burden
```

## Using Drivers in Options Evaluation

### Evaluation Matrix

| Option | Driver 1 | Driver 2 | Driver 3 | Score |
|--------|----------|----------|----------|-------|
| Option A | ++ | + | - | 4 |
| Option B | + | ++ | + | 5 |
| Option C | - | + | ++ | 4 |

Scoring: ++ (2), + (1), 0 (0), - (-1), -- (-2)

### Qualitative Evaluation

For each option, evaluate against each driver:
```markdown
### Option 1: PostgreSQL

* **High availability**: Good - supports replication, mature tooling
* **Limited budget**: Moderate - open source but requires expertise
* **Team expertise**: Good - team has SQL experience
```

## Common Pitfalls

### Avoid These Mistakes

1. **Missing drivers** - Failing to identify all relevant factors
2. **Vague drivers** - "Performance" instead of "sub-100ms response time"
3. **No prioritization** - Treating all drivers as equal
4. **Ignoring constraints** - Forgetting budget, timeline, compliance
5. **Technology bias** - Letting preferred tech drive requirements
6. **Single perspective** - Not gathering input from all stakeholders

## Driver Discovery Workshops

### Stakeholder Input

Gather drivers from:
- Product owners (business requirements)
- Architects (technical requirements)
- Operations (operational requirements)
- Security team (security requirements)
- Users (usability requirements)

### Workshop Questions

1. What would make this decision successful?
2. What would make it fail?
3. What constraints must we work within?
4. What quality attributes matter most?
5. What trade-offs are acceptable?
6. What risks concern you?

## Additional Resources

### Reference Files

For comprehensive guidance on specific aspects:
- **`references/quality-attributes.md`** - Detailed quality attribute definitions
- **`references/trade-off-patterns.md`** - Common trade-off patterns and resolutions

### Related Skills

- **adr-fundamentals** - ADR basics and lifecycle
- **adr-quality** - Quality review criteria
- **adr-format-madr** - MADR format with decision drivers section
- **adr-compliance** - Auditing code against ADR decisions
