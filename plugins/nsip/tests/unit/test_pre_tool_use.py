"""
Unit Tests for PreToolUse Hooks

Tests:
- lpn_validator.py
- breed_context_injector.py
- trait_dictionary.py
"""

import json
import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase


class TestLPNValidator(BaseHookTestCase):
    """Test lpn_validator.py hook."""

    def test_valid_lpn_passes(self):
        """Valid LPN IDs should pass validation."""
        valid_ids = [
            "6####92020###249",
            "NSWK123456",
            "1234567890",
            "ABC-12345",
            "XYZ_98765",
            "12345#6789"
        ]

        for lpn_id in valid_ids:
            with self.subTest(lpn_id=lpn_id):
                input_data = {
                    "tool": {
                        "name": "mcp__nsip__nsip_get_animal",
                        "parameters": {"lpn_id": lpn_id}
                    }
                }

                result = self.run_hook('lpn_validator.py', input_data)

                self.assertHookContinues(result, f"LPN {lpn_id} should be valid")
                self.assertEqual(
                    result['output']['metadata']['validation'],
                    'passed'
                )

    def test_invalid_lpn_blocks(self):
        """Invalid LPN IDs should block execution."""
        invalid_ids = [
            ("", "empty string"),
            ("abc", "too short"),
            ("123", "too short"),
            ("X", "too short"),
            ("!@#$%", "invalid characters"),
            ("ID WITH SPACES", "contains spaces"),
            ("invalid@chars", "invalid @ character")
        ]

        for lpn_id, reason in invalid_ids:
            with self.subTest(lpn_id=lpn_id, reason=reason):
                input_data = {
                    "tool": {
                        "name": "mcp__nsip__nsip_get_animal",
                        "parameters": {"lpn_id": lpn_id}
                    }
                }

                result = self.run_hook('lpn_validator.py', input_data)

                self.assertHookBlocks(result, f"LPN {lpn_id} should be invalid: {reason}")
                self.assertHookHasError(result)
                self.assertEqual(
                    result['output']['metadata']['validation'],
                    'failed'
                )

    def test_no_lpn_parameter_skips_validation(self):
        """Tools without LPN parameters should skip validation."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_list_breeds",
                "parameters": {}
            }
        }

        result = self.run_hook('lpn_validator.py', input_data)

        self.assertHookContinues(result)
        self.assertEqual(
            result['output']['metadata']['validation'],
            'skipped'
        )

    def test_lpn_length_validation(self):
        """LPN IDs should meet length requirements."""
        # Too short
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "1234"}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        self.assertHookBlocks(result)

        # Too long (over 50 characters)
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "X" * 51}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        self.assertHookBlocks(result)

        # Just right
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "12345"}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        self.assertHookContinues(result)

    def test_lpn_alternative_parameter_names(self):
        """Should validate LPN in alternative parameter names."""
        parameter_names = ["lpn_id", "animal_id", "id"]

        for param_name in parameter_names:
            with self.subTest(param_name=param_name):
                input_data = {
                    "tool": {
                        "name": "mcp__nsip__nsip_get_animal",
                        "parameters": {param_name: "VALID12345"}
                    }
                }

                result = self.run_hook('lpn_validator.py', input_data)
                self.assertHookContinues(result)

    def test_lpn_whitespace_handling(self):
        """Should handle whitespace in LPN IDs."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "  VALID12345  "}
            }
        }

        result = self.run_hook('lpn_validator.py', input_data)
        # Should trim whitespace and pass
        self.assertHookContinues(result)

    def test_lpn_error_handling(self):
        """Should handle errors gracefully and continue."""
        # Malformed input - missing tool/parameters structure
        input_data = {"invalid": "structure"}

        result = self.run_hook('lpn_validator.py', input_data)

        # Should continue even on error (validation skipped)
        self.assertHookContinues(result)
        self.assertEqual(
            result['output']['metadata']['validation'],
            'skipped',
            "Validator should skip when no LPN parameter found"
        )
        self.assertIn('reason', result['output']['metadata'])


class TestBreedContextInjector(BaseHookTestCase):
    """Test breed_context_injector.py hook."""

    def test_injects_context_for_known_breeds(self):
        """Should inject context for known breed IDs."""
        known_breeds = {
            "1": "Merino",
            "2": "Border Leicester",
            "3": "Poll Dorset",
            "4": "White Suffolk",
            "5": "Dorper",
            "6": "Corriedale"
        }

        for breed_id, breed_name in known_breeds.items():
            with self.subTest(breed_id=breed_id, breed_name=breed_name):
                input_data = {
                    "tool": {
                        "name": "mcp__nsip__nsip_search_animals",
                        "parameters": {"breed_id": breed_id}
                    }
                }

                result = self.run_hook('breed_context_injector.py', input_data)

                self.assertHookContinues(result)
                self.assertTrue(
                    result['output']['metadata']['context_injected']
                )
                self.assertEqual(
                    result['output']['metadata']['breed_name'],
                    breed_name
                )
                self.assertHookHasContext(result)

    def test_skips_irrelevant_tools(self):
        """Should skip context injection for non-search tools."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"breed_id": "1"}
            }
        }

        result = self.run_hook('breed_context_injector.py', input_data)

        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata']['context_injected']
        )

    def test_handles_missing_breed_id(self):
        """Should handle tools without breed_id parameter."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {}
            }
        }

        result = self.run_hook('breed_context_injector.py', input_data)

        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata']['context_injected']
        )

    def test_handles_unknown_breed_id(self):
        """Should handle unknown breed IDs gracefully."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "999"}
            }
        }

        result = self.run_hook('breed_context_injector.py', input_data)

        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata']['context_injected']
        )

    def test_context_message_format(self):
        """Context message should be well-formatted."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "1"}
            }
        }

        result = self.run_hook('breed_context_injector.py', input_data)

        context = result['output'].get('context', '')

        # Should mention breed name
        self.assertIn('Merino', context)

        # Should have breeding focus
        self.assertIn('breeding focus', context.lower())

    def test_alternative_breed_parameter_names(self):
        """Should recognize alternative breed parameter names."""
        parameter_variants = ["breed_id", "breedId", "breed", "Breed"]

        for param_name in parameter_variants:
            with self.subTest(param_name=param_name):
                input_data = {
                    "tool": {
                        "name": "mcp__nsip__nsip_search_animals",
                        "parameters": {param_name: "1"}
                    }
                }

                result = self.run_hook('breed_context_injector.py', input_data)

                # Should recognize the parameter
                if param_name in ["breed_id", "breedId", "breed", "Breed"]:
                    self.assertTrue(
                        result['output']['metadata']['context_injected']
                    )

    def test_error_handling(self):
        """Should handle errors gracefully."""
        # Malformed input
        input_data = {"invalid": "data"}

        result = self.run_hook('breed_context_injector.py', input_data)

        # Should continue even on error
        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata']['context_injected']
        )


class TestTraitDictionary(BaseHookTestCase):
    """Test trait_dictionary.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when trait_dictionary.py exists."""
        # This hook might not be implemented yet
        # Add tests when the hook is created
        pass


if __name__ == '__main__':
    unittest.main()
