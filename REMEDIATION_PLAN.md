# Marketplace Remediation Plan

**Generated:** 2025-12-20
**Review Scope:** Layout, Prompt Engineering, Versioning, Documentation

---

## Executive Summary

Four parallel specialist agents reviewed all 5 local plugins across 4 dimensions. This plan consolidates **47 findings** into prioritized remediation phases.

### Severity Distribution

| Severity | Count | Description |
|----------|-------|-------------|
| **Critical** | 4 | Blocking issues (non-existent files, incorrect descriptions) |
| **High** | 12 | Major gaps affecting adoption/usability |
| **Medium** | 18 | Improvements for consistency and quality |
| **Low** | 13 | Nice-to-haves and polish |

---

## Phase 1: Critical Fixes (Immediate)

### 1.1 zircote: Missing Commands Directory

**Issue**: `plugin.json` references `./commands/code/review-fix.md`, `./commands/code/review.md`, `./commands/deep-research.md`, `./commands/explore.md` but the `commands/` directory doesn't exist.

**Severity**: Critical

**Fix Options**:
- A) Create the commands directory with the referenced files
- B) Remove the `commands` array from plugin.json

**Recommendation**: Option A - The commands are valuable and likely exist elsewhere (possibly in zircote home directory)

---

### 1.2 gh: Incorrect Plugin Description

**Issue**: `plugin.json` description says "115+ specialized Opus 4.5 agents" but only 1 agent exists.

**Severity**: Critical

**Fix**:
```json
// Before
"description": "Comprehensive agent library featuring 115+ specialized Opus 4.5 agents organized by domain"

// After
"description": "GitHub ecosystem integration with git workflows, Copilot configuration, and multi-CI migration"
```

---

### 1.3 gh: Incorrect Keywords

**Issue**: Keywords copied from zircote plugin, don't reflect actual purpose.

**Severity**: Critical

**Fix**:
```json
// Before
"keywords": ["agents", "opus-4.5", "development", "skills", "commands", "specialists", "subagents"]

// After
"keywords": ["github", "copilot", "git-workflow", "ci-cd", "actions", "ecosystem", "migration"]
```

---

### 1.4 Marketplace: Missing LICENSE

**Issue**: No LICENSE file at marketplace root despite MIT references.

**Severity**: Critical

**Fix**: Create `/LICENSE` with MIT license text.

---

## Phase 2: High Priority Fixes (This Week)

### 2.1 All Plugins: Add Author Email

**Issue**: 4 of 5 plugins missing email in author field.

**Affected**: zircote, gh, document-skills, datadog

**Fix**: Add `"email": "zircote@gmail.com"` to all author objects.

---

### 2.2 All Skills: Add Trigger Phrases

**Issue**: Skills rely on implicit activation, reducing discoverability.

**Pattern to Add** (to all SKILL.md files):
```markdown
## Trigger Phrases
Activate when user says:
- "[phrase 1]"
- "[phrase 2]"
- "[phrase 3]"
```

**Priority Skills** (most commonly used):
1. `anthropic-prompt-engineer/SKILL.md`
2. `sequential-thinking/SKILL.md`
3. `mcp-builder/SKILL.md`
4. `code-review/SKILL.md`
5. `python-project-skel/SKILL.md`

---

### 2.3 shepherd.md: Add Anti-Hallucination Rules

**Issue**: Veterinary advice lacks grounding constraints.

**Add to `plugins/nsip/agents/shepherd.md`**:
```markdown
## Critical Rules
1. **NEVER GUESS** veterinary treatment protocols - direct to veterinarian for serious conditions
2. **NEVER FABRICATE** NSIP data - always verify with API tools
3. **ALWAYS CITE** accuracy scores when making breeding recommendations
```

---

### 2.4 All Commands: Standardize Error Handling

**Issue**: Some commands have detailed error handling (ff.md), others have none (pr.md).

**Template for All Commands**:
```markdown
## Error Handling
| Error | Response |
|-------|----------|
| [error type] | [user-friendly message with remediation] |
```

---

### 2.5 Marketplace: Create CONTRIBUTING.md

**Issue**: No contributor guidance exists.

