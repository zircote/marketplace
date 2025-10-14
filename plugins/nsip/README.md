# NSIP API Client - Claude Code Plugin

Access NSIP sheep breeding data through Claude Code with one-command installation.

## Quick Start

```bash
# Install the plugin from GitHub
/plugin marketplace add epicpast/marketplace
/plugin install nsip

# That's it! The MCP server and all tools are automatically configured.
```

**What you get:**
- 9 MCP tools for sheep breeding data
- 9 slash commands for quick workflows
- 5 automatic hooks for enhanced functionality
- Automatic package installation via `uvx`
- No manual setup required

## Enhanced Features (Hooks)

The NSIP plugin includes intelligent hooks that automatically enhance your workflow:

| Hook | When | What It Does |
|------|------|--------------|
| API Health Check | Session start | Verifies NSIP API connectivity |
| LPN Validator | Before calls | Validates LPN ID format to prevent errors |
| Query Logger | After calls | Logs all API calls for audit/debugging |
| Result Cache | After calls | Caches frequently accessed data (60min TTL) |
| CSV Exporter | After searches | Auto-exports search results to CSV |

See [hooks/README.md](./hooks/README.md) for detailed hook documentation.

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
| `/nsip/discover` | Show database info, breeds, statuses | `/nsip/discover` |
| `/nsip/lookup` | Get animal details by LPN ID | `/nsip/lookup 6####92020###249` |
| `/nsip/profile` | Complete animal profile | `/nsip/profile 6####92020###249` |
| `/nsip/health` | Server performance metrics | `/nsip/health` |
| `/nsip/test-api` | Validate API connectivity | `/nsip/test-api` |
| `/nsip/search` | Search animals with filters | `/nsip/search` |
| `/nsip/traits` | Get trait ranges for breed | `/nsip/traits 486` |
| `/nsip/lineage` | Get pedigree tree | `/nsip/lineage 6####92020###249` |
| `/nsip/progeny` | List offspring | `/nsip/progeny 6####92020###249` |

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

- **Query Logs**: `~/.claude-code/nsip-logs/query_log.jsonl`
- **Cache Files**: `~/.claude-code/nsip-cache/` (60-minute TTL)
- **CSV Exports**: `~/.claude-code/nsip-exports/`

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
   /plugin disable nsip-api-client
   /plugin enable nsip-api-client
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
- Use: `/nsip/test-api` command to diagnose
- Verify internet connectivity

### Hook Issues

**If hooks aren't working:**
- Check: `~/.claude-code/` directory permissions
- Clear cache: `rm -rf ~/.claude-code/nsip-cache/*`
- View logs: `tail -f ~/.claude-code/nsip-logs/query_log.jsonl`

See [hooks/README.md](./hooks/README.md) for detailed troubleshooting.

## Plugin Structure

```
.claude-plugin/
├── plugin.json          # Plugin config + MCP server setup
├── marketplace.json     # Marketplace listing
├── README.md           # This file
├── MCP_SERVER_FIX.md   # Technical documentation
├── commands/           # Slash commands
│   └── nsip/
│       ├── discover.md
│       ├── health.md
│       ├── lineage.md
│       ├── lookup.md
│       ├── profile.md
│       ├── progeny.md
│       ├── search.md
│       ├── test-api.md
│       └── traits.md
└── hooks/              # Plugin hooks
    ├── README.md       # Hook documentation
    ├── hooks.json      # Hook configuration
    └── scripts/        # Hook implementations
        ├── api_health_check.py
        ├── lpn_validator.py
        ├── query_logger.py
        ├── result_cache.py
        └── csv_exporter.py
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

See `MCP_SERVER_FIX.md` for technical details.

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

See [docs/DISTRIBUTION.md](../docs/DISTRIBUTION.md) for details.

## Platform Support

Works identically on:
- Claude Code CLI (terminal)
- Claude Code VS Code extension
- 100% feature parity across platforms

## Support

- **Repository**: https://github.com/epicpast/nsip-api-client
- **Issues**: https://github.com/epicpast/nsip-api-client/issues
- **Changelog**: https://github.com/epicpast/nsip-api-client/blob/main/docs/CHANGELOG.md
- **Technical Details**: [MCP_SERVER_FIX.md](./MCP_SERVER_FIX.md)
- **Hook Documentation**: [hooks/README.md](./hooks/README.md)

## Version

Current plugin version: **1.3.0**
Current hooks version: **1.0.0**

See [CHANGELOG](../docs/CHANGELOG.md) for release history.
