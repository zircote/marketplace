---
name: lsp-setup
description: Set up LSP hooks and CLAUDE.md sections for the current project
argument-hint: "[language] or auto-detect"
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
LSP_SETUP(1)                                         User Commands                                         LSP_SETUP(1)

NAME
    lsp-setup - Set up LSP hooks and CLAUDE.md sections for the current...

SYNOPSIS
    /lsp-tools:lsp-setup [language] or auto-detect

DESCRIPTION
    Set up LSP hooks and CLAUDE.md sections for the current project

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /lsp-tools:lsp-setup                    
    /lsp-tools:lsp-setup <language>         
    /lsp-tools:lsp-setup --help             

SEE ALSO
    /lsp-tools:* for related commands

                                                                      LSP_SETUP(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# LSP Setup Command

Set up Language Server Protocol hooks and configuration for the current project.

## What This Command Does

1. Detects languages used in the project (or accepts explicit language argument)
2. Copies appropriate LSP hooks to `.claude/hooks.json`
3. Merges with existing hooks if present
4. Optionally appends LSP guidance to `CLAUDE.md`

## Execution Steps

<step number="1" name="Determine Languages">

If a language argument is provided (e.g., `typescript`, `go`, `rust`), use that.

Otherwise, auto-detect by scanning for file extensions:
- `.ts`, `.tsx`, `.js`, `.jsx` → TypeScript/JavaScript
- `.py`, `.pyi` → Python
- `.go` → Go
- `.rs` → Rust
- `.java` → Java
- `.kt` → Kotlin
- `.cpp`, `.c`, `.h`, `.hpp` → C/C++
- `.cs` → C#
- `.php` → PHP
- `.rb` → Ruby
- `.html`, `.css`, `.scss` → HTML/CSS
- `.tex` → LaTeX

Use Glob to scan: `**/*.{ts,tsx,js,jsx,py,pyi,go,rs,java,kt,cpp,c,h,cs,php,rb,html,css,tex}`

</step>

<step number="2" name="Locate Hook Files">

The hook template files are in the skill's references directory:
`${CLAUDE_PLUGIN_DIR}/skills/lsp-enable/references/`

Available hook files:
- `typescript-hooks.json`
- `python-hooks.json`
- `go-hooks.json`
- `rust-hooks.json`
- `java-hooks.json`
- `kotlin-hooks.json`
- `cpp-hooks.json`
- `csharp-hooks.json`
- `php-hooks.json`
- `ruby-hooks.json`
- `html-css-hooks.json`
- `latex-hooks.json`

</step>

<step number="3" name="Check Existing Hooks">

Check if `.claude/hooks.json` already exists in the project.

If it exists:
- Read existing hooks
- Ask user: "Merge with existing hooks or replace?"
- If merge: combine hook arrays, avoiding duplicates by name

If it doesn't exist:
- Create `.claude/` directory if needed
- Copy hooks directly

</step>

<step number="4" name="Install Hooks">

For single language:
```bash
mkdir -p .claude
cp ${HOOKS_SOURCE} .claude/hooks.json
```

For multiple languages, merge hooks using this pattern:
```bash
# Read both files and combine hooks arrays
jq -s '{ hooks: [ .[0].hooks[], .[1].hooks[] ] | unique_by(.name) }' \
  file1.json file2.json > .claude/hooks.json
```

</step>

<step number="5" name="Offer CLAUDE.md Section">

Ask user: "Would you like to add LSP guidance to your project's CLAUDE.md?"

If yes:
- Check if CLAUDE.md exists
- If exists: append the language-specific LSP section
- If not: create with LSP section as initial content

LSP section files are at:
`${CLAUDE_PLUGIN_DIR}/skills/lsp-enable/references/{language}-lsp-section.md`

</step>

<step number="6" name="Verify Setup">

After installation, confirm:
1. `.claude/hooks.json` exists and is valid JSON
2. Hooks are appropriate for detected languages
3. Report what was installed

</step>

## Output Format

```
LSP Setup Complete
==================

Languages detected: TypeScript, Go
Hooks installed:
  - format-on-edit (TypeScript)
  - lint-check-on-edit (TypeScript)
  - typecheck-on-edit (TypeScript)
  - pre-commit-quality-gate (TypeScript)
  - format-on-edit (Go)
  - vet-on-edit (Go)

Files created/modified:
  - .claude/hooks.json (created)
  - CLAUDE.md (appended LSP sections)

Next steps:
  1. Ensure ENABLE_LSP_TOOL=1 is set in your shell
  2. Install language servers: npm install -g @vtsls/language-server
  3. Restart Claude Code session to activate hooks
```

<error_handling>

- If no supported languages detected: Inform user and ask which language to configure
- If hook file not found: Report error with path
- If JSON merge fails: Fall back to replacement with user confirmation
- If CLAUDE.md append fails: Report error but don't fail entire setup

</error_handling>

## Tips

- Run `lsp-setup auto` to auto-detect languages
- Run `lsp-setup typescript` to set up only TypeScript hooks
- Run `lsp-setup typescript go` to set up multiple languages
- Hooks can be customized after installation in `.claude/hooks.json`
