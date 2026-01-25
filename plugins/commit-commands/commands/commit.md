---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash, Read, Write, Glob, Grep
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Before Starting: Check Related Memories

Search for relevant commit patterns and conventions:
```bash
rg -i "commit" ~/.claude/mnemonic/ --glob "*.memory.md" -l 2>/dev/null | head -5
```

If patterns exist, read and apply them to ensure consistency.

## Your task

Based on the above changes, create a single git commit.

You have the capability to call multiple tools in a single response. Stage and create the commit using a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.

## Post-Commit: Capture to Mnemonic (Optional)

If the commit represents a significant pattern, decision, or learning:
- Use `/mnemonic:capture patterns "Commit convention: {description}"` for recurring patterns
- Use `/mnemonic:capture decisions "Decision: {description}"` for architectural choices
- Follow `mnemonic-format` skill for MIF Level 3 structure
