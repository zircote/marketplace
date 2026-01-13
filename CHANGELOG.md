# Changelog

All notable changes to the Zircote Claude Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.7.0] - 2026-01-13

### Added
- **documentation-review**: Documentation quality management plugin
  - `doc-review`, `doc-create`, `doc-update`, `doc-cleanup`, `doc-setup` commands
  - `changelog`, `documentation-standards`, `api-documentation` skills
  - `doc-writer` and `doc-reviewer` agents
- **terraform-lsp**: Terraform Language Server integration
- **rust-lsp**: Rust Analyzer LSP integration with diagnostic hooks
- **markdown-lsp**: Markdown language server support
- **gh**: Changelog management skill for release documentation
- **lsp-tools**: Automated LSP server installation with per-server prompts
- **lsp-tools**: Comprehensive LSP setup and troubleshooting guide
- Python hooks for formatting, linting, and type checking

### Changed
- Renamed marketplace from `zircote-claude-marketplace` to `zircote`
- **lsp-tools**: Updated to v0.4.0 with expanded language support

### Fixed
- **gh**: Enforce mandatory thread resolution in review-comments
- **gh**: Correct GraphQL escaping in review-comments command
- **gh**: Fix thread resolution in review-comments command
- Corrected plugin install syntax to use `@zircote-claude-marketplace`
- Address code review feedback on XML structure

### Removed
- Deprecated LSP server registry and setup verification guide
- Language-specific LSP hooks and sections for PHP, Python, Ruby, Rust, and TypeScript/JavaScript (consolidated into lsp-tools)
- Deprecated LSP plugins from marketplace.json

## [1.6.0] - 2025-12-23

### Added
- **lsp-tools**: v0.1.0 - LSP-first code intelligence for Claude Code
  - `lsp-enable` skill enforcing "Three Iron Laws" of LSP-first development
  - `/lsp-setup` command for language-specific hook installation
  - Support for 12 languages: TypeScript/JavaScript, Python, Go, Rust, Java, Kotlin, C#, C/C++, Ruby, PHP, HTML/CSS, LaTeX
  - Reference documentation: Operations Guide, Enforcement Protocol, Decision Matrix, Setup Verification
- CONTRIBUTING.md with comprehensive plugin development guidelines
- Descriptions for all local plugins in marketplace.json
- **shepherd**: Anti-hallucination rules added to agent
- Trigger phrases to priority skills (anthropic-prompt-engineer, sequential-thinking, mcp-builder, code-review, python-project-skel)
- **gh**: Comprehensive error handling to pr.md command

### Changed
- **gh**: Rewrote README.md to document all 9 commands, agent, and skill
- **gh**: Updated plugin.json with accurate description and keywords
- Standardized author email field across all plugin.json files

### Fixed
- **gh**: Added missing `gm-ci-assist.md` command to plugin.json manifest
- **datadog**: Corrected README.md version (0.2.1) to match plugin.json
- **zircote**: Removed non-existent commands array from plugin.json
- **gh**: Fixed plugin.json description (was incorrectly claiming 115+ agents)
- **gh**: Fixed plugin.json keywords (were copied from wrong plugin)

### Removed
- **copilot**: Removed references to deprecated plugin (merged into gh)

## [1.5.0] - 2025-12-19

### Added
- **gh**: GitHub ecosystem integration
- **memory-capture**: External plugin reference
- **git-adr**: External plugin reference
- LICENSE file at marketplace root

### Changed
- **claude-spec**: Renamed from cs plugin

## [1.4.0] - 2025-12-18

### Added
- **nsip**: v1.3.1 with 14 intelligent hooks
- **shepherd**: Agent for expert sheep breeding advice
- 10 NSIP commands for animal lookup and analysis

## [1.3.0] - 2025-12-17

### Added
- **document-skills**: PDF, DOCX, XLSX, PPTX processing
- **datadog**: Monitoring specialists

## [1.2.0] - 2025-12-15

### Added
- **zircote**: 116 agents and 54 skills
- Agent organization by domain (10 categories)

## [1.0.0] - 2025-12-01

### Added
- Initial marketplace structure
- Plugin manifest format
- External plugin support

[Unreleased]: https://github.com/zircote/marketplace/compare/v1.7.0...HEAD
[1.7.0]: https://github.com/zircote/marketplace/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/zircote/marketplace/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/zircote/marketplace/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/zircote/marketplace/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/zircote/marketplace/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/zircote/marketplace/compare/v1.0.0...v1.2.0
[1.0.0]: https://github.com/zircote/marketplace/releases/tag/v1.0.0
