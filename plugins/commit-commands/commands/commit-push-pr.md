---
allowed-tools: Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*), Bash, Read, Write, Glob, Grep
description: Commit, push, and open a PR
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Before Starting: Check Related Memories

Search for PR conventions and branch naming patterns:
```bash
rg -i "pull.request\|branch\|pr" ~/.claude/mnemonic/ --glob "*.memory.md" -l 2>/dev/null | head -5
```

If patterns exist, read and apply them to ensure consistency.

## Your task

Based on the above changes:

1. Create a new branch if on main
2. Create a single commit with an appropriate message
3. Push the branch to origin
4. Create a pull request using `gh pr create`
5. You have the capability to call multiple tools in a single response. You MUST do all of the above in a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.

## Post-PR: Capture to Mnemonic (Optional)

If the PR represents a significant pattern or decision:
- Use `/mnemonic:capture patterns "PR convention: {description}"` for recurring patterns
- Use `/mnemonic:capture decisions "Decision: {description}"` for architectural choices
- Follow `mnemonic-format` skill for MIF Level 3 structure
