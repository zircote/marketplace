---
name: ADR Integration
description: This skill should be used when the user asks about "ADR integration", "ADR CI/CD", "ADR tooling", "ADR automation", "export ADRs", "ADR documentation site", or needs guidance on integrating ADRs with CI/CD, documentation sites, and other tools.
version: 1.0.0
---

# ADR Integration

This skill provides guidance on integrating ADRs with CI/CD pipelines, documentation sites, and other development tools for automated workflows and better discoverability.

## CI/CD Integration

### GitHub Actions

```yaml
name: ADR Checks

on:
  pull_request:
    paths:
      - 'docs/adr/**'

jobs:
  adr-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check ADR format
        run: |
          # Verify ADR numbering
          # Check required sections
          # Validate links

      - name: Update ADR index
        run: |
          # Regenerate README.md
          # Check for changes
```

### GitLab CI

```yaml
adr-validation:
  stage: lint
  rules:
    - changes:
        - docs/adr/**
  script:
    - ./scripts/validate-adrs.sh
    - ./scripts/update-adr-index.sh
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: adr-lint
        name: Lint ADRs
        entry: ./scripts/lint-adr.sh
        language: script
        files: ^docs/adr/.*\.md$
```

## Documentation Site Integration

### MkDocs

```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - Architecture:
    - Overview: architecture/overview.md
    - Decision Records: architecture/adr/README.md

plugins:
  - search
  - macros:
      module_name: adr_macros
```

### Docusaurus

```js
// docusaurus.config.js
module.exports = {
  docs: {
    sidebar: {
      Architecture: [
        'architecture/overview',
        {
          type: 'category',
          label: 'Decision Records',
          items: ['architecture/adr/README'],
        },
      ],
    },
  },
};
```

### Sphinx

```rst
.. toctree::
   :maxdepth: 2
   :caption: Architecture

   architecture/overview
   architecture/adr/index
```

## Export Formats

### HTML Export

Generate standalone HTML:
- Apply CSS styling
- Include navigation
- Add status badges
- Generate table of contents

### JSON Export

Export for tooling integration:
```json
{
  "adrs": [
    {
      "id": "0001",
      "title": "Use PostgreSQL",
      "status": "accepted",
      "date": "2025-01-15",
      "file": "docs/adr/0001-use-postgresql.md",
      "supersedes": [],
      "superseded_by": null,
      "related": ["0003", "0007"]
    }
  ],
  "stats": {
    "total": 25,
    "accepted": 20,
    "proposed": 3,
    "deprecated": 1,
    "superseded": 1
  }
}
```

### PDF Export

Generate PDFs for:
- Stakeholder presentations
- Audit documentation
- Offline reading
- Compliance records

## Tool Integrations

### Jira/Issue Trackers

Link ADRs to tickets:
- Create "ADR" issue type
- Link implementation tickets to ADRs
- Track ADR lifecycle in workflow

### Confluence/Wiki

Sync ADRs to wiki:
- Auto-publish accepted ADRs
- Include cross-links
- Maintain version history

### Slack/Teams

ADR notifications:
- New ADR proposed
- ADR accepted/rejected
- Compliance violations

### Architecture Tools

Export to architecture tools:
- C4 model diagrams
- Enterprise architecture tools
- Design documentation

## Git Integration

### Commit Messages

Reference ADRs in commits:
```
feat: implement event-driven order processing

Implements ADR-0012 (Event-Driven Architecture)

- Add order event publisher
- Create payment event handler
- Remove synchronous calls
```

### Branch Naming

Include ADR reference:
```
feature/adr-0012-event-driven-orders
fix/adr-0015-auth-compliance
```

### Pull Request Templates

```markdown
## Related ADRs

- [ ] This PR implements ADR-XXXX
- [ ] This PR complies with accepted ADRs
- [ ] This PR proposes new ADR (link below)

### ADR Compliance Check

- [ ] Architecture patterns followed
- [ ] Technology choices match ADRs
- [ ] No ADR violations introduced
```

## Automation Scripts

### Index Generation

Auto-generate README.md index:
```bash
#!/bin/bash
# Generate ADR index from files

echo "# Architecture Decision Records"
echo ""
echo "| ID | Title | Status | Date |"
echo "|----|-------|--------|------|"

for file in docs/adr/[0-9]*.md; do
  # Extract metadata
  # Format table row
  echo "| $id | [$title]($file) | $status | $date |"
done
```

### Link Validation

Check ADR cross-references:
```bash
#!/bin/bash
# Validate ADR links

for file in docs/adr/*.md; do
  # Find ADR references (ADR-XXXX)
  # Verify linked ADRs exist
  # Report broken links
done
```

### Status Sync

Ensure bidirectional links:
```bash
#!/bin/bash
# Sync supersedes/superseded-by

for file in docs/adr/*.md; do
  # If A supersedes B
  # Verify B has superseded-by: A
done
```

## Monitoring and Metrics

### ADR Health Dashboard

Track metrics:
- Total ADRs by status
- ADRs created per month
- Average time to accept
- Supersession rate
- Compliance violations

### Alerts

Set up notifications for:
- ADRs proposed > 30 days
- Deprecated ADRs without successors
- Compliance violations
- Missing links/metadata

## Configuration

Configure integrations in `.claude/adr.local.md`:

```yaml
git:
  enabled: true
  auto_commit: false
  commit_template: "docs(adr): {action} ADR-{id} {title}"

export:
  default_format: html
  html_template: default
  include_toc: true
  output_dir: null

integration:
  docs_site: mkdocs
  issue_tracker: jira
  notifications: slack
```

## Additional Resources

### Reference Files

- **`references/ci-templates.md`** - CI/CD pipeline templates
- **`references/export-templates.md`** - Export format templates

### Related Skills

- **adr-compliance** - Compliance checking integration
- **adr-fundamentals** - Basic ADR workflow
