#!/usr/bin/env python3
"""
Error Notifier Hook (PostToolUse)
Detect repeated failures and create alert files.
Triggers on: All mcp__nsip__* tools
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class ErrorNotifier:
    """Track and notify about repeated API failures."""

    def __init__(self, log_dir: Path = None):
        """
        Initialize error notifier.

        Args:
            log_dir: Directory to store error tracking and alerts
        """
        if log_dir is None:
            log_dir = Path.home() / ".claude-code" / "nsip-logs"

        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.tracker_file = self.log_dir / "error_tracker.json"
        self.failure_threshold = 3  # failures to trigger alert
        self.time_window = timedelta(minutes=5)  # time window for counting failures

    def _load_error_tracker(self) -> Dict:
        """
        Load error tracker state.

        Returns:
            Error tracker data
        """
        try:
            if self.tracker_file.exists():
                with open(self.tracker_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass

        return {
            "failures": [],
            "last_alert": None
        }

    def _save_error_tracker(self, tracker_data: Dict):
        """
        Save error tracker state.

        Args:
            tracker_data: Tracker data to save
        """
        try:
            with open(self.tracker_file, "w", encoding="utf-8") as f:
                json.dump(tracker_data, f, indent=2)
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

    def _clean_old_failures(self, failures: List[Dict]) -> List[Dict]:
        """
        Remove failures outside the time window.

        Args:
            failures: List of failure records

        Returns:
            Filtered list of recent failures
        """
        cutoff_time = datetime.utcnow() - self.time_window
        recent_failures = []

        for failure in failures:
            try:
                failure_time = datetime.fromisoformat(failure["timestamp"].rstrip("Z"))
                if failure_time > cutoff_time:
                    recent_failures.append(failure)
            except Exception:
                continue

        return recent_failures

    def _get_troubleshooting_tips(self) -> List[str]:
        """
        Get troubleshooting tips for NSIP API failures.

        Returns:
            List of troubleshooting tips
        """
        return [
            "Check your internet connection",
            "Verify the NSIP API is operational: http://nsipsearch.nsip.org",
            "Check if your API credentials are valid (if required)",
            "Try accessing the API directly in a browser",
            "Check the Claude Code logs for detailed error messages",
            "Wait a few minutes and try again - the API may be temporarily unavailable",
            "Contact NSIP support if the issue persists"
        ]

    def _create_alert(self, failures: List[Dict]) -> str:
        """
        Create alert file for repeated failures.

        Args:
            failures: List of recent failures

        Returns:
            Path to alert file
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        alert_file = self.log_dir / f"ALERT_{timestamp}.txt"

        # Group failures by tool
        tool_failures = {}
        for failure in failures:
            tool = failure.get("tool", "unknown")
            if tool not in tool_failures:
                tool_failures[tool] = []
            tool_failures[tool].append(failure)

        # Build alert content
        lines = []
        lines.append("=" * 80)
        lines.append("NSIP API FAILURE ALERT")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Alert Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        lines.append(f"Total Failures: {len(failures)} in the last {int(self.time_window.total_seconds() / 60)} minutes")
        lines.append("")

        lines.append("AFFECTED TOOLS:")
        lines.append("-" * 80)
        for tool, tool_failures_list in sorted(tool_failures.items()):
            lines.append(f"  {tool}: {len(tool_failures_list)} failure(s)")
        lines.append("")

        lines.append("FAILURE DETAILS:")
        lines.append("-" * 80)
        for i, failure in enumerate(failures[-5:], 1):  # Show last 5
            lines.append(f"{i}. Tool: {failure.get('tool', 'unknown')}")
            lines.append(f"   Time: {failure.get('timestamp', 'unknown')}")
            lines.append(f"   Error: {failure.get('error_reason', 'unknown')}")
            lines.append("")

        lines.append("TROUBLESHOOTING STEPS:")
        lines.append("-" * 80)
        for i, tip in enumerate(self._get_troubleshooting_tips(), 1):
            lines.append(f"{i}. {tip}")
        lines.append("")

        lines.append("=" * 80)
        lines.append("This alert was automatically generated by the NSIP plugin error notifier.")
        lines.append("=" * 80)

        # Save alert file
        try:
            with open(alert_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return str(alert_file)
        except Exception:
            return ""

    def track_and_notify(
        self,
        tool_name: str,
        result: dict
    ) -> Dict:
        """
        Track failures and create alerts if threshold exceeded.

        Args:
            tool_name: Name of the tool
            result: Tool result

        Returns:
            Metadata about notification status
        """
        # Check if this is a failure
        if not self._is_failure(result):
            return {
                "error_tracked": False,
                "reason": "No failure detected"
            }

        # Load tracker
        tracker = self._load_error_tracker()

        # Add this failure
        failure_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool": tool_name,
            "error_reason": result.get("error", "Unknown error")
        }

        tracker["failures"].append(failure_record)

        # Clean old failures
        tracker["failures"] = self._clean_old_failures(tracker["failures"])

        # Check if we should create an alert
        recent_failure_count = len(tracker["failures"])
        should_alert = recent_failure_count >= self.failure_threshold

        # Check if we recently alerted (avoid spam)
        last_alert = tracker.get("last_alert")
        if last_alert:
            try:
                last_alert_time = datetime.fromisoformat(last_alert.rstrip("Z"))
                time_since_alert = datetime.utcnow() - last_alert_time
                # Don't alert again within 10 minutes
                if time_since_alert < timedelta(minutes=10):
                    should_alert = False
            except Exception:
                pass

        alert_path = None
        if should_alert:
            alert_path = self._create_alert(tracker["failures"])
            tracker["last_alert"] = datetime.utcnow().isoformat() + "Z"

        # Save tracker
        self._save_error_tracker(tracker)

        return {
            "error_tracked": True,
            "recent_failure_count": recent_failure_count,
            "alert_created": bool(alert_path),
            "alert_path": alert_path,
            "threshold": self.failure_threshold
        }


def main():
    """Process PostToolUse hook for error notification."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_result = hook_data.get("result", {})

        # Only handle NSIP tools
        if not tool_name.startswith("mcp__nsip__"):
            result = {
                "continue": True,
                "metadata": {"error_tracked": False, "reason": "Not an NSIP tool"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Track errors and notify
        notifier = ErrorNotifier()
        notify_metadata = notifier.track_and_notify(tool_name, tool_result)

        # Build result
        result = {
            "continue": True,
            "metadata": notify_metadata
        }

        # Add context message if alert was created
        if notify_metadata.get("alert_created"):
            result["context"] = (
                f"ALERT: {notify_metadata['recent_failure_count']} API failures detected. "
                f"Alert file created at: {notify_metadata['alert_path']}"
            )

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "error_tracked": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
