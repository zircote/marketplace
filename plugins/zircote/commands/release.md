---
allowed-tools: Bash(*), Read, Write, Glob, Grep, AskUserQuestion
argument-hint: [patch|minor|major] [--dry-run] [--skip-commit] [--pr]
description: Prepare and execute a plugin release with version bump, validation, and optional PR creation
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
RELEASE(1)                      User Commands                      RELEASE(1)

NAME
    release - Marketplace plugin release with version bump and validation

SYNOPSIS
    /zircote:release [patch|minor|major] [--dry-run] [--skip-commit] [--pr]

DESCRIPTION
    Execute a comprehensive release workflow for marketplace plugins:
    pre-flight validation, change analysis, version bump, push/tag,
    and optional PR creation. Prompts for release type if not specified.

OPTIONS
    patch                     Patch release (bug fixes, 0.0.X)
    minor                     Minor release (new features, 0.X.0)
    major                     Major release (breaking changes, X.0.0)
    --dry-run                 Preview changes without executing
    --skip-commit             Skip auto-commit of uncommitted changes
    --pr                      Create PR instead of pushing directly
    --help, -h                Show this help message

EXAMPLES
    /zircote:release                  Interactive release type selection
    /zircote:release patch            Patch release
    /zircote:release minor --pr       Minor release with PR creation
    /zircote:release --dry-run        Preview release without changes

