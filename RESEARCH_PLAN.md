# Research Plan: Zircote Marketplace Codebase Analysis

## Research Type
**CODEBASE** - Software architecture, implementation patterns, dependencies

## Research Subject
Zircote Claude Marketplace (`./`) - A curated collection of Claude Code plugins featuring specialized agents, development workflows, monitoring integrations, and document processing capabilities.

## Success Criteria

### Primary Questions
1. What is the overall architecture and structure of the marketplace?
2. How are plugins organized and what are the key patterns for each plugin type (agents, commands, skills, hooks)?
3. What external integrations exist (GitHub, MCP servers, external repos)?
4. What are the dependencies between plugins?
5. How does the plugin registration and discovery system work?

### Expected Deliverables
- Complete codebase architecture map
- Plugin-by-plugin analysis with component inventory
- Pattern documentation for reusable abstractions
- Dependency graph (internal and external)
- Quality and consistency assessment

## Research Scope

### In Scope
- 5 local plugins: `zircote`, `gh`, `datadog`, `nsip`, `document-skills`
- 3 external plugins (GitHub-sourced): `claude-spec`, `memory-capture`, `git-adr`
- Marketplace configuration (`.claude-plugin/marketplace.json`)
- Agent definitions, command definitions, skill definitions, hook implementations
- MCP server configurations

### Out of Scope
- Node module internals in `chrome-devtools/scripts/node_modules/`
- Git internal files
- External repo source code (only referenced, not cloned locally)

## Methodology

### Phase 1: Scope Definition ✓
- Define research questions and success criteria
- Write this RESEARCH_PLAN.md

### Phase 2: Evidence Gathering - Plugin Architectures
- Read each plugin's `plugin.json` manifest
- Read each plugin's `README.md`
- Inventory all agents, commands, skills, hooks per plugin
- Map MCP server configurations

### Phase 3: Pattern Analysis
- Identify common patterns across agents
- Document command naming conventions
- Analyze skill structure standards
- Examine hook implementation patterns

### Phase 4: Dependency Mapping
- Internal plugin dependencies
- External GitHub repository references
- MCP server dependencies
- Tool/utility dependencies

### Phase 5: Synthesis and Report
- Cross-reference all findings
- Identify architectural strengths and gaps
- Produce final RESEARCH_REPORT.md

## Parallel Subagent Opportunities

The following can be investigated in parallel:
1. **Plugin Inventory Agent**: Count and categorize all components per plugin
2. **Pattern Analysis Agent**: Identify reusable patterns and conventions
3. **Dependency Mapping Agent**: Trace all internal and external dependencies
4. **Quality Assessment Agent**: Evaluate consistency and documentation coverage

## Estimated Complexity
- **Scope**: Medium-large (5 local plugins, 3 external references, ~200+ files)
- **Depth**: Medium (architecture-level, not line-by-line)
- **Risk**: Low (read-only analysis, no code changes)

## Notes
- Current branch: `feat/python-skel-bump-version`
- There are staged changes to `.claude-plugin/marketplace.json`
- Some deleted files in `plugins/copilot/` suggest recent restructuring
