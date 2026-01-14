# Trade-off Patterns for Architectural Decisions

Common architectural trade-offs and strategies for resolving them.

## Quality Attribute Trade-offs

### Performance vs. Maintainability

**Trade-off**: Optimized code is often harder to understand and maintain.

**Example Scenarios**:
- Loop unrolling vs. readable loops
- Caching complexity vs. data freshness
- Denormalized data vs. normalized schema

**Resolution Strategies**:
1. **Measure first**: Only optimize proven bottlenecks
2. **Isolate complexity**: Keep optimizations in separate modules
3. **Document thoroughly**: Explain why non-obvious code exists
4. **Benchmark continuously**: Ensure optimizations remain necessary

**ADR Consequence Format**:
```markdown
* Good, because response time reduced from 500ms to 50ms
* Bad, because cache invalidation logic adds complexity
* Neutral, because team agrees optimization is justified by SLA requirements
```

### Security vs. Usability

**Trade-off**: More security measures often increase friction for users.

**Example Scenarios**:
- Multi-factor authentication vs. quick login
- Strict password policies vs. user convenience
- Session timeouts vs. user experience

**Resolution Strategies**:
1. **Risk-based approach**: Apply strongest security where risk is highest
2. **Progressive security**: Increase requirements for sensitive operations
3. **Modern methods**: Use passwordless auth, biometrics
4. **User research**: Find security/UX balance through testing

**ADR Consequence Format**:
```markdown
* Good, because unauthorized access risk reduced significantly
* Bad, because users must complete additional verification step
* Neutral, because security requirements are non-negotiable for financial data
```

### Scalability vs. Cost

**Trade-off**: Systems designed for high scale often cost more.

**Example Scenarios**:
- Kubernetes vs. single server
- Distributed database vs. single instance
- CDN vs. origin-only serving

**Resolution Strategies**:
1. **Design for growth**: Architecture supports scaling without rewrite
2. **Scale when needed**: Start simple, add capacity as required
3. **Right-size**: Match infrastructure to actual demand
4. **Cost monitoring**: Track cost per transaction/user

**ADR Consequence Format**:
```markdown
* Good, because system can handle 100x current load
* Bad, because infrastructure cost increases by 3x
* Neutral, because growth projections justify investment
```

### Flexibility vs. Simplicity

**Trade-off**: Configurable systems are more complex.

**Example Scenarios**:
- Plugin architecture vs. monolithic
- Feature flags vs. code branches
- Generic solutions vs. specific implementations

**Resolution Strategies**:
1. **YAGNI principle**: Don't add flexibility until needed
2. **Extension points**: Design for extension, not modification
3. **Configuration limits**: Only expose commonly needed options
4. **Default behaviors**: Provide sensible defaults

**ADR Consequence Format**:
```markdown
* Good, because new integrations can be added without code changes
* Bad, because plugin system adds architectural complexity
* Neutral, because expected integration volume justifies flexibility
```

### Consistency vs. Availability (CAP Theorem)

**Trade-off**: Distributed systems must choose between consistency and availability during partitions.

**Example Scenarios**:
- Strong vs. eventual consistency
- Synchronous vs. asynchronous replication
- Single leader vs. multi-leader

**Resolution Strategies**:
1. **Understand requirements**: Not all data needs strong consistency
2. **Hybrid approach**: Different consistency for different data
3. **Compensating actions**: Design for eventual consistency with rollback
4. **User expectations**: Set appropriate expectations in UI

**ADR Consequence Format**:
```markdown
* Good, because system remains available during network partitions
* Bad, because users may see stale data for up to 5 seconds
* Neutral, because use case tolerates eventual consistency
```

## Technology Trade-offs

### Build vs. Buy

**Trade-off**: Building provides control, buying provides speed.

| Factor | Build | Buy |
|--------|-------|-----|
| Time to market | Slower | Faster |
| Control | Full | Limited |
| Cost (short-term) | Higher | Lower |
| Cost (long-term) | Variable | Predictable |
| Maintenance | Internal | Vendor |
| Customization | Unlimited | Constrained |

**Decision Framework**:
1. Is this a core competency?
2. Do off-the-shelf solutions meet requirements?
3. What is the total cost of ownership?
4. What are the switching costs?

### Monolith vs. Microservices

**Trade-off**: Monoliths are simpler; microservices scale independently.

| Factor | Monolith | Microservices |
|--------|----------|---------------|
| Complexity | Lower | Higher |
| Deployment | Simpler | More complex |
| Scaling | All-or-nothing | Granular |
| Team autonomy | Shared codebase | Independent |
| Data consistency | Easier | Harder |
| Debugging | Simpler | Distributed tracing needed |

