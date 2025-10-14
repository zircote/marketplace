#!/usr/bin/env python3
"""
Fallback Cache Hook (PostToolUse)
Provide cached data when API calls fail.
Triggers on: All mcp__nsip__* tools
"""

import json
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict


class FallbackCacheHandler:
    """Handle fallback to cached data on API failures."""

    def __init__(self, cache_dir: Path = None, log_dir: Path = None):
        """
        Initialize fallback cache handler.

        Args:
            cache_dir: Directory containing cached data
            log_dir: Directory to store logs
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".claude-code" / "nsip-cache"
        if log_dir is None:
            log_dir = Path.home() / ".claude-code" / "nsip-logs"

        self.cache_dir = cache_dir
        self.log_dir = log_dir

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.log_file = self.log_dir / "fallback_log.jsonl"

    def _log_fallback(self, log_entry: dict):
        """
        Log fallback usage to JSONL file.

        Args:
            log_entry: Log entry to append
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass

    def _is_failure(self, result: dict) -> bool:
        """
        Determine if result indicates a failure.

        Args:
            result: Tool result to check

        Returns:
            True if result indicates failure
        """
        # Check for explicit error flag
        if result.get("isError", False):
            return True

        # Check for empty content
        content = result.get("content", [])
        if not content:
            return True

        # Check for error messages in content
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text", "")
                    if isinstance(text, str):
                        if "error" in text.lower() or "failed" in text.lower():
                            return True

        return False

    def _get_cache_key(self, tool_name: str, parameters: dict) -> str:
        """
        Generate cache key from tool name and parameters.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters

        Returns:
            Cache key (hash)
        """
        param_str = json.dumps(parameters, sort_keys=True)
        key_str = f"{tool_name}:{param_str}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """
        Get path to cache file.

        Args:
            cache_key: Cache key

        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{cache_key}.json"

    def _load_cached_data(self, tool_name: str, parameters: dict) -> Optional[Dict]:
        """
        Load cached data for given tool and parameters.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters

        Returns:
            Cached data or None if not found
        """
        try:
            cache_key = self._get_cache_key(tool_name, parameters)
            cache_path = self._get_cache_path(cache_key)

            if not cache_path.exists():
                return None

            with open(cache_path, "r", encoding="utf-8") as f:
                cache_entry = json.load(f)

            return cache_entry

        except Exception:
            return None

    def handle_fallback(
        self,
        tool_name: str,
        parameters: dict,
        result: dict
    ) -> Dict:
        """
        Handle fallback to cached data if API failed.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters
            result: Failed result

        Returns:
            Metadata about fallback handling
        """
        # Check if this is a failure
        if not self._is_failure(result):
            return {
                "fallback_used": False,
                "reason": "No failure detected"
            }

        # Try to load cached data
        cached_data = self._load_cached_data(tool_name, parameters)

        if not cached_data:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "tool": tool_name,
                "parameters": parameters,
                "status": "no_cache_available"
            }
            self._log_fallback(log_entry)

            return {
                "fallback_used": False,
                "reason": "No cached data available"
            }

        # Extract metadata from cache
        cached_at = cached_data.get("cached_at", "Unknown")
        cached_result = cached_data.get("result", {})

        # Calculate cache age
        try:
            cached_time = datetime.fromisoformat(cached_at.rstrip("Z"))
            age_seconds = (datetime.utcnow() - cached_time).total_seconds()
            age_minutes = int(age_seconds / 60)
            age_hours = int(age_minutes / 60)

            if age_hours > 0:
                age_str = f"{age_hours} hour(s) old"
            else:
                age_str = f"{age_minutes} minute(s) old"
        except Exception:
            age_str = "unknown age"

        # Log fallback usage
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": tool_name,
            "parameters": parameters,
            "cached_at": cached_at,
            "cache_age": age_str,
            "status": "fallback_used"
        }
        self._log_fallback(log_entry)

        # Build context message
        context_message = (
            f"Warning: API call failed. Using cached data from {cached_at} "
            f"({age_str}). Data may be outdated."
        )

        return {
            "fallback_used": True,
            "cached_at": cached_at,
            "cache_age": age_str,
            "cached_result": cached_result,
            "context_message": context_message
        }


def main():
    """Process PostToolUse hook for fallback cache."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_params = hook_data.get("tool", {}).get("parameters", {})
        tool_result = hook_data.get("result", {})

        # Only handle NSIP tools
        if not tool_name.startswith("mcp__nsip__"):
            result = {
                "continue": True,
                "metadata": {"fallback_checked": False, "reason": "Not an NSIP tool"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Handle fallback logic
        fallback_handler = FallbackCacheHandler()
        fallback_metadata = fallback_handler.handle_fallback(
            tool_name,
            tool_params,
            tool_result
        )

        # Build result
        result = {
            "continue": True,
            "metadata": {
                "fallback_checked": True,
                **fallback_metadata
            }
        }

        # Add context message if fallback was used
        if fallback_metadata.get("context_message"):
            result["context"] = fallback_metadata["context_message"]

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "fallback_checked": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
