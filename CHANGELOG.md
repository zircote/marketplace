# Changelog

All notable changes to the Zircote Claude Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.10.0] - 2026-01-21

### Added
- **auto-harness**: Hook-driven test framework generator for Claude Code projects v1.0.2
  - `/harness:init` command to scaffold test infrastructure
  - `/run-tests` command for automated test execution
  - UserPromptSubmit hook for test interception
  - YAML/JSON test definitions with variable capture
  - Markdown and JSON report generation
- **sdlc**: Software development lifecycle quality tools and workflows (repo: zircote/sdlc-quality)
- **rlm-rs**: Rust-based RLM plugin for Claude Code (repo: zircote/rlm-rs-plugin)
- **github-social**: GitHub social preview and repository metadata generator v0.2.0
  - `/github-social:social-preview` command for generating social preview images
  - `/github-social:repo-metadata` command for optimized descriptions and topics
  - `/github-social:setup` interactive configuration wizard
- **aesth**: Design system validation and pattern capture plugin v0.1.0
  - `/aesth:validate` command for code validation against design tokens
  - `/aesth:capture` command for capturing design patterns to Subcog memory
  - `/aesth:extract` command for extracting patterns from existing code
  - `/aesth:status` and `/aesth:init` commands for design system state management
- **human-voice**: AI writing pattern detection plugin v0.1.0
  - Multi-tier pattern detection: characters, language, structural, and voice analysis
  - `/human-voice:review` command for comprehensive content analysis
  - `/human-voice:fix` command for automated character-level fixes
  - `voice-reviewer` agent for proactive content review after edits
  - Detection patterns for em dashes, smart quotes, AI buzzwords, hedging phrases
  - Reference documentation for all pattern tiers with examples
- **adr**: Complete Architectural Decision Record lifecycle management plugin
  - Multi-format support: MADR 4.0.0 (default), Structured MADR, Nygard, Y-Statement, Alexandrian, Business Case, Tyree-Akerman
  - **Structured MADR format**: New format with YAML frontmatter for machine-readable metadata, comprehensive option analysis with risk assessments, and required audit sections for compliance tracking
  - 7 commands: `adr-new`, `adr-list`, `adr-update`, `adr-supersede`, `adr-search`, `adr-setup`, `adr-export`
  - 3 agents: `adr-author` (proactive detection), `adr-compliance` (code auditing), `adr-researcher` (context gathering)
  - 11 skills covering fundamentals, decision drivers, quality, formats, compliance, and integration
  - Export to HTML, JSON, PDF with JSON schema definition
  - Git integration with auto-commit support
  - Configurable status workflow, numbering patterns, and multi-directory support
  - ADR linking: supersedes, relates-to, amends relationships
  - CI/CD pipeline templates for GitHub Actions, GitLab CI, Azure DevOps, Jenkins
- **documentation-review**: Add references and examples for changelog skill
  - Semantic-release configuration patterns reference
  - Conventional commits to changelog mapping reference
  - Sample changelog example following Keep a Changelog format
- **lsp-tools**: Add SQL LSP configuration

### Changed
- **gh**: Migrated to standalone repository (zircote/gh)
- **zircote**: Migrated to standalone repository (zircote/zircote)
- **nsip**: Migrated to standalone repository (zircote/nsip)
- **documentation-review**: Migrated to standalone repository (zircote/documentation-review)
- **adr**: Migrated to standalone repository (zircote/adr)
- **human-voice**: Migrated to standalone repository (zircote/human-voice)

### Fixed
- **agents**: Renamed plugin reference from 'zircote' to 'agents'
- **adr**: Remove broken cross-reference in structured-madr example

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

[Unreleased]: https://github.com/zircote/marketplace/compare/v1.10.0...HEAD
[1.10.0]: https://github.com/zircote/marketplace/compare/v1.7.0...v1.10.0
[1.7.0]: https://github.com/zircote/marketplace/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/zircote/marketplace/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/zircote/marketplace/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/zircote/marketplace/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/zircote/marketplace/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/zircote/marketplace/compare/v1.0.0...v1.2.0
[1.0.0]: https://github.com/zircote/marketplace/releases/tag/v1.0.0
