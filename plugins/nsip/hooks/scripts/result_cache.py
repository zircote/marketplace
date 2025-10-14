#!/usr/bin/env python3
"""
Result Cache Hook (PostToolUse)
Caches frequently accessed animal data to improve performance and reduce API load.
"""

import json
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class ResultCache:
    """Simple file-based cache for NSIP results."""

    def __init__(self, cache_dir: Path = None, ttl_minutes: int = 60):
        """
        Initialize cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_minutes: Time-to-live for cached entries in minutes
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".claude-code" / "nsip-cache"

        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(minutes=ttl_minutes)

    def _get_cache_key(self, tool_name: str, parameters: dict) -> str:
        """Generate cache key from tool name and parameters."""
        # Create deterministic string from parameters
        param_str = json.dumps(parameters, sort_keys=True)
        key_str = f"{tool_name}:{param_str}"

        # Hash for filename safety
        return hashlib.sha256(key_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path to cache file."""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, tool_name: str, parameters: dict) -> Optional[dict]:
        """
        Get cached result if available and not expired.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters

        Returns:
            Cached result or None if not found/expired
        """
        cache_key = self._get_cache_key(tool_name, parameters)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_entry = json.load(f)

            # Check expiration
            cached_at = datetime.fromisoformat(cache_entry["cached_at"].rstrip("Z"))
            if datetime.utcnow() - cached_at > self.ttl:
                # Expired - delete the file
                cache_path.unlink()
                return None

            return cache_entry["result"]

        except Exception:
            # On any error, treat as cache miss
            return None

    def set(self, tool_name: str, parameters: dict, result: dict):
        """
        Store result in cache.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters
            result: Tool result to cache
        """
        cache_key = self._get_cache_key(tool_name, parameters)
        cache_path = self._get_cache_path(cache_key)

        try:
            cache_entry = {
                "tool": tool_name,
                "parameters": parameters,
                "result": result,
                "cached_at": datetime.utcnow().isoformat() + "Z"
            }

            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_entry, f, indent=2)

        except Exception:
            # Silently fail caching - don't break execution
            pass

    def clear(self):
        """Clear all cached entries."""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except Exception:
                pass

    def get_stats(self) -> dict:
        """Get cache statistics."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            "entries": len(cache_files),
            "total_size_bytes": total_size,
            "cache_dir": str(self.cache_dir)
        }


def should_cache_tool(tool_name: str) -> bool:
    """Determine if a tool's results should be cached."""
    # Cache read operations, not searches or mutations
    cacheable_tools = [
        "nsip_get_animal",
        "nsip_search_by_lpn",
        "nsip_get_lineage",
        "nsip_get_progeny"
    ]

    # Extract base tool name (remove mcp__nsip__ prefix if present)
    base_name = tool_name.replace("mcp__nsip__", "")

    return base_name in cacheable_tools


def main():
    """Process PostToolUse hook for result caching."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_params = hook_data.get("tool", {}).get("parameters", {})
        tool_result = hook_data.get("result", {})

        # Initialize cache
        cache = ResultCache(ttl_minutes=60)

        # Only cache successful results for cacheable tools
        if should_cache_tool(tool_name) and not tool_result.get("isError", False):
            cache.set(tool_name, tool_params, tool_result)

            result = {
                "continue": True,
                "metadata": {
                    "cached": True,
                    "cache_stats": cache.get_stats()
                }
            }
        else:
            result = {
                "continue": True,
                "metadata": {
                    "cached": False,
                    "reason": "Not cacheable or error result"
                }
            }

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "cached": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
