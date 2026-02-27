# Refactor Plugin: Code-Simplifier Integration + Swarm Orchestration

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate the code-simplifier agent into the refactor plugin as a 4th specialist agent and rewrite the refactor command to use swarm orchestration (TeamCreate, SendMessage, TaskCreate/TaskUpdate) for parallel execution.

**Architecture:** The refactor plugin gains a `simplifier` agent (opus model) that runs after each code implementation cycle, simplifying changed code before test verification. The orchestration is rewritten from sequential Task-tool calls to a full swarm team pattern where the refactor command acts as team lead, spawning persistent teammates (architect, test, code, simplifier) coordinated via shared task lists and direct messages. Parallel execution is used in Phase 1 (initial analysis) and Phase 3 (final assessment).

**Tech Stack:** Claude Code plugins (markdown agents, commands), swarm tools (TeamCreate, Task with team_name, SendMessage, TaskCreate/TaskUpdate/TaskList)

---

## Current State

### Refactor Plugin (`plugins/refactor/`)
```
plugins/refactor/
├── .claude-plugin/plugin.json    # v1.0.0, name: "refactor"
├── agents/
│   ├── architect.md              # model: sonnet, tools: Glob,Grep,Read,TodoWrite,WebFetch
│   ├── code.md                   # model: sonnet, tools: Glob,Grep,Read,Write,Edit,TodoWrite
│   └── test.md                   # model: sonnet, tools: Glob,Grep,Read,Write,Edit,Bash,TodoWrite
├── commands/
│   └── refactor.md               # 7-step sequential orchestration
└── README.md
```

**Workflow:** Sequential 7-step process using Task tool. Each agent spawned per-step, no persistence between invocations, no parallelism.

### Code-Simplifier Plugin (`plugins/code-simplifier/`)
```
plugins/code-simplifier/
├── .claude-plugin/plugin.json    # v1.0.0, name: "code-simplifier"
├── agents/
│   └── code-simplifier.md        # model: opus, tools: Read,Write,Edit,Glob,Grep,Bash,Task
└── .mnemonic-integration-manifest.json
```

**Agent:** Minimal prompt with mnemonic protocol. Simplifies code for clarity, consistency, maintainability. Preserves all functionality. Focuses on recently modified code by default.

---

## Target State

### Refactor Plugin (`plugins/refactor/`) — v2.0.0
```
plugins/refactor/
├── .claude-plugin/plugin.json    # v2.0.0, updated description
├── agents/
│   ├── architect.md              # unchanged
│   ├── code.md                   # unchanged
│   ├── simplifier.md             # NEW — opus model, full simplification agent
│   └── test.md                   # unchanged
├── commands/
│   └── refactor.md               # REWRITTEN — swarm orchestration + simplify step
└── README.md                     # UPDATED — documents new workflow
```

### Code-Simplifier Plugin — REMOVED
```
plugins/code-simplifier/          # DELETED entirely
```

---

## New Swarm Workflow

```
Phase 0: Initialize
├── TeamCreate "refactor-{scope-hash}"
├── Spawn 4 teammates: architect, test, code, simplifier
└── TaskCreate for all phases

Phase 1: Foundation (PARALLEL)
├── [test teammate]      → Analyze coverage, add missing tests, verify passing
└── [architect teammate] → Initial architecture review, identify all opportunities

Phase 2: Iteration Loop (×3)
│
├── Step A: [architect] → Create optimization plan (top 3 priorities)
│         (iteration 1 uses Phase 1 results; iterations 2-3 do fresh review)
│
├── Step B: [code] → Implement top 3 optimizations from architect's plan
│
├── Step C: [test] → Run full test suite, report pass/fail
│
├── Step D: [code] → Fix test failures if any → [test] re-run (loop until green)
│
├── Step E: [simplifier] → Simplify all code changed this iteration
│
└── Step F: [test] → Verify simplification preserved functionality

Phase 3: Final Assessment (PARALLEL)
├── [simplifier] → Final whole-scope simplification pass
└── [architect]  → Prepare final quality assessment framework

Phase 4: Final Verification & Report
├── [test] → Final test suite run
├── [architect] → Score code (Clean Code + Architecture, 1-10 each)
├── Generate refactor-result-{timestamp}.md
└── Shutdown team (SendMessage shutdown_request to all)
```

