# Changelog

All notable changes to the Zircote Claude Marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CONTRIBUTING.md with comprehensive plugin development guidelines
- Descriptions for all local plugins in marketplace.json
- Anti-hallucination rules to shepherd.md agent
- Trigger phrases to priority skills (anthropic-prompt-engineer, sequential-thinking, mcp-builder, code-review, python-project-skel)
- Comprehensive error handling to pr.md command

### Changed
- Rewrote gh plugin README.md to document all 9 commands, agent, and skill
- Updated gh plugin.json with accurate description and keywords
- Standardized author email field across all plugin.json files

### Fixed
- Removed non-existent commands array from zircote plugin.json
- Fixed gh plugin.json description (was incorrectly claiming 115+ agents)
- Fixed gh plugin.json keywords (were copied from wrong plugin)

### Removed
- Removed references to deprecated copilot plugin (merged into gh)

## [1.5.0] - 2025-12-19

### Added
- gh plugin with GitHub ecosystem integration
- memory-capture external plugin reference
- git-adr external plugin reference
- LICENSE file at marketplace root

### Changed
- Renamed cs plugin to claude-spec

## [1.4.0] - 2025-12-18

### Added
- nsip plugin v1.3.1 with 14 intelligent hooks
- shepherd agent for expert sheep breeding advice
- 10 NSIP commands for animal lookup and analysis

## [1.3.0] - 2025-12-17

### Added
- document-skills plugin for PDF, DOCX, XLSX, PPTX processing
- datadog plugin with monitoring specialists

## [1.2.0] - 2025-12-15

### Added
- zircote plugin with 116 agents and 54 skills
- Agent organization by domain (10 categories)

## [1.0.0] - 2025-12-01

### Added
- Initial marketplace structure
- Plugin manifest format
- External plugin support
