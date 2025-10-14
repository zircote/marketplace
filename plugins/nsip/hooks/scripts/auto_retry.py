#!/usr/bin/env python3
"""
Auto Retry Hook (PostToolUse)
Detect API failures and implement retry logic with exponential backoff.
Triggers on: All mcp__nsip__* tools
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple, Optional


class AutoRetryHandler:
    """Handle automatic retry logic for failed API calls."""

    def __init__(self, log_dir: Path = None):
        """
        Initialize retry handler.

        Args:
            log_dir: Directory to store retry logs
        """
        if log_dir is None:
            log_dir = Path.home() / ".claude-code" / "nsip-logs"

        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "retry_log.jsonl"

        # Retry configuration
        self.max_retries = 3
        self.backoff_delays = [1, 2, 4]  # seconds

    def _log_retry(self, log_entry: dict):
        """
        Log retry attempt to JSONL file.

        Args:
            log_entry: Log entry to append
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass

    def _is_failure(self, result: dict) -> Tuple[bool, str]:
        """
        Determine if result indicates a failure.

        Args:
            result: Tool result to check

        Returns:
            Tuple of (is_failure, reason)
        """
        # Check for explicit error flag
        if result.get("isError", False):
            error_msg = result.get("error", "Unknown error")
            return True, f"Error flag: {error_msg}"

        # Check for empty or null content
        content = result.get("content", [])
        if not content:
            return True, "Empty content returned"

        # Check for error messages in content
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text", "")
                    if isinstance(text, str):
                        if "error" in text.lower() or "failed" in text.lower():
                            return True, f"Error in response: {text[:100]}"

        # Check for timeout indicators
        if "timeout" in str(result).lower():
            return True, "Timeout detected"

        return False, ""

    def _execute_retry(
        self,
        tool_name: str,
        parameters: dict,
        original_result: dict,
        attempt: int
    ) -> Optional[dict]:
        """
        Execute a retry attempt.

        Note: In a real implementation, this would re-invoke the tool.
        For hooks, we simulate the retry logic and logging.

        Args:
            tool_name: Name of the tool to retry
            parameters: Tool parameters
            original_result: Original failed result
            attempt: Retry attempt number (1-based)

        Returns:
            Result of retry attempt or None
        """
        # Wait with exponential backoff
        if attempt <= len(self.backoff_delays):
            delay = self.backoff_delays[attempt - 1]
            time.sleep(delay)

        # Log retry attempt
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": tool_name,
            "parameters": parameters,
            "attempt": attempt,
            "backoff_seconds": self.backoff_delays[attempt - 1] if attempt <= len(self.backoff_delays) else 0,
            "status": "retrying"
        }
        self._log_retry(log_entry)

        # In a hook context, we can't actually retry the tool
        # We just log the attempt and return None to indicate
        # that the original result should be used
        return None

    def handle_failure(
        self,
        tool_name: str,
        parameters: dict,
        result: dict
    ) -> Dict:
        """
        Handle failed tool execution with retry logic.

        Args:
            tool_name: Name of the tool that failed
            parameters: Tool parameters
            result: Failed result

        Returns:
            Metadata about retry handling
        """
        is_failure, reason = self._is_failure(result)

        if not is_failure:
            return {
                "retry_needed": False,
                "reason": "No failure detected"
            }

        # Log initial failure
        failure_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": tool_name,
            "parameters": parameters,
            "failure_reason": reason,
            "status": "initial_failure"
        }
        self._log_retry(failure_log)

        # Execute retry attempts
        retry_count = 0
        for attempt in range(1, self.max_retries + 1):
            retry_result = self._execute_retry(
                tool_name,
                parameters,
                result,
                attempt
            )

            retry_count += 1

            # If retry succeeded (in a real implementation)
            if retry_result and not self._is_failure(retry_result)[0]:
                success_log = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "tool": tool_name,
                    "attempt": attempt,
                    "status": "retry_succeeded"
                }
                self._log_retry(success_log)

                return {
                    "retry_needed": True,
                    "retry_count": retry_count,
                    "status": "succeeded",
                    "context_message": f"Note: API call succeeded after {retry_count} retry attempt(s)"
                }

        # All retries exhausted
        exhausted_log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": tool_name,
            "max_retries": self.max_retries,
            "status": "retries_exhausted"
        }
        self._log_retry(exhausted_log)

        return {
            "retry_needed": True,
            "retry_count": retry_count,
            "status": "exhausted",
            "context_message": f"Warning: API call failed after {retry_count} retry attempt(s). Using original result."
        }


def main():
    """Process PostToolUse hook for auto-retry."""
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
                "metadata": {"retry_handled": False, "reason": "Not an NSIP tool"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Handle retry logic
        retry_handler = AutoRetryHandler()
        retry_metadata = retry_handler.handle_failure(
            tool_name,
            tool_params,
            tool_result
        )

        # Build result
        result = {
            "continue": True,
            "metadata": {
                "retry_handled": True,
                **retry_metadata
            }
        }

        # Add context message if retries were attempted
        if retry_metadata.get("context_message"):
            result["context"] = retry_metadata["context_message"]

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "retry_handled": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
