# MADR Examples

Complete examples of MADR (Markdown Architectural Decision Records) format.

## Example 1: Database Selection (Full Template)

```markdown
# Use PostgreSQL for Primary Data Storage

## Status

Accepted

## Context and Problem Statement

Our application needs a reliable, scalable database for storing user data, transactions, and analytics. We need to choose a primary database that can handle our current load of 10K daily active users and scale to 100K within 2 years.

## Decision Drivers

* Must support ACID transactions for financial data integrity
* Need JSON support for flexible schema portions
* Team has strongest experience with SQL databases
* Budget limited to $5K/month for database infrastructure
* Must support replication for high availability

## Considered Options

* PostgreSQL
* MySQL 8.0
* MongoDB
* CockroachDB

## Decision Outcome

Chosen option: "PostgreSQL", because it provides the best balance of ACID compliance, JSON support via JSONB, and aligns with team expertise while staying within budget.

### Consequences

* Good, because mature ecosystem with excellent tooling
* Good, because JSONB provides flexibility without sacrificing query performance
* Good, because team can leverage existing SQL knowledge
* Bad, because horizontal scaling requires additional tools (Citus, partitioning)
* Bad, because operational complexity increases with replication setup

### Confirmation

Implementation will be verified through:
* Architecture review of database schema design
* Load testing against 10x current traffic
* Failover testing of replication setup

## Pros and Cons of the Options

### PostgreSQL

Industry-leading open-source relational database with advanced features.

* Good, because excellent ACID compliance and data integrity
* Good, because JSONB provides document-store flexibility with SQL querying
* Good, because extensive extension ecosystem (PostGIS, pg_trgm, etc.)
* Good, because strong community and commercial support options
* Neutral, because requires DBA expertise for optimal configuration
* Bad, because horizontal scaling more complex than NoSQL alternatives

### MySQL 8.0

Popular open-source database with improved JSON support in version 8.

* Good, because widely known and easy to find expertise
* Good, because good performance for read-heavy workloads
* Good, because native JSON type support improved in 8.0
* Bad, because JSON querying less powerful than PostgreSQL JSONB
* Bad, because historically weaker ACID compliance (improved in 8.0)

### MongoDB

Document-oriented NoSQL database.

* Good, because native JSON storage aligns with application data model
* Good, because built-in horizontal scaling via sharding
* Good, because flexible schema for evolving data structures
* Bad, because team would need significant training
* Bad, because ACID transactions only added recently, less mature
* Bad, because higher licensing costs for enterprise features

### CockroachDB

Distributed SQL database with PostgreSQL compatibility.

* Good, because PostgreSQL-compatible SQL interface
* Good, because built-in horizontal scaling and fault tolerance
* Good, because strong consistency guarantees
* Bad, because relatively new, smaller community
* Bad, because significantly higher infrastructure cost
* Bad, because complexity may be overkill for current scale

## More Information

* Team discussion notes: [Confluence link]
* Performance benchmark results: [Internal wiki]
* Decision participants: @alice, @bob, @charlie
* Review date: Q4 2024 or when approaching 50K DAU
```

## Example 2: API Design (Minimal Template)

```markdown
# Use REST over GraphQL for Public API

## Status

Accepted

## Context and Problem Statement

We need to expose our core functionality via a public API. Partners and third-party developers will integrate with this API. We need to decide between REST and GraphQL approaches.

## Decision Outcome

Chosen option: "REST", because our API consumers are primarily enterprise partners who are more familiar with REST conventions, and our use cases don't require the flexible querying that GraphQL provides.

### Consequences

* Good, because easier onboarding for enterprise partners
* Good, because simpler caching strategy with HTTP caching
* Good, because extensive tooling and documentation patterns available
* Bad, because may require multiple endpoints for complex data fetching
* Bad, because versioning will require careful API evolution strategy
```

## Example 3: Authentication Strategy

```markdown
# Adopt OAuth 2.0 with JWT for Authentication

## Status

Accepted

## Context and Problem Statement

How should we handle authentication for our microservices architecture? We need a solution that works across multiple services, supports third-party integrations, and scales with our user base.

## Decision Drivers

* Services need to verify identity without hitting a central auth server for every request
* Must support SSO with enterprise identity providers
* Mobile apps need token-based authentication
* Tokens must be revocable for security incidents

## Considered Options

* OAuth 2.0 with JWT access tokens
* Session-based authentication with Redis
* OAuth 2.0 with opaque tokens
* Custom token system

## Decision Outcome

Chosen option: "OAuth 2.0 with JWT access tokens", because it enables stateless verification at each service while providing standard flows for third-party integration.

### Consequences

* Good, because services can verify tokens locally using public keys
* Good, because standard OAuth flows work with enterprise IdPs
* Good, because well-understood security model with extensive tooling
* Bad, because JWT revocation requires additional infrastructure (token blacklist)
* Bad, because token size larger than opaque tokens

### Confirmation

* Security review of token handling implementation
* Penetration testing of authentication flows
* Load testing of token verification under peak traffic

## Pros and Cons of the Options

### OAuth 2.0 with JWT access tokens

Standard OAuth with self-contained JWT tokens.

* Good, because stateless verification reduces auth server load
* Good, because tokens contain claims for authorization decisions
* Good, because standard libraries available in all languages
* Bad, because tokens cannot be revoked until expiry without blacklist
* Bad, because sensitive claims in token if not encrypted

### Session-based authentication with Redis

Traditional sessions with distributed cache.

* Good, because immediate session invalidation
* Good, because small session ID, no sensitive data exposed
* Bad, because Redis dependency for every request
* Bad, because doesn't fit microservices model well
* Bad, because mobile apps prefer token-based approaches

### OAuth 2.0 with opaque tokens

OAuth with reference tokens requiring introspection.

* Good, because immediate revocation possible
* Good, because no sensitive data in token
* Bad, because every service must call auth server
* Bad, because auth server becomes bottleneck

### Custom token system

Build proprietary token system.

* Good, because full control over implementation
* Bad, because reinventing well-solved problems
* Bad, because security risks from custom crypto
* Bad, because no interoperability with third parties

## More Information

* Security team review: Approved 2024-01-15
* Implementation guide: [Internal docs]
* Related: ADR-0003 (API Gateway selection)
```

## Tips for Writing MADR

### Do

- Keep the context focused on the actual problem
- List 2-5 realistic options that were genuinely considered
- Be specific about consequences (both good and bad)
- Include quantifiable criteria when possible
- Reference related ADRs

### Don't

- Include options just to reject them
- Write only positive consequences
- Leave placeholder text in final ADR
- Forget to update status when decisions change
- Make the context too broad or philosophical
