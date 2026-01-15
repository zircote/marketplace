---
title: "{TITLE}"
description: "{DESCRIPTION}"
type: adr
category: {CATEGORY}
tags:
  - {tag}
status: proposed
created: {DATE}
updated: {DATE}
author: {AUTHOR}
project: {PROJECT}
technologies:
  - {technology}
audience:
  - developers
related:
  - {related_adr}
---

# ADR-{NUMBER}: {TITLE}

## Status

Proposed

## Context

### Background and Problem Statement

{Describe the context requiring this decision. Include relevant history, current state, and what is driving the need for a decision. Be specific about the problem being solved.}

### Current Limitations

{Describe limitations of the current approach or system that this decision addresses. Use numbered lists for multiple limitations with explanations.}

## Decision Drivers

### Primary Decision Drivers

{List the most important factors influencing this decision. These should be weighted most heavily in evaluation.}

1. **{Driver 1}**: {Explanation of why this matters}
2. **{Driver 2}**: {Explanation of why this matters}

### Secondary Decision Drivers

{List factors that influenced the decision but were not individually decisive.}

1. **{Driver 1}**: {Explanation}
2. **{Driver 2}**: {Explanation}

## Considered Options

### Option 1: {Option Title}

**Description**: {Brief description of this option}

**Technical Characteristics**:
- {characteristic 1}
- {characteristic 2}

**Advantages**:
- {advantage 1}
- {advantage 2}

**Disadvantages**:
- {disadvantage 1}
- {disadvantage 2}

**Risk Assessment**:
- **Technical Risk**: {Low|Medium|High}. {Explanation}
- **Schedule Risk**: {Low|Medium|High}. {Explanation}
- **Ecosystem Risk**: {Low|Medium|High}. {Explanation}

### Option 2: {Option Title}

**Description**: {Brief description of this option}

**Technical Characteristics**:
- {characteristic 1}
- {characteristic 2}

**Advantages**:
- {advantage 1}
- {advantage 2}

**Disadvantages**:
- {disadvantage 1}
- {disadvantage 2}

**Disqualifying Factor** (if applicable): {Why this option was rejected}

**Risk Assessment**:
- **Technical Risk**: {Low|Medium|High}. {Explanation}
- **Schedule Risk**: {Low|Medium|High}. {Explanation}
- **Ecosystem Risk**: {Low|Medium|High}. {Explanation}

## Decision

{State the decision clearly and directly. Include specifics about implementation choices, technologies, and standards to be followed.}

The implementation will use:
- **{Component 1}** for {purpose}
- **{Component 2}** for {purpose}

## Consequences

### Positive

1. **{Consequence Title}**: {Detailed explanation of the positive outcome}
2. **{Consequence Title}**: {Detailed explanation of the positive outcome}

### Negative

1. **{Consequence Title}**: {Detailed explanation of the negative outcome and any mitigations}
2. **{Consequence Title}**: {Detailed explanation of the negative outcome and any mitigations}

### Neutral

1. **{Consequence Title}**: {Explanation of neutral outcomes that don't clearly favor or disfavor the decision}

## Decision Outcome

{Summarize how the decision achieves (or is expected to achieve) its primary objectives. Include measurable outcomes where possible.}

Mitigations:
- {Mitigation for negative consequence 1}
- {Mitigation for negative consequence 2}

## Related Decisions

- [ADR-{NUMBER}: {Title}]({filename}) - {Brief description of relationship}

## Links

- [{Resource name}]({url}) - {Brief description}

## More Information

- **Date:** {DATE}
- **Source:** {Reference document, specification, or discussion}
- **Related ADRs:** {List of related ADRs}

## Audit

### {DATE}

**Status:** Pending

**Findings:**

| Finding | Files | Lines | Assessment |
|---------|-------|-------|------------|
| {Description of finding} | `{file_path}` | L{start}-L{end} | {compliant\|non-compliant\|partial} |

**Summary:** {Brief summary of audit findings}

**Action Required:** {None \| Description of required actions}
