# nsip Plugin - NSIP API Client for Claude Code

Access NSIP (National Sheep Improvement Program) sheep breeding data through Claude Code with one-command installation.

## Quick Start

```bash
# Add the marketplace and install
claude /plugin marketplace add zircote/marketplace
claude /plugin install nsip

# That's it! The MCP server and all tools are automatically configured.
```

**What you get:**
- 9 MCP tools for sheep breeding data
- 10 slash commands for quick workflows
- 1 expert agent for breeding consultation
- 14 automatic hooks for enhanced functionality
- Automatic package installation via `uvx`
- No manual setup required

## Verify Installation

After installing, verify the MCP tools and commands are working:

```bash
# Test API connectivity
claude "/nsip:test-api"

# Get database info (should show last update date)
claude "/nsip:discover"

# Verify MCP tools are available
claude "Use nsip_list_breeds to show available sheep breeds"
```

You should see a successful API connection, the last update date, and a list of sheep breeds including Katahdin, Dorper, and others.

## Enhanced Features (Hooks)

The NSIP plugin includes 14 intelligent hooks that automatically enhance your workflow:

### Hook Categories

**Error Resilience (3 hooks)**
- Auto-retry with exponential backoff
- Fallback to cached data on failures
- Alert tracking for repeated errors

**Context Enhancement (2 hooks)**
- Breed-specific characteristics injection
- Comprehensive trait definitions

**Data Export (2 hooks)**
- Pedigree tree visualizations
- Breeding analysis reports

**Workflow Intelligence (2 hooks)**
- Smart LPN ID detection in prompts
- Comparative analysis suggestions

**Core Operations (5 hooks)**
- API health monitoring
- LPN format validation
- Query logging
- Result caching
- CSV exports

See [hooks/README.md](./hooks/README.md) for detailed documentation on all 14 hooks.

## How It Works

The plugin uses `uvx` to automatically install the `nsip-client` package from GitHub in an isolated environment. When you install the plugin:

1. Claude Code reads `.claude-plugin/plugin.json`
2. Finds the MCP server configuration
3. Runs: `uvx --from git+https://github.com/epicpast/nsip-api-client.git nsip-mcp-server`
4. `uvx` automatically downloads and installs the package
5. MCP server starts and connects
6. All tools become available
7. Hooks automatically activate

**No manual installation required!**

## Prerequisites

