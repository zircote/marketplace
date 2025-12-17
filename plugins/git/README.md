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

Located in `adr/skills/`: Manage Architecture Decision Records using the git-adr CLI tool.

**Key Features:**
- ADRs as Machine Memory - decisions persist across Claude sessions
- Auto-loads ADR summaries at session start in any git repository
- Supports multiple formats: MADR, Nygard, Y-Statement, Alexandrian, Business Case, Planguage
- All git-adr CLI commands: init, new, edit, list, show, search, sync, supersede, link, attach, stats, export

**Trigger Phrases:**
- "architecture decisions", "ADR", "decision record"
- "what did we decide", "record this decision", "document this decision"

**Installation:**
```bash
# macOS (Homebrew) - Recommended
brew tap zircote/git-adr && brew install git-adr

# Any platform (pip)
pip install git-adr

# With AI features
pip install 'git-adr[ai]'
```

**Quick Commands:**
```bash
git adr init                          # Initialize ADR tracking
git adr new "Use PostgreSQL"          # Create new ADR
git adr list                          # List all ADRs
git adr show <id>                     # Display an ADR
git adr search "<query>"              # Search ADRs
git adr sync push                     # Push ADRs to remote
```

#### GitHub Ecosystem

Located in `ecosystem/skills/`: Generate comprehensive GitHub configuration for any project.

**Components Generated:**
- **GitHub Actions** - CI/CD workflows with multi-version testing, security scanning, coverage
- **Issue Templates** - Bug reports, feature requests, template chooser
- **PR Templates** - PR checklist with change types
- **CODEOWNERS** - Code ownership definitions
- **Dependabot** - Automated dependency updates
- **Copilot Instructions** - GitHub Copilot context

**Supported Languages:**
| Language | Detection | CI Tools |
|----------|-----------|----------|
| Python | pyproject.toml, setup.py | ruff, mypy, bandit, pytest |
| Go | go.mod | golangci-lint, go test |
| TypeScript | package.json + tsconfig.json | eslint, prettier, tsc, vitest |

**Usage:**
```bash
# Auto-detect language and generate all config
python scripts/generate_github_config.py --project-path .

# Generate specific components
python scripts/generate_github_config.py --components workflows,templates
```

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

### ADR Workflow

```bash
# Start using ADRs
git adr init

# Record a decision
git adr new "Use PostgreSQL for persistence"

# Find past decisions
git adr search "database"

# Share with team
git adr sync push
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
- **z plugin**: Use `technical-writer` for CHANGELOG updates before releases

## Version

**Plugin:** 1.0.0
