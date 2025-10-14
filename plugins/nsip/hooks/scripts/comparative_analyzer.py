#!/usr/bin/env python3
"""
Comparative Analyzer Hook (UserPromptSubmit)
Detect multiple animal mentions and suggest comparative analysis.
Triggers on: UserPromptSubmit (all user prompts)
"""

import json
import sys
import re
from datetime import datetime
from typing import List, Dict, Tuple


class ComparativeAnalyzer:
    """Detect comparative analysis opportunities in user prompts."""

    def __init__(self):
        """Initialize comparative analyzer."""
        # Patterns for detecting multiple animals
        self.animal_patterns = [
            r'\b\d{1,4}#{0,10}\d{4,10}#{0,10}\d{1,4}\b',  # e.g., 6####92020###249
            r'\b[A-Z]{2,4}\d{6,10}\b',  # LPN IDs
            r'\b\d{10,15}\b',            # Numeric IDs
        ]

        # Comparison keywords
        self.comparison_keywords = [
            "compare", "comparison", "versus", "vs", "vs.", "v.",
            "better", "worse", "difference", "between",
            "which", "best", "superior", "prefer",
            "against", "relative to", "compared to"
        ]

        # Multiple animal indicators
        self.multiple_indicators = [
            "animals", "sheep", "rams", "ewes",
            "these", "those", "both", "all",
            "multiple", "several", "few", "pair"
        ]

    def _detect_animal_ids(self, text: str) -> List[str]:
        """
        Detect animal ID patterns in text.

        Args:
            text: User prompt text

        Returns:
            List of detected animal IDs
        """
        detected_ids = []

        for pattern in self.animal_patterns:
            matches = re.findall(pattern, text)
            detected_ids.extend(matches)

        # Remove duplicates while preserving order
        seen = set()
        unique_ids = []
        for animal_id in detected_ids:
            if animal_id not in seen:
                seen.add(animal_id)
                unique_ids.append(animal_id)

        return unique_ids

    def _detect_comparison_intent(self, text: str) -> bool:
        """
        Detect if user intends to compare animals.

        Args:
            text: User prompt text

        Returns:
            True if comparison intent detected
        """
        text_lower = text.lower()

        # Check for comparison keywords
        has_comparison_keyword = any(
            keyword in text_lower
            for keyword in self.comparison_keywords
        )

        # Check for multiple animal indicators
        has_multiple_indicator = any(
            indicator in text_lower
            for indicator in self.multiple_indicators
        )

        return has_comparison_keyword or has_multiple_indicator

    def _detect_trait_focus(self, text: str) -> List[str]:
        """
        Detect which traits the user is interested in.

        Args:
            text: User prompt text

        Returns:
            List of detected trait interests
        """
        text_lower = text.lower()

        trait_keywords = {
            "weight": ["weight", "wwt", "pwwt", "ywt"],
            "wool": ["wool", "fleece", "fiber", "micron", "cfw"],
            "meat": ["meat", "muscle", "carcass", "eye muscle", "fat"],
            "parasite": ["parasite", "worm", "fec", "wec", "resistance"],
            "growth": ["growth", "gain", "rate"],
            "reproduction": ["reproduction", "lambing", "fertility", "nlb", "nlw"]
        }

        detected_traits = []
        for trait_category, keywords in trait_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_traits.append(trait_category)

        return detected_traits

    def _build_suggestion_message(
        self,
        animal_count: int,
        animal_ids: List[str],
        has_comparison: bool,
        trait_focus: List[str]
    ) -> str:
        """
        Build context message with comparative analysis suggestions.

        Args:
            animal_count: Number of detected animals
            animal_ids: List of detected animal IDs
            has_comparison: Whether comparison intent detected
            trait_focus: List of trait categories of interest

        Returns:
            Suggestion message
        """
        if animal_count < 2 and not has_comparison:
            return ""

        lines = []

        # Main detection message
        if animal_count >= 2:
            lines.append(
                f"I detected {animal_count} animals in your query: {', '.join(animal_ids)}"
            )
        elif has_comparison:
            lines.append(
                "I detected that you're interested in comparing animals."
            )

        # Suggest comparative workflow
        lines.append("\nSuggested comparative analysis workflow:")

        if animal_ids:
            lines.append("  1. Use nsip_get_animal for each LPN ID to retrieve full details")
        else:
            lines.append("  1. Use nsip_search_animals to find animals matching your criteria")

        # Trait-specific suggestions
        if trait_focus:
            traits_str = ", ".join(trait_focus)
            lines.append(f"  2. Compare {traits_str} traits across the animals")
        else:
            lines.append("  2. Compare key trait values (weights, EBVs, etc.)")

        lines.append("  3. Consider genetic relationships using nsip_get_lineage")
        lines.append("  4. Evaluate breeding complementarity based on strengths/weaknesses")

        # Add trait comparison tips
        lines.append("\nComparison tips:")
        lines.append("  - Look at EBVs (Estimated Breeding Values) for genetic merit")
        lines.append("  - Consider trait accuracy and reliability scores")
        lines.append("  - Evaluate complementarity for breeding pairs")
        lines.append("  - Account for environmental differences in trait expression")

        return "\n".join(lines)

    def analyze_prompt(self, prompt: str) -> Dict:
        """
        Analyze user prompt for comparative analysis opportunities.

        Args:
            prompt: User prompt text

        Returns:
            Analysis metadata
        """
        # Detect animal IDs
        animal_ids = self._detect_animal_ids(prompt)

        # Detect comparison intent
        has_comparison = self._detect_comparison_intent(prompt)

        # Detect trait focus
        trait_focus = self._detect_trait_focus(prompt)

        # Build suggestion message
        suggestion_message = self._build_suggestion_message(
            len(animal_ids),
            animal_ids,
            has_comparison,
            trait_focus
        )

        return {
            "analysis_performed": True,
            "animals_detected": len(animal_ids),
            "animal_ids": animal_ids,
            "comparison_intent": has_comparison,
            "trait_focus": trait_focus,
            "suggestion_message": suggestion_message
        }


def main():
    """Process UserPromptSubmit hook for comparative analysis."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        # Extract user prompt
        prompt = hook_data.get("prompt", "")

        if not prompt:
            result = {
                "continue": True,
                "metadata": {"analysis_performed": False, "reason": "Empty prompt"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Analyze prompt
        analyzer = ComparativeAnalyzer()
        analysis_metadata = analyzer.analyze_prompt(prompt)

        # Only provide suggestions if relevant
        if (analysis_metadata["animals_detected"] < 2 and
            not analysis_metadata["comparison_intent"]):
            result = {
                "continue": True,
                "metadata": {
                    "analysis_performed": True,
                    "comparative_analysis_suggested": False,
                    "reason": "No comparative analysis detected"
                }
            }
            print(json.dumps(result))
            sys.exit(0)

        # Build result
        result = {
            "continue": True,
            "metadata": {
                **analysis_metadata,
                "comparative_analysis_suggested": True
            }
        }

        # Add context message if suggestions were generated
        if analysis_metadata.get("suggestion_message"):
            result["context"] = analysis_metadata["suggestion_message"]

        print(json.dumps(result))

    except Exception as e:
        # On error, continue but report the error
        error_result = {
            "continue": True,
            "metadata": {
                "analysis_performed": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