SEE ALSO
    /gh:pr              Create pull requests
    /gh:cp              Stage, commit, and push

                                                                  RELEASE(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# Marketplace Release Command

You are executing a comprehensive release workflow for the zircote marketplace plugins. This command handles:

1. Pre-flight validation and change detection
2. Staging and committing uncommitted changes
3. Running validation checks
4. Version bumping (patch/minor/major)
5. Creating git tags and pushing
6. Optionally creating a pull request

## Arguments

Parse `$ARGUMENTS` for:
- **Release type**: `patch` (default), `minor`, or `major`
- **`--dry-run`**: Preview changes without executing
- **`--skip-commit`**: Skip auto-commit of uncommitted changes
- **`--pr`**: Create a PR instead of pushing directly to current branch

If no release type is provided, use AskUserQuestion to prompt:

```
AskUserQuestion with options:
- question: "What type of release is this?"
- header: "Release Type"
- options:
  - label: "patch (Recommended)"
    description: "Bug fixes, documentation updates, minor improvements (0.0.X)"
  - label: "minor"
    description: "New features, significant improvements (0.X.0)"
  - label: "major"
    description: "Breaking changes, major refactors (X.0.0)"
```

---

# PHASE 1: PRE-FLIGHT CHECKS

## 1.1 Environment Verification

Verify we're in the correct directory and have required tools:

```bash
# Verify we're in marketplace root
if [ ! -f "Makefile" ] || [ ! -d "plugins" ]; then
  echo "ERROR: Must run from marketplace root directory"
  exit 1
fi

# Check for required tools
which python3 > /dev/null || { echo "ERROR: python3 required"; exit 1; }
which git > /dev/null || { echo "ERROR: git required"; exit 1; }
```

## 1.2 Git Status Assessment

```bash
echo "=== Current Branch ==="
git branch --show-current

echo ""
echo "=== Remote Status ==="
git fetch origin --dry-run 2>&1 || echo "Note: Could not fetch from origin"

echo ""
echo "=== Uncommitted Changes ==="
git status --porcelain

echo ""
echo "=== Recent Commits (not pushed) ==="
git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -5
```

## 1.3 Current Versions

Display current plugin versions before changes:

```bash
make version
```

---

# PHASE 2: CHANGE ANALYSIS

## 2.1 Detect Modified Plugins

Use the smart-bump script's detection logic:

```bash
echo "=== Plugins with Changes Since Last Release ==="
python3 scripts/smart-bump.py --dry-run patch 2>&1 | head -30
```

## 2.2 Summarize Changes

For each changed plugin, summarize what changed:

```bash
echo ""
echo "=== Change Summary ==="
for plugin in plugins/*/; do
  plugin_name=$(basename "$plugin")
  changes=$(git diff --stat HEAD~10..HEAD -- "$plugin" 2>/dev/null | tail -1)
  if [ -n "$changes" ]; then
    echo "  $plugin_name: $changes"
  fi
done
```

---

# PHASE 3: UNCOMMITTED CHANGES HANDLING

If `--skip-commit` is NOT specified and there are uncommitted changes:

## 3.1 Review Changes

```bash
git diff --stat
git diff --cached --stat
```

## 3.2 Auto-Commit Decision

Use AskUserQuestion:
- question: "There are uncommitted changes. How should we proceed?"
- header: "Changes"
- options:
  - label: "Commit all changes (Recommended)"
    description: "Stage and commit all changes with auto-generated message"
  - label: "Commit staged only"
    description: "Only commit currently staged changes"
  - label: "Skip commit"
    description: "Proceed without committing (changes will not be in release)"
  - label: "Abort"
    description: "Stop the release process to handle changes manually"

## 3.3 Commit Changes

If committing, follow these rules:

1. **Check for sensitive files**:
   - Never commit: `.env*`, `*.key`, `*credentials*`, `*secret*`

2. **Generate commit message**:
   - Use conventional commit format
   - For agent changes: `perf(agents): <summary>`
   - For skill changes: `feat(skills): <summary>` or `perf(skills): <summary>`
   - For command changes: `feat(commands): <summary>`
   - For infrastructure: `chore: <summary>`

3. **Execute commit**:
   ```bash
   git add -A
   git commit -m "<generated message>"
   ```

---

# PHASE 4: VALIDATION

## 4.1 Run All Validations

```bash
echo "=== Running Validation Suite ==="
make validate
```

If validation fails, stop and report issues.

## 4.2 Check for Breaking Changes

For `major` releases, look for:
- Removed files
- Renamed agents/skills/commands
- Changed frontmatter schemas

```bash
echo "=== Checking for Breaking Changes ==="
git diff --name-status $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD -- plugins/ | grep -E "^D|^R"
```

---

# PHASE 5: VERSION BUMP

## 5.1 Execute Version Bump

Based on release type:

```bash
# For --dry-run, show what would happen
python3 scripts/smart-bump.py --dry-run <release_type>

# For actual release
python3 scripts/smart-bump.py <release_type>
```

## 5.2 Verify Version Changes

```bash
echo "=== Updated Versions ==="
make version

echo ""
echo "=== Version Commits ==="
git log --oneline -5
```

---

# PHASE 6: PUSH & TAG

## 6.1 Standard Push (no --pr flag)

```bash
echo "=== Pushing Changes and Tags ==="
git push --follow-tags
```

## 6.2 PR Creation (with --pr flag)

If `--pr` is specified:

1. Create a release branch:
   ```bash
   RELEASE_BRANCH="release/$(date +%Y%m%d)-$(git rev-parse --short HEAD)"
   git checkout -b "$RELEASE_BRANCH"
   git push -u origin "$RELEASE_BRANCH"
   ```

2. Create the PR:
   ```bash
   gh pr create \
     --title "chore(release): bump plugin versions" \
     --body "$(cat <<'EOF'
   ## Release Summary

   ### Plugins Updated
   [List from version diff]

   ### Changes Included
   [Summary from git log]

   ### Validation
   - [x] All validations passed
   - [x] Version bumps applied
   - [x] Tags created

   ---

   **Release Type**: [patch|minor|major]
   **Release Date**: [current date]
   EOF
   )"
   ```

---

# PHASE 7: POST-RELEASE

## 7.1 Release Summary

Display final summary:

```bash
echo ""
echo "=========================================="
echo "          RELEASE COMPLETE"
echo "=========================================="
echo ""
echo "Plugins Released:"
make version
echo ""
echo "Tags Created:"
git tag --list --sort=-creatordate | head -5
echo ""
echo "Push Status:"
git log --oneline origin/$(git branch --show-current)..HEAD 2>/dev/null || echo "All changes pushed"
```

## 7.2 Next Steps Reminder

- Update CHANGELOG.md if significant changes
- Monitor CI/CD pipeline for any issues
- Verify plugin availability in marketplace

---

# ERROR HANDLING

## Validation Failure
If `make validate` fails:
1. Display error details
2. Ask user: Continue anyway / Abort / Fix and retry

## Push Failure
If git push fails:
1. Check for conflicts: `git fetch && git rebase origin/main`
2. Retry push
3. If still failing, create PR instead

## Version Bump Failure
If smart-bump.py fails:
1. Check for uncommitted changes in plugin.json files
2. Verify .bumpversion.toml exists in each plugin
3. Manual fallback: `cd plugins/<name> && bump-my-version bump <type>`

---

# DRY RUN MODE

When `--dry-run` is specified:

1. Run all detection and validation
2. Show what commits would be created
3. Show what version changes would occur
4. Show what tags would be created
5. **Do not modify any files or git state**

Output format:
```
=== DRY RUN MODE ===

Would commit:
  - [file list]
  - Message: "<commit message>"

Would bump versions:
  - zircote: 0.5.1 -> 0.5.2
  - gh: 0.3.0 -> 0.3.1

Would create tags:
  - zircote-v0.5.2
  - gh-v0.3.1

Would push to: origin/main
```

---

# EXECUTION PROTOCOL

1. **Start with Phase 1** - Verify environment and git state
2. **Prompt for release type** if not provided in arguments
3. **Handle uncommitted changes** unless `--skip-commit`
4. **Run validation** - Stop on failure unless user overrides
5. **Execute version bump** - Use dry-run preview first
6. **Push or create PR** based on `--pr` flag
7. **Display summary** with next steps

**Safety Rules:**
- Never force push
- Never skip validation without explicit user confirmation
- Always show what will happen before executing
- Preserve all git history
