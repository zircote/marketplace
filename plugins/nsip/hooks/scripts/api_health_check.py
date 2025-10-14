#!/usr/bin/env python3
"""
API Health Check Hook (SessionStart)
Verifies NSIP API connectivity and availability at session start.
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Tuple, Optional


# NSIP API endpoints
NSIP_API_BASE = "http://nsipsearch.nsip.org/api"
HEALTH_CHECK_ENDPOINT = f"{NSIP_API_BASE}/GetLastUpdate"


def check_api_health(timeout: int = 5) -> Tuple[bool, Optional[dict], Optional[str]]:
    """
    Check NSIP API health by calling GetLastUpdate endpoint.

    Args:
        timeout: Request timeout in seconds

    Returns:
        Tuple of (is_healthy, response_data, error_message)
    """
    try:
        req = urllib.request.Request(
            HEALTH_CHECK_ENDPOINT,
            headers={'User-Agent': 'Claude-Code-NSIP-Plugin/1.0'}
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return True, data, None
            else:
                return False, None, f"HTTP {response.status}"

    except urllib.error.HTTPError as e:
        return False, None, f"HTTP Error {e.code}: {e.reason}"

    except urllib.error.URLError as e:
        return False, None, f"Connection Error: {e.reason}"

    except Exception as e:
        return False, None, f"Unexpected Error: {str(e)}"


def format_health_report(is_healthy: bool, data: Optional[dict], error: Optional[str]) -> dict:
    """
    Format health check report.

    Args:
        is_healthy: Whether API is healthy
        data: Response data if successful
        error: Error message if failed

    Returns:
        Formatted health report
    """
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "api_healthy": is_healthy,
        "api_endpoint": HEALTH_CHECK_ENDPOINT
    }

    if is_healthy and data:
        report["last_update"] = data.get("LastUpdate", "Unknown")
        report["status"] = "API is operational"
    else:
        report["status"] = "API is not accessible"
        report["error"] = error

    return report


def main():
    """Process SessionStart hook for API health check."""
    try:
        # Check API health
        is_healthy, data, error = check_api_health(timeout=5)

        # Format health report
        health_report = format_health_report(is_healthy, data, error)

        # Prepare hook result
        if is_healthy:
            result = {
                "continue": True,
                "metadata": {
                    "health_check": "passed",
                    **health_report
                }
            }
        else:
            # Continue even if API is down, but warn user
            result = {
                "continue": True,
                "warning": f"NSIP API health check failed: {error}",
                "metadata": {
                    "health_check": "failed",
                    **health_report
                }
            }

        print(json.dumps(result))

    except Exception as e:
        # On unexpected error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "health_check": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
