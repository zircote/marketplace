# git Plugin

Git workflow commands and GitHub ecosystem integration skills for streamlined version control operations.

## Installation

```bash
claude /plugin marketplace add zircote/marketplace
claude /plugin install git
```

## Contents

### Commands

Git workflow automation in `commands/`:

| Command | Description |
|---------|-------------|
| `/git:cm` | Stage all files and create a commit with conventional commit format |
| `/git:cp` | Stage, commit, and push all changes in one operation |
| `/git:pr [to-branch] [from-branch]` | Create a pull request using `gh` CLI |
| `/git:fr [remote] [branch]` | Fetch from remote and rebase current branch |
| `/git:sync [remote] [branch]` | Full sync: fetch, rebase, and push |
| `/git:ff [remote] [branch]` | Fast-forward merge only (no rebase) |
| `/git:prune [--force]` | Clean up stale local branches (dry-run by default) |

### Skills

#### ADR (Architecture Decision Records)
Located in `adr/skills/`:
- Create and manage ADRs
- Link ADRs to code and commits
- Generate ADR indexes

#### GitHub Ecosystem
Located in `ecosystem/skills/`:
- GitHub Actions workflow generation
- Issue and PR template creation
- CODEOWNERS configuration
- Dependabot setup
- Copilot instructions generation

## Usage Examples

### Daily Workflow

```bash
# Stage and commit with conventional commit message
claude /git:cm

# Full commit and push
claude /git:cp

# Create PR to main
claude /git:pr main feature-branch
```

### Branch Management

```bash
# Sync with remote (fetch, rebase, push)
claude /git:sync origin main

# Clean up merged branches (dry-run first)
claude /git:prune

# Force clean (skip dry-run)
claude /git:prune --force
```

### Rebase Workflow

```bash
# Fetch and rebase onto main
claude /git:fr origin main

# Fast-forward only (no merge commits)
claude /git:ff origin main
```

## Commit Format

The `/git:cm` command generates commits following conventional commit format:

| Type | Description |
|------|-------------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation changes |
| `refactor:` | Code refactoring |
| `test:` | Test additions or modifications |
| `chore:` | Maintenance tasks |

All commits include proper attribution:
```
feat: Add user authentication

Implements OAuth2 login flow with token refresh.

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

## GitHub CLI Integration

PR commands require the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install gh
brew install gh        # macOS
sudo apt install gh    # Ubuntu/Debian
winget install gh      # Windows

# Authenticate
gh auth login
```

## Integration with Other Plugins

- **z plugin**: Use `code-reviewer` agent before `/git:pr`
- **cs plugin**: Commit specification documents with `/git:cm`

## Version

**Plugin:** 1.0.0