**Content Required**:
- Plugin structure requirements
- Required files checklist
- Pull request process
- Style guidelines

---

### 2.6 gh: Rewrite README.md

**Issue**: README incomplete - doesn't document all 9 commands, agent, or ecosystem skill.

**Required Sections**:
- All commands with examples
- copilot-assistant agent documentation
- ecosystem skill documentation
- Troubleshooting section

---

### 2.7 Version Mismatches

**Issue**: Version inconsistencies between plugin.json and README.md.

| Plugin | plugin.json | README | Action |
|--------|-------------|--------|--------|
| zircote | 0.4.0 | 1.0.1 | Sync to 1.0.1 |
| gh | 0.2.0 | 1.0.0 | Sync to 1.0.0 |
| nsip | 1.3.1 | 1.3.0 | Sync to 1.3.1 |
| datadog | 0.1.0 | 1.0.0 | Sync to 1.0.0 |

---

## Phase 3: Medium Priority (This Sprint)

### 3.1 All Agents: Add Opus 4.5 Capabilities Section

**Issue**: Only DataDog agents include Opus 4.5 capability exploitation.

**Template to Add**:
```markdown
## Opus 4.5 Capabilities

### Parallel Execution Strategy
```
PARALLEL: [independent operations]
SEQUENTIAL when: [dependency conditions]
```

### Deliberate Protocol
Before [action]:
1. [Precondition]
2. [Precondition]
```

---

### 3.2 Marketplace: Add Descriptions to Local Plugins

**Issue**: `marketplace.json` local plugins lack descriptions.

**Fix**:
```json
{
  "name": "zircote",
  "source": "./plugins/zircote",
  "description": "116 specialized agents across 10 domains with 54 skills"
}
```

---

### 3.3 Marketplace: Add Version Constraints for External Plugins

**Issue**: External plugins have no version pinning.

**Fix**:
```json
{
  "name": "claude-spec",
  "source": { "source": "github", "repo": "zircote/claude-spec" },
  "version": "^1.0.0"
}
```

---

### 3.4 All Plugins: Create CHANGELOG.md

**Format**: Keep a Changelog format.

**Content per Plugin**:
```markdown
# Changelog

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD
### Added
- Initial release
```

---

### 3.5 gh: Normalize JSON Indentation

**Issue**: Uses 4-space indentation while all others use 2-space.

---

### 3.6 migrate.md: Refactor Into Modular References

**Issue**: 712 lines is too long for a single command file.

**Recommendation**: Split into:
- `commands/migrate.md` (200 lines - core workflow)
- `references/ci-translations/concourse.md`
- `references/ci-translations/jenkins.md`
- etc.

---

### 3.7 All Skills: Add Output Format Specifications

**Template**:
```markdown
## Output Format
[Specify exact structure of responses]
```

---

### 3.8 datadog Agents: Consolidate Duplicates

**Issue**: datadog-pro.md and datadog-api-expert.md have 86% overlap.

**Options**:
- A) Merge into single agent
- B) Clearly differentiate roles (strategic vs tactical)

---

## Phase 4: Version Bumping Infrastructure

### 4.1 Per-Plugin Configuration

Create `.bumpversion.toml` for each plugin with independent versioning:

**Example for zircote plugin** (`plugins/zircote/.bumpversion.toml`):
```toml
[tool.bumpversion]
current_version = "1.0.1"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
commit = true
tag = false
message = "chore(zircote): bump version to {new_version}"

[[tool.bumpversion.files]]
filename = ".claude-plugin/plugin.json"
search = "\"version\": \"{current_version}\""
replace = "\"version\": \"{new_version}\""

[[tool.bumpversion.files]]
filename = "README.md"
search = "**Version:** {current_version}"
replace = "**Version:** {new_version}"
```

### 4.2 Smart Bump Script

