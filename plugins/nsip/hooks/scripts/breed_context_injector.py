#!/usr/bin/env python3
"""
Breed Context Injector Hook (PreToolUse)
Inject breed-specific context before searches and queries.
Triggers on: mcp__nsip__nsip_search_animals, mcp__nsip__nsip_get_trait_ranges
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional


class BreedContextInjector:
    """Inject breed-specific context and characteristics."""

    def __init__(self, cache_dir: Path = None):
        """
        Initialize breed context injector.

        Args:
            cache_dir: Directory to cache breed information
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".claude-code" / "nsip-cache" / "breeds"

        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Static breed information database
        self.breed_data = {
            "1": {
                "name": "Merino",
                "characteristics": "fine wool production, adapted to various climates",
                "key_traits": ["fleece weight", "fiber diameter", "staple length"],
                "breeding_focus": "wool quality and quantity"
            },
            "2": {
                "name": "Border Leicester",
                "characteristics": "maternal breed, good milk production, easy lambing",
                "key_traits": ["maternal ability", "growth rate", "carcass quality"],
                "breeding_focus": "maternal characteristics and lamb growth"
            },
            "3": {
                "name": "Poll Dorset",
                "characteristics": "terminal sire breed, excellent meat production",
                "key_traits": ["growth rate", "muscle depth", "fat depth"],
                "breeding_focus": "meat production and carcass quality"
            },
            "4": {
                "name": "White Suffolk",
                "characteristics": "terminal sire breed, rapid growth, good conformation",
                "key_traits": ["post-weaning weight", "eye muscle depth", "fat depth"],
                "breeding_focus": "meat production and growth rate"
            },
            "5": {
                "name": "Dorper",
                "characteristics": "hair sheep, adapted to harsh conditions, good meat",
                "key_traits": ["weaning weight", "adaptation", "meat quality"],
                "breeding_focus": "adaptability and meat production"
            },
            "6": {
                "name": "Corriedale",
                "characteristics": "dual-purpose breed, wool and meat production",
                "key_traits": ["fleece weight", "body weight", "fiber diameter"],
                "breeding_focus": "balanced wool and meat production"
            }
        }

    def _get_breed_info(self, breed_id: str) -> Optional[Dict]:
        """
        Get breed information from cache or static data.

        Args:
            breed_id: Breed identifier

        Returns:
            Breed information or None if not found
        """
        # Check static data first
        if breed_id in self.breed_data:
            return self.breed_data[breed_id]

        # Check cache for custom breed data
        cache_file = self.cache_dir / f"breed_{breed_id}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        return None

    def _format_breed_context(self, breed_info: Dict) -> str:
        """
        Format breed information as context message.

        Args:
            breed_info: Breed information dictionary

        Returns:
            Formatted context message
        """
        name = breed_info.get("name", "Unknown")
        characteristics = breed_info.get("characteristics", "")
        key_traits = breed_info.get("key_traits", [])
        breeding_focus = breed_info.get("breeding_focus", "")

        context_parts = [
            f"You are working with {name} breed."
        ]

        if characteristics:
            context_parts.append(f"This breed is known for: {characteristics}.")

        if key_traits:
            traits_str = ", ".join(key_traits)
            context_parts.append(f"Key traits to consider: {traits_str}.")

        if breeding_focus:
            context_parts.append(f"Primary breeding focus: {breeding_focus}.")

        return " ".join(context_parts)

    def inject_context(self, parameters: dict) -> Dict:
        """
        Inject breed context based on parameters.

        Args:
            parameters: Tool parameters

        Returns:
            Metadata about context injection
        """
        # Look for breed_id in parameters
        breed_id = None

        # Check various parameter names
        for param_name in ["breed_id", "breedId", "breed", "Breed"]:
            if param_name in parameters:
                breed_id = str(parameters[param_name])
                break

        if not breed_id:
            return {
                "context_injected": False,
                "reason": "No breed_id found in parameters"
            }

        # Get breed information
        breed_info = self._get_breed_info(breed_id)

        if not breed_info:
            return {
                "context_injected": False,
                "reason": f"Breed information not found for breed_id: {breed_id}"
            }

        # Format context message
        context_message = self._format_breed_context(breed_info)

        return {
            "context_injected": True,
            "breed_id": breed_id,
            "breed_name": breed_info.get("name", "Unknown"),
            "context_message": context_message
        }


def main():
    """Process PreToolUse hook for breed context injection."""
    try:
        # Read hook input from stdin
        hook_data = json.loads(sys.stdin.read())

        tool_name = hook_data.get("tool", {}).get("name", "")
        tool_params = hook_data.get("tool", {}).get("parameters", {})

        # Only inject context for relevant tools
        relevant_tools = ["search_animals", "get_trait_ranges"]
        is_relevant = any(tool in tool_name.lower() for tool in relevant_tools)

        if not is_relevant:
            result = {
                "continue": True,
                "metadata": {"context_injected": False, "reason": "Not a relevant tool"}
            }
            print(json.dumps(result))
            sys.exit(0)

        # Inject breed context
        injector = BreedContextInjector()
        inject_metadata = injector.inject_context(tool_params)

        # Build result
        result = {
            "continue": True,
            "metadata": inject_metadata
        }

        # Add context message if injection succeeded
        if inject_metadata.get("context_message"):
            result["context"] = inject_metadata["context_message"]

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
