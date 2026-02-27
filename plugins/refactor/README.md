# Refactor Plugin

Swarm-orchestrated iterative code refactoring with specialized AI agents that ensure test coverage, design optimizations, simplify code, and verify quality through parallel execution and multiple refinement cycles.

## Overview

The Refactor plugin orchestrates four specialized agents as a swarm team to systematically improve code quality while preserving functionality:

- **Architect Agent** — Reviews code architecture, plans optimizations, scores quality
- **Refactor-Test Agent** — Ensures comprehensive test coverage and validates changes
- **Refactor-Code Agent** — Implements clean code improvements safely
- **Simplifier Agent** — Simplifies changed code for clarity, consistency, and maintainability

## How It Works

The refactoring process uses swarm orchestration (TeamCreate, TaskCreate/TaskUpdate, SendMessage) with parallel execution where possible:

```
Phase 0: Initialize
├── Create swarm team
├── Spawn 4 teammates: architect, refactor-test, refactor-code, simplifier
└── Create phase tasks

Phase 1: Foundation (PARALLEL)
├── [refactor-test]      → Analyze coverage, add missing tests, verify passing
└── [architect] → Initial architecture review, identify all opportunities

Phase 2: Iteration Loop (×3)
│
├── Step A: [architect]       → Create optimization plan (top 3 priorities)
├── Step B: [refactor-code]  → Implement top 3 optimizations
├── Step C: [refactor-test]  → Run full test suite, report pass/fail
├── Step D: [refactor-code]  → Fix test failures if any → [refactor-test] re-run
├── Step E: [simplifier]     → Simplify all code changed this iteration
└── Step F: [refactor-test]  → Verify simplification preserved functionality

Phase 3: Final Assessment (PARALLEL)
├── [simplifier] → Final whole-scope simplification pass
└── [architect]  → Prepare final quality assessment framework

Phase 4: Final Verification & Report
├── [refactor-test] → Final test suite run
├── [architect]     → Score code (Clean Code + Architecture, 1-10 each)
├── Generate refactor-result-{timestamp}.md
└── Shutdown team
```

## Quick Start

```bash
# Refactor entire codebase
/refactor

# Refactor specific directory
/refactor src/utils/

# Refactor specific file
/refactor src/app.ts

# Refactor by description
/refactor "authentication logic"
```

## Features

### Safety First
- **No Functionality Changes**: Only improves code quality, never alters behavior
- **Test-Driven**: Ensures tests pass before and after each change
- **Iterative Validation**: Multiple checkpoints prevent regressions
- **Simplification Verification**: Tests run after every simplification pass

### Parallel Execution
- **Phase 1**: Test coverage analysis and architecture review run simultaneously
- **Phase 3**: Final simplification and quality assessment run simultaneously
- **Swarm Coordination**: TeamCreate, TaskCreate/TaskUpdate, and SendMessage for efficient orchestration

### Comprehensive Coverage
- **Automatic Test Generation**: Adds missing test cases to meet production standards
- **Edge Case Detection**: Identifies and tests boundary conditions
- **Coverage Analysis**: Reports before/after coverage metrics

### Architecture Excellence
- **Design Review**: Evaluates SOLID principles, patterns, and structure
- **Prioritized Planning**: Focuses on high-impact improvements
- **Quality Scoring**: Provides objective Clean Code and Architecture scores (1-10)

### Code Simplification
- **Post-Implementation Polish**: Simplifier reviews every code change for clarity
- **Naming Improvements**: Replaces unclear names with intention-revealing alternatives
- **Flow Simplification**: Guard clauses, early returns, reduced nesting
- **Redundancy Removal**: Dead code, unnecessary comments, redundant checks
- **Cross-File Consistency**: Final pass ensures consistent patterns across all files

### Detailed Reporting
- **Iteration Summaries**: Track progress through each cycle
- **Simplification Reports**: Document all clarity improvements
- **Final Assessment**: Comprehensive quality report with scores
- **Actionable Insights**: Identifies remaining improvements

## The Four Agents

### Architect Agent
**Role**: Design and architecture analysis

**Capabilities**: Code structure review, pattern identification, optimization planning, quality scoring

**Tools**: Glob, Grep, Read, TodoWrite, WebFetch

### Refactor-Test Agent
**Role**: Quality assurance through testing

**Capabilities**: Coverage analysis, test case generation, test execution, failure diagnosis

**Tools**: Glob, Grep, Read, Write, Edit, Bash, TodoWrite

### Refactor-Code Agent
**Role**: Implementation of refactoring

**Capabilities**: Clean code refactoring, safe incremental changes, test failure fixing, best practice application

**Tools**: Glob, Grep, Read, Write, Edit, TodoWrite

