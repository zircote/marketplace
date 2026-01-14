# ADR Review Checklist

Use this checklist to review ADRs before accepting them.

## Essential Elements

### Title
- [ ] Clear and specific
- [ ] Action-oriented (verb + noun)
- [ ] Searchable keywords
- [ ] Not too generic ("database decision") or too detailed

### Status
- [ ] Valid status value (proposed/accepted/rejected/deprecated/superseded)
- [ ] Consistent with actual state
- [ ] Date recorded for status changes

### Context
- [ ] Problem statement is clear
- [ ] Background information sufficient
- [ ] Current state described
- [ ] Stakeholders identified
- [ ] Constraints documented

### Decision
- [ ] Clear statement of what was decided
- [ ] Specific enough to be actionable
- [ ] Scope is defined

### Consequences
- [ ] Both positive and negative documented
- [ ] Trade-offs explicitly stated
- [ ] Risks identified
- [ ] Mitigation strategies where applicable

## Quality Criteria

### Completeness
- [ ] All required sections present
- [ ] No placeholder text remaining
- [ ] Links to related ADRs included
- [ ] References to external docs where needed

### Clarity
- [ ] Readable by team members not involved in decision
- [ ] Technical jargon explained or avoided
- [ ] Acronyms defined
- [ ] Future reader perspective considered

### Objectivity
- [ ] Options presented fairly
- [ ] Bias avoided in option descriptions
- [ ] Both pros and cons for each option
- [ ] Evidence-based reasoning

### Consistency
- [ ] Follows project ADR template
- [ ] Naming convention followed
- [ ] Status workflow adhered to
- [ ] Formatting consistent

## Technical Review

### Decision Drivers
- [ ] All relevant forces identified
- [ ] Prioritization clear
- [ ] No missing obvious factors
- [ ] Appropriate weight given to each

### Options Considered
- [ ] Multiple options documented (usually 2-4)
- [ ] Options are genuinely different approaches
- [ ] No straw man options included just to reject
- [ ] "Do nothing" considered if appropriate

### Trade-off Analysis
- [ ] Clear comparison between options
- [ ] Winner justified against drivers
- [ ] Rejected options have clear reasoning

## Process Review

### Stakeholder Input
- [ ] Appropriate stakeholders consulted
- [ ] Dissenting opinions captured
- [ ] Decision makers identified
- [ ] Review process followed

### Timeliness
- [ ] Created before or during decision (not long after)
- [ ] Reflects current state of thinking
- [ ] Not outdated by subsequent changes

### Integration
- [ ] Added to ADR index
- [ ] Related ADRs linked both directions
- [ ] Superseded ADRs updated if applicable

## Red Flags

### Warning Signs to Address

- [ ] No cons listed for chosen option
- [ ] Only one option considered
- [ ] Context is just problem statement (no background)
- [ ] Consequences only list benefits
- [ ] Status doesn't match actual state
- [ ] Missing links to superseded ADRs
- [ ] Technical details without business context
- [ ] Business rationale without technical analysis

## Review Questions

Ask these questions during review:

### Understanding
- Would a new team member understand this decision?
- Are the constraints and context clear?
- Is the reasoning logical and complete?

### Alternatives
- Were alternatives seriously considered?
- Is the comparison fair and complete?
- Are there missing options that should be evaluated?

### Consequences
- Are all significant consequences captured?
- Are the trade-offs acceptable?
- What could go wrong?

### Future
- Will this decision age well?
- When should this be revisited?
- What would trigger reconsideration?

## Post-Acceptance

### After ADR is Accepted

- [ ] Status updated to "accepted"
- [ ] Index README updated
- [ ] Team notified of decision
- [ ] Implementation tickets created if needed
- [ ] Documentation updated to reference ADR
- [ ] Related code comments added where helpful
