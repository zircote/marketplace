# Decision Criteria for ADRs

This reference provides detailed criteria for determining when architectural decisions warrant formal documentation in an ADR.

## The ADR Decision Matrix

### High-Impact Decisions (Always Document)

| Criteria | Description | Examples |
|----------|-------------|----------|
| **Irreversibility** | Changes that are costly or impossible to undo | Database schema design, API contracts, data model |
| **Cross-cutting** | Affects multiple components or teams | Authentication strategy, logging framework, error handling |
| **Compliance** | Required for regulatory or legal reasons | Data retention, encryption, audit logging |
| **Cost implications** | Significant financial impact | Cloud provider, licensing, infrastructure |
| **Team precedent** | Sets patterns others will follow | Coding standards, architectural patterns |

### Medium-Impact Decisions (Usually Document)

| Criteria | Description | Examples |
|----------|-------------|----------|
| **Technology adoption** | New tools or frameworks | Adding a new library, upgrading major versions |
| **Performance** | Affects system performance significantly | Caching strategy, query optimization approach |
| **Integration** | External system integrations | Third-party API integration, message broker |
| **Security** | Security-related choices | Token format, session management |

### Low-Impact Decisions (Document If Contentious)

| Criteria | Description | Examples |
|----------|-------------|----------|
| **Local scope** | Affects single component | Internal module structure |
| **Easily reversible** | Can be changed with minimal effort | UI component choice, utility function approach |
| **Obvious choice** | Industry standard or best practice | Using HTTPS, UTF-8 encoding |

## Decision Significance Scoring

Rate each criterion 0-3:

| Score | Meaning |
|-------|---------|
| 0 | Not applicable |
| 1 | Minor consideration |
| 2 | Moderate impact |
| 3 | Major impact |

### Scoring Dimensions

1. **Reversibility Cost** (0-3)
   - 0: Trivially reversible
   - 1: Hours to reverse
   - 2: Days/weeks to reverse
   - 3: Months or prohibitively expensive

2. **Scope of Impact** (0-3)
   - 0: Single function/class
   - 1: Single module/service
   - 2: Multiple modules/services
   - 3: Entire system or multiple systems

3. **Stakeholder Interest** (0-3)
   - 0: No external interest
   - 1: Team interest
   - 2: Department/org interest
   - 3: Executive/customer interest

4. **Future Implications** (0-3)
   - 0: No future constraints
   - 1: Minor future constraints
   - 2: Moderate path dependencies
   - 3: Major architectural constraints

### Score Interpretation

| Total Score | Recommendation |
|-------------|----------------|
| 0-3 | Skip ADR |
| 4-6 | Consider ADR |
| 7-9 | ADR recommended |
| 10-12 | ADR required |

## Domain-Specific Criteria

### Backend Systems

Document decisions about:
- Database selection and schema design
- API design and versioning
- Authentication and authorization
- Caching strategies
- Message queue selection
- Microservice boundaries
- Service discovery
- Configuration management

### Frontend Applications

Document decisions about:
- Framework selection
- State management approach
- Build and bundling strategy
- Component library choice
- Internationalization approach
- Accessibility standards
- Performance optimization strategies

### Data Systems

Document decisions about:
- Data model design
- ETL pipeline architecture
- Data warehouse schema
- Real-time vs batch processing
- Data retention policies
- Privacy and compliance measures

### Infrastructure

Document decisions about:
- Cloud provider selection
- Container orchestration
- CI/CD pipeline design
- Monitoring and alerting strategy
- Disaster recovery approach
- Scaling strategy
- Network topology

## Time-Based Triggers

Create ADRs when:

### Starting New Projects
- Technology stack selection
- Architecture patterns
- Development workflow
- Testing strategy

### Major Milestones
- Pre-production architecture review
- Post-incident architectural changes
- Major version upgrades
- Significant refactoring

### Team Changes
- New team members asking "why?"
- Knowledge transfer needs
- Onboarding documentation gaps

## Red Flags: Document These

Create an ADR if:
- The decision took more than one meeting to make
- Multiple people had strong opinions
- Someone said "we should document this"
- The decision contradicts industry norms
- Future developers will wonder "why?"
- Similar questions keep coming up
- The decision involves trade-offs with no clear winner

## Green Flags: Skip the ADR

Skip formal ADR if:
- Industry best practice with no alternatives
- Team has full consensus in minutes
- Decision is easily reversible
- Scope is limited to single module
- No impact on other teams or systems
- Standard pattern everyone understands
