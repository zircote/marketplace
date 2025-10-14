#!/usr/bin/env python3
"""
LPN Validator Hook (PreToolUse)
Validates LPN ID format before making NSIP API calls to prevent errors.
"""

import re
import sys
import json


def validate_lpn(lpn_id: str) -> tuple[bool, str]:
    """
    Validate LPN ID format.

    Expected format: Typically numeric with possible special characters
    Example: 6####92020###249 or similar patterns

    Returns:
        tuple: (is_valid, error_message)
    """
    if not lpn_id:
        return False, "LPN ID cannot be empty"

    # Remove whitespace
    lpn_id = lpn_id.strip()

    # Check minimum length (LPN IDs are typically longer than 5 characters)
    if len(lpn_id) < 5:
        return False, f"LPN ID '{lpn_id}' is too short (minimum 5 characters)"

    # Check maximum length (reasonable upper bound)
    if len(lpn_id) > 50:
        return False, f"LPN ID '{lpn_id}' is too long (maximum 50 characters)"

    # Check for valid characters (alphanumeric, #, -, _)
    if not re.match(r'^[A-Za-z0-9#\-_]+$', lpn_id):
        return False, f"LPN ID '{lpn_id}' contains invalid characters (only alphanumeric, #, -, _ allowed)"

    return True, ""


def main():
    """Process PreToolUse hook for LPN validation."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_params = hook_data.get("tool", {}).get("parameters", {})

        # Extract LPN ID from parameters
        lpn_id = None
        if "lpn_id" in tool_params:
            lpn_id = tool_params["lpn_id"]
        elif "animal_id" in tool_params:
            lpn_id = tool_params["animal_id"]
        elif "id" in tool_params:
            lpn_id = tool_params["id"]

        # If no LPN ID found, allow the call to proceed
        if lpn_id is None:
            result = {
                "continue": True,
                "metadata": {
                    "validation": "skipped",
                    "reason": "No LPN ID parameter found"
                }
            }
            print(json.dumps(result))
            return

        # Validate the LPN ID
        is_valid, error_message = validate_lpn(str(lpn_id))

        if is_valid:
            result = {
                "continue": True,
                "metadata": {
                    "validation": "passed",
                    "lpn_id": lpn_id,
                    "tool": tool_name
                }
            }
        else:
            result = {
                "continue": False,
                "error": error_message,
                "metadata": {
                    "validation": "failed",
                    "lpn_id": lpn_id,
                    "tool": tool_name
                }
            }

        print(json.dumps(result))

    except Exception as e:
        # On error, allow the call to proceed but log the error
        error_result = {
            "continue": True,
            "metadata": {
                "validation": "error",
                "error": str(e)
            }
        }
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