Create `scripts/smart-bump.py`:
```python
#!/usr/bin/env python3
"""Bump versions only for plugins with changes since last release."""

import subprocess
from pathlib import Path

def get_changed_plugins():
    """Detect which plugins have changes."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1"],
        capture_output=True, text=True
    )

    changed_plugins = set()
    for file in result.stdout.strip().split('\n'):
        if file.startswith('plugins/'):
            plugin = file.split('/')[1]
            changed_plugins.add(plugin)

    return changed_plugins

def bump_plugin(plugin: str, part: str = "patch"):
    """Bump version for a specific plugin."""
    plugin_dir = Path(f"plugins/{plugin}")
    subprocess.run(
        ["bump-my-version", "bump", part],
        cwd=plugin_dir
    )
```

### 4.3 Makefile Targets

Add to root Makefile:
```makefile
# Bump specific plugin
bump-zircote:
	cd plugins/zircote && bump-my-version bump patch

bump-gh:
	cd plugins/gh && bump-my-version bump patch

# Smart bump (only changed plugins)
bump-changed:
	python scripts/smart-bump.py patch

# Release all changed plugins
release:
	python scripts/smart-bump.py patch
	git push --follow-tags
```

---

## Phase 5: Documentation & Polish (Backlog)

### 5.1 Normalize Trailing Newlines

**Goal:** Ensure consistent file endings across all markdown and JSON files.

**Action Items:**
1. Run `find plugins -name "*.md" -exec sed -i '' -e '$a\' {} \;` to add trailing newlines to markdown
2. Run `find plugins -name "*.json" -exec sed -i '' -e '$a\' {} \;` to add trailing newlines to JSON
3. Add `.editorconfig` at marketplace root:
   ```ini
   root = true
   [*]
   insert_final_newline = true
   trim_trailing_whitespace = true
   ```

**Affected Files:** All `.md` and `.json` files in `plugins/`

**Acceptance:** `git diff --check` returns no whitespace errors

---

### 5.2 Add Supplementary Keywords to plugin.json

**Goal:** Improve plugin discoverability with comprehensive keywords.

**Action Items:**
1. **zircote/plugin.json** - Add: `["claude-code", "automation", "workflow", "ai-agents", "productivity"]`
2. **gh/plugin.json** - Add: `["version-control", "pull-requests", "branches", "gh-cli"]`
3. **nsip/plugin.json** - Add: `["agriculture", "livestock", "genetics", "farming", "ebv"]`
4. **datadog/plugin.json** - Add: `["logging", "traces", "sre", "devops", "infrastructure"]`
5. **document-skills/plugin.json** - Add: `["parsing", "conversion", "microsoft-office", "ai-analysis"]`

**Acceptance:** Each plugin.json has 8-12 relevant keywords

---

### 5.3 Document Custom Fields (references, scripts)

**Goal:** Document non-standard plugin.json fields for contributors.

**Action Items:**
1. Update `CONTRIBUTING.md` section "plugin.json" to include:
   ```markdown
   **Extended fields (optional):**
   - `references`: Glob patterns for reference documentation (e.g., `["./references/*.md"]`)
   - `scripts`: Glob patterns for utility scripts (e.g., `["./scripts/*.py"]`)
   - `hooks`: Glob patterns for event hooks (e.g., `["./hooks/*.sh"]`)
   - `mcp`: MCP server configuration object with `command` and `args`
   ```
2. Add examples from nsip plugin (most comprehensive)
3. Create `docs/PLUGIN_SCHEMA.md` with full JSON schema for plugin.json

**Affected Files:** `CONTRIBUTING.md`, new `docs/PLUGIN_SCHEMA.md`

**Acceptance:** Contributors can understand all valid plugin.json fields

---

### 5.4 Add Verification Steps to Installation Docs

**Goal:** Help users verify successful plugin installation.

**Action Items:**
1. Update marketplace `README.md` installation section:
   ```markdown
   ## Verifying Installation

   After installing a plugin, verify it's active:

   ```bash
   # List installed plugins
   claude /plugin list

   # Verify specific plugin
   claude /plugin info <plugin-name>

   # Test a command (example for gh plugin)
   claude "/git:ff --help"
   ```
   ```

2. Add verification section to each plugin README:
   - **gh**: Test with `/git:ff` (should show help or error about not in git repo)
   - **nsip**: Test with `/nsip:breeds` (should list available breeds)
   - **datadog**: Verify agents appear in `/agents list`
   - **document-skills**: Test by asking to "analyze a PDF"
   - **zircote**: Verify with `/agents list | grep python-pro`

