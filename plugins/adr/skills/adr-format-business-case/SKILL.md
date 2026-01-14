---
name: Business Case ADR Format
description: This skill should be used when the user asks about "business case ADR", "MBA-style ADR", "cost-benefit ADR", "SWOT ADR", "executive ADR", "ROI ADR", or needs guidance on creating ADRs using the business case format for executive and financial analysis.
version: 1.0.0
---

# Business Case ADR Format

The Business Case format is designed for decisions requiring financial analysis, stakeholder sign-off, and executive-level documentation. It includes SWOT analysis, cost-benefit analysis, and ROI assessment.

## About Business Case Format

The Business Case format is:
- **Executive-focused** - Clear for non-technical stakeholders
- **Financial** - Includes cost-benefit and ROI analysis
- **Comprehensive** - SWOT, risks, and implementation planning
- **Formal** - Stakeholder sign-off section

## Template Structure

```markdown
# {NUMBER}. {TITLE}

Date: {DATE}

## Status

{STATUS}

## Executive Summary

{2-3 sentence overview}

## Business Context

{Business situation description}

## Problem Statement

{Business problem or opportunity}

## SWOT Analysis

### Strengths
### Weaknesses
### Opportunities
### Threats

## Options Considered

### Option 1: {Title}
**Cost**: {Estimate}
**Effort**: {High/Medium/Low}
**Risk**: {High/Medium/Low}
**Alignment**: {Strategic alignment}

## Decision

{Chosen option and justification}

## Cost-Benefit Analysis

### Costs
### Benefits
### ROI Assessment

## Implementation

### Timeline
### Resources Required
### Success Metrics

## Risk Assessment

{Risk table with likelihood, impact, mitigation}

## Stakeholder Sign-off

{Sign-off table}
```

## Section Guide

### Executive Summary

Brief overview for executives:
- What decision was made
- Why it matters to the business
- Key financial impact

### Business Context

Describe business situation:
- Market conditions
- Competitive pressures
- Customer needs
- Organizational goals

### SWOT Analysis

| Category | Focus |
|----------|-------|
| **Strengths** | Internal positive factors |
| **Weaknesses** | Internal limitations |
| **Opportunities** | External potential gains |
| **Threats** | External risks |

### Options with Business Metrics

For each option, document:
- **Cost**: Initial and ongoing
- **Effort**: Implementation effort
- **Risk**: Overall risk level
- **Alignment**: Fit with strategic goals

### Cost-Benefit Analysis

**Costs:**
- Initial investment
- Ongoing operational costs
- Opportunity costs

**Benefits:**
- Short-term gains
- Long-term value
- Intangible benefits

**ROI Assessment:**
- Expected return
- Payback period
- Break-even point

### Implementation Planning

Include:
- Phased timeline
- Resource requirements
- Key milestones
- Success metrics (KPIs)

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | High/Med/Low | High/Med/Low | {Strategy} |

### Stakeholder Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Sponsor | | | |
| Technical Lead | | | |
| Finance | | | |

## When to Use Business Case Format

**Best for:**
- Executive-level decisions
- Significant financial impact
- Decisions requiring formal approval
- Cross-departmental decisions
- Compliance/governance requirements

**Consider other formats when:**
- Purely technical decisions
- Small scope/low cost
- Quick documentation needed
- Internal team decisions

## Business Case Best Practices

### Executive Communication

- Lead with business impact
- Quantify benefits where possible
- Be clear about costs and risks
- Provide actionable recommendations

### Financial Analysis

- Include all cost categories
- Consider total cost of ownership
- Project multi-year costs
- Account for opportunity costs

## Additional Resources

### Templates

Template available at:
`${CLAUDE_PLUGIN_ROOT}/templates/business-case/adr-template.md`
