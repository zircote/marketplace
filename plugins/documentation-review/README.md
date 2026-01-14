# Documentation Review Plugin

Comprehensive documentation management for Claude Code: review, create, update, and maintain high-quality documentation.

## Features

- **Documentation Review** - Analyze existing docs for accuracy, completeness, and quality
- **Documentation Creation** - Generate new docs from codebase analysis (README, API docs, templates)
- **Documentation Updates** - Keep docs current with codebase changes
- **Documentation Cleanup** - Identify obsolete or outdated content
- **Changelog Management** - Maintain CHANGELOG.md with Keep a Changelog format
- **Quality Validation** - Automatic checks on markdown file edits
- **Multi-format Support** - Markdown with awareness of MkDocs, Sphinx, Docusaurus
- **API Documentation** - OpenAPI/Swagger and AsyncAPI integration

## Installation

Add to your Claude Code plugins or install via marketplace.

## Commands

| Command | Description |
|---------|-------------|
| `/doc-review [path]` | Review documentation for issues (file, directory, or project-wide) |
| `/doc-create [type]` | Generate new documentation (readme, api, template) |
| `/doc-update [path]` | Update outdated documentation with current information |
| `/doc-cleanup` | Identify and report obsolete documentation |
| `/doc-setup` | Interactive setup for project configuration |
| `/changelog [action]` | Manage CHANGELOG.md (add, review, generate, preview) |

## Agents

| Agent | Description |
|-------|-------------|
| `doc-reviewer` | Comprehensive documentation audit with proactive triggering |
| `doc-writer` | Content generation and documentation updates |

## Skills

- **documentation-standards** - Markdown best practices, structure guidelines, writing quality
- **api-documentation** - OpenAPI/Swagger/AsyncAPI patterns and endpoint documentation
- **changelog** - Keep a Changelog format, semantic-release, conventional commits mapping

## Configuration

Create `.claude/documentation-review.local.md` in your project root to customize behavior.

### Quick Setup

Run `/doc-setup` for interactive configuration, or manually create the file:

```markdown
---
# Documentation paths to scan (default: auto-detect)
doc_paths:
  - docs/
  - README.md
  - "*.md"

# Files/patterns to ignore
ignore:
  - "**/node_modules/**"
  - "**/vendor/**"
  - "**/.git/**"
  - "**/dist/**"
  - "**/build/**"
  - "CHANGELOG.md"

# Documentation standards
standards:
  require_description: true
  max_heading_depth: 4
  require_code_examples: false
  check_links: true
  check_spelling: false

# API documentation settings
api_docs:
  openapi_path: null           # Auto-detect
  asyncapi_path: null          # Auto-detect
  generate_from_code: false

# Static site generator integration
site_generator:
  type: auto                   # auto, mkdocs, sphinx, docusaurus
  config_path: null            # Auto-detect

# Output preferences
output:
  verbosity: normal            # minimal, normal, detailed
  format: markdown             # markdown, json
---

# Project Documentation Notes

Add project-specific documentation context here...
```

### Configuration Options

#### doc_paths
Directories and files to include in documentation operations. Supports glob patterns.

#### ignore
Patterns to exclude from documentation operations.

#### standards
Quality checks applied during review and validation:
- `require_description` - First paragraph should describe document purpose
- `max_heading_depth` - Maximum heading level (h1-h6) to use
- `require_code_examples` - Technical docs should include code examples
- `check_links` - Validate internal markdown links
- `check_spelling` - Enable spell checking (slower)

#### api_docs
API documentation settings:
- `openapi_path` - Path to OpenAPI/Swagger spec (null for auto-detect)
- `asyncapi_path` - Path to AsyncAPI spec (null for auto-detect)
- `generate_from_code` - Generate API docs from source code analysis

#### site_generator
Static site generator integration:
- `type` - Generator type: `auto`, `mkdocs`, `sphinx`, `docusaurus`
- `config_path` - Path to generator config file

#### output
Output preferences:
- `verbosity` - Detail level: `minimal`, `normal`, `detailed`
- `format` - Output format: `markdown`, `json`

## Usage Examples

### Review all project documentation
```bash
/doc-review
```

### Review specific file
```bash
/doc-review docs/api-reference.md
```

### Generate README from codebase
```bash
/doc-create readme
```

### Generate API documentation
```bash
/doc-create api
```

### Find outdated documentation
```bash
/doc-cleanup
```

## Hooks

Hooks are defined directly in component frontmatter (modern pattern):

**doc-reviewer agent:**
- PostToolUse hook on Read - tracks markdown files being reviewed

**doc-writer agent:**
- PostToolUse hook on Write/Edit - validates documentation changes

This component-scoped approach keeps validation logic with the components that use it.

## Version

**Plugin:** 0.1.0

## License

MIT
