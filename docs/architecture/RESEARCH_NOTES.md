# Research Notes: XML Demarcation Audit

## Evidence Collection Summary

### Source 1: Anthropic Official Documentation

**URL**: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags

**Key Quotes (Verbatim)**:

> "When your prompts involve multiple components like context, instructions, and examples, XML tags can be a game-changer. They help Claude parse your prompts more accurately, leading to higher-quality outputs."

**Benefits (verbatim from docs)**:
- **Clarity**: Clearly separate different parts of your prompt and ensure your prompt is well structured.
- **Accuracy**: Reduce errors caused by Claude misinterpreting parts of your prompt.
- **Flexibility**: Easily find, add, remove, or modify parts of your prompt without rewriting everything.
- **Parseability**: Having Claude use XML tags in its output makes it easier to extract specific parts of its response by post-processing.

**Best Practices (verbatim)**:
1. "Be consistent: Use the same tag names throughout your prompts"
2. "Nest tags for hierarchical content"
3. "There are no canonical 'best' XML tags that Claude has been trained with in particular, although we recommend that your tag names make sense with the information they surround."

**Power User Pattern**:
> "Combine XML tags with other techniques like multishot prompting (`<examples>`) or chain of thought (`<thinking>`, `<answer>`). This creates super-structured, high-performance prompts."

**Training Context**:
> "Claude was trained specifically to recognize XML tags as a prompt organizing mechanism."

### Source 2: AWS Prompt Engineering Guide

**URL**: https://github.com/aws-samples/prompt-engineering-with-anthropic-claude-v-3

**Key Insight**:
> "XML tags are angle-bracket tags like `<tag></tag>`. They come in pairs and consist of an opening tag...and a closing tag marked by a `/`."

**Purpose**:
> "Prevent Claude from misinterpreting where variable data begins and ends, particularly when data contains formatting that might resemble instructions."

### Source 3: Anthropic Cookbook

**URL**: https://github.com/anthropics/anthropic-cookbook

**Patterns from Official Examples**:
- `<instructions>` for task instructions
- `<documents>` / `<document>` for input documents
- `<quotes>` for extracted citations
- `<answer>` for final responses
- `<thinking>` for chain of thought
- `<example>` for few-shot examples

---

## Audit Results Summary

### Commands Audit (41 files across 6 plugins)

| Plugin | Files | Current XML | Key Gaps |
|--------|-------|-------------|----------|
| gh | 12 | `<help_check>`, `<help_output>` | Phase structure, conditionals, templates |
| zircote | 1 | `<help_check>` | Minimal, appropriate |
| claude-spec | 11 | 40+ custom tags | Over-engineered, needs consolidation |
| git-notes | 6 | `<help_check>` | Missing error handling, step structure |
| nsip | 10 | `<help_check>` | Missing MCP integration tags |
| lsp-tools | 1 | `<help_check>` | Missing validation tags |

### Agents Audit (~116 files in zircote/agents)

**Current State**: 0% XML usage (pure markdown)

**Opportunities Identified**:
1. `<deliberate_protocol>` - All agents have protocol sections
2. `<execution_strategy>` - Parallel/sequential rules in all agents
3. `<checklist>` - Validation checklists in all agents
4. `<output_format>` - Completion message templates
5. `<conditional_requirements>` - MCP tool dependencies
6. `<examples>` - Good/bad patterns (currently missing)

### Skills Audit (59 directories, 332 files)

**Current State**: ~4% heavy XML usage, ~87% no XML

**Exemplar**: `anthropic-prompt-engineer` (10/10 XML implementation)

**Opportunities**:
1. `<example>` wrappers around code snippets
2. `<constraints>` for limitations sections
3. `<output_template>` for response formats
4. `<triggers>` for activation conditions
5. `<configuration>` for setup sections

---

## Cross-Cutting Patterns Identified

### Pattern 1: Help Check (100% adoption - KEEP)
```xml
<help_check>
  If $ARGUMENTS contains --help/-h:
    Output help text
    HALT immediately
</help_check>
```

### Pattern 2: Phase/Step Structure (NEEDS STANDARDIZATION)
- claude-spec: Uses `<phase>` tags
- gh: Uses markdown headers
- others: Mixed approach

**Recommendation**: Unified `<step>` tag

### Pattern 3: Conditional Logic (NEEDS FORMALIZATION)
- Currently: Embedded in prose
- Recommendation: `<conditional>` or `<when>` tags

### Pattern 4: Error Handling (GAPS)
- Only 8/41 commands have structured error handling
- Recommendation: Universal `<error_handling>` section

### Pattern 5: Parallel Execution (INCONSISTENT)
- claude-spec: 3 different approaches
- others: None
- Recommendation: Unified `<parallel_pattern>` meta-tag

### Pattern 6: User Interaction (UNSTANDARDIZED)
- AskUserQuestion used in 8+ commands
- No consistent structure
- Recommendation: `<ask_user_question>` template

---

## Confidence Levels

| Finding | Confidence | Rationale |
|---------|------------|-----------|
| XML tags improve parsing | HIGH | Official Anthropic docs |
| Semantic tag names preferred | HIGH | Official guidance |
| No "magic" tags exist | HIGH | Explicitly stated |
| Nesting for hierarchy | HIGH | Official best practice |
| Agents would benefit | MEDIUM | Logical extension, no explicit guidance |
| 40+ tags in claude-spec excessive | MEDIUM | Based on maintenance burden |
| Skills need more XML | MEDIUM | Based on exemplar comparison |

---

## Open Questions

1. **Agent-specific guidance?** - Anthropic docs focus on prompts, not agent files specifically
2. **Performance impact?** - No metrics on XML vs markdown parsing speed
3. **Nesting depth limit?** - No official guidance on max nesting
4. **Tag naming conventions?** - "Semantic" is guidance, but no style guide

---

## Key Insights for Implementation

1. **Start with high-impact, low-effort changes** - Add XML to examples, constraints, error handling
2. **Don't over-engineer** - claude-spec's 40+ tags show complexity risk
3. **Consolidate before expanding** - Fix inconsistencies first
4. **Follow the exemplar** - anthropic-prompt-engineer skill is the gold standard
5. **Markdown still valid** - For simple linear content, markdown headers suffice
