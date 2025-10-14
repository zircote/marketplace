#!/usr/bin/env python3
"""
CSV Exporter Hook (PostToolUse)
Exports search results and animal data to CSV files for analysis.
"""

import json
import sys
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def get_export_dir() -> Path:
    """Get the export directory, creating it if needed."""
    export_dir = Path.home() / ".claude-code" / "nsip-exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir


def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    """
    Flatten nested dictionary for CSV export.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nested items
        sep: Separator for nested keys

    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Convert lists to comma-separated strings
            items.append((new_key, ', '.join(map(str, v)) if v else ''))
        else:
            items.append((new_key, v))

    return dict(items)


def export_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Export data to CSV file.

    Args:
        data: List of dictionaries to export
        filename: Name of the output file

    Returns:
        Path to the exported file
    """
    if not data:
        return None

    export_dir = get_export_dir()
    filepath = export_dir / filename

    # Flatten all dictionaries
    flattened_data = [flatten_dict(item) for item in data]

    # Get all unique keys across all items
    all_keys = set()
    for item in flattened_data:
        all_keys.update(item.keys())

    all_keys = sorted(all_keys)

    # Write to CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()

        for item in flattened_data:
            # Fill missing keys with empty strings
            row = {key: item.get(key, '') for key in all_keys}
            writer.writerow(row)

    return str(filepath)


def extract_results(result_data: dict) -> List[Dict[str, Any]]:
    """
    Extract exportable data from tool result.

    Args:
        result_data: Tool result data

    Returns:
        List of items to export
    """
    # Handle different result structures
    if isinstance(result_data, list):
        return result_data

    # Check for common result patterns
    for key in ['animals', 'results', 'data', 'items']:
        if key in result_data and isinstance(result_data[key], list):
            return result_data[key]

    # If result contains animal data directly
    if 'lpn_id' in result_data or 'animal_id' in result_data:
        return [result_data]

    # Check if result has content that looks like it contains the data
    if 'content' in result_data:
        content = result_data['content']
        if isinstance(content, list):
            return content
        elif isinstance(content, dict):
            return extract_results(content)

    return []


def generate_filename(tool_name: str) -> str:
    """
    Generate filename for export.

    Args:
        tool_name: Name of the tool

    Returns:
        Filename with timestamp
    """
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    base_name = tool_name.replace('mcp__nsip__', '').replace('__', '_')
    return f"{base_name}_{timestamp}.csv"


def main():
    """Process PostToolUse hook for CSV export."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_result = hook_data.get("result", {})

        # Check if result is an error
        if tool_result.get("isError", False):
            result = {
                "continue": True,
                "metadata": {
                    "exported": False,
                    "reason": "Error result not exported"
                }
            }
            print(json.dumps(result))
            return

        # Extract data to export
        data_to_export = extract_results(tool_result)

        if not data_to_export:
            result = {
                "continue": True,
                "metadata": {
                    "exported": False,
                    "reason": "No exportable data found"
                }
            }
            print(json.dumps(result))
            return

        # Generate filename and export
        filename = generate_filename(tool_name)
        filepath = export_to_csv(data_to_export, filename)

        result = {
            "continue": True,
            "metadata": {
                "exported": True,
                "filepath": filepath,
                "record_count": len(data_to_export),
                "export_dir": str(get_export_dir())
            }
        }

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "exported": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
