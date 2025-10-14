#!/usr/bin/env python3
"""
Smart Search Detector Hook (UserPromptSubmit)
Detect LPN IDs in user prompts and suggest appropriate tools.
Triggers on: UserPromptSubmit (all user prompts)
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class SmartSearchDetector:
    """Detect patterns in user prompts and suggest NSIP tools."""

    def __init__(self, log_dir: Path = None):
        """
        Initialize smart search detector.

        Args:
            log_dir: Directory to store detection logs
        """
        if log_dir is None:
            log_dir = Path.home() / ".claude-code" / "nsip-logs"

        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "detected_ids.jsonl"

        # LPN ID patterns (common formats)
        self.lpn_patterns = [
            r'\b\d{1,4}#{0,10}\d{4,10}#{0,10}\d{1,4}\b',  # e.g., 6####92020###249
            r'\b[A-Z]{2,4}\d{6,10}\b',  # e.g., NSWK123456
            r'\b\d{10,15}\b',            # e.g., 621879202000024
            r'\bLPN[:\s-]?([A-Z0-9#]+)\b',  # e.g., LPN:ABC123 or LPN:6####92020###249
        ]

    def _log_detection(self, log_entry: dict):
        """
        Log detected IDs to JSONL file.

        Args:
            log_entry: Log entry to append
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass

    def _detect_lpn_ids(self, text: str) -> List[str]:
        """
        Detect LPN ID patterns in text.

        Args:
            text: User prompt text

        Returns:
            List of detected LPN IDs
        """
        detected_ids = []

        for pattern in self.lpn_patterns:
            matches = re.findall(pattern, text)
            detected_ids.extend(matches)

        # Remove duplicates while preserving order
        seen = set()
        unique_ids = []
        for lpn_id in detected_ids:
            if lpn_id not in seen:
                seen.add(lpn_id)
                unique_ids.append(lpn_id)

        return unique_ids

    def _detect_query_intent(self, text: str) -> Dict[str, bool]:
        """
        Detect user's query intent from text.

        Args:
            text: User prompt text

        Returns:
            Dictionary of detected intents
        """
        text_lower = text.lower()

        intents = {
            "search_animal": any(
                keyword in text_lower
                for keyword in ["search", "find", "look for", "locate"]
            ),
            "get_lineage": any(
                keyword in text_lower
                for keyword in ["lineage", "pedigree", "parents", "ancestors", "family"]
            ),
            "get_progeny": any(
                keyword in text_lower
                for keyword in ["progeny", "offspring", "children", "descendants"]
            ),
            "compare_traits": any(
                keyword in text_lower
                for keyword in ["compare", "comparison", "versus", "vs", "difference"]
            ),
            "trait_analysis": any(
                keyword in text_lower
                for keyword in [
                    "trait", "ebv", "breeding value", "weight", "wool",
                    "parasite", "resistance", "muscle", "fat"
                ]
            )
        }

        return intents

    def _build_suggestion_message(
        self,
        detected_ids: List[str],
        intents: Dict[str, bool]
    ) -> str:
        """
        Build context message with suggestions.

        Args:
            detected_ids: List of detected LPN IDs
            intents: Detected query intents

        Returns:
            Suggestion message
        """
        lines = []

        # LPN ID detection
        if detected_ids:
            if len(detected_ids) == 1:
                lines.append(f"I detected an LPN ID in your query: {detected_ids[0]}")
            else:
                ids_str = ", ".join(detected_ids)
                lines.append(f"I detected multiple LPN IDs in your query: {ids_str}")

        # Intent-based suggestions
        suggestions = []

        if detected_ids:
            if intents.get("get_lineage"):
                suggestions.append(
                    "Use nsip_get_lineage to explore ancestry and pedigree"
                )
            elif intents.get("get_progeny"):
                suggestions.append(
                    "Use nsip_get_progeny to view offspring and descendants"
                )
            elif intents.get("compare_traits") and len(detected_ids) > 1:
                suggestions.append(
                    "Use nsip_get_animal for each ID, then compare their trait values"
                )
            else:
                # Default suggestion
                if len(detected_ids) == 1:
                    suggestions.append(
                        "Consider using nsip_get_animal or nsip_search_by_lpn to retrieve full details"
                    )
                else:
                    suggestions.append(
                        "Consider using nsip_get_animal for each ID to retrieve full details"
                    )

        if intents.get("trait_analysis") and not detected_ids:
            suggestions.append(
                "Use nsip_search_animals to find animals with specific trait criteria"
            )

        # Build final message
        if suggestions:
            lines.append("\nSuggested NSIP tools:")
            for i, suggestion in enumerate(suggestions, 1):
                lines.append(f"  {i}. {suggestion}")

        return "\n".join(lines) if lines else ""

    def analyze_prompt(self, prompt: str) -> Dict:
        """
        Analyze user prompt for LPN IDs and intent.

        Args:
            prompt: User prompt text

        Returns:
            Analysis metadata
        """
        # Detect LPN IDs
        detected_ids = self._detect_lpn_ids(prompt)

        # Detect query intent
        intents = self._detect_query_intent(prompt)

        # Log detection
        if detected_ids or any(intents.values()):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "detected_ids": detected_ids,
                "intents": {k: v for k, v in intents.items() if v},
                "prompt_length": len(prompt)
            }
            self._log_detection(log_entry)

        # Build suggestion message
        suggestion_message = self._build_suggestion_message(detected_ids, intents)

        return {
            "detection_performed": True,
            "ids_detected": len(detected_ids),
            "detected_ids": detected_ids,
            "intents": intents,
            "suggestion_message": suggestion_message
        }


def main():
    """Process UserPromptSubmit hook for smart search detection."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        # Extract user prompt
        prompt = hook_data.get("prompt", "")

        if not prompt:
            result = {
                "continue": True,
                "metadata": {"detection_performed": False, "reason": "Empty prompt"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Analyze prompt
        detector = SmartSearchDetector()
        analysis_metadata = detector.analyze_prompt(prompt)

        # Build result
        result = {
            "continue": True,
            "metadata": analysis_metadata
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
                "detection_performed": False,
                "error": str(e)
            }
        }
        print(json.dumps(error_result))

    sys.exit(0)


if __name__ == "__main__":
    main()