**Decision Framework**:
1. Team size and structure
2. Scale requirements
3. Rate of change by component
4. Operational maturity

### SQL vs. NoSQL

**Trade-off**: SQL provides consistency; NoSQL provides flexibility.

| Factor | SQL | NoSQL |
|--------|-----|-------|
| Schema | Fixed | Flexible |
| ACID | Native | Variable |
| Scaling | Vertical | Horizontal |
| Query language | Standardized | Vendor-specific |
| Joins | Efficient | Limited/none |
| Use case | Transactions | Unstructured data |

**Decision Framework**:
1. Data structure complexity
2. Query patterns
3. Consistency requirements
4. Scale requirements

## Resolution Patterns

### Pattern 1: Prioritized Requirements

**When to use**: Multiple valid options, need objective selection.

**Process**:
1. List all decision drivers
2. Assign weights (1-5) based on importance
3. Score each option against drivers
4. Calculate weighted score
5. Choose highest-scoring option

**Template**:
```markdown
| Driver | Weight | Option A | Option B | Option C |
|--------|--------|----------|----------|----------|
| Performance | 5 | 4 (20) | 3 (15) | 5 (25) |
| Cost | 3 | 3 (9) | 5 (15) | 2 (6) |
| Maintainability | 4 | 5 (20) | 3 (12) | 3 (12) |
| **Total** | | **49** | **42** | **43** |
```

### Pattern 2: Time-Based Trade-off

**When to use**: Short-term and long-term needs differ.

**Process**:
1. Identify immediate needs
2. Project long-term requirements
3. Choose option that balances both
4. Document migration path if needed

**Template**:
```markdown
### Short-term (0-6 months)
- Need: Quick deployment
- Solution: Simple single-server setup

### Long-term (6-24 months)
- Need: Handle 10x growth
- Solution: Migrate to Kubernetes

### Migration Path
1. Phase 1: Containerize application
2. Phase 2: Deploy to managed K8s
3. Phase 3: Add horizontal scaling
```

### Pattern 3: Risk-Based Decision

**When to use**: Options have different risk profiles.

**Process**:
1. Identify risks for each option
2. Assess likelihood and impact
3. Consider risk tolerance
4. Choose option with acceptable risk

**Template**:
```markdown
| Option | Risk | Likelihood | Impact | Score |
|--------|------|------------|--------|-------|
| A | Vendor lock-in | High | Medium | 6 |
| A | Data migration | Low | High | 4 |
| B | Performance issues | Medium | High | 6 |
| B | Learning curve | High | Low | 3 |
```

### Pattern 4: Reversibility Analysis

**When to use**: Uncertain about long-term needs.

**Process**:
1. Assess how reversible each option is
2. Prefer reversible choices when uncertain
3. Document switching costs
4. Plan for potential changes

**Categories**:
- **Type 1 (Irreversible)**: Major commitment, hard to undo
- **Type 2 (Reversible)**: Can change direction with reasonable effort

**Guidance**: Make Type 1 decisions carefully; make Type 2 decisions quickly.

## Trade-off Documentation

### Explicit Trade-off Section

```markdown
## Trade-offs Accepted

This decision accepts the following trade-offs:

### Performance vs. Simplicity
We accept slightly lower performance (estimated 10% slower) in exchange for:
- Simpler codebase
- Easier onboarding
- Faster development

### Cost vs. Reliability
We accept higher infrastructure cost ($2K/month) in exchange for:
- 99.9% uptime SLA
- Automatic failover
- Managed backups

### Flexibility vs. Speed
We accept vendor lock-in in exchange for:
- Faster time to market
- Reduced operational burden
- Access to managed services
```

### Trade-off Matrix

```markdown
## Trade-off Analysis

| Trade-off | Option A | Option B | Our Choice |
|-----------|----------|----------|------------|
| Perf vs. Maint | +Perf | +Maint | B (Maint) |
| Cost vs. Scale | +Cost | +Scale | A (Cost) |
| Simple vs. Flex | +Simple | +Flex | A (Simple) |
```

## Best Practices

### Document Explicitly

Always document:
1. What trade-off was made
2. Why this balance was chosen
3. What was given up
4. When to revisit the decision

### Involve Stakeholders

Different stakeholders have different priorities:
- **Product**: User experience, time to market
- **Engineering**: Maintainability, technical debt
- **Operations**: Reliability, observability
- **Finance**: Cost, ROI

### Review Periodically

Trade-offs should be revisited when:
- Requirements change significantly
- Technology landscape shifts
- Scale increases beyond projections
- Pain points emerge in operations