- Claude Code CLI or VS Code extension
- `uv` package manager (install from https://docs.astral.sh/uv/)
- Internet connection (for first-time package download)

## Slash Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/nsip:consult` | **Expert breeding consultation** (uses shepherd agent) | `/nsip:consult I need a terminal sire` |
| `/nsip:discover` | Show database info, breeds, statuses | `/nsip:discover` |
| `/nsip:lookup` | Get animal details by LPN ID | `/nsip:lookup 6####92020###249` |
| `/nsip:profile` | Complete animal profile | `/nsip:profile 6####92020###249` |
| `/nsip:health` | Server performance metrics | `/nsip:health` |
| `/nsip:test-api` | Validate API connectivity | `/nsip:test-api` |
| `/nsip:search` | Search animals with filters | `/nsip:search` |
| `/nsip:traits` | Get trait ranges for breed | `/nsip:traits 486` |
| `/nsip:lineage` | Get pedigree tree | `/nsip:lineage 6####92020###249` |
| `/nsip:progeny` | List offspring | `/nsip:progeny 6####92020###249` |

### Expert Agent Commands

**`/nsip:consult`** - This command invokes the `nsip:shepherd` expert agent, which provides:
- Breeding decision support with NSIP data analysis
- Health diagnosis and treatment recommendations
- Nutrition planning across production stages
- Flock management and culling guidance
- Genetic trait interpretation and selection strategies

The shepherd agent has access to all NSIP tools and provides expert interpretation of breeding values, genetics, and farm operations.

## MCP Tools

Ask Claude to use these tools directly:

- `nsip_get_last_update`: Database update date
- `nsip_list_breeds`: Available breed groups
- `nsip_get_statuses`: Animal statuses by breed
- `nsip_get_trait_ranges`: Trait ranges for breed
- `nsip_search_animals`: Search with pagination
- `nsip_get_animal`: Detailed animal information
- `nsip_get_lineage`: Pedigree tree
- `nsip_get_progeny`: Offspring list
- `nsip_search_by_lpn`: Complete animal profile

Example:
```
"Use nsip_list_breeds to show me all available sheep breeds"
"Search for Katahdin sheep using nsip_search_animals with breed_id 64"
```

## Hook Data Locations

The plugin hooks store data in your home directory:

**Logs**:
- `~/.claude-code/nsip-logs/query_log.jsonl` - All API calls
- `~/.claude-code/nsip-logs/retry_log.jsonl` - Retry attempts
- `~/.claude-code/nsip-logs/fallback_log.jsonl` - Cache fallbacks
- `~/.claude-code/nsip-logs/detected_ids.jsonl` - LPN detections
- `~/.claude-code/nsip-logs/ALERT_*.txt` - Error alerts

**Cache**:
- `~/.claude-code/nsip-cache/` - Cached API responses (60-min TTL)

**Exports**:
- `~/.claude-code/nsip-exports/` - CSV, pedigrees, breeding reports

All hook operations are automatic and transparent. See [hooks/README.md](./hooks/README.md) for maintenance.

## Troubleshooting

### MCP Server Doesn't Connect

**Symptoms:**
- Plugin installs successfully
- Slash commands work
- MCP tools don't appear

**Solutions:**

1. **Check uv installation:**
   ```bash
   uv --version
   uvx --version
   ```
   If not installed: https://docs.astral.sh/uv/

2. **Test the MCP server command manually:**
   ```bash
   uvx --from git+https://github.com/epicpast/nsip-api-client.git nsip-mcp-server
   ```
   Should output: "NSIP MCP Server running on stdio transport"

3. **Check internet connectivity:**
   - First run downloads the package from GitHub
   - Verify GitHub is accessible

4. **Re-enable the plugin:**
   ```bash
   claude /plugin disable nsip
   claude /plugin enable nsip
   ```

5. **Check Claude Code MCP panel:**
   - Look for error messages
   - Verify "nsip-api-client" server appears

### Package Installation Issues

**If `uvx` can't install the package:**

Install manually and update the plugin config:
```bash
# Install globally with uv
uv tool install git+https://github.com/epicpast/nsip-api-client.git

# Verify installation
nsip-mcp-server --help
```

Then update `.claude-plugin/plugin.json` to use the installed command:
```json
{
  "mcpServers": {
    "nsip-api-client": {
      "command": "nsip-mcp-server",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

### API Connection Errors

**Note**: The NSIP API is public and requires no authentication.

**If API calls fail:**
- Check: `curl http://nsipsearch.nsip.org/api/GetLastUpdate`
- Use: `/nsip:test-api` command to diagnose
- Verify internet connectivity

### Hook Issues

**If hooks aren't working:**
- Check: `~/.claude-code/` directory permissions
- Clear cache: `rm -rf ~/.claude-code/nsip-cache/*`
- View logs: `tail -f ~/.claude-code/nsip-logs/query_log.jsonl`

See [hooks/README.md](./hooks/README.md) for detailed troubleshooting.

## Plugin Structure

```
plugins/nsip/
├── README.md                    # This file
├── .mcp.json                    # MCP server configuration
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest with hooks
├── commands/                    # Slash commands (10 total)
│   ├── consult.md              # Expert agent consultation
│   ├── discover.md
│   ├── health.md
│   ├── lineage.md
│   ├── lookup.md
│   ├── profile.md
│   ├── progeny.md
│   ├── search.md
│   ├── test-api.md
│   └── traits.md
├── agents/                      # Expert agents
│   └── shepherd.md             # Sheep breeding expert
├── hooks/                       # Plugin hooks (14 total)
│   ├── README.md               # Hook documentation
│   └── scripts/                # Hook implementations
│       ├── api_health_check.py
│       ├── lpn_validator.py
│       ├── breed_context_injector.py
│       ├── trait_dictionary.py
│       ├── auto_retry.py
│       ├── fallback_cache.py
│       ├── error_notifier.py
│       ├── query_logger.py
│       ├── result_cache.py
│       ├── csv_exporter.py
│       ├── pedigree_visualizer.py
│       ├── breeding_report.py
│       ├── smart_search_detector.py
│       └── comparative_analyzer.py
└── tests/                       # Test suite (78 tests)
    ├── README.md
    ├── unit/
    ├── integration/
    └── fixtures/
```

## MCP Server Configuration

The plugin uses this configuration in `plugin.json`:

```json
{
  "mcpServers": {
    "nsip-api-client": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/epicpast/nsip-api-client.git",
        "nsip-mcp-server"
      ],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

**Why this works:**
- `uvx` automatically installs packages in isolated environments
- `--from git+https://...` installs from GitHub
- `nsip-mcp-server` is the entry point from `pyproject.toml`
- Works for all users, no local setup needed

## Development Testing

For local development:

```bash
# 1. Clone repository
git clone https://github.com/epicpast/nsip-api-client.git
cd nsip-api-client

# 2. Install in editable mode
uv pip install -e .

# 3. Test MCP server
python -m nsip_mcp.cli

# 4. Or test with uvx from local directory
uvx --from . nsip-mcp-server
```

## Distribution

**Important**: This package is NOT published to PyPI. It's distributed via:
- GitHub Releases (wheel files)
- Direct Git URLs
- Plugin auto-installation with `uvx`

## Platform Support

Works identically on:
- Claude Code CLI (terminal)
- Claude Code VS Code extension
- 100% feature parity across platforms

## Integration with Other Plugins

- **zircote plugin**: Use `data-analyst` for breeding data analysis
- **gh plugin**: Commit breeding reports with `/git:cp`
- **document-skills**: Export pedigrees to PDF/XLSX

## Support

- **Repository**: https://github.com/epicpast/nsip-api-client
- **Issues**: https://github.com/epicpast/nsip-api-client/issues
- **Hook Documentation**: [hooks/README.md](./hooks/README.md)

## Version

- **Plugin**: 1.3.0
- **Hooks**: 2.0.0 (14 hooks across 4 lifecycle events)
- **Tests**: 78 tests with 98.7% success rate
