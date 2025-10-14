#!/usr/bin/env python3
"""
Trait Dictionary Hook (PreToolUse)
Inject breeding terminology and trait definitions for NSIP queries.
Triggers on: All mcp__nsip__* tools
"""

import json
import sys
from typing import Dict, List, Optional


class TraitDictionary:
    """Provide trait definitions and breeding terminology."""

    def __init__(self):
        """Initialize trait dictionary with NSIP trait definitions."""
        # Common NSIP traits and their definitions
        self.traits = {
            "WWT": {
                "name": "Weaning Weight",
                "description": "Weight of lamb at weaning (typically 100 days)",
                "unit": "kg",
                "typical_range": "15-35 kg",
                "significance": "Indicates early growth performance and maternal ability"
            },
            "PWWT": {
                "name": "Post-Weaning Weight",
                "description": "Weight gain after weaning period",
                "unit": "kg",
                "typical_range": "40-70 kg",
                "significance": "Reflects growth potential and feed efficiency"
            },
            "YWT": {
                "name": "Yearling Weight",
                "description": "Weight at approximately 12 months of age",
                "unit": "kg",
                "typical_range": "50-90 kg",
                "significance": "Indicator of mature size and growth rate"
            },
            "PEMD": {
                "name": "Post-Weaning Eye Muscle Depth",
                "description": "Ultrasound measurement of loin muscle",
                "unit": "mm",
                "typical_range": "20-40 mm",
                "significance": "Indicator of meat yield and carcass quality"
            },
            "PFAT": {
                "name": "Post-Weaning Fat Depth",
                "description": "Ultrasound measurement of fat over loin",
                "unit": "mm",
                "typical_range": "2-8 mm",
                "significance": "Important for meat quality and finish"
            },
            "FEC": {
                "name": "Faecal Egg Count",
                "description": "Parasite resistance measure (worm eggs in feces)",
                "unit": "eggs per gram",
                "typical_range": "0-2000 epg",
                "significance": "Lower values indicate better parasite resistance"
            },
            "WEC": {
                "name": "Worm Egg Count",
                "description": "Measure of internal parasite burden",
                "unit": "eggs per gram",
                "typical_range": "0-2000 epg",
                "significance": "Key indicator of animal health and resilience"
            },
            "CFW": {
                "name": "Clean Fleece Weight",
                "description": "Weight of wool after washing",
                "unit": "kg",
                "typical_range": "2-8 kg",
                "significance": "Primary wool production measure"
            },
            "FD": {
                "name": "Fiber Diameter",
                "description": "Average wool fiber thickness (micron)",
                "unit": "microns",
                "typical_range": "15-25 microns",
                "significance": "Determines wool quality and price"
            },
            "SS": {
                "name": "Staple Strength",
                "description": "Measure of wool fiber strength",
                "unit": "N/ktex",
                "typical_range": "25-45 N/ktex",
                "significance": "Important for processing and yarn quality"
            },
            "SL": {
                "name": "Staple Length",
                "description": "Length of wool staple",
                "unit": "mm",
                "typical_range": "60-120 mm",
                "significance": "Affects processing and wool type"
            },
            "NLB": {
                "name": "Number of Lambs Born",
                "description": "Reproductive trait - lambs born per ewe",
                "unit": "count",
                "typical_range": "1-3",
                "significance": "Key reproductive performance indicator"
            },
            "NLW": {
                "name": "Number of Lambs Weaned",
                "description": "Lambs successfully raised to weaning",
                "unit": "count",
                "typical_range": "1-2.5",
                "significance": "Measures maternal ability and lamb survival"
            }
        }

        # Breeding terminology
        self.terminology = {
            "EBV": "Estimated Breeding Value - genetic prediction of an animal's performance",
            "ASB": "Australian Sheep Breeding Value - standardized genetic evaluation",
            "Sire": "Male parent",
            "Dam": "Female parent",
            "Progeny": "Offspring",
            "Pedigree": "Family tree/lineage",
            "LPN": "Livestock Production Number - unique animal identifier",
            "Flock": "Group of sheep managed together",
            "Selection Index": "Weighted combination of multiple traits for breeding decisions"
        }

    def _detect_mentioned_traits(self, parameters: dict) -> List[str]:
        """
        Detect which traits are mentioned in parameters.

        Args:
            parameters: Tool parameters

        Returns:
            List of detected trait codes
        """
        detected = []

        # Convert parameters to string for searching
        param_str = json.dumps(parameters, default=str).upper()

        for trait_code in self.traits.keys():
            if trait_code in param_str:
                detected.append(trait_code)

        return detected

    def _format_trait_info(self, trait_code: str) -> str:
        """
        Format trait information as readable text.

        Args:
            trait_code: Trait code (e.g., 'WWT')

        Returns:
            Formatted trait information
        """
        trait = self.traits.get(trait_code, {})

        parts = [
            f"{trait_code} ({trait.get('name', 'Unknown')}): {trait.get('description', '')}"
        ]

        if trait.get("typical_range"):
            parts.append(f"Typical range: {trait['typical_range']}")

        if trait.get("significance"):
            parts.append(f"Significance: {trait['significance']}")

        return ". ".join(parts)

    def _build_context_message(self, detected_traits: List[str]) -> str:
        """
        Build context message with trait definitions.

        Args:
            detected_traits: List of detected trait codes

        Returns:
            Context message
        """
        lines = ["NSIP Trait Reference:"]

        if detected_traits:
            lines.append("\nRelevant traits in your query:")
            for trait_code in detected_traits[:5]:  # Limit to 5
                lines.append(f"  - {self._format_trait_info(trait_code)}")
        else:
            # Provide general overview if no specific traits detected
            lines.append("\nCommon NSIP traits:")
            common_traits = ["WWT", "PWWT", "PEMD", "FEC", "CFW"]
            for trait_code in common_traits:
                if trait_code in self.traits:
                    trait = self.traits[trait_code]
                    lines.append(f"  - {trait_code}: {trait.get('name', 'Unknown')}")

        # Add terminology section
        lines.append("\nKey terminology:")
        for term, definition in list(self.terminology.items())[:3]:  # First 3
            lines.append(f"  - {term}: {definition}")

        return "\n".join(lines)

    def generate_context(self, parameters: dict) -> Dict:
        """
        Generate trait context for the query.

        Args:
            parameters: Tool parameters

        Returns:
            Metadata about context generation
        """
        # Detect mentioned traits
        detected_traits = self._detect_mentioned_traits(parameters)

        # Build context message
        context_message = self._build_context_message(detected_traits)

        return {
            "context_injected": True,
            "detected_traits": detected_traits,
            "total_traits_available": len(self.traits),
            "context_message": context_message
        }


def main():
    """Process PreToolUse hook for trait dictionary."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_params = hook_data.get("tool", {}).get("parameters", {})

        # Only process NSIP tools
        if not tool_name.startswith("mcp__nsip__"):
            result = {
                "continue": True,
                "metadata": {"context_injected": False, "reason": "Not an NSIP tool"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Generate trait context
        dictionary = TraitDictionary()
        context_metadata = dictionary.generate_context(tool_params)

        # Build result
        result = {
            "continue": True,
            "metadata": context_metadata
        }

        # Add context message
        if context_metadata.get("context_message"):
            result["context"] = context_metadata["context_message"]

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "context_injected": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
