# Changelog

All notable changes to the LSP Tools plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-23

### Added

#### Core Skill: `lsp-enable`
- **Three Iron Laws** for mandatory LSP usage:
  1. No modifying unfamiliar code without `goToDefinition` first
  2. No refactoring without `findReferences` impact analysis first
  3. No claiming code works without LSP diagnostics verification
- **Decision Tree** for choosing between LSP, Grep, Glob, and Read
- **Pre-Edit Protocol** with mandatory checklist
- **Post-Edit Verification** workflow
- **LSP Availability Check** with graceful fallback
- **Token Optimization Awareness** documentation

#### Command: `/lsp-setup`
- Auto-detect project languages by file extensions
- Copy appropriate hooks to `.claude/hooks.json`
- Merge with existing hooks if present
- Optionally append LSP sections to `CLAUDE.md`
- Support for explicit language arguments

#### Language Support (12 languages)
- TypeScript/JavaScript (vtsls)
- Python (pyright)
- Go (gopls)
- Rust (rust-analyzer)
- Java (jdtls)
- Kotlin (kotlin-language-server)
- C/C++ (clangd)
- C# (OmniSharp)
- PHP (phpactor)
- Ruby (ruby-lsp)
- HTML/CSS (vscode-langservers)
- LaTeX (texlab)

#### Reference Documentation
- `lsp-operations-guide.md` - Complete guide to all 9 LSP operations
- `lsp-enforcement-protocol.md` - Detailed enforcement patterns
- `lsp-decision-matrix.md` - Tool selection guidance
- `lsp-setup-verification.md` - Installation and troubleshooting
- `SETUP-GUIDE-ALL-LANGUAGES.md` - Quick setup reference

#### Per-Language Resources
- `{language}-lsp-section.md` - CLAUDE.md sections for each language
- `{language}-hooks.json` - Pre-configured hooks for each language

### Technical Details

- Plugin structure follows Claude Code plugin best practices
- Skills use progressive disclosure (lean SKILL.md, detailed references)
- Hooks use `${CLAUDE_PLUGIN_DIR}` for portability
- Strong enforcement patterns modeled after systematic-debugging skill

[0.1.0]: https://github.com/zircote/marketplace/releases/tag/lsp-tools-v0.1.0
