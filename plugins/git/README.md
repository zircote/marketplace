# git Plugin

Git workflow commands and GitHub ecosystem integration skills for streamlined version control operations.

## Installation

```bash
claude /plugin install ./plugins/git
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

# Clean up merged branches
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
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for test additions
- `chore:` for maintenance tasks

## GitHub CLI Integration

PR commands require the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install gh
brew install gh  # macOS
sudo apt install gh  # Ubuntu

# Authenticate
gh auth login
```
