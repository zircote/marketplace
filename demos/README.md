# Plugin Demos

Animated terminal demos for marketplace plugins, generated using [vhs](https://github.com/charmbracelet/vhs).

## Generating Demos

### Local Generation

```bash
# Install vhs (requires ttyd for terminal recording)
brew install vhs

# Generate all demos
make demos

# Generate specific demo
cd demos && vhs nsip-discover.tape
```

**Note**: vhs requires an interactive terminal with ttyd. If you get connection errors, ensure no other process is using port 2300.

### GitHub Actions

Demos can also be generated via the **Generate Demos** workflow:
1. Go to Actions → Generate Demos
2. Select demo to generate (or "all")
3. Run workflow

Generated GIFs are automatically committed to the repo.

## Available Demos

| Plugin | Demo | Description |
|--------|------|-------------|
| **nsip** | [nsip-discover.gif](nsip-discover.gif) | Database discovery command |
| **gh** | [gh-prune.gif](gh-prune.gif) | Branch cleanup workflow |
| **zircote** | [zircote-explore.gif](zircote-explore.gif) | Codebase exploration |
| **datadog** | [datadog-monitor.gif](datadog-monitor.gif) | Monitor creation |
| **document-skills** | [docskills-pdf.gif](docskills-pdf.gif) | PDF analysis |

## Customizing Demos

Edit the `.tape` files to customize:
- `Set Theme` - Terminal color scheme
- `Set FontSize` - Text size
- `Set Width`/`Set Height` - GIF dimensions
- `Set TypingSpeed` - Characters per second
- `Sleep` - Pause duration

## Demo Guidelines

1. Keep demos under 30 seconds
2. Show one feature per demo
3. Use realistic but simple examples
4. Pause on important output

## Non-Interactive Execution

All demos use these flags for non-interactive recording:

```bash
claude --dangerously-skip-permissions -p '<prompt>'
```

- `--dangerously-skip-permissions` - Auto-allows all tool use (no prompts)
- `-p` - Print mode (outputs to stdout, exits when done)

This ensures demos run without user interaction for automated recording.
