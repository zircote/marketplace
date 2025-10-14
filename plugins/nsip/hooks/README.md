# NSIP Plugin Hooks

This directory contains Claude Code plugin hooks that enhance the NSIP plugin functionality with automatic logging, caching, validation, and export capabilities.

## Overview

The NSIP plugin includes 5 high-value hooks that execute at different stages of tool usage:

| Hook Name | Type | Purpose | Status |
|-----------|------|---------|--------|
| API Health Check | SessionStart | Verify API connectivity at session start | Active |
| LPN Validator | PreToolUse | Validate LPN ID format before API calls | Active |
| Query Logger | PostToolUse | Log all API calls with timestamps | Active |
| Result Cache | PostToolUse | Cache frequently accessed data | Active |
| CSV Exporter | PostToolUse | Export search results to CSV | Active |

## Hook Types

### SessionStart Hooks

Execute once when Claude Code session begins.

**API Health Check** (`api_health_check.py`)
- Verifies NSIP API is accessible
- Checks database last update timestamp
- Warns if API is unavailable
- Timeout: 5 seconds

### PreToolUse Hooks

Execute before tool calls, can prevent execution.

**LPN Validator** (`lpn_validator.py`)
- Validates LPN ID format
- Prevents invalid API calls
- Checks length and character requirements
- Applied to: `nsip_get_animal`, `nsip_search_by_lpn`, `nsip_get_lineage`, `nsip_get_progeny`

### PostToolUse Hooks

Execute after tool calls, cannot modify results.

**Query Logger** (`query_logger.py`)
- Logs all NSIP tool calls
- Captures timestamps, parameters, and results
- Stores logs in `~/.claude-code/nsip-logs/query_log.jsonl`
- JSONL format for easy parsing
- Applied to: All 5 main NSIP tools

**Result Cache** (`result_cache.py`)
- Caches animal data, lineage, and progeny
- TTL: 60 minutes
- Cache location: `~/.claude-code/nsip-cache/`
- Improves performance for repeated queries
- Applied to: `nsip_get_animal`, `nsip_search_by_lpn`, `nsip_get_lineage`, `nsip_get_progeny`

**CSV Exporter** (`csv_exporter.py`)
- Exports search results to CSV
- Auto-flattens nested data structures
- Exports to: `~/.claude-code/nsip-exports/`
- Timestamp-based filenames
- Applied to: `nsip_search_animals`

## Installation

Hooks are automatically loaded when the NSIP plugin is installed. No manual setup required.

```bash
/plugin install nsip
```

## Configuration

Hook configuration is stored in `hooks.json`:

```json
{
  "PreToolUse": [...],
  "PostToolUse": [...],
  "SessionStart": [...]
}
```

## Hook Locations

```
plugins/nsip/hooks/
├── README.md              # This file
├── hooks.json             # Hook configuration
└── scripts/
    ├── api_health_check.py    # SessionStart hook
    ├── lpn_validator.py       # PreToolUse hook
    ├── query_logger.py        # PostToolUse hook
    ├── result_cache.py        # PostToolUse hook
    └── csv_exporter.py        # PostToolUse hook
```

## Data Locations

### Query Logs
- **Path**: `~/.claude-code/nsip-logs/query_log.jsonl`
- **Format**: JSONL (one JSON object per line)
- **Rotation**: None (manual cleanup required)

Example log entry:
```json
{
  "timestamp": "2025-10-13T14:30:45.123Z",
  "tool": "mcp__nsip__nsip_get_animal",
  "parameters": {"lpn_id": "6####92020###249"},
  "success": true,
  "error": null,
  "result_size": 1234,
  "duration_ms": 250
}
```

### Cache Files
- **Path**: `~/.claude-code/nsip-cache/`
- **Format**: JSON files with SHA-256 hashed filenames
- **TTL**: 60 minutes
- **Cleanup**: Automatic on expiration

Cache entry structure:
```json
{
  "tool": "mcp__nsip__nsip_get_animal",
  "parameters": {"lpn_id": "6####92020###249"},
  "result": {...},
  "cached_at": "2025-10-13T14:30:45.123Z"
}
```

### CSV Exports
- **Path**: `~/.claude-code/nsip-exports/`
- **Format**: CSV with flattened nested data
- **Naming**: `{tool_name}_{timestamp}.csv`
- **Cleanup**: Manual

Example filename: `nsip_search_animals_20251013_143045.csv`

## Hook Behavior

### Validation Flow (PreToolUse)

```
Tool Call Request
    ↓
LPN Validator Hook
    ↓
Valid? → Yes → Continue to API
    ↓
    No → Block Call → Return Error
```

### Logging Flow (PostToolUse)

```
Tool Call Completes
    ↓
Query Logger Hook → Log to JSONL
    ↓
Result Cache Hook → Cache if applicable
    ↓
CSV Exporter Hook → Export if search
    ↓
Return Result to User
```

### Health Check Flow (SessionStart)

```
Claude Code Session Starts
    ↓
API Health Check Hook
    ↓
Call: http://nsipsearch.nsip.org/api/GetLastUpdate
    ↓
Success? → Yes → Continue silently
    ↓
    No → Display warning → Continue anyway
```

## Error Handling

All hooks follow fail-safe principles:

1. **Never block execution on hook errors**
2. **Log errors but continue**
3. **Return metadata about hook status**
4. **Graceful degradation**

Example error response:
```json
{
  "continue": true,
  "metadata": {
    "logged": false,
    "error": "Permission denied writing to log file"
  }
}
```

## Performance Impact

| Hook | Overhead | When |
|------|----------|------|
| API Health Check | ~100ms | Once per session |
| LPN Validator | <1ms | Before validated calls |
| Query Logger | <5ms | After all calls |
| Result Cache | <2ms | After cached calls |
| CSV Exporter | 10-50ms | After searches only |

**Total overhead**: <2% for typical usage

## Debugging Hooks

### Enable verbose logging

```bash
# Check log file
tail -f ~/.claude-code/nsip-logs/query_log.jsonl

# View cache statistics
ls -lh ~/.claude-code/nsip-cache/

# Check exports
ls -lt ~/.claude-code/nsip-exports/
```

### Test individual hooks

```bash
# Test LPN validator
echo '{"tool":{"name":"nsip_get_animal","parameters":{"lpn_id":"123"}}}' | \
  python3 scripts/lpn_validator.py

# Test API health check
python3 scripts/api_health_check.py
```

### Common Issues

**Issue**: Hooks not executing
- Check: `hooks.json` syntax is valid
- Check: Scripts have execute permissions
- Check: Python 3 is available

**Issue**: Permission denied errors
- Check: `~/.claude-code/` directory permissions
- Solution: `chmod 755 ~/.claude-code/`

**Issue**: Cache not working
- Check: Available disk space
- Check: `~/.claude-code/nsip-cache/` exists and is writable
- Clear cache: `rm -rf ~/.claude-code/nsip-cache/*`

## Maintenance

### Clear cache

```bash
rm -rf ~/.claude-code/nsip-cache/*
```

### Archive logs

```bash
mv ~/.claude-code/nsip-logs/query_log.jsonl \
   ~/.claude-code/nsip-logs/query_log.$(date +%Y%m%d).jsonl
```

### View cache statistics

```bash
du -sh ~/.claude-code/nsip-cache/
ls ~/.claude-code/nsip-cache/ | wc -l
```

## Development

### Adding New Hooks

1. Create Python script in `scripts/`
2. Add entry to `hooks.json`
3. Follow hook interface:

```python
import json
import sys

def main():
    hook_data = json.loads(sys.stdin.read())
    # Process hook
    result = {"continue": True, "metadata": {...}}
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

### Hook Interface

**Input** (stdin):
```json
{
  "tool": {
    "name": "mcp__nsip__nsip_get_animal",
    "parameters": {"lpn_id": "..."}
  },
  "result": {...},  // PostToolUse only
  "metadata": {...}
}
```

**Output** (stdout):
```json
{
  "continue": true,  // or false to block (PreToolUse only)
  "error": "...",    // if continue=false
  "warning": "...",  // optional warning message
  "metadata": {...}  // custom metadata
}
```

### Testing Hooks

```bash
# Run hook with test input
cat test_input.json | python3 scripts/query_logger.py

# Check exit code
echo $?  # Should be 0

# Validate JSON output
cat test_input.json | python3 scripts/query_logger.py | jq .
```

## Security Considerations

- **No sensitive data**: NSIP API requires no authentication
- **Local file access**: All data stored in user's home directory
- **No network calls**: Except API health check to public endpoint
- **No data transmission**: Hooks operate locally only

## Support

For issues or questions:
- Repository: https://github.com/epicpast/marketplace
- NSIP API: https://github.com/epicpast/nsip-api-client
- Plugin Issues: https://github.com/epicpast/marketplace/issues

## Version

Current hooks version: **1.0.0**

Compatible with NSIP plugin version: **1.3.0+**

## License

Same license as the NSIP plugin and marketplace repository.
