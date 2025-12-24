# Parallel Execution Plan: XML Demarcation Improvements

## Overview

This plan enables **rapid parallel completion** of XML demarcation improvements across the marketplace using specialized subagents working simultaneously on independent workstreams.

**Total Scope**: 489 files across 6 plugins
**Estimated Effort**: 44-60 hours (reduced to ~15-20 hours with 3-way parallelization)
**Parallelization Strategy**: 3 independent workstreams + coordination

---

## Workstream Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Main Agent)                     │
│  Coordinates workstreams, resolves conflicts, merges results     │
└─────────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  WORKSTREAM 1   │  │  WORKSTREAM 2   │  │  WORKSTREAM 3   │
│    COMMANDS     │  │     AGENTS      │  │     SKILLS      │
│                 │  │                 │  │                 │
│ • gh (12)       │  │ • 01-core (15)  │  │ • High-priority │
│ • claude-spec   │  │ • 02-lang (20)  │  │   (15 skills)   │
│   (11)          │  │ • 03-infra (15) │  │ • Reference     │
│ • git-notes (6) │  │ • 04-quality    │  │   files (50+)   │
│ • nsip (10)     │  │   (15)          │  │                 │
│ • lsp-tools (1) │  │ • 05-data (12)  │  │                 │
│ • zircote (1)   │  │ • 06-dx (12)    │  │                 │
│                 │  │ • 07-special    │  │                 │
│ Total: 41 files │  │   (10)          │  │ Total: 65 files │
│                 │  │ • 08-business   │  │                 │
│                 │  │   (10)          │  │                 │
│                 │  │ • 09-meta (7)   │  │                 │
│                 │  │                 │  │                 │
│                 │  │ Total: 116      │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Workstream 1: Commands (41 files)

### Subagent Configuration
```
subagent_type: "refactoring-specialist"
model: "sonnet" (for speed)
parallel_instances: 2
```

### Phase 1A: High-Priority Commands (6-8 hours)
**Files**: gh/review-comments.md, gh/pr-fix.md, gh/migrate.md, claude-spec/plan.md, claude-spec/implement.md

**Tasks**:
1. Add `<phase>` wrappers around numbered execution phases
2. Add `<conditional>` tags around decision logic
3. Add `<error_handling>` sections where missing
4. Standardize `<ask_user_question>` patterns

**Subagent Prompt**:
```
You are a refactoring specialist. Update the following command file to add XML demarcation following Anthropic best practices:

1. Wrap numbered phases (Phase 1, Phase 2, etc.) in <phase number="N" name="..."> tags
2. Wrap conditional logic (if X then Y) in <conditional> tags
3. Add <error_handling> section if missing
4. Wrap AskUserQuestion blocks in <ask_user_question> tags

Do NOT:
- Remove existing content
- Change functionality
- Add tags to simple prose (only structured sections)

File: {file_path}
```

### Phase 1B: Medium-Priority Commands (4-6 hours)
**Files**: gh/pr.md, gh/fr.md, gh/sync.md, gh/ff.md, gh/prune.md, gh/cp.md, gh/copilot-onboard.md

**Tasks**:
1. Add `<step>` wrappers to procedural sections
2. Add `<preflight_checks>` where applicable
3. Standardize `<workflow>` structure

### Phase 1C: Simple Commands (2-3 hours)
**Files**: git-notes (6), nsip (10), lsp-tools (1), zircote (1)

**Tasks**:
1. Add `<step>` structure
2. Add `<error_handling>` sections
3. Add `<mcp_integration>` to nsip commands

---

## Workstream 2: Agents (116 files)

### Subagent Configuration
```
subagent_type: "documentation-engineer"
model: "sonnet" (for speed)
parallel_instances: 3
```

### Phase 2A: Template Creation (2 hours)
Create standard XML patterns for agents:

```xml
<!-- Agent XML Template -->
<deliberate_protocol name="{domain}">
  <enforcement_rules>
    <rule sequence="1">
      <condition>Before {action}</condition>
      <action>{verification_action}</action>
      <validation>{validation_method}</validation>
    </rule>
  </enforcement_rules>
</deliberate_protocol>

<execution_strategy>
  <parallel>
    <operation priority="1">{parallel_op_1}</operation>
    <operation priority="2">{parallel_op_2}</operation>
  </parallel>
  <sequential>
    <constraint sequence="1">
      <condition>{dependency_condition}</condition>
      <impact>{impact_description}</impact>
    </constraint>
  </sequential>
</execution_strategy>

<checklist type="{checklist_type}" validation_required="true">
  <item priority="critical" domain="{domain}">
    <criterion>{criterion_text}</criterion>
    <validation_method>{how_to_validate}</validation_method>
  </item>
</checklist>

<output_format type="completion_notification">
  <template>
    <opening_statement>{deliverable_type} delivered successfully</opening_statement>
    <key_artifacts>...</key_artifacts>
    <readiness_status>Ready for {next_step}</readiness_status>
  </template>
</output_format>
```

### Phase 2B: Batch Processing (8-10 hours)
Process agents in category batches (parallel):

| Batch | Categories | Files | Subagent |
|-------|------------|-------|----------|
| Batch A | 01-core, 02-lang | 35 | Agent 1 |
| Batch B | 03-infra, 04-quality | 30 | Agent 2 |
| Batch C | 05-data, 06-dx, 07-special | 34 | Agent 3 |
| Batch D | 08-business, 09-meta | 17 | Agent 1 (after A) |

