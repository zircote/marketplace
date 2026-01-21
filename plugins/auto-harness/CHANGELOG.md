# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-01-21

### Added

- **Docs**: Add CHANGELOG.md with complete release history

### Fixed

- **Tests**: Reorder meta tests to prevent self-validation conflict where `meta_validate_pass` consumed the next test's validation slot

## [1.0.1] - 2026-01-21

### Added

- **GitHub**: Social preview image, badges, and infographic for README

### Fixed

- **Commands**: `/run-tests` now executes all tests automatically without requiring manual `next` commands
- **SVG**: Use GitHub-compatible fonts and icons in infographic
- **SVG**: Merge duplicate `<defs>` blocks causing rendering issues

### Changed

- **Config**: Add `.gitignore` with runtime state exclusions (`.claude/test-state.json`)

## [1.0.0] - 2026-01-21

### Added

- **Core**: Hook-driven test framework generator for Claude Code projects
- **Commands**: `/harness:init` to scaffold test infrastructure into target projects
- **Commands**: `/run-tests` to execute functional test suites
- **Runner**: Bash-based test runner with init, next, validate, skip, status, report commands
- **Hooks**: `UserPromptSubmit` hook for automated test execution
- **Templates**: YAML and JSON test definition formats
- **Templates**: Customizable runner and hook templates
- **Features**: Variable capture with `save_as` and `${var}` substitution
- **Features**: Test filtering by category and tags
- **Features**: Markdown and JSON report generation
- **Features**: Test dependencies with `depends_on`

[Unreleased]: https://github.com/zircote/auto-harness/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/zircote/auto-harness/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/zircote/auto-harness/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/zircote/auto-harness/releases/tag/v1.0.0