**Affected Files:** `README.md`, `plugins/*/README.md`

**Acceptance:** Each plugin has a "Verify Installation" section with testable commands

---

### 5.5 Create Architecture Diagrams

**Goal:** Visual documentation of marketplace and plugin architecture.

**Action Items:**
1. Create `docs/architecture/` directory
2. Create `docs/architecture/marketplace-overview.md` with Mermaid diagram:
   ```mermaid
   graph TB
       subgraph Marketplace
           MJ[marketplace.json]
           subgraph Plugins
               Z[zircote] --> ZA[116 Agents]
               Z --> ZS[54 Skills]
               GH[gh] --> GHC[9 Commands]
               GH --> GHA[1 Agent]
               NSIP[nsip] --> NC[10 Commands]
               NSIP --> NH[14 Hooks]
               NSIP --> NM[MCP Server]
           end
       end
   ```
3. Create `docs/architecture/plugin-lifecycle.md` showing:
   - Plugin discovery → Registration → Installation → Activation
4. Create `docs/architecture/hook-flow.md` showing event flow

**Deliverables:**
- `docs/architecture/marketplace-overview.md`
- `docs/architecture/plugin-lifecycle.md`
- `docs/architecture/hook-flow.md`

**Acceptance:** Diagrams render correctly in GitHub markdown preview

---

### 5.6 Add Video/GIF Demonstrations

**Goal:** Create visual demos for key features.

**Action Items:**
1. Create `docs/demos/` directory
2. Record terminal GIFs using `asciinema` or `terminalizer`:
   - `git-workflow-demo.gif` - Shows `/git:cp` → `/git:pr` workflow
   - `nsip-lookup-demo.gif` - Shows `/nsip:lookup` → `/nsip:profile`
   - `copilot-onboard-demo.gif` - Shows `/gh:copilot-onboard` output
3. Add GIFs to respective plugin READMEs
4. Create `docs/demos/README.md` index of all demos

**Tools Required:** `asciinema`, `agg` (for GIF conversion), or `terminalizer`

**Deliverables:**
- 3+ terminal recording GIFs
- Updated plugin READMEs with embedded GIFs

**Acceptance:** GIFs load and play correctly on GitHub

---

### 5.7 Add Quick Start to document-skills

**Goal:** Improve document-skills onboarding experience.

**Action Items:**
1. Update `plugins/document-skills/README.md` with Quick Start section:
   ```markdown
   ## Quick Start

   ### PDF Analysis
   ```bash
   claude "Analyze the contents of ./report.pdf"
   claude "Extract all tables from ./data.pdf"
   claude "What are the form fields in ./application.pdf"
   ```

   ### Excel Processing
   ```bash
   claude "Read the data from ./sales.xlsx"
   claude "What formulas are in ./budget.xlsx"
   claude "List all sheets in ./workbook.xlsx"
   ```

   ### Word Documents
   ```bash
   claude "Extract text from ./document.docx"
   claude "What comments are in ./review.docx"
   ```

   ### PowerPoint
   ```bash
   claude "Summarize the slides in ./presentation.pptx"
   claude "Extract speaker notes from ./talk.pptx"
   ```
   ```

2. Add "Common Use Cases" section with real-world examples
3. Add "Troubleshooting" section for common errors

**Affected Files:** `plugins/document-skills/README.md`

**Acceptance:** New users can start using skills within 2 minutes of reading README

---

### 5.8 Expand datadog Plugin Content

**Goal:** Make datadog plugin more comprehensive and actionable.

**Action Items:**
1. **Add example queries to agents:**
   - Update `datadog-pro.md` with 5 common metric queries
   - Update `datadog-api-expert.md` with monitor/dashboard examples

2. **Create reference materials:**
   - `plugins/datadog/references/common-queries.md` - Top 20 DataDog queries
   - `plugins/datadog/references/dashboard-templates.md` - JSON templates for common dashboards
   - `plugins/datadog/references/monitor-examples.md` - Alert configurations