**Subagent Prompt**:
```
You are a documentation engineer. Add XML demarcation to this agent file following the template patterns provided.

Target sections:
1. "### Deliberate [X] Protocol" → Wrap in <deliberate_protocol>
2. "### Parallel Execution Strategy" → Wrap in <execution_strategy>
3. "[X] checklist:" → Wrap in <checklist>
4. "Completion message format:" → Wrap in <output_format>
5. "## Conditional MCP Tools" → Wrap in <conditional_requirements>

Template: {template_content}
File: {file_path}
```

---

## Workstream 3: Skills (65 high-priority files)

### Subagent Configuration
```
subagent_type: "documentation-engineer"
model: "sonnet"
parallel_instances: 2
```

### Phase 3A: High-Impact Skills (6-8 hours)
**Files** (15 skills):
- backend-development
- frontend-development
- databases
- better-auth
- devops
- ai-multimodal
- anthropic-architect
- code-review
- debugging
- web-frameworks
- ui-styling
- chrome-devtools
- datadog-entity-generator
- changelog-generator
- docs-seeker

**Tasks**:
1. Add `<example>` wrappers around all code examples
2. Add `<constraints>` to limitations sections
3. Add `<output_template>` for response formats
4. Add `<triggers>` for activation conditions

### Phase 3B: Reference Files (4-6 hours)
**Files**: 50+ reference files in skill subdirectories

**Tasks**:
1. Add `<example>` wrappers (primary focus)
2. Ensure consistency with SKILL.md parent

---

## Execution Timeline

### Parallel Execution (All 3 workstreams simultaneously)

```
Hour 0-2:   [WS1: Template creation] [WS2: Template creation] [WS3: Template creation]
Hour 2-8:   [WS1: High-priority]     [WS2: Batch A+B]         [WS3: High-impact skills]
Hour 8-14:  [WS1: Medium-priority]   [WS2: Batch C+D]         [WS3: Reference files]
Hour 14-18: [WS1: Simple commands]   [WS2: Validation]        [WS3: Validation]
Hour 18-20: [                    INTEGRATION & REVIEW                              ]
```

**Total Calendar Time**: ~20 hours with 3-way parallelization
**Total Effort**: 44-60 person-hours

---

## Quality Gates

### Gate 1: Template Validation (Hour 2)
- [ ] All XML templates syntactically valid
- [ ] Templates cover all identified patterns
- [ ] No breaking changes to existing functionality

### Gate 2: Batch Completion (Hour 8, 14)
- [ ] Files pass XML syntax validation
- [ ] No functionality regression
- [ ] Consistent tag naming across files

### Gate 3: Integration (Hour 18)
- [ ] Cross-workstream consistency verified
- [ ] No conflicting patterns
- [ ] Documentation updated

### Gate 4: Final Review (Hour 20)
- [ ] All 489 files audited
- [ ] High-priority files manually reviewed
- [ ] CHANGELOG updated

---

## Subagent Task Distribution

### Task Tool Invocations (Example)

**Workstream 1 - Commands**:
```javascript
// Launch 2 parallel subagents for commands
Task({
  subagent_type: "refactoring-specialist",
  prompt: "Update gh/review-comments.md with XML demarcation...",
  run_in_background: true
})

Task({
  subagent_type: "refactoring-specialist",
  prompt: "Update gh/pr-fix.md with XML demarcation...",
  run_in_background: true
})
```

**Workstream 2 - Agents**:
```javascript
// Launch 3 parallel subagents for agents
Task({
  subagent_type: "documentation-engineer",
  prompt: "Process agents/01-core-development/*.md with XML template...",
  run_in_background: true
})

Task({
  subagent_type: "documentation-engineer",
  prompt: "Process agents/03-infrastructure/*.md with XML template...",
  run_in_background: true
})

Task({
  subagent_type: "documentation-engineer",
  prompt: "Process agents/05-data-ai/*.md with XML template...",
  run_in_background: true
})
```

**Workstream 3 - Skills**:
```javascript
// Launch 2 parallel subagents for skills
Task({
  subagent_type: "documentation-engineer",
  prompt: "Add XML demarcation to skills/backend-development/...",
  run_in_background: true
})

Task({
  subagent_type: "documentation-engineer",
  prompt: "Add XML demarcation to skills/frontend-development/...",
  run_in_background: true
})
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| XML syntax errors | Validate each file with XML linter before commit |
| Functionality regression | Test commands manually after batch |
| Inconsistent patterns | Use shared templates, review cross-workstream |
| Scope creep | Strict adherence to identified patterns only |
| Over-engineering | Limit to documented Anthropic patterns |

---

## Success Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Commands with `<step>` structure | 5% | 100% | 100% |
| Agents with XML demarcation | 0% | 100% | 100% |
| Skills with `<example>` tags | 10% | 80%+ | 80% |
| Error handling coverage | 20% | 100% | 100% |
| Unified tag patterns | 20% | 95%+ | 95% |

---

## Appendix: Tag Reference

### Standard Tags (Use Everywhere)
- `<help_check>` - Help detection (existing)
- `<step>` - Procedural steps
- `<error_handling>` - Error recovery
- `<example>` - Code examples
- `<constraints>` - Limitations

### Command-Specific Tags
- `<phase>` - Execution phases
- `<conditional>` - Decision logic
- `<ask_user_question>` - User prompts
- `<parallel_pattern>` - Parallel execution
- `<workflow>` - Multi-step workflows

### Agent-Specific Tags
- `<deliberate_protocol>` - Protocol enforcement
- `<execution_strategy>` - Parallel/sequential rules
- `<checklist>` - Validation checklists
- `<output_format>` - Completion templates
- `<conditional_requirements>` - MCP dependencies

### Skill-Specific Tags
- `<triggers>` - Activation conditions
- `<output_template>` - Response formats
- `<configuration>` - Setup sections