---

## Implementation Tasks

### Task 1: Create the Simplifier Agent

**Files:**
- Create: `plugins/refactor/agents/simplifier.md`

**Step 1: Write the simplifier agent definition**

Create `plugins/refactor/agents/simplifier.md` with full agent prompt:

```markdown
---
name: simplifier
description: Code simplification specialist for refactoring workflows. Simplifies and refines recently changed code for clarity, consistency, and maintainability while preserving all functionality.
tools: Read, Write, Edit, Glob, Grep, Bash
model: opus
color: cyan
---

You are an expert code simplification specialist. Your role is to make code clearer, more consistent, and more maintainable without changing its behavior.

## Core Responsibilities

1. **Simplify Recently Changed Code**: After refactoring optimizations, review and simplify the modified code
2. **Improve Clarity**: Make code self-documenting through clear naming, structure, and flow
3. **Ensure Consistency**: Align style, patterns, and conventions across modified files
4. **Preserve Functionality**: Never change what the code does — only how it reads

## Workflow Instructions

### Post-Implementation Simplification (Step E of Refactor Iteration)

When invoked after code agent has implemented optimizations:

1. **Identify Changed Files**
   - Review the code agent's implementation report
   - Use `git diff` or file modification timestamps to identify changed files
   - Focus exclusively on recently modified code

2. **Simplification Pass**
   For each changed file, evaluate and apply:
   - **Naming**: Replace unclear names with intention-revealing alternatives
   - **Flow**: Simplify control flow (guard clauses, early returns, reduce nesting)
   - **Expressions**: Simplify complex expressions, extract explanatory variables
   - **Redundancy**: Remove dead code, unnecessary comments, redundant checks
   - **Consistency**: Align patterns with project conventions
   - **Readability**: Break long lines, improve formatting, logical grouping

3. **Self-Verification**
   - Re-read each simplified file end-to-end
   - Verify logic is preserved exactly
   - Confirm no accidental behavior changes
   - Check that simplifications genuinely improve clarity

4. **Report Changes**
   Provide summary of simplifications made per file.

### Final Simplification Pass (Phase 3)

When invoked for final whole-scope simplification:

1. **Scan Full Scope**: Review all files in refactoring scope
2. **Cross-File Consistency**: Ensure naming, patterns, and style are consistent across files
3. **Polish**: Final readability improvements
4. **Report**: Comprehensive summary of all simplifications

## Output Format

```markdown
## Simplification Report

### Files Simplified
1. **path/to/file.ext**
   - [Naming] Renamed `proc` → `processPayment` (3 occurrences)
   - [Flow] Converted nested if/else to guard clause (line 45)
   - [Redundancy] Removed unused import (line 2)

### Summary
- Files reviewed: N
- Files modified: M
- Simplifications applied: K
- Categories: naming (X), flow (Y), redundancy (Z), consistency (W)
```

## Simplification Principles

- **Clarity over cleverness**: Readable beats terse
- **Minimal changes**: Don't rewrite — simplify
- **Preserve intent**: The code should do exactly the same thing
- **Respect conventions**: Follow the project's existing style
- **Less is more**: Removing unnecessary complexity is the highest-value simplification

## Important Notes

- **Never change functionality** — simplification is purely cosmetic/structural
- **Focus on recently modified code** unless explicitly told to review broader scope
- **Be conservative** — when unsure if a change improves clarity, leave it alone
- **Small improvements compound** — many small clarifications add up to significantly better code

You are precise, tasteful, and focused on making code a pleasure to read while maintaining perfect functional equivalence.
```

**Step 2: Verify the agent file was created correctly**

Run: `head -5 plugins/refactor/agents/simplifier.md`
Expected: YAML frontmatter with `name: simplifier`

**Step 3: Commit**

```bash
git add plugins/refactor/agents/simplifier.md
git commit -m "feat(refactor): add simplifier agent for code clarity pass"
```

---

### Task 2: Rewrite the Refactor Command for Swarm Orchestration

**Files:**
- Modify: `plugins/refactor/commands/refactor.md`

