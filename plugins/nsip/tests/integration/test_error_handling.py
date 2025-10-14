"""
Integration Tests for Error Handling

Tests resilience, edge cases, and error recovery across hooks.
"""

import json
import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase


class TestHookFailSafety(BaseHookTestCase):
    """Test that all hooks are fail-safe and never break execution."""

    def test_all_hooks_exit_zero(self):
        """All hooks should always exit with code 0."""

        hooks = [
            'lpn_validator.py',
            'breed_context_injector.py',
            'auto_retry.py',
            'query_logger.py',
            'smart_search_detector.py'
        ]

        # Test with malformed input
        malformed_inputs = [
            {},
            {"invalid": "structure"},
            {"tool": None},
            {"tool": {"name": None}},
            None,
        ]

        for hook in hooks:
            for input_data in malformed_inputs:
                with self.subTest(hook=hook, input=input_data):
                    # Some inputs might cause JSON decode errors
                    # which is acceptable - test with empty input instead
                    if input_data is None:
                        continue

                    result = self.run_hook(hook, input_data)

                    # All hooks should exit 0
                    self.assertEqual(
                        result['returncode'],
                        0,
                        f"{hook} should exit 0 even with malformed input"
                    )

    def test_hooks_continue_on_internal_errors(self):
        """Hooks should continue even when they encounter internal errors."""

        # Test LPN validator with missing parameters
        input_data = {"tool": {"name": "test", "parameters": None}}
        result = self.run_hook('lpn_validator.py', input_data)
        self.assertHookContinues(result)

        # Test breed injector with invalid structure
        input_data = {"tool": None}
        result = self.run_hook('breed_context_injector.py', input_data)
        self.assertHookContinues(result)

        # Test query logger with no result
        input_data = {"tool": {"name": "test"}}
        result = self.run_hook('query_logger.py', input_data)
        self.assertHookContinues(result)

    def test_hooks_handle_missing_stdin(self):
        """Hooks should handle missing or empty stdin gracefully."""
        import subprocess

        hooks = [
            'lpn_validator.py',
            'breed_context_injector.py',
            'query_logger.py'
        ]

        for hook in hooks:
            with self.subTest(hook=hook):
                hook_path = self.env.get_hook_path(hook)

                # Run with empty stdin
                proc = subprocess.run(
                    ['python3', str(hook_path)],
                    input='',
                    capture_output=True,
                    text=True
                )

                # Should exit 0 (fail-safe)
                self.assertEqual(proc.returncode, 0)


class TestEdgeCases(BaseHookTestCase):
    """Test edge cases and boundary conditions."""

    def test_empty_strings(self):
        """Test hooks with empty string values."""

        # LPN validator with empty LPN
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": ""}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        self.assertHookBlocks(result)

        # Smart detector with empty prompt
        input_data = {"prompt": ""}
        result = self.run_hook('smart_search_detector.py', input_data)
        self.assertHookContinues(result)

    def test_very_long_inputs(self):
        """Test hooks with very long input values."""

        # Very long LPN (should be rejected)
        long_lpn = "X" * 100
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": long_lpn}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        self.assertHookBlocks(result)

        # Very long prompt (should handle gracefully)
        long_prompt = "Search for animal " + "X" * 10000
        input_data = {"prompt": long_prompt}
        result = self.run_hook('smart_search_detector.py', input_data)
        self.assertHookContinues(result)

    def test_unicode_handling(self):
        """Test hooks with unicode characters."""

        # Unicode in LPN
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST123🐑"}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        # Should reject (invalid characters)
        self.assertHookBlocks(result)

        # Unicode in prompt (should handle)
        input_data = {"prompt": "Show me sheep 🐑 with ID TEST123"}
        result = self.run_hook('smart_search_detector.py', input_data)
        self.assertHookContinues(result)

    def test_special_characters(self):
        """Test hooks with special characters."""

        special_chars = [
            "ID<script>alert('xss')</script>",
            "ID'; DROP TABLE animals; --",
            "ID\n\r\t",
            "ID\\x00\\x01",
        ]

        for lpn_id in special_chars:
            with self.subTest(lpn_id=lpn_id):
                input_data = {
                    "tool": {
                        "name": "mcp__nsip__nsip_get_animal",
                        "parameters": {"lpn_id": lpn_id}
                    }
                }
                result = self.run_hook('lpn_validator.py', input_data)

                # Should handle gracefully (likely block)
                self.assertHookSuccess(result)

    def test_null_values(self):
        """Test hooks with null values."""

        # Null LPN
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": None}
            }
        }
        result = self.run_hook('lpn_validator.py', input_data)
        # Should handle gracefully
        self.assertHookSuccess(result)

        # Null prompt
        input_data = {"prompt": None}
        result = self.run_hook('smart_search_detector.py', input_data)
        self.assertHookSuccess(result)


class TestConcurrentExecution(BaseHookTestCase):
    """Test concurrent hook execution scenarios."""

    def test_concurrent_logging(self):
        """Test that concurrent hooks can log safely."""
        import threading

        results = []

        def run_logger(i):
            input_data = {
                "tool": {
                    "name": f"mcp__nsip__nsip_tool_{i}",
                    "parameters": {}
                },
                "result": {"isError": False, "content": []}
            }
            result = self.run_hook('query_logger.py', input_data)
            results.append(result)

        # Run multiple hooks concurrently
        threads = []
        for i in range(5):
            t = threading.Thread(target=run_logger, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # All should succeed
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertHookContinues(result)

        # Verify all entries logged
        log_entries = self.env.read_log_file('query_log.jsonl')
        self.assertEqual(len(log_entries), 5)


class TestResourceLimits(BaseHookTestCase):
    """Test hooks under resource constraints."""

    def test_disk_space_handling(self):
        """Test hooks when disk space might be limited."""
        # This is hard to test without actually filling the disk
        # Just verify hooks handle write errors gracefully

        # Write many log entries
        for i in range(100):
            input_data = {
                "tool": {
                    "name": f"mcp__nsip__nsip_tool_{i}",
                    "parameters": {}
                },
                "result": {"isError": False, "content": []}
            }
            result = self.run_hook('query_logger.py', input_data)
            self.assertHookContinues(result)

    def test_large_result_handling(self):
        """Test hooks with very large results."""

        # Create large result
        large_content = "X" * 100000
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {}
            },
            "result": {
                "isError": False,
                "content": [
                    {"type": "text", "text": large_content}
                ]
            }
        }

        result = self.run_hook('query_logger.py', input_data)
        self.assertHookContinues(result)

        # Verify it was logged
        log_entries = self.env.read_log_file('query_log.jsonl')
        self.assertGreater(len(log_entries), 0)
        self.assertGreater(log_entries[0]['result_size'], 100000)


class TestPermissionHandling(BaseHookTestCase):
    """Test hooks with permission issues."""

    def test_readonly_log_directory(self):
        """Test hooks when log directory is read-only."""
        import os
        import stat

        # Make log directory read-only
        log_dir = self.env.nsip_logs_dir
        original_mode = log_dir.stat().st_mode

        try:
            # Remove write permissions
            log_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)

            input_data = {
                "tool": {
                    "name": "mcp__nsip__nsip_get_animal",
                    "parameters": {}
                },
                "result": {"isError": False, "content": []}
            }

            result = self.run_hook('query_logger.py', input_data)

            # Should continue even if logging fails
            self.assertHookContinues(result)

        finally:
            # Restore permissions
            log_dir.chmod(original_mode)


if __name__ == '__main__':
    unittest.main()
