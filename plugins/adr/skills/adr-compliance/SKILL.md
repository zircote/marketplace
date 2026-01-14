---
name: ADR Compliance
description: This skill should be used when the user asks about "ADR compliance", "architecture compliance", "ADR audit", "enforce ADRs", "check code against ADRs", "ADR violations", or needs guidance on auditing code compliance with accepted architectural decision records.
version: 1.0.0
---

# ADR Compliance

This skill provides guidance on auditing code and system compliance with accepted Architectural Decision Records. Compliance checking ensures that architectural decisions are actually implemented and followed.

## What is ADR Compliance?

ADR Compliance verifies that:
- Implementation matches documented decisions
- New code follows accepted patterns
- Deviations are intentional and documented
- Technical debt from violations is tracked

## Compliance Workflow

### 1. Identify Enforceable ADRs

Not all ADRs require compliance checking:

| ADR Type | Enforcement |
|----------|-------------|
| Technology choice | Check for usage/imports |
| Pattern adoption | Check for structure/patterns |
| Constraint | Check for violations |
| Process decision | Manual review |
| Organizational | Manual audit |

### 2. Define Compliance Criteria

For each enforceable ADR, define:
- What code patterns indicate compliance
- What patterns indicate violations
- Where to look (file patterns, modules)
- How to verify (automated vs manual)

### 3. Check Implementation

Methods for checking:
- Code analysis (grep, AST)
- Architecture tests (ArchUnit, etc.)
- Manual code review
- Runtime verification

### 4. Report and Remediate

Document findings:
- List violations found
- Assess severity
- Recommend remediation
- Track resolution

## Compliance Checking Approaches

### Code Pattern Analysis

Search for patterns that should/shouldn't exist:

```bash
# Check for prohibited imports (ADR says don't use library X)
grep -r "import libraryX" src/

# Check for required patterns (ADR says use factory pattern)
grep -r "Factory.create" src/
```

### Architecture Testing

Use architecture test frameworks:

**Java (ArchUnit):**
```java
@ArchTest
static final ArchRule servicesShouldNotAccessRepositories =
    noClasses().that().resideInAPackage("..service..")
    .should().accessClassesThat().resideInAPackage("..repository..");
```

**TypeScript:**
```typescript
// Custom architecture rules
describe('Architecture compliance', () => {
  it('services should not import from UI layer', () => {
    // Check import patterns
  });
});
```

### Manual Review Checklist

For ADRs requiring manual review:
- [ ] Implementation matches decision
- [ ] No unauthorized deviations
- [ ] Documentation updated
- [ ] Tests reflect architecture

## ADR-Specific Compliance Checks

### Technology Selection ADRs

"Use PostgreSQL for primary storage"

**Compliance checks:**
- Database connections use PostgreSQL
- No other databases for primary data
- Configuration points to PostgreSQL

### Pattern Adoption ADRs

"Adopt event-driven architecture"

**Compliance checks:**
- Components communicate via events
- Direct calls minimized
- Event schemas defined
- Event handlers implemented

### Constraint ADRs

"All external APIs must use authentication"

**Compliance checks:**
- No unauthenticated endpoints
- Auth middleware applied
- Token validation present

### Integration ADRs

"Use service X for notifications"

**Compliance checks:**
- Service X client used
- No alternative notification services
- Configuration for service X present

## Compliance Reporting

### Violation Report Format

```markdown
## ADR Compliance Report

**Date**: {date}
**Scope**: {files/modules checked}

### Summary

| Status | Count |
|--------|-------|
| Compliant | X |
| Violations | Y |
| Undetermined | Z |

### Violations Found

#### ADR-001: Use PostgreSQL

**Severity**: High
**Location**: `src/legacy/data.js:45`
**Issue**: Direct MySQL connection found
**Recommendation**: Migrate to PostgreSQL adapter

#### ADR-007: Event-Driven Architecture

**Severity**: Medium
**Location**: `src/services/order.ts:123`
**Issue**: Synchronous call to payment service
**Recommendation**: Emit PaymentRequired event
```

### Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **Critical** | Security or data risk | Immediate fix |
| **High** | Architectural violation | Fix in next sprint |
| **Medium** | Pattern deviation | Plan remediation |
| **Low** | Minor inconsistency | Track for cleanup |

## Continuous Compliance

### CI/CD Integration

Add compliance checks to pipeline:
1. Run architecture tests
2. Execute pattern checks
3. Generate compliance report
4. Fail/warn on violations

### Periodic Audits

Schedule regular compliance audits:
- Weekly: Automated checks
- Monthly: New ADR verification
- Quarterly: Full architecture audit

### Tracking Violations

Maintain violation backlog:
- Tag violations with ADR reference
- Track remediation status
- Monitor violation trends
- Celebrate compliance improvements

## Compliance Configuration

Configure in `.claude/adr.local.md`:

```yaml
compliance:
  enabled: true
  check_all_accepted: true
  file_patterns:
    - "**/*.ts"
    - "**/*.py"
  ignore_patterns:
    - "**/test/**"
    - "**/node_modules/**"
```

## Additional Resources

### Reference Files

- **`references/compliance-patterns.md`** - Common compliance check patterns
- **`references/automation.md`** - Automation strategies

### Related Skills

- **adr-integration** - CI/CD integration patterns
- **adr-quality** - ADR quality for compliance