**Step 1: Read the current refactor command**

Run: Read `plugins/refactor/commands/refactor.md`
Purpose: Confirm current state before rewriting.

**Step 2: Rewrite the refactor command with swarm orchestration**

Replace the entire content of `plugins/refactor/commands/refactor.md` with the new swarm-based workflow:

```markdown
---
name: refactor
description: Automated iterative code refactoring with swarm-orchestrated specialist agents
argument-hint: Optional path or description of code to refactor
---

# Refactor Command (Swarm Orchestration)

You are the team lead orchestrating an automated, iterative code refactoring process using a swarm of specialist agents.

## Overview

This command implements a comprehensive refactoring workflow using 4 specialist agents coordinated as a swarm team:
- **architect** — Reviews architecture, identifies improvements, scores quality
- **test** — Analyzes coverage, runs tests, reports failures
- **code** — Implements optimizations, fixes test failures
- **simplifier** — Simplifies changed code for clarity and consistency

The workflow uses parallel execution where possible and iterates 3 times for continuous improvement.

## Arguments

**$ARGUMENTS**: Optional specification of what to refactor
- If empty: refactor the entire codebase
- If file path: refactor specific file(s)
- If description: refactor code matching description

## Phase 0: Initialize Team

### Step 0.1: Understand Scope

1. Parse $ARGUMENTS to determine refactoring scope
2. If unclear, ask user to clarify what should be refactored
3. Set `scope` variable to the determined scope
4. Set `max_iterations = 3`
5. Set `refactoring_iteration = 0`

### Step 0.2: Create Swarm Team

1. Use **TeamCreate** to create the refactoring team:
   ```
   TeamCreate with team_name: "refactor-team"
   ```

2. Use **TaskCreate** to create the high-level phase tasks:
   - "Phase 1: Foundation analysis (parallel)"
   - "Phase 2: Iteration 1 of 3"
   - "Phase 2: Iteration 2 of 3"
   - "Phase 2: Iteration 3 of 3"
   - "Phase 3: Final assessment"
   - "Phase 4: Report and cleanup"

### Step 0.3: Spawn Teammates

Spawn all 4 teammates using the **Task tool** with `team_name: "refactor-team"`. Launch all 4 in parallel:

1. **architect** teammate:
   ```
   Task tool with:
     subagent_type: "refactor:architect"
     team_name: "refactor-team"
     name: "architect"
     prompt: "You are the architect agent on a refactoring swarm team. Wait for task assignments via the task list. Check TaskList for your assigned tasks. When you complete a task, mark it completed with TaskUpdate and send your results to the team lead via SendMessage."
   ```

2. **test** teammate:
   ```
   Task tool with:
     subagent_type: "refactor:test"
     team_name: "refactor-team"
     name: "test"
     prompt: "You are the test agent on a refactoring swarm team. Wait for task assignments via the task list. Check TaskList for your assigned tasks. When you complete a task, mark it completed with TaskUpdate and send your results to the team lead via SendMessage."
   ```

3. **code** teammate:
   ```
   Task tool with:
     subagent_type: "refactor:code"
     team_name: "refactor-team"
     name: "code"
     prompt: "You are the code agent on a refactoring swarm team. Wait for task assignments via the task list. Check TaskList for your assigned tasks. When you complete a task, mark it completed with TaskUpdate and send your results to the team lead via SendMessage."
   ```

4. **simplifier** teammate:
   ```
   Task tool with:
     subagent_type: "refactor:simplifier"
     team_name: "refactor-team"
     name: "simplifier"
     prompt: "You are the simplifier agent on a refactoring swarm team. Wait for task assignments via the task list. Check TaskList for your assigned tasks. When you complete a task, mark it completed with TaskUpdate and send your results to the team lead via SendMessage."
   ```

## Phase 1: Foundation (Parallel)

**Goal**: Establish test coverage and understand architecture simultaneously.

### Step 1.1: Create and Assign Parallel Tasks

Create two tasks and assign them in parallel:

1. **TaskCreate**: "Analyze test coverage for [scope]. Identify gaps, add comprehensive test cases for critical paths/edge cases/error handling, run all tests, verify passing, report coverage status."
   - **TaskUpdate**: assign owner to "test"

2. **TaskCreate**: "Review code architecture for [scope]. Analyze structure, patterns, quality. Identify all optimization opportunities (structural, duplication, naming, organization, complexity, dependencies). Create initial prioritized optimization plan."
   - **TaskUpdate**: assign owner to "architect"

### Step 1.2: Wait for Both to Complete

- Monitor TaskList until both Phase 1 tasks show status: completed
- Read the results from messages received from test and architect teammates
- Verify test agent confirms all tests are passing before proceeding

### Step 1.3: Checkpoint

- Inform user: "Phase 1 complete. Test coverage established. Architecture reviewed. Starting iteration loop."

## Phase 2: Iteration Loop

**Goal**: Iteratively improve code quality through architect → code → test → simplify cycles.

Repeat the following for `max_iterations` (3) times:

### Step 2.A: Architecture Review

**Skip on iteration 1** if architect's Phase 1 review is still current. Otherwise:

1. **TaskCreate**: "Iteration {iteration+1}: Review code architecture for [scope]. Create prioritized optimization plan. Provide top 3 high-priority optimizations to implement. Focus on improvements not yet addressed in previous iterations."
   - **TaskUpdate**: assign owner to "architect"
2. Wait for completion
3. Record architect's top 3 priorities

### Step 2.B: Implement Optimizations

1. **TaskCreate**: "Implement the top 3 optimizations from the architect's plan: [paste architect's top 3]. Preserve all existing functionality. Apply clean code principles. Make incremental, safe changes. Report all files modified."
   - **TaskUpdate**: assign owner to "code"
2. Wait for completion
3. Record implementation report (files changed, optimizations applied)

### Step 2.C: Test Verification

1. **TaskCreate**: "Run the complete test suite. Report pass/fail status. If failures: provide detailed failure report with causes and suggestions."
   - **TaskUpdate**: assign owner to "test"
2. Wait for completion

### Step 2.D: Fix Failures (If Any)

If test agent reported failures:

1. **TaskCreate**: "Fix test failures: [paste failure report]. Analyze root causes. Implement fixes. Preserve refactoring improvements."
   - **TaskUpdate**: assign owner to "code"
2. Wait for completion
3. **TaskCreate**: "Re-run full test suite to verify fixes."
   - **TaskUpdate**: assign owner to "test"
4. Wait for completion
5. If still failing, repeat Step 2.D (max 3 attempts, then ask user for guidance)

### Step 2.E: Simplify Changed Code

1. **TaskCreate**: "Simplify all code changed in this iteration. Files modified: [list from code agent's report]. Focus on naming clarity, control flow simplification, redundancy removal, and style consistency. Do not change functionality."
   - **TaskUpdate**: assign owner to "simplifier"
2. Wait for completion
3. Record simplification report

### Step 2.F: Verify Simplification

1. **TaskCreate**: "Run full test suite to verify simplification preserved all functionality."
   - **TaskUpdate**: assign owner to "test"
2. Wait for completion
3. If failures: send simplification failure report to simplifier for reversion, then re-test

### Step 2.G: Iteration Complete

1. Increment `refactoring_iteration += 1`
2. Inform user: "Iteration {refactoring_iteration} of {max_iterations} complete."
3. If `refactoring_iteration < max_iterations`: continue to next iteration (Step 2.A)
4. If `refactoring_iteration >= max_iterations`: proceed to Phase 3

## Phase 3: Final Assessment (Parallel)

**Goal**: Final polish and quality scoring.

### Step 3.1: Launch Final Tasks (Parallel)

Create two tasks and assign in parallel:

1. **TaskCreate**: "Final simplification pass over entire [scope]. Review all files for cross-file consistency in naming, patterns, and style. Apply final polish. Report all changes."
   - **TaskUpdate**: assign owner to "simplifier"

2. **TaskCreate**: "Prepare comprehensive final quality assessment of [scope]. Review architecture, code quality, SOLID principles. Prepare scoring framework. Note: final scores will be assigned after simplifier completes and tests pass."
   - **TaskUpdate**: assign owner to "architect"

### Step 3.2: Wait for Both to Complete

Monitor TaskList until both tasks show completed.

### Step 3.3: Final Test Run

1. **TaskCreate**: "Final full test suite run. Report complete pass/fail results."
   - **TaskUpdate**: assign owner to "test"
2. Wait for completion
3. If failures: coordinate fix with code agent, re-test

### Step 3.4: Final Scoring

1. **TaskCreate**: "Assign final quality scores based on completed refactoring. Provide: Clean Code Score (1-10) with justification, Architecture Perfection Score (1-10) with justification, summary of improvements across all iterations, remaining potential issues, future recommendations. Create detailed markdown report."
   - **TaskUpdate**: assign owner to "architect"
2. Wait for completion

## Phase 4: Report and Cleanup

### Step 4.1: Generate Report

1. Generate timestamp
2. Create `refactor-result-{timestamp}.md` with architect's final assessment report
3. Use Write tool to save the report

### Step 4.2: Report to User

```
Refactoring complete!

