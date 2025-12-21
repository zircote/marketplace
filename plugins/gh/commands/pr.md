---
description: Create a pull request
argument-hint: [to-branch] [from-branch]
---

## Variables

- **TO_BRANCH**: First argument, defaults to `main`
- **FROM_BRANCH**: Second argument, defaults to current branch

## Pre-flight Checks

1. **Verify `gh` CLI is available**:
   ```bash
   which gh
   ```

   If not found, display:
   > **GitHub CLI Required**
   >
   > The `gh` command is not installed. Install it first:
   > - macOS: `brew install gh`
   > - Linux: `sudo apt install gh` or see https://github.com/cli/cli#installation
   > - Windows: `winget install GitHub.cli`
   >
   > Then authenticate: `gh auth login`

2. **Verify authentication**:
   ```bash
   gh auth status
   ```

   If not authenticated:
   > **GitHub CLI Not Authenticated**
   >
   > Run `gh auth login` to authenticate with GitHub.

3. **Check for uncommitted changes**:
   ```bash
   git status --porcelain
   ```

   If uncommitted changes exist:
   > "You have uncommitted changes. Commit or stash them before creating a PR.
   > Use `/git:cp` to commit and push all changes first."

4. **Check if branch is pushed**:
   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null
   ```

   If no upstream:
   > "Current branch is not pushed to remote. Push it first:
   > ```bash
   > git push -u origin $(git branch --show-current)
   > ```"

## Workflow

1. **Get current branch** (if FROM_BRANCH not specified):
   ```bash
   git branch --show-current
   ```

2. **Create pull request**:
   ```bash
   gh pr create --base ${TO_BRANCH} --head ${FROM_BRANCH}
   ```

   The `gh` CLI will prompt for:
   - Title
   - Body
   - Whether to submit, save as draft, or continue in browser

3. **Report success**:
   Display the PR URL returned by `gh pr create`.

## Error Handling

| Error | Response |
|-------|----------|
| `gh: command not found` | Install GitHub CLI: `brew install gh` (macOS) |
| `gh auth status` fails | Run `gh auth login` to authenticate |
| No commits between branches | Inform user there are no changes to create a PR for |
| Branch doesn't exist on remote | Push branch first: `git push -u origin ${FROM_BRANCH}` |
| PR already exists | Display existing PR URL with `gh pr view --web` |

## Notes

- Use `gh pr create --draft` if you want to create a draft PR
- Use `gh pr create --web` to complete PR creation in browser
- The `--fill` flag auto-fills title/body from commits if you want less interaction