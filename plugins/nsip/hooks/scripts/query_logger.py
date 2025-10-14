#!/usr/bin/env python3
"""
Query Logger Hook (PostToolUse)
Logs all NSIP API calls with timestamps for audit and debugging.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def get_log_file() -> Path:
    """Get the log file path, creating directories if needed."""
    log_dir = Path.home() / ".claude-code" / "nsip-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "query_log.jsonl"


def log_query(tool_name: str, parameters: dict, result: dict, duration_ms: float = None):
    """
    Log a query to the JSONL log file.

    Args:
        tool_name: Name of the tool that was called
        parameters: Parameters passed to the tool
        result: Result returned by the tool
        duration_ms: Duration of the call in milliseconds
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "parameters": parameters,
        "success": not result.get("isError", False),
        "error": result.get("error"),
        "result_size": len(json.dumps(result)),
        "duration_ms": duration_ms
    }

    # Redact sensitive data if any (currently none for NSIP)
    # This is a placeholder for future use
    if "api_key" in log_entry["parameters"]:
        log_entry["parameters"]["api_key"] = "***REDACTED***"

    log_file = get_log_file()

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        # Silently fail logging - don't break the tool execution
        print(json.dumps({
            "metadata": {
                "log_error": str(e)
            }
        }), file=sys.stderr)


def main():
    """Process PostToolUse hook for query logging."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "unknown")
        tool_params = hook_data.get("tool", {}).get("parameters", {})
        tool_result = hook_data.get("result", {})

        # Extract duration if available
        duration_ms = hook_data.get("metadata", {}).get("duration_ms")

        # Log the query
        log_query(tool_name, tool_params, tool_result, duration_ms)

        # Return success with metadata
        result = {
            "continue": True,
            "metadata": {
                "logged": True,
                "log_file": str(get_log_file()),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "logged": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