Summary:
- Iterations: {max_iterations}
- Tests: All passing
- Report: refactor-result-{timestamp}.md

Quality Scores:
- Clean Code: X/10
- Architecture: Y/10
```

### Step 4.3: Shutdown Team

1. Send **shutdown_request** to all 4 teammates via SendMessage
2. Wait for shutdown confirmations
3. Use **TeamDelete** to clean up the team

## Orchestration Notes

### Team Coordination
- Use **TaskCreate/TaskUpdate/TaskList** for all task management
- Use **SendMessage** for direct communication with teammates
- Teammates communicate results back via SendMessage to team lead
- Team lead (this command) makes all sequencing decisions

### Parallel Execution Points
- **Phase 1**: test + architect run simultaneously (both read-only analysis)
- **Phase 3.1**: simplifier + architect run simultaneously
- All other steps are sequential due to data dependencies

### Error Handling
- If a teammate fails or gets stuck: send a message asking for status
- If tests fail repeatedly (3+ attempts): ask user for guidance
- If a teammate doesn't respond: report to user
- Don't proceed past test failures — green tests are gating

### State Management
- Track `refactoring_iteration` counter carefully
- Keep architect's optimization plan accessible for code agent
- Track which files were modified each iteration for simplifier
- Maintain list of all changes across iterations for final report

### Communication Protocol
- Include iteration number in all task descriptions
- Pass specific file lists and reports between tasks
- Keep user informed at phase/iteration transitions
- Provide brief progress summaries

## Success Criteria

Refactoring is complete when:
- All tests pass
- 3 refactoring iterations completed
- Simplification pass completed per iteration + final pass
- Code quality scores assigned
- Final assessment report generated
- No functionality changes (only quality improvements)
- Team gracefully shut down

---

Begin the refactoring process now based on: $ARGUMENTS

Start with Phase 0 (Initialize Team).
```