### Simplifier Agent
**Role**: Code clarity and consistency

**Capabilities**: Naming improvements, control flow simplification, redundancy removal, cross-file consistency, readability polish

**Tools**: Read, Write, Edit, Glob, Grep, Bash

**Model**: opus (benefits from most capable model for nuanced clarity decisions)

## Understanding the Quality Scores

### Clean Code Score (1-10)

- **9-10**: Exemplary code - clear, simple, maintainable
- **7-8**: Good quality with minor improvement opportunities
- **5-6**: Acceptable but needs notable improvements
- **3-4**: Poor quality with significant issues
- **1-2**: Very poor, requires major refactoring

**Evaluates**: Naming, function size, DRY principle, comments, error handling, formatting

### Architecture Perfection Score (1-10)

- **9-10**: Excellent architecture following best practices
- **7-8**: Good design with minor concerns
- **5-6**: Acceptable architecture, some issues
- **3-4**: Poor architecture needing significant redesign
- **1-2**: Very poor, major architectural problems

**Evaluates**: SOLID principles, coupling/cohesion, abstraction levels, testability, extensibility

## Use Cases

### When to Use Refactor

**Good for**:
- Legacy code that needs modernization
- Code with low test coverage
- Code with known quality issues
- Preparation before adding features
- Technical debt reduction
- Post-implementation cleanup
- Code review follow-up

**Not suitable for**:
- Adding new features (functionality changes)
- Quick fixes during incidents
- Code with no tests and no test framework
- Experimental or prototype code
- Code scheduled for deletion

## Best Practices

### Before Running Refactor

1. **Commit Your Work**: Ensure clean git state
2. **Set Expectations**: Large codebases take time
3. **Review Scope**: Be specific about what to refactor if needed

### During Refactoring

1. **Be Patient**: Quality takes time, trust the process
2. **Monitor Progress**: Watch the iteration and phase updates
3. **Stay Available**: May need input on ambiguous situations

### After Refactoring

1. **Review the Report**: Read `refactor-result-{timestamp}.md`
2. **Check the Scores**: Understand quality improvements
3. **Review Changes**: Use `git diff` to see modifications
4. **Run Manual Tests**: Verify in your development environment
5. **Consider Remaining Issues**: Plan follow-up work if needed

## Configuration

The refactoring process uses these defaults:

- **Max Iterations**: 3
- **Optimizations per Iteration**: Top 3
- **Test Coverage Target**: Production quality (typically 80%+)

These are currently hardcoded but designed for future configurability.

## Troubleshooting

### Tests Keep Failing

**Issue**: Tests fail repeatedly after fixes

**Solution**:
- Review the test failure patterns
- Check if the code has hidden dependencies
- Ensure test environment is properly configured
- May need to run `/refactor` on smaller scope first

### Iteration Takes Too Long

**Issue**: Each iteration is very slow

**Solution**:
- Reduce scope (refactor specific files/directories)
- Ensure fast test suite (split out slow integration tests)
- Check for performance bottlenecks in codebase

### Agent Gets Stuck

**Issue**: An agent doesn't complete its task

**Solution**:
- The team lead will send a status check message
- May need to cancel and restart with smaller scope
- Report issue if it's a bug in agent instructions

## FAQ

**Q: Will this change my code's functionality?**
A: No. The refactoring process explicitly preserves all functionality. Only code quality and structure are improved.

**Q: What's new in v2.0.0?**
A: Swarm orchestration replaces sequential execution, a new simplifier agent polishes code after each iteration, and parallel execution speeds up analysis phases.

**Q: What does the simplifier do?**
A: After each code implementation cycle, the simplifier reviews changed files for naming clarity, control flow improvements, redundancy removal, and style consistency — without changing functionality.

**Q: Can I stop mid-refactor?**
A: Yes, but you'll lose progress. Better to start with smaller scope.

**Q: Do I need to review every change?**
A: Recommended. While agents are thorough, human review is valuable.

**Q: What if my project has no tests?**
A: The test agent will create them! That's Phase 1.

**Q: What languages/frameworks are supported?**
A: All languages. Agents adapt to your project's testing framework and conventions.

## Version

Current version: 2.0.0

## Changelog

### 2.0.0
- Swarm orchestration (TeamCreate, TaskCreate/TaskUpdate, SendMessage)
- New simplifier agent (opus model) for code clarity passes
- Parallel execution in Phase 1 (foundation) and Phase 3 (final assessment)
- 4-phase workflow replacing 7-step sequential process
- Code simplification step after each iteration cycle

### 1.0.0
- Initial release with sequential 7-step workflow
- Three agents: architect, refactor-test, refactor-code
