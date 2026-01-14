# ADR Export Templates

Templates and configurations for exporting ADRs to various formats.

## HTML Export

### Single ADR Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - ADR</title>
    <style>
        :root {
            --color-accepted: #28a745;
            --color-proposed: #ffc107;
            --color-deprecated: #6c757d;
            --color-superseded: #dc3545;
            --color-rejected: #dc3545;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            color: white;
        }

        .badge-accepted { background-color: var(--color-accepted); }
        .badge-proposed { background-color: var(--color-proposed); color: #333; }
        .badge-deprecated { background-color: var(--color-deprecated); }
        .badge-superseded { background-color: var(--color-superseded); }
        .badge-rejected { background-color: var(--color-rejected); }

        .metadata {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 2rem;
        }

        h1 { border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
        h2 { margin-top: 2rem; color: #495057; }

        ul { padding-left: 1.5rem; }
        li { margin-bottom: 0.5rem; }

        code {
            background: #f4f4f4;
            padding: 0.125rem 0.375rem;
            border-radius: 3px;
            font-size: 0.9em;
        }

        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }

        .nav-links {
            display: flex;
            justify-content: space-between;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }

        @media print {
            .nav-links { display: none; }
            body { max-width: none; }
        }
    </style>
</head>
<body>
    <article>
        <div class="metadata">
            <span class="badge badge-{{status_class}}">{{status}}</span>
            <span style="margin-left: 1rem; color: #666;">ADR-{{id}} | {{date}}</span>
        </div>

        <h1>{{title}}</h1>

        {{content}}
    </article>

    <nav class="nav-links">
        {{#if prev_adr}}
        <a href="./{{prev_adr}}.html">&larr; Previous: ADR-{{prev_id}}</a>
        {{else}}
        <span></span>
        {{/if}}

        <a href="./index.html">Index</a>

        {{#if next_adr}}
        <a href="./{{next_adr}}.html">Next: ADR-{{next_id}} &rarr;</a>
        {{else}}
        <span></span>
        {{/if}}
    </nav>
</body>
</html>
```

### Combined Index Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture Decision Records</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }

        .search-box {
            width: 100%;
            padding: 0.75rem;
            font-size: 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 1.5rem;
        }

        .filter-buttons {
            margin-bottom: 1rem;
        }

        .filter-btn {
            padding: 0.5rem 1rem;
            margin-right: 0.5rem;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
        }

        .filter-btn.active {
            background: #007bff;
            color: white;
            border-color: #007bff;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background: #f8f9fa;
            font-weight: 600;
        }

        tr:hover { background: #f8f9fa; }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-accepted { background: #d4edda; color: #155724; }
        .badge-proposed { background: #fff3cd; color: #856404; }
        .badge-deprecated { background: #e2e3e5; color: #383d41; }
        .badge-superseded { background: #f8d7da; color: #721c24; }

        .stats {
            display: flex;
            gap: 2rem;
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 4px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
        }

        .stat-label {
            font-size: 0.875rem;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Architecture Decision Records</h1>

    <div class="stats">
        <div class="stat-item">
            <div class="stat-number">{{total}}</div>
            <div class="stat-label">Total</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{{accepted}}</div>
            <div class="stat-label">Accepted</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{{proposed}}</div>
            <div class="stat-label">Proposed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{{deprecated}}</div>
            <div class="stat-label">Deprecated</div>
        </div>
    </div>

    <input type="text" class="search-box" placeholder="Search ADRs..." id="search">

    <div class="filter-buttons">
        <button class="filter-btn active" data-status="all">All</button>
        <button class="filter-btn" data-status="accepted">Accepted</button>
        <button class="filter-btn" data-status="proposed">Proposed</button>
        <button class="filter-btn" data-status="deprecated">Deprecated</button>
        <button class="filter-btn" data-status="superseded">Superseded</button>
    </div>

    <table id="adr-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Status</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            {{#each adrs}}
            <tr data-status="{{status}}">
                <td>{{id}}</td>
                <td><a href="./{{file}}">{{title}}</a></td>
                <td><span class="badge badge-{{status}}">{{status}}</span></td>
                <td>{{date}}</td>
            </tr>
            {{/each}}
        </tbody>
    </table>

    <script>
        // Search functionality
        document.getElementById('search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('#adr-table tbody tr').forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });

        // Filter functionality
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const status = this.dataset.status;
                document.querySelectorAll('#adr-table tbody tr').forEach(row => {
                    if (status === 'all' || row.dataset.status === status) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>
```

## JSON Schema

### ADR Export Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ADR Export",
  "description": "Schema for exported Architecture Decision Records",
  "type": "object",
  "required": ["metadata", "adrs"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["project", "exported", "total"],
      "properties": {
        "project": {
          "type": "string",
          "description": "Project name"
        },
        "exported": {
          "type": "string",
          "format": "date-time",
          "description": "Export timestamp in ISO 8601 format"
        },
        "total": {
          "type": "integer",
          "minimum": 0,
          "description": "Total number of ADRs exported"
        },
        "version": {
          "type": "string",
          "description": "Export schema version"
        }
      }
    },
    "adrs": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/adr"
      }
    },
    "statistics": {
      "$ref": "#/definitions/statistics"
    }
  },
  "definitions": {
    "adr": {
      "type": "object",
      "required": ["id", "title", "status", "file"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[0-9]+$",
          "description": "ADR identifier (numeric)"
        },
        "title": {
          "type": "string",
          "description": "ADR title"
        },
        "slug": {
          "type": "string",
          "description": "URL-friendly slug"
        },
        "status": {
          "type": "string",
          "enum": ["proposed", "accepted", "deprecated", "superseded", "rejected"],
          "description": "Current status"
        },
        "date": {
          "type": "string",
          "format": "date",
          "description": "Creation or decision date"
        },
        "format": {
          "type": "string",
          "enum": ["madr", "nygard", "y-statement", "alexandrian", "business-case", "tyree-akerman"],
          "description": "ADR template format used"
        },
        "file": {
          "type": "string",
          "description": "Relative file path"
        },
        "sections": {
          "type": "object",
          "description": "Parsed ADR sections",
          "properties": {
            "context": { "type": "string" },
            "decision": { "type": "string" },
            "consequences": {
              "type": "array",
              "items": { "type": "string" }
            },
            "options": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        },
        "links": {
          "type": "object",
          "description": "ADR relationships",
          "properties": {
            "supersedes": {
              "type": "array",
              "items": { "type": "string" }
            },
            "superseded_by": {
              "type": ["string", "null"]
            },
            "relates_to": {
              "type": "array",
              "items": { "type": "string" }
            },
            "amends": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "statistics": {
      "type": "object",
      "properties": {
        "by_status": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "by_month": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        },
        "by_format": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        }
      }
    }
  }
}
```

### Example JSON Export

```json
{
  "metadata": {
    "project": "My Application",
    "exported": "2024-01-15T10:30:00Z",
    "total": 25,
    "version": "1.0.0"
  },
  "adrs": [
    {
      "id": "0001",
      "title": "Use PostgreSQL for Primary Storage",
      "slug": "use-postgresql-for-primary-storage",
      "status": "accepted",
      "date": "2024-01-10",
      "format": "madr",
      "file": "docs/adr/0001-use-postgresql.md",
      "sections": {
        "context": "Our application needs a reliable, scalable database...",
        "decision": "We will use PostgreSQL as our primary database.",
        "consequences": [
          "Good: Mature ecosystem with excellent tooling",
          "Bad: Horizontal scaling requires additional tools"
        ],
        "options": ["PostgreSQL", "MySQL", "MongoDB"]
      },
      "links": {
        "supersedes": [],
        "superseded_by": null,
        "relates_to": ["0003", "0007"]
      },
      "tags": ["database", "infrastructure"]
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
      "2024-01": 5,
      "2023-12": 3,
      "2023-11": 4
    },
    "by_format": {
      "madr": 20,
      "nygard": 5
    }
  }
}
```

## PDF Export

### LaTeX Template

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{accepted}{RGB}{40, 167, 69}
\definecolor{proposed}{RGB}{255, 193, 7}
\definecolor{deprecated}{RGB}{108, 117, 125}
\definecolor{superseded}{RGB}{220, 53, 69}

\pagestyle{fancy}
\fancyhf{}
\rhead{Architecture Decision Records}
\lhead{{{project}}}
\rfoot{Page \thepage}

\title{Architecture Decision Records\\{{project}}}
\author{Generated by ADR Plugin}
\date{{{date}}}

\begin{document}

\maketitle
\tableofcontents
\newpage

{{#each adrs}}
\section{ADR-{{id}}: {{title}}}

\textbf{Status:} \textcolor{{{status_color}}}{{{status}}}\\
\textbf{Date:} {{date}}

\subsection{Context}
{{context}}

\subsection{Decision}
{{decision}}

\subsection{Consequences}
\begin{itemize}
{{#each consequences}}
\item {{this}}
{{/each}}
\end{itemize}

\newpage
{{/each}}

\end{document}
```

### Pandoc Command

```bash
# Convert ADRs to PDF using Pandoc
pandoc docs/adr/*.md \
  -o adrs.pdf \
  --toc \
  --toc-depth=2 \
  -V geometry:margin=1in \
  -V colorlinks=true \
  --pdf-engine=xelatex \
  --metadata title="Architecture Decision Records"
```

## Export Scripts

### export-html.sh

```bash
#!/bin/bash
# Export ADRs to HTML

OUTPUT_DIR="${1:-docs/adr/export}"
ADR_PATH="${ADR_PATH:-docs/adr}"

mkdir -p "$OUTPUT_DIR"

# Generate individual HTML files
for file in "$ADR_PATH"/[0-9]*.md; do
    [ -f "$file" ] || continue
    BASENAME=$(basename "$file" .md)

    # Convert markdown to HTML (requires pandoc)
    pandoc "$file" \
        -o "$OUTPUT_DIR/$BASENAME.html" \
        --template=templates/adr-single.html \
        --standalone
done

# Generate index
./scripts/generate-index-html.sh "$OUTPUT_DIR"

echo "HTML export complete: $OUTPUT_DIR"
```

### export-json.sh

```bash
#!/bin/bash
# Export ADRs to JSON

OUTPUT_FILE="${1:-adrs.json}"
ADR_PATH="${ADR_PATH:-docs/adr}"

echo '{' > "$OUTPUT_FILE"
echo '  "metadata": {' >> "$OUTPUT_FILE"
echo "    \"project\": \"$(basename $(pwd))\"," >> "$OUTPUT_FILE"
echo "    \"exported\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$OUTPUT_FILE"

# Count ADRs
TOTAL=$(ls "$ADR_PATH"/[0-9]*.md 2>/dev/null | wc -l | tr -d ' ')
echo "    \"total\": $TOTAL" >> "$OUTPUT_FILE"
echo '  },' >> "$OUTPUT_FILE"
echo '  "adrs": [' >> "$OUTPUT_FILE"

FIRST=true
for file in "$ADR_PATH"/[0-9]*.md; do
    [ -f "$file" ] || continue

    [ "$FIRST" = true ] && FIRST=false || echo ',' >> "$OUTPUT_FILE"

    ID=$(basename "$file" | grep -oE '^[0-9]+')
    TITLE=$(grep -m1 "^# " "$file" | sed 's/^# //')
    STATUS=$(grep -A1 "^## Status" "$file" | tail -1 | tr -d '\n\r')

    echo -n "    {\"id\": \"$ID\", \"title\": \"$TITLE\", \"status\": \"$STATUS\", \"file\": \"$file\"}" >> "$OUTPUT_FILE"
done

echo '' >> "$OUTPUT_FILE"
echo '  ]' >> "$OUTPUT_FILE"
echo '}' >> "$OUTPUT_FILE"

echo "JSON export complete: $OUTPUT_FILE"
```
