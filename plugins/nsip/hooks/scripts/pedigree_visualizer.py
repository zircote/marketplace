#!/usr/bin/env python3
"""
Pedigree Visualizer Hook (PostToolUse)
Generate visual family tree diagrams from lineage data.
Triggers on: mcp__nsip__nsip_get_lineage
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PedigreeVisualizer:
    """Generate ASCII and text-based pedigree visualizations."""

    def __init__(self, export_dir: Path = None):
        """
        Initialize visualizer.

        Args:
            export_dir: Directory to store pedigree exports
        """
        if export_dir is None:
            export_dir = Path.home() / ".claude-code" / "nsip-exports"

        self.export_dir = export_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def _extract_lineage_data(self, result: dict) -> Optional[Dict]:
        """
        Extract lineage data from tool result.

        Args:
            result: Tool result containing lineage information

        Returns:
            Extracted lineage data or None if not found
        """
        try:
            # Handle different result formats
            if "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    if isinstance(content[0], dict) and "text" in content[0]:
                        # Parse JSON from text content
                        text_data = content[0]["text"]
                        if isinstance(text_data, str):
                            return json.loads(text_data)
                        return text_data
            return result
        except Exception:
            return None

    def _format_animal_info(self, animal: dict) -> str:
        """
        Format animal information for display.

        Args:
            animal: Animal data dictionary

        Returns:
            Formatted animal string
        """
        lpn = animal.get("LPN", "Unknown")
        name = animal.get("AnimalName", "Unnamed")
        breed = animal.get("Breed", "")

        if breed:
            return f"{name} ({lpn}) [{breed}]"
        return f"{name} ({lpn})"

    def _generate_ascii_tree(self, lineage: dict) -> str:
        """
        Generate ASCII art family tree.

        Args:
            lineage: Lineage data dictionary

        Returns:
            ASCII tree representation
        """
        lines = []
        lines.append("=" * 80)
        lines.append("PEDIGREE VISUALIZATION")
        lines.append("=" * 80)
        lines.append("")

        # Subject animal
        subject = lineage.get("subject", {})
        if subject:
            lines.append("Subject Animal:")
            lines.append(f"  {self._format_animal_info(subject)}")
            lines.append("")

        # Parents (Generation 1)
        sire = lineage.get("sire", {})
        dam = lineage.get("dam", {})

        if sire or dam:
            lines.append("Parents (Generation 1):")
            if sire:
                lines.append(f"  Sire:  {self._format_animal_info(sire)}")
            else:
                lines.append("  Sire:  Unknown")

            if dam:
                lines.append(f"  Dam:   {self._format_animal_info(dam)}")
            else:
                lines.append("  Dam:   Unknown")
            lines.append("")

        # Grandparents (Generation 2)
        grandparents = lineage.get("grandparents", {})
        if grandparents:
            lines.append("Grandparents (Generation 2):")

            sire_sire = grandparents.get("sire_sire", {})
            sire_dam = grandparents.get("sire_dam", {})
            dam_sire = grandparents.get("dam_sire", {})
            dam_dam = grandparents.get("dam_dam", {})

            if sire_sire or sire_dam:
                lines.append("  Paternal:")
                if sire_sire:
                    lines.append(f"    Sire: {self._format_animal_info(sire_sire)}")
                if sire_dam:
                    lines.append(f"    Dam:  {self._format_animal_info(sire_dam)}")

            if dam_sire or dam_dam:
                lines.append("  Maternal:")
                if dam_sire:
                    lines.append(f"    Sire: {self._format_animal_info(dam_sire)}")
                if dam_dam:
                    lines.append(f"    Dam:  {self._format_animal_info(dam_dam)}")
            lines.append("")

        # Generation summary
        total_ancestors = 0
        if sire or dam:
            total_ancestors += sum([bool(sire), bool(dam)])
        if grandparents:
            total_ancestors += sum([
                bool(grandparents.get("sire_sire")),
                bool(grandparents.get("sire_dam")),
                bool(grandparents.get("dam_sire")),
                bool(grandparents.get("dam_dam"))
            ])

        lines.append(f"Total Ancestors Identified: {total_ancestors}")
        lines.append("=" * 80)

        return "\n".join(lines)

    def _generate_simple_hierarchy(self, lineage: dict) -> str:
        """
        Generate simple text hierarchy.

        Args:
            lineage: Lineage data dictionary

        Returns:
            Hierarchical text representation
        """
        lines = []
        lines.append("LINEAGE HIERARCHY")
        lines.append("")

        subject = lineage.get("subject", {})
        if subject:
            lines.append(f"└─ {self._format_animal_info(subject)}")

            sire = lineage.get("sire", {})
            dam = lineage.get("dam", {})

            if sire:
                lines.append(f"   ├─ SIRE: {self._format_animal_info(sire)}")

                grandparents = lineage.get("grandparents", {})
                if grandparents:
                    sire_sire = grandparents.get("sire_sire", {})
                    sire_dam = grandparents.get("sire_dam", {})

                    if sire_sire:
                        lines.append(f"   │  ├─ {self._format_animal_info(sire_sire)}")
                    if sire_dam:
                        lines.append(f"   │  └─ {self._format_animal_info(sire_dam)}")

            if dam:
                lines.append(f"   └─ DAM:  {self._format_animal_info(dam)}")

                grandparents = lineage.get("grandparents", {})
                if grandparents:
                    dam_sire = grandparents.get("dam_sire", {})
                    dam_dam = grandparents.get("dam_dam", {})

                    if dam_sire:
                        lines.append(f"      ├─ {self._format_animal_info(dam_sire)}")
                    if dam_dam:
                        lines.append(f"      └─ {self._format_animal_info(dam_dam)}")

        return "\n".join(lines)

    def visualize_and_save(self, result: dict) -> Optional[str]:
        """
        Generate and save pedigree visualization.

        Args:
            result: Tool result containing lineage data

        Returns:
            Path to saved file or None if failed
        """
        try:
            lineage_data = self._extract_lineage_data(result)
            if not lineage_data:
                return None

            # Generate visualizations
            ascii_tree = self._generate_ascii_tree(lineage_data)
            hierarchy = self._generate_simple_hierarchy(lineage_data)

            # Combine both formats
            output = f"{ascii_tree}\n\n{hierarchy}\n"

            # Add metadata
            output += f"\nGenerated: {datetime.utcnow().isoformat()}Z\n"

            # Save to file
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"pedigree_{timestamp}.txt"
            filepath = self.export_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output)

            return str(filepath)

        except Exception:
            return None


def main():
    """Process PostToolUse hook for pedigree visualization."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_result = hook_data.get("result", {})

        # Only process lineage queries
        if "get_lineage" not in tool_name.lower():
            result = {
                "continue": True,
                "metadata": {"pedigree_generated": False, "reason": "Not a lineage query"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Skip if error result
        if tool_result.get("isError", False):
            result = {
                "continue": True,
                "metadata": {"pedigree_generated": False, "reason": "Tool returned error"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Generate visualization
        visualizer = PedigreeVisualizer()
        filepath = visualizer.visualize_and_save(tool_result)

        if filepath:
            result = {
                "continue": True,
                "metadata": {
                    "pedigree_generated": True,
                    "export_path": filepath
                }
            }
        else:
            result = {
                "continue": True,
                "metadata": {
                    "pedigree_generated": False,
                    "reason": "Failed to generate visualization"
                }
            }

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "pedigree_generated": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