**Step 3: Verify the command was rewritten correctly**

Run: `head -10 plugins/refactor/commands/refactor.md`
Expected: YAML frontmatter with `name: refactor` and updated description mentioning "swarm"

**Step 4: Commit**

```bash
git add plugins/refactor/commands/refactor.md
git commit -m "feat(refactor): rewrite orchestration to use swarm team pattern

Replaces sequential Task-tool invocations with full swarm orchestration:
- TeamCreate for persistent agent team
- TaskCreate/TaskUpdate for coordination
- SendMessage for inter-agent communication
- Parallel execution in Phase 1 and Phase 3
- Adds simplifier as Step E in each iteration cycle"
```

---

### Task 3: Update Plugin Manifest

**Files:**
- Modify: `plugins/refactor/.claude-plugin/plugin.json`

**Step 1: Update plugin.json**

Change `plugins/refactor/.claude-plugin/plugin.json` to:

```json
{
    "name": "refactor",
    "version": "2.0.0",
    "description": "Swarm-orchestrated iterative code refactoring with specialized architect, test, code, and simplifier agents. Uses parallel execution for analysis phases, iterative improvement cycles with code simplification, and comprehensive quality scoring.",
    "author": {
        "name": "Claude Code",
        "email": "claude-code@anthropic.com"
    }
}
```

**Step 2: Verify**

