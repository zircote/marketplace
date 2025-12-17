# Decision Capture: Creating ADRs from Conversation

Guide for extracting and documenting architectural decisions from ongoing conversations.

## Trigger Detection

Watch for phrases that indicate a decision has been made:

| Trigger Phrase | Intent |
|----------------|--------|
| "Record this decision" | Explicit capture request |
| "Create an ADR from this" | Explicit capture request |
| "Document this decision" | Explicit capture request |
| "We should document that..." | Implicit capture suggestion |
| "Let's go with [option]" | Decision made, offer to capture |
| "I've decided to use..." | Decision made, offer to capture |

## Extraction Process

### Step 1: Identify Decision Components

From the conversation, extract:

1. **Title**: One-line summary of the decision
2. **Context**: What's the situation? What problem are we solving?
3. **Decision**: What was decided?
4. **Consequences**: What are the implications?
5. **Alternatives** (if discussed): What else was considered?

### Step 2: Confirm Understanding

Before creating the ADR, summarize back to the user:

```
Based on our conversation, I understand the decision as:

**Decision**: Use PostgreSQL for the application database

**Context**: We need a reliable, ACID-compliant database for our
order processing system. Expected data volume is 10M orders/year.

**Key reasons**:
- Strong transactional guarantees for financial data
- Team has PostgreSQL expertise
- Excellent JSON support for flexible schemas

**Alternatives considered**:
- MySQL: Rejected due to weaker JSON support
- MongoDB: Rejected for ACID compliance concerns

**Consequences**:
- Will need to set up PostgreSQL infrastructure
- Team can leverage existing expertise
- May need to consider read replicas for scaling

Is this accurate? Should I create an ADR with this content?
```

### Step 3: Generate ADR

After user confirms, use the project's configured format:

```bash
# Check configured template
git config --get adr.template  # Default: madr

# Create the ADR
git adr new "Use PostgreSQL for application database"
```

Then provide the content for the editor, following the appropriate format template from `references/formats/`.

## MADR-Guided Questions

When context is incomplete, ask clarifying questions:

### Essential Questions

1. **What is being decided?**
   - "What's the specific decision we're recording?"
   - "Is this about technology choice, architecture pattern, or process?"

2. **Why is this decision needed?**
   - "What problem does this solve?"
   - "What constraints are we working within?"

3. **What was chosen?**
   - "What's the final decision?"
   - "What's the primary reason for this choice?"

### If Time Permits

4. **What alternatives were considered?**
   - "Were there other options on the table?"
   - "Why were they rejected?"

5. **What are the consequences?**
   - "What are the benefits of this approach?"
   - "What risks or tradeoffs are we accepting?"

## Decision Quality Checklist

Before creating the ADR, verify:

- [ ] **Significant**: Is this decision worth documenting?
  - Affects multiple components?
  - Hard to reverse?
  - Team members need to understand this?

- [ ] **Clear context**: Would a new team member understand WHY?

- [ ] **Explicit decision**: Is the choice unambiguous?

- [ ] **Actionable consequences**: Do we know what happens next?

## Example Capture Flow

### Conversation Context

```
User: "We've been going back and forth on the authentication approach.
I think we should use JWT tokens with short expiry and refresh tokens.
This gives us stateless verification while still being secure."

Claude: "That sounds like a significant architectural decision.
Would you like me to capture this as an ADR?

Based on our discussion, I'd document:
- Decision: Use JWT with refresh token pattern
- Context: Need stateless auth for distributed API
- Key benefit: No session store required
- Tradeoff: More complex token management"

User: "Yes, please create it. Also mention we considered session-based
auth but rejected it for scalability."

Claude: "Creating ADR now..."
```

### Execution

```bash
# Create the ADR
git adr new "Use JWT with refresh tokens for authentication"
```

Content generated:
```markdown
# Use JWT with Refresh Tokens for Authentication

## Status

Accepted

## Context

Our distributed API architecture requires authentication that can scale
horizontally without shared state. We need to verify user identity across
multiple service instances without requiring a centralized session store.

## Decision

We will use JSON Web Tokens (JWT) with short expiry (15 minutes) combined
with refresh tokens (7 days) for authentication.

- Access tokens (JWT) are stateless and verified by signature
- Refresh tokens are stored server-side for revocation capability
- Token refresh happens automatically before expiry

## Consequences

### Positive
- Stateless verification enables horizontal scaling
- No session store required for authentication
- Works well with microservices architecture

### Negative
- More complex token management logic
- Must handle token refresh edge cases
- Tokens cannot be immediately revoked (15 min window)

### Neutral
- Standard pattern with good library support
- Team needs to understand JWT security model

## Alternatives Considered

### Session-based Authentication
- Rejected because requires shared session store
- Would create scaling bottleneck
- Adds infrastructure complexity
```

## When NOT to Create an ADR

- **Too detailed**: Implementation specifics that aren't architectural
- **Temporary**: Decisions that will be revisited soon
- **Trivial**: Choices with negligible impact
- **Already documented**: Check if similar ADR exists first

```bash
# Check for existing decisions first
git adr search "authentication|auth|jwt" --regex
```

## Post-Capture Actions

After creating the ADR:

1. **Confirm creation**: Show the ADR ID to user
2. **Suggest linking**: If implementing now, offer to link to commit later
3. **Remind about sync**: If team collaboration, suggest `git adr sync push`

```
ADR created: 20251216-use-jwt-with-refresh-tokens

The decision is now documented. When you implement this:
- Use `git adr link 20251216-use-jwt-with-refresh-tokens <commit>`
  to connect the decision to its implementation

If working with a team, push the ADR:
- `git adr sync push`
```
