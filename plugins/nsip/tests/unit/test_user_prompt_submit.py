"""
Unit Tests for UserPromptSubmit Hooks

Tests:
- smart_search_detector.py
- comparative_analyzer.py
"""

import json
import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase


class TestSmartSearchDetector(BaseHookTestCase):
    """Test smart_search_detector.py hook."""

    def test_detects_single_lpn_id(self):
        """Should detect single LPN ID in prompt."""
        input_data = {
            "prompt": "Show me details for animal 6####92020###249"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        self.assertHookContinues(result)
        self.assertTrue(
            result['output']['metadata']['detection_performed']
        )
        self.assertEqual(
            result['output']['metadata']['ids_detected'],
            1
        )

    def test_detects_multiple_lpn_ids(self):
        """Should detect multiple LPN IDs in prompt."""
        input_data = {
            "prompt": "Compare animals 6####92020###249 and NSWK123456"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        self.assertHookContinues(result)
        self.assertGreaterEqual(
            result['output']['metadata']['ids_detected'],
            2
        )

    def test_detects_lineage_intent(self):
        """Should detect lineage-related queries."""
        lineage_prompts = [
            "Show me the pedigree for 6####92020###249",
            "What are the parents of NSWK123456?",
            "I need to see the family tree for ABC123",
            "Show ancestors of XYZ789"
        ]

        for prompt in lineage_prompts:
            with self.subTest(prompt=prompt):
                input_data = {"prompt": prompt}

                result = self.run_hook('smart_search_detector.py', input_data)

                self.assertHookContinues(result)
                intents = result['output']['metadata'].get('intents', {})
                self.assertTrue(intents.get('get_lineage', False))

    def test_detects_progeny_intent(self):
        """Should detect progeny-related queries."""
        progeny_prompts = [
            "List all offspring of 6####92020###249",
            "Show me the descendants",
            "What children does this animal have?",
            "Get progeny information for ABC123"
        ]

        for prompt in progeny_prompts:
            with self.subTest(prompt=prompt):
                input_data = {"prompt": prompt}

                result = self.run_hook('smart_search_detector.py', input_data)

                self.assertHookContinues(result)
                intents = result['output']['metadata'].get('intents', {})
                self.assertTrue(intents.get('get_progeny', False))

    def test_detects_comparison_intent(self):
        """Should detect comparison queries."""
        comparison_prompts = [
            "Compare 6####92020###249 vs NSWK123456",
            "What's the difference between these two animals?",
            "Show comparison of trait values"
        ]

        for prompt in comparison_prompts:
            with self.subTest(prompt=prompt):
                input_data = {"prompt": prompt}

                result = self.run_hook('smart_search_detector.py', input_data)

                self.assertHookContinues(result)
                intents = result['output']['metadata'].get('intents', {})
                self.assertTrue(intents.get('compare_traits', False))

    def test_detects_trait_analysis_intent(self):
        """Should detect trait analysis queries."""
        trait_prompts = [
            "What are the EBVs for this animal?",
            "Show me breeding values",
            "Analyze wool traits",
            "Check parasite resistance levels",
            "What is the muscle depth?"
        ]

        for prompt in trait_prompts:
            with self.subTest(prompt=prompt):
                input_data = {"prompt": prompt}

                result = self.run_hook('smart_search_detector.py', input_data)

                self.assertHookContinues(result)
                intents = result['output']['metadata'].get('intents', {})
                self.assertTrue(intents.get('trait_analysis', False))

    def test_detects_search_intent(self):
        """Should detect search queries."""
        search_prompts = [
            "Search for Merino sheep with high wool quality",
            "Find animals with good growth rates",
            "Locate sheep from NSW region"
        ]

        for prompt in search_prompts:
            with self.subTest(prompt=prompt):
                input_data = {"prompt": prompt}

                result = self.run_hook('smart_search_detector.py', input_data)

                self.assertHookContinues(result)
                intents = result['output']['metadata'].get('intents', {})
                self.assertTrue(intents.get('search_animal', False))

    def test_provides_suggestions_with_lpn(self):
        """Should provide tool suggestions when LPN detected."""
        input_data = {
            "prompt": "Show me details for animal 6####92020###249"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        self.assertHookContinues(result)
        self.assertHookHasContext(result)

        # Suggestion should mention detected ID
        context = result['output']['context']
        self.assertIn('6####92020###249', context)

    def test_provides_lineage_suggestion(self):
        """Should suggest lineage tool for lineage queries."""
        input_data = {
            "prompt": "Show me the pedigree for 6####92020###249"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        self.assertHookContinues(result)
        self.assertHookHasContext(result)

        context = result['output']['context']
        self.assertIn('lineage', context.lower())

    def test_provides_progeny_suggestion(self):
        """Should suggest progeny tool for progeny queries."""
        input_data = {
            "prompt": "List all offspring of 6####92020###249"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        self.assertHookContinues(result)
        self.assertHookHasContext(result)

        context = result['output']['context']
        self.assertIn('progeny', context.lower())

    def test_handles_empty_prompt(self):
        """Should handle empty prompt gracefully."""
        input_data = {"prompt": ""}

        result = self.run_hook('smart_search_detector.py', input_data)

        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata']['detection_performed']
        )

    def test_handles_non_nsip_prompts(self):
        """Should handle prompts without NSIP content."""
        non_nsip_prompts = [
            "What is the weather today?",
            "Calculate 2 + 2",
            "Write a poem about sheep"
        ]

        for prompt in non_nsip_prompts:
            with self.subTest(prompt=prompt):
                input_data = {"prompt": prompt}

                result = self.run_hook('smart_search_detector.py', input_data)

                self.assertHookContinues(result)

                # Should not detect IDs
                self.assertEqual(
                    result['output']['metadata'].get('ids_detected', 0),
                    0
                )

    def test_logs_detection(self):
        """Should log detected IDs."""
        input_data = {
            "prompt": "Show me details for animal 6####92020###249"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        # Check log file exists
        log_entries = self.env.read_log_file('detected_ids.jsonl')
        self.assertGreater(len(log_entries), 0)

        log_entry = log_entries[0]
        self.assertIn('timestamp', log_entry)
        self.assertIn('detected_ids', log_entry)

    def test_removes_duplicate_ids(self):
        """Should remove duplicate LPN IDs."""
        input_data = {
            "prompt": "Compare 6####92020###249 with 6####92020###249"
        }

        result = self.run_hook('smart_search_detector.py', input_data)

        detected_ids = result['output']['metadata'].get('detected_ids', [])
        # Should only have one unique ID
        self.assertEqual(len(detected_ids), len(set(detected_ids)))

    def test_error_handling(self):
        """Should handle errors gracefully."""
        # Malformed input
        input_data = {"invalid": "data"}

        result = self.run_hook('smart_search_detector.py', input_data)

        # Should continue even on error
        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata'].get('detection_performed', False)
        )


class TestComparativeAnalyzer(BaseHookTestCase):
    """Test comparative_analyzer.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when comparative_analyzer.py exists."""
        pass


if __name__ == '__main__':
    unittest.main()
