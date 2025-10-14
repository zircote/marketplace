#!/usr/bin/env python3
"""
Breeding Report Hook (PostToolUse)
Generate formatted breeding reports with trait analysis.
Triggers on: mcp__nsip__nsip_get_animal, mcp__nsip__nsip_search_by_lpn
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class BreedingReportGenerator:
    """Generate comprehensive breeding reports in Markdown format."""

    def __init__(self, export_dir: Path = None):
        """
        Initialize report generator.

        Args:
            export_dir: Directory to store reports
        """
        if export_dir is None:
            export_dir = Path.home() / ".claude-code" / "nsip-exports"

        self.export_dir = export_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def _extract_animal_data(self, result: dict) -> Optional[Dict]:
        """
        Extract animal data from tool result.

        Args:
            result: Tool result containing animal information

        Returns:
            Extracted animal data or None if not found
        """
        try:
            # Handle different result formats
            if "content" in result:
                content = result["content"]
                if isinstance(content, list) and len(content) > 0:
                    if isinstance(content[0], dict) and "text" in content[0]:
                        text_data = content[0]["text"]
                        if isinstance(text_data, str):
                            return json.loads(text_data)
                        return text_data
            return result
        except Exception:
            return None

    def _format_basic_info(self, animal: dict) -> str:
        """
        Format basic animal information section.

        Args:
            animal: Animal data dictionary

        Returns:
            Markdown formatted basic info
        """
        lines = []
        lines.append("## Basic Information")
        lines.append("")

        lpn = animal.get("LPN", "Unknown")
        name = animal.get("AnimalName", "Unnamed")
        breed = animal.get("Breed", "Unknown")
        sex = animal.get("Sex", "Unknown")
        birth_date = animal.get("BirthDate", "Unknown")
        status = animal.get("Status", "Unknown")

        lines.append(f"- **LPN ID:** {lpn}")
        lines.append(f"- **Name:** {name}")
        lines.append(f"- **Breed:** {breed}")
        lines.append(f"- **Sex:** {sex}")
        lines.append(f"- **Birth Date:** {birth_date}")
        lines.append(f"- **Status:** {status}")

        # Optional fields
        if "Flock" in animal:
            lines.append(f"- **Flock:** {animal['Flock']}")
        if "Owner" in animal:
            lines.append(f"- **Owner:** {animal['Owner']}")

        return "\n".join(lines)

    def _format_traits(self, animal: dict) -> str:
        """
        Format trait information section.

        Args:
            animal: Animal data dictionary

        Returns:
            Markdown formatted trait info
        """
        lines = []
        lines.append("## Production Traits")
        lines.append("")

        # Common trait fields to look for
        trait_fields = {
            "WWT": "Weaning Weight",
            "PWWT": "Post-Weaning Weight",
            "YWT": "Yearling Weight",
            "FWT": "Final Weight",
            "PEMD": "Parasite Resistance (EMD)",
            "PFEC": "Parasite Resistance (FEC)",
            "NFAT": "Fat Depth",
            "NLEYE": "Eye Muscle Depth",
            "WormResistance": "Worm Resistance",
            "FleeceMeasurements": "Fleece Quality"
        }

        found_traits = False
        for field, label in trait_fields.items():
            if field in animal and animal[field]:
                value = animal[field]
                if isinstance(value, (int, float)):
                    lines.append(f"- **{label}:** {value:.2f}")
                else:
                    lines.append(f"- **{label}:** {value}")
                found_traits = True

        if not found_traits:
            lines.append("*No trait data available*")

        return "\n".join(lines)

    def _format_breeding_values(self, animal: dict) -> str:
        """
        Format breeding value section.

        Args:
            animal: Animal data dictionary

        Returns:
            Markdown formatted breeding values
        """
        lines = []
        lines.append("## Breeding Values (EBVs)")
        lines.append("")

        # Look for EBV-related fields
        ebv_fields = {}
        for key, value in animal.items():
            if "EBV" in key.upper() or "BV" in key.upper():
                ebv_fields[key] = value

        if ebv_fields:
            for field, value in sorted(ebv_fields.items()):
                if isinstance(value, (int, float)):
                    lines.append(f"- **{field}:** {value:.3f}")
                else:
                    lines.append(f"- **{field}:** {value}")
        else:
            lines.append("*No breeding values available*")

        return "\n".join(lines)

    def _format_recommendations(self, animal: dict) -> str:
        """
        Generate breeding recommendations based on data.

        Args:
            animal: Animal data dictionary

        Returns:
            Markdown formatted recommendations
        """
        lines = []
        lines.append("## Breeding Recommendations")
        lines.append("")

        sex = animal.get("Sex", "").upper()
        status = animal.get("Status", "").upper()

        # Basic recommendations based on sex and status
        if sex == "M" or sex == "MALE":
            lines.append("### As a Sire")
            lines.append("- Evaluate progeny performance to confirm genetic merit")
            lines.append("- Consider genetic diversity when selecting mates")
            lines.append("- Monitor for any genetic defects in offspring")

        elif sex == "F" or sex == "FEMALE":
            lines.append("### As a Dam")
            lines.append("- Select complementary sire based on trait weaknesses")
            lines.append("- Monitor reproductive performance over time")
            lines.append("- Track progeny success rates")

        # Status-based recommendations
        if "ACTIVE" in status or "ALIVE" in status:
            lines.append("")
            lines.append("### Management Notes")
            lines.append("- Animal is active in the breeding program")
            lines.append("- Continue regular trait assessments")
            lines.append("- Maintain accurate lineage records")

        # Generic recommendations
        lines.append("")
        lines.append("### General Considerations")
        lines.append("- Compare traits with breed standards")
        lines.append("- Consider environmental factors in trait expression")
        lines.append("- Consult with breeding advisors for specific decisions")

        return "\n".join(lines)

    def generate_report(self, result: dict) -> Optional[str]:
        """
        Generate and save breeding report.

        Args:
            result: Tool result containing animal data

        Returns:
            Report content as string or None if failed
        """
        try:
            animal_data = self._extract_animal_data(result)
            if not animal_data:
                return None

            # Build report
            report_lines = []

            # Title
            animal_name = animal_data.get("AnimalName", "Unnamed")
            lpn = animal_data.get("LPN", "Unknown")
            report_lines.append(f"# Breeding Report: {animal_name} ({lpn})")
            report_lines.append("")
            report_lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

            # Sections
            report_lines.append(self._format_basic_info(animal_data))
            report_lines.append("")
            report_lines.append(self._format_traits(animal_data))
            report_lines.append("")
            report_lines.append(self._format_breeding_values(animal_data))
            report_lines.append("")
            report_lines.append(self._format_recommendations(animal_data))
            report_lines.append("")

            # Footer
            report_lines.append("---")
            report_lines.append("")
            report_lines.append("*This report is generated automatically and should be reviewed by a breeding specialist.*")

            return "\n".join(report_lines)

        except Exception:
            return None

    def save_report(self, report_content: str) -> Optional[str]:
        """
        Save report to file.

        Args:
            report_content: Report content to save

        Returns:
            Path to saved file or None if failed
        """
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"breeding_report_{timestamp}.txt"
            filepath = self.export_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report_content)

            return str(filepath)

        except Exception:
            return None


def main():
    """Process PostToolUse hook for breeding report generation."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_result = hook_data.get("result", {})

        # Only process animal queries
        is_animal_query = any(
            keyword in tool_name.lower()
            for keyword in ["get_animal", "search_by_lpn"]
        )

        if not is_animal_query:
            result = {
                "continue": True,
                "metadata": {"report_generated": False, "reason": "Not an animal query"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Skip if error result
        if tool_result.get("isError", False):
            result = {
                "continue": True,
                "metadata": {"report_generated": False, "reason": "Tool returned error"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Generate report
        generator = BreedingReportGenerator()
        report_content = generator.generate_report(tool_result)

        if report_content:
            filepath = generator.save_report(report_content)
            if filepath:
                result = {
                    "continue": True,
                    "metadata": {
                        "report_generated": True,
                        "export_path": filepath
                    }
                }
            else:
                result = {
                    "continue": True,
                    "metadata": {
                        "report_generated": False,
                        "reason": "Failed to save report"
                    }
                }
        else:
            result = {
                "continue": True,
                "metadata": {
                    "report_generated": False,
                    "reason": "Failed to generate report"
                }
            }

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "report_generated": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