3. **Add Quick Start to README.md:**
   ```markdown
   ## Quick Start

   ### Create a Monitor
   ```
   Using the datadog-api-expert agent, create a monitor for:
   - High CPU usage (>80% for 5 minutes)
   - Alert via Slack to #alerts channel
   ```

   ### Query Metrics
   ```
   Using the datadog-pro agent, show me:
   - Average response time for my-service over last hour
   - Error rate trend for the past 24 hours
   ```
   ```

4. **Update plugin.json** to reference new files:
   ```json
   "references": ["./references/*.md"]
   ```

**Affected Files:**
- `plugins/datadog/README.md`
- `plugins/datadog/agents/datadog-pro.md`
- `plugins/datadog/agents/datadog-api-expert.md`
- New: `plugins/datadog/references/*.md` (3 files)

**Acceptance:** Users can create monitors and query metrics following README examples

---

## Phase 5 Prioritization

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| 5.7 Quick Start (document-skills) | Low | High | **P1** |
| 5.8 Expand datadog | Medium | High | **P1** |
| 5.4 Verification Steps | Low | Medium | **P2** |
| 5.3 Document Custom Fields | Low | Medium | **P2** |
| 5.2 Supplementary Keywords | Low | Low | **P3** |
| 5.1 Trailing Newlines | Low | Low | **P3** |
| 5.5 Architecture Diagrams | Medium | Medium | **P3** |
| 5.6 Video/GIF Demos | High | Medium | **P4** |

**Recommended Order:** 5.7 → 5.8 → 5.4 → 5.3 → 5.2 → 5.1 → 5.5 → 5.6

---

## Implementation Order

### Week 1: Critical + High Priority

| Day | Tasks |
|-----|-------|
| 1 | Fix gh plugin.json description and keywords |
| 1 | Create LICENSE file |
| 2 | Fix/create zircote commands directory |
| 2 | Add author emails to all plugins |
| 3 | Add trigger phrases to top 5 skills |
| 3 | Add anti-hallucination rules to shepherd.md |
| 4 | Rewrite gh README.md |
| 4 | Sync all version mismatches |
| 5 | Create CONTRIBUTING.md |
| 5 | Standardize error handling in commands |

### Week 2: Medium Priority

| Day | Tasks |
|-----|-------|
| 1-2 | Add Opus 4.5 sections to all agents |
| 2 | Add descriptions to marketplace.json |
| 3 | Create CHANGELOG.md for all plugins |
| 3 | Normalize gh indentation |
| 4 | Refactor migrate.md |
| 5 | Add output format specs to skills |

### Week 3: Versioning Infrastructure

| Day | Tasks |
|-----|-------|
| 1 | Create .bumpversion.toml for each plugin |
| 2 | Create smart-bump.py script |
| 3 | Add Makefile targets |
| 4 | Test version bumping workflow |
| 5 | Document versioning process |

---

## Acceptance Criteria

Before considering remediation complete:

- [ ] All plugin.json files pass JSON validation
- [ ] All descriptions accurately reflect plugin contents
- [ ] All authors have email fields
- [ ] All skills have trigger phrases section
- [ ] All agents have anti-hallucination rules (where applicable)
- [ ] All commands have error handling section
- [ ] LICENSE exists at marketplace root
- [ ] CONTRIBUTING.md exists at marketplace root
- [ ] CHANGELOG.md exists for marketplace and each plugin
- [ ] Version bumping works for each plugin independently
- [ ] gh README.md documents all commands/agents/skills
- [ ] No version mismatches between plugin.json and README.md

---

## Questions for User Before Proceeding

1. **Commands for zircote**: Should I create the commands directory with new files, or locate existing files to move?

2. **Version source of truth**: Should plugin.json or README.md be the canonical version source?

3. **Copilot plugin**: The README mentions it but it's deleted - should we restore or remove references?

4. **Git tags**: Should plugin versions create per-plugin tags (e.g., `zircote-v1.0.2`)?

5. **Marketplace version**: Should marketplace.json version bump when ANY plugin is bumped, or only on explicit release?

---

*Report Synthesized from 4 Parallel Agent Reviews*
