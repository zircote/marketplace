"""
Pytest Configuration and Shared Fixtures

Provides test environment setup, cleanup, and common fixtures for all tests.
"""

import json
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
import unittest


class TestEnvironment:
    """
    Test environment manager for isolated hook testing.

    Creates temporary directories mimicking ~/.claude-code/ structure
    and provides helper methods for running hooks.
    """

    def __init__(self):
        """Initialize test environment."""
        self.temp_dir = None
        self.claude_code_dir = None
        self.nsip_logs_dir = None
        self.nsip_cache_dir = None
        self.nsip_exports_dir = None
        self.hooks_dir = None

    def setup(self):
        """Create temporary test environment."""
        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp(prefix="nsip_test_"))

        # Create mock ~/.claude-code/ structure
        self.claude_code_dir = self.temp_dir / ".claude-code"
        self.claude_code_dir.mkdir(parents=True)

        # Create subdirectories
        self.nsip_logs_dir = self.claude_code_dir / "nsip-logs"
        self.nsip_logs_dir.mkdir(parents=True)

        self.nsip_cache_dir = self.claude_code_dir / "nsip-cache"
        self.nsip_cache_dir.mkdir(parents=True)

        self.nsip_exports_dir = self.claude_code_dir / "nsip-exports"
        self.nsip_exports_dir.mkdir(parents=True)

        # Get hooks directory
        self.hooks_dir = Path(__file__).parent.parent / "hooks" / "scripts"

        return self

    def teardown(self):
        """Clean up temporary test environment."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def get_hook_path(self, hook_name: str) -> Path:
        """
        Get path to hook script.

        Args:
            hook_name: Name of hook script (e.g., 'lpn_validator.py')

        Returns:
            Path to hook script
        """
        return self.hooks_dir / hook_name

    def mock_home_dir(self) -> str:
        """
        Get temporary home directory for mocking.

        Returns:
            Path to temporary directory
        """
        return str(self.temp_dir)

    def get_log_file(self, filename: str) -> Path:
        """
        Get path to log file.

        Args:
            filename: Log filename (e.g., 'query_log.jsonl')

        Returns:
            Path to log file
        """
        return self.nsip_logs_dir / filename

    def get_cache_file(self, filename: str) -> Path:
        """
        Get path to cache file.

        Args:
            filename: Cache filename

        Returns:
            Path to cache file
        """
        return self.nsip_cache_dir / filename

    def get_export_file(self, filename: str) -> Path:
        """
        Get path to export file.

        Args:
            filename: Export filename

        Returns:
            Path to export file
        """
        return self.nsip_exports_dir / filename

    def read_log_file(self, filename: str) -> list:
        """
        Read JSONL log file.

        Args:
            filename: Log filename

        Returns:
            List of parsed JSON objects
        """
        log_file = self.get_log_file(filename)

        if not log_file.exists():
            return []

        entries = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))

        return entries

    def read_cache_file(self, filename: str) -> Dict[str, Any]:
        """
        Read JSON cache file.

        Args:
            filename: Cache filename

        Returns:
            Parsed JSON object
        """
        cache_file = self.get_cache_file(filename)

        if not cache_file.exists():
            return {}

        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)


class BaseHookTestCase(unittest.TestCase):
    """
    Base test case for hook testing with common setup/teardown.

    Provides helper methods for running hooks and asserting results.
    """

    def setUp(self):
        """Set up test environment before each test."""
        self.env = TestEnvironment()
        self.env.setup()

        # Store original HOME to restore later
        self.original_home = os.environ.get('HOME')

        # Mock HOME directory for hooks
        os.environ['HOME'] = self.env.mock_home_dir()

    def tearDown(self):
        """Clean up test environment after each test."""
        # Restore original HOME
        if self.original_home:
            os.environ['HOME'] = self.original_home
        else:
            os.environ.pop('HOME', None)

        # Clean up test environment
        self.env.teardown()

    def run_hook(self, hook_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a hook script with given input.

        Args:
            hook_name: Name of hook script (e.g., 'lpn_validator.py')
            input_data: Input data to pass to hook via stdin

        Returns:
            Dictionary with 'returncode', 'stdout', 'stderr', 'output'
        """
        import subprocess

        hook_path = self.env.get_hook_path(hook_name)

        # Run hook with input
        proc = subprocess.run(
            ['python3', str(hook_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True
        )

        # Parse output
        output = None
        if proc.stdout:
            try:
                output = json.loads(proc.stdout)
            except json.JSONDecodeError:
                pass

        return {
            'returncode': proc.returncode,
            'stdout': proc.stdout,
            'stderr': proc.stderr,
            'output': output
        }

    def assertHookSuccess(self, result: Dict[str, Any], msg: str = None):
        """
        Assert hook executed successfully.

        Args:
            result: Result from run_hook()
            msg: Optional assertion message
        """
        self.assertEqual(result['returncode'], 0, msg or "Hook should exit with code 0")
        self.assertIsNotNone(result['output'], msg or "Hook should output valid JSON")

    def assertHookContinues(self, result: Dict[str, Any], msg: str = None):
        """
        Assert hook allows continuation.

        Args:
            result: Result from run_hook()
            msg: Optional assertion message
        """
        self.assertHookSuccess(result, msg)
        self.assertTrue(
            result['output'].get('continue', True),
            msg or "Hook should allow continuation"
        )

    def assertHookBlocks(self, result: Dict[str, Any], msg: str = None):
        """
        Assert hook blocks continuation.

        Args:
            result: Result from run_hook()
            msg: Optional assertion message
        """
        self.assertHookSuccess(result, msg)
        self.assertFalse(
            result['output'].get('continue', True),
            msg or "Hook should block continuation"
        )

    def assertHookHasMetadata(self, result: Dict[str, Any], key: str, msg: str = None):
        """
        Assert hook output contains metadata key.

        Args:
            result: Result from run_hook()
            key: Metadata key to check
            msg: Optional assertion message
        """
        self.assertHookSuccess(result, msg)
        self.assertIn(
            key,
            result['output'].get('metadata', {}),
            msg or f"Hook metadata should contain '{key}'"
        )

    def assertHookHasError(self, result: Dict[str, Any], msg: str = None):
        """
        Assert hook output contains error.

        Args:
            result: Result from run_hook()
            msg: Optional assertion message
        """
        self.assertHookSuccess(result, msg)
        self.assertIn(
            'error',
            result['output'],
            msg or "Hook output should contain error"
        )

    def assertHookHasContext(self, result: Dict[str, Any], msg: str = None):
        """
        Assert hook output contains context message.

        Args:
            result: Result from run_hook()
            msg: Optional assertion message
        """
        self.assertHookSuccess(result, msg)
        self.assertIn(
            'context',
            result['output'],
            msg or "Hook output should contain context message"
        )
