# Research Plan: XML Demarcation Improvements for Marketplace Plugins

## Research Classification
- **Type**: TECHNICAL + CODEBASE
- **Subject**: XML tag usage optimization in Claude Code plugin prompts (commands, agents, skills)
- **Scope**: All marketplace plugins (gh, zircote, nsip, lsp-tools) + external plugins (claude-spec, git-notes-memory-manager)

## Success Criteria
1. Document Anthropic's official XML tag best practices with source citations
2. Audit all existing commands, agents, and skills for XML demarcation patterns
3. Identify improvement opportunities based on official guidance
4. Create actionable parallel execution plan

## Primary Sources to Investigate

### Anthropic Official Documentation
- [x] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
- [x] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
- [x] Claude Code documentation via claude-code-guide agent
- [x] Anthropic Cookbook (github.com/anthropics/anthropic-cookbook)

### Codebase Audit
- [ ] plugins/gh/commands/*.md (12 files)
- [ ] plugins/zircote/commands/*.md (1 file)
- [ ] plugins/zircote/agents/**/*.md (~116 files)
- [ ] plugins/zircote/skills/*.md
- [ ] plugins/nsip/commands/*.md (10 files)
- [ ] plugins/lsp-tools/commands/*.md (1 file)
- [ ] ../claude-spec/commands/*.md (11 files)
- [ ] ../git-notes-memory-manager/commands/*.md (6 files)

## Key Findings from Anthropic Research

### Official XML Tag Best Practices (Source: Anthropic Docs)

1. **When to Use XML Tags**:
   > "When your prompts involve multiple components like context, instructions, and examples, XML tags can be a game-changer. They help Claude parse your prompts more accurately, leading to higher-quality outputs."

2. **Benefits** (verbatim from docs):
   - **Clarity**: Clearly separate different parts of your prompt
   - **Accuracy**: Reduce errors caused by Claude misinterpreting parts
   - **Flexibility**: Easily find, add, remove, or modify parts without rewriting
   - **Parseability**: Makes post-processing and extraction simpler

3. **Tag Naming** (verbatim):
   > "There are no canonical 'best' XML tags that Claude has been trained with in particular, although we recommend that your tag names make sense with the information they surround."

4. **Best Practices**:
   - Be consistent with tag names throughout prompts
   - Reference tag names in instructions (e.g., "Using the contract in `<contract>` tags...")
   - Nest tags for hierarchical content: `<outer><inner></inner></outer>`
   - Use semantic tag names that describe the content

5. **Power User Pattern** (verbatim):
   > "Combine XML tags with other techniques like multishot prompting (`<examples>`) or chain of thought (`<thinking>`, `<answer>`). This creates super-structured, high-performance prompts."

6. **Claude Training Context**:
   > "Claude was trained specifically to recognize XML tags as a prompt organizing mechanism."

### Common Tag Patterns from Official Sources

| Tag | Purpose | Source |
|-----|---------|--------|
| `<instructions>` | Task instructions | Anthropic Docs |
| `<example>` / `<examples>` | Multishot examples | Anthropic Docs |
| `<thinking>` | Chain of thought | Anthropic Docs |
| `<answer>` | Final response | Anthropic Docs |
| `<document>` / `<documents>` | Document content | Anthropic Cookbook |
| `<quotes>` | Extracted citations | Anthropic Cookbook |
| `<data>` | Variable input data | AWS Guide |
| `<context>` | Background information | Anthropic Cookbook |

### Claude 4.x Specific Guidance

- Claude 4.x models have improved instruction following
- Sensitive to word "think" when extended thinking disabled - use "consider", "evaluate"
- XML tags work well with interleaved thinking
- Can use `<thinking>` and `<answer>` for structured CoT

## Deliverables

1. **RESEARCH_NOTES.md** - Detailed audit findings
2. **RESEARCH_REPORT.md** - Final synthesis with recommendations
3. **PARALLEL_EXECUTION_PLAN.md** - Implementation plan with agent assignments

## Potential Rabbit Holes to Avoid

- Don't invent new patterns not supported by official docs
- Don't over-engineer - simple tags for simple content
- Focus on high-impact improvements (conditional logic, examples, constraints)
- Avoid gratuitous XML wrapping of simple prose
