---
name: adr-export
description: Export ADRs to HTML, JSON, or PDF format
argument-hint: "[--format=html|json|pdf] [--output=<path>]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Export ADRs

Export Architectural Decision Records to HTML, JSON, or PDF format for sharing, documentation sites, or archival.

## Process

1. **Parse export options**
2. **Read all ADRs**
3. **Parse and structure content**
4. **Generate output** in specified format
5. **Write to output location**

## Argument Parsing

Supported arguments:
- `--format=<format>`: Output format (html, json, pdf)
- `--output=<path>`: Output directory or file
- `--filter=<status>`: Only export ADRs with status
- `--single`: Export as single combined file
- `--ids=<ids>`: Export specific ADRs (comma-separated)

Default: HTML format to `{adr_path}/export/`

## HTML Export

### Single ADR Export

Convert each ADR to styled HTML:
- Apply CSS styling
- Add status badges
- Format code blocks
- Include navigation links

### Combined Export

Create single HTML document:
- Table of contents
- All ADRs in sequence
- Status filtering
- Search functionality (if JavaScript enabled)

### Styling

Apply project styling or defaults:
- Status badge colors
- Typography
- Responsive layout
- Print-friendly styles

Example HTML structure:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Architecture Decision Records</title>
  <style>/* ADR styles */</style>
</head>
<body>
  <header>
    <h1>Architecture Decision Records</h1>
    <nav><!-- TOC --></nav>
  </header>
  <main>
    <article id="adr-0001">
      <span class="badge badge-accepted">Accepted</span>
      <h2>ADR-0001: Use PostgreSQL</h2>
      <!-- Content -->
    </article>
  </main>
</body>
</html>
```

## JSON Export

Export structured data for tooling integration.

**Schema**: See `${CLAUDE_PLUGIN_ROOT}/schemas/adr-export.schema.json` for the full JSON schema.

```json
{
  "metadata": {
    "project": "Project Name",
    "exported": "{ISO-8601-timestamp}",
    "total": 25
  },
  "adrs": [
    {
      "id": "0001",
      "title": "Use PostgreSQL for Primary Storage",
      "slug": "use-postgresql-for-primary-storage",
      "status": "accepted",
      "date": "{date}",
      "format": "madr",
      "file": "docs/adr/0001-use-postgresql.md",
      "sections": {
        "context": "...",
        "decision": "...",
        "consequences": ["...", "..."]
      },
      "links": {
        "supersedes": [],
        "superseded_by": null,
        "relates_to": ["0003", "0007"]
      }
    }
  ],
  "statistics": {
    "by_status": {
      "accepted": 20,
      "proposed": 3,
      "deprecated": 1,
      "superseded": 1
    },
    "by_month": {
      "2025-01": 5,
      "2024-12": 3
    }
  }
}
```

## PDF Export

Generate PDF document:

### Using Markdown-to-PDF

```bash
# If pandoc available
pandoc docs/adr/*.md -o adrs.pdf --toc
```

### Via HTML

1. Generate HTML
2. Use browser print-to-PDF
3. Or use headless Chrome/Puppeteer

### PDF Styling

- Professional document layout
- Page numbers
- Table of contents
- Status indicators
- Header/footer with project name

## Output Options

### Directory Export

Export each ADR as separate file:
```
export/
├── index.html
├── 0001-use-postgresql.html
├── 0002-event-driven.html
└── assets/
    └── styles.css
```

### Single File Export

Combine all ADRs:
```
export/adrs.html
export/adrs.json
export/adrs.pdf
```

## Configuration

Read from `.claude/adr.local.md`:
```yaml
export:
  default_format: html
  html_template: default
  include_toc: true
  include_status_badges: true
  output_dir: null
```

## Output

Report export complete:
- Format: {format}
- ADRs exported: {count}
- Output location: {path}
- Total size: {size}

## Error Handling

- If output directory doesn't exist, create it
- If PDF tools unavailable, suggest alternatives
- If ADRs have parsing errors, report and continue