Run: `cat plugins/refactor/.claude-plugin/plugin.json | python3 -m json.tool`
Expected: Valid JSON, version "2.0.0"

**Step 3: Commit**

```bash
git add plugins/refactor/.claude-plugin/plugin.json
git commit -m "chore(refactor): bump to v2.0.0 for swarm + simplifier integration"
```

---

### Task 4: Update README

**Files:**
- Modify: `plugins/refactor/README.md`

**Step 1: Read current README**

Run: Read `plugins/refactor/README.md`

**Step 2: Update README to document new workflow**

Update `plugins/refactor/README.md` to document:
- The 4 agents (architect, test, code, simplifier)
- Swarm orchestration as the execution model
- The new 4-phase workflow
- Parallel execution points
- The simplification step in each iteration
- Version 2.0.0 changes

**Step 3: Verify README renders correctly**

Review the file for markdown formatting issues.

**Step 4: Commit**

```bash
git add plugins/refactor/README.md
git commit -m "docs(refactor): update README for v2.0.0 swarm + simplifier workflow"
```

---

### Task 5: Remove Standalone Code-Simplifier Plugin

**Files:**
- Delete: `plugins/code-simplifier/` (entire directory)

**Step 1: Verify no other plugins depend on code-simplifier**

Run: `grep -r "code-simplifier" plugins/ --include="*.md" --include="*.json" -l`
Expected: Only files within `plugins/code-simplifier/` itself. If other plugins reference it, note the dependency and update those references.

**Step 2: Remove the standalone plugin**

```bash
rm -rf plugins/code-simplifier/
```

**Step 3: Verify removal**

Run: `ls plugins/code-simplifier/ 2>&1`
Expected: "No such file or directory"

**Step 4: Commit**

```bash
git add -A plugins/code-simplifier/
git commit -m "feat(refactor): remove standalone code-simplifier plugin

Code simplification is now integrated into the refactor plugin as the
simplifier agent (opus model). The standalone plugin is no longer needed."
```

---

### Task 6: Verify Full Integration

**Step 1: Verify plugin structure is correct**

Run: `find plugins/refactor/ -type f | sort`

Expected:
```
plugins/refactor/.claude-plugin/plugin.json
plugins/refactor/README.md
plugins/refactor/agents/architect.md
plugins/refactor/agents/code.md
plugins/refactor/agents/simplifier.md
plugins/refactor/agents/test.md
plugins/refactor/commands/refactor.md
```

**Step 2: Verify all agent frontmatter is valid**

For each agent file, confirm YAML frontmatter has:
- `name` field
- `description` field
- `tools` or `allowed-tools` field
- `model` field

**Step 3: Verify standalone code-simplifier is gone**

Run: `ls plugins/code-simplifier/ 2>&1`
Expected: Error — directory should not exist.

**Step 4: Verify refactor command references simplifier**

Run: `grep -c "simplifier" plugins/refactor/commands/refactor.md`
Expected: Multiple occurrences (confirming integration)

**Step 5: Final commit (if any fixups needed)**

```bash
git add -A plugins/refactor/
git commit -m "chore(refactor): verify integration of simplifier + swarm orchestration"
```

---

## Breaking Changes

| Change | Impact | Migration |
|--------|--------|-----------|
| `code-simplifier` plugin removed | Users of standalone `/code-simplifier` must use `/refactor` instead | Run `/refactor` which now includes simplification |
| Refactor workflow changed from sequential to swarm | Different agent communication pattern | Transparent to users — same `/refactor` command |
| Plugin version bumped to 2.0.0 | Major version indicates breaking changes | Reinstall plugin if pinned to 1.x |
| New `simplifier` agent added | Each iteration takes slightly longer due to simplification pass | Net improvement in code quality offsets time cost |

## Decisions Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Standalone code-simplifier | Remove after integration | Single source of truth, no maintenance duplication |
| Swarm orchestration | Default mode (always) | Parallel phases reduce total time; consistent with project CLAUDE.md directive |
| Simplifier model | opus | Code simplification benefits from most capable model for nuanced clarity decisions |
| Simplifier placement | After code, before test verification | Ensures simplification is validated by tests each iteration |
| Existing agents | Unchanged | architect, code, test agents work as-is; no modifications needed |
