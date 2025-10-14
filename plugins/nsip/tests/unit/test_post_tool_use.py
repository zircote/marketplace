"""
Unit Tests for PostToolUse Hooks

Tests:
- auto_retry.py
- fallback_cache.py
- error_notifier.py
- query_logger.py
- result_cache.py
- csv_exporter.py
- pedigree_visualizer.py
- breeding_report.py
"""

import json
import sys
import unittest
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase


class TestAutoRetry(BaseHookTestCase):
    """Test auto_retry.py hook."""

    def test_no_retry_on_success(self):
        """Should not retry on successful result."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": False,
                "content": [
                    {"type": "text", "text": '{"lpn_id": "TEST123"}'}
                ]
            }
        }

        result = self.run_hook('auto_retry.py', input_data)

        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata'].get('retry_needed', False)
        )

    def test_retry_on_error_flag(self):
        """Should detect retry needed when isError is True."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": True,
                "error": "Animal not found",
                "content": []
            }
        }

        result = self.run_hook('auto_retry.py', input_data)

        self.assertHookContinues(result)
        self.assertTrue(
            result['output']['metadata'].get('retry_needed', False)
        )

    def test_retry_on_empty_content(self):
        """Should detect retry needed on empty content."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": False,
                "content": []
            }
        }

        result = self.run_hook('auto_retry.py', input_data)

        self.assertHookContinues(result)
        self.assertTrue(
            result['output']['metadata'].get('retry_needed', False)
        )

    def test_retry_log_created(self):
        """Should create retry log file."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": True,
                "error": "Connection timeout",
                "content": []
            }
        }

        result = self.run_hook('auto_retry.py', input_data)

        # Check log file exists
        log_entries = self.env.read_log_file('retry_log.jsonl')
        self.assertGreater(len(log_entries), 0)

        # Verify log entry structure
        log_entry = log_entries[0]
        self.assertIn('timestamp', log_entry)
        self.assertIn('tool', log_entry)
        self.assertIn('status', log_entry)

    def test_skips_non_nsip_tools(self):
        """Should skip retry for non-NSIP tools."""
        input_data = {
            "tool": {
                "name": "other_tool",
                "parameters": {}
            },
            "result": {
                "isError": True,
                "content": []
            }
        }

        result = self.run_hook('auto_retry.py', input_data)

        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata'].get('retry_handled', False)
        )

    def test_error_handling(self):
        """Should handle errors gracefully."""
        # Malformed input
        input_data = {"invalid": "data"}

        result = self.run_hook('auto_retry.py', input_data)

        # Should continue even on error
        self.assertHookContinues(result)
        self.assertFalse(
            result['output']['metadata'].get('retry_handled', False)
        )


class TestQueryLogger(BaseHookTestCase):
    """Test query_logger.py hook."""

    def test_logs_successful_query(self):
        """Should log successful API calls."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": False,
                "content": [
                    {"type": "text", "text": '{"data": "test"}'}
                ]
            }
        }

        result = self.run_hook('query_logger.py', input_data)

        self.assertHookContinues(result)
        self.assertTrue(result['output']['metadata']['logged'])

        # Verify log file
        log_entries = self.env.read_log_file('query_log.jsonl')
        self.assertEqual(len(log_entries), 1)

        log_entry = log_entries[0]
        self.assertEqual(log_entry['tool'], 'mcp__nsip__nsip_get_animal')
        self.assertTrue(log_entry['success'])

    def test_logs_failed_query(self):
        """Should log failed API calls."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": True,
                "error": "Not found",
                "content": []
            }
        }

        result = self.run_hook('query_logger.py', input_data)

        self.assertHookContinues(result)

        # Verify log file
        log_entries = self.env.read_log_file('query_log.jsonl')
        self.assertEqual(len(log_entries), 1)

        log_entry = log_entries[0]
        self.assertFalse(log_entry['success'])
        self.assertEqual(log_entry['error'], 'Not found')

    def test_includes_result_size(self):
        """Should include result size in log."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "1"}
            },
            "result": {
                "isError": False,
                "content": [
                    {"type": "text", "text": '{"animals": []}'}
                ]
            }
        }

        result = self.run_hook('query_logger.py', input_data)

        # Verify log entry
        log_entries = self.env.read_log_file('query_log.jsonl')
        log_entry = log_entries[0]
        self.assertIn('result_size', log_entry)
        self.assertGreater(log_entry['result_size'], 0)

    def test_includes_timestamp(self):
        """Should include timestamp in log."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123"}
            },
            "result": {
                "isError": False,
                "content": []
            }
        }

        result = self.run_hook('query_logger.py', input_data)

        # Verify timestamp
        log_entries = self.env.read_log_file('query_log.jsonl')
        log_entry = log_entries[0]
        self.assertIn('timestamp', log_entry)

    def test_multiple_queries_append(self):
        """Should append to log file for multiple queries."""
        for i in range(3):
            input_data = {
                "tool": {
                    "name": f"mcp__nsip__nsip_tool_{i}",
                    "parameters": {}
                },
                "result": {
                    "isError": False,
                    "content": []
                }
            }

            self.run_hook('query_logger.py', input_data)

        # Verify all entries logged
        log_entries = self.env.read_log_file('query_log.jsonl')
        self.assertEqual(len(log_entries), 3)

    def test_error_handling(self):
        """Should handle errors gracefully."""
        # Malformed input
        input_data = {"invalid": "data"}

        result = self.run_hook('query_logger.py', input_data)

        # Should continue even on error (and still logs the attempt)
        self.assertHookContinues(result)
        # Query logger logs all inputs, even malformed ones
        self.assertTrue(result['output']['metadata'].get('logged', False),
                       "Query logger should log even malformed inputs for debugging")


class TestResultCache(BaseHookTestCase):
    """Test result_cache.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when result_cache.py exists."""
        pass


class TestFallbackCache(BaseHookTestCase):
    """Test fallback_cache.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when fallback_cache.py exists."""
        pass


class TestErrorNotifier(BaseHookTestCase):
    """Test error_notifier.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when error_notifier.py exists."""
        pass


class TestCSVExporter(BaseHookTestCase):
    """Test csv_exporter.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when csv_exporter.py exists."""
        pass


class TestPedigreeVisualizer(BaseHookTestCase):
    """Test pedigree_visualizer.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when pedigree_visualizer.py exists."""
        pass


class TestBreedingReport(BaseHookTestCase):
    """Test breeding_report.py hook (if exists)."""

    def test_placeholder(self):
        """Placeholder test - implement when breeding_report.py exists."""
        pass


if __name__ == '__main__':
    unittest.main()
