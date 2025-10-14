"""
Unit Tests for SessionStart Hooks

Tests:
- api_health_check.py
"""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
import urllib.error

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase


class TestAPIHealthCheck(BaseHookTestCase):
    """Test api_health_check.py hook."""

    @unittest.skip("Requires external API - may fail if NSIP API is down")
    def test_health_check_continues_on_success(self):
        """Hook should continue when API is healthy."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Mock successful API response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.read.return_value = json.dumps({
                "LastUpdate": "2025-01-15"
            }).encode('utf-8')
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_urlopen.return_value = mock_response

            result = self.run_hook('api_health_check.py', input_data)

        self.assertHookContinues(result)
        self.assertHookHasMetadata(result, 'health_check')
        self.assertEqual(
            result['output']['metadata']['health_check'],
            'passed'
        )

    def test_health_check_continues_on_failure(self):
        """Hook should continue even when API is down (with warning)."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Mock failed API response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

            result = self.run_hook('api_health_check.py', input_data)

        self.assertHookContinues(result)
        self.assertHookHasMetadata(result, 'health_check')
        self.assertEqual(
            result['output']['metadata']['health_check'],
            'failed'
        )
        self.assertIn('warning', result['output'])

    def test_health_check_handles_http_errors(self):
        """Hook should handle HTTP errors gracefully."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Mock HTTP error
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.HTTPError(
                url='http://test.com',
                code=500,
                msg='Internal Server Error',
                hdrs={},
                fp=None
            )

            result = self.run_hook('api_health_check.py', input_data)

        self.assertHookContinues(result)
        self.assertEqual(
            result['output']['metadata']['health_check'],
            'failed'
        )

    def test_health_check_handles_timeout(self):
        """Hook should handle timeout errors."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Mock timeout
        with patch('urllib.request.urlopen') as mock_urlopen:
            import socket
            mock_urlopen.side_effect = socket.timeout("Request timed out")

            result = self.run_hook('api_health_check.py', input_data)

        self.assertHookContinues(result)
        self.assertEqual(
            result['output']['metadata']['health_check'],
            'failed'
        )

    def test_health_check_includes_timestamp(self):
        """Hook should include timestamp in metadata."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Mock successful API response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.read.return_value = json.dumps({
                "LastUpdate": "2025-01-15"
            }).encode('utf-8')
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_urlopen.return_value = mock_response

            result = self.run_hook('api_health_check.py', input_data)

        self.assertHookContinues(result)
        self.assertIn('timestamp', result['output']['metadata'])

    def test_health_check_handles_malformed_json(self):
        """Hook should handle malformed JSON responses."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Mock malformed response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.read.return_value = b"Not valid JSON"
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_urlopen.return_value = mock_response

            result = self.run_hook('api_health_check.py', input_data)

        # Should continue even with malformed response
        self.assertHookContinues(result)

    def test_health_check_always_exits_zero(self):
        """Hook should always exit with code 0 (fail-safe)."""
        input_data = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        # Test with various error conditions
        error_scenarios = [
            urllib.error.URLError("Connection refused"),
            urllib.error.HTTPError('http://test.com', 404, 'Not Found', {}, None),
            Exception("Unexpected error")
        ]

        for error in error_scenarios:
            with patch('urllib.request.urlopen') as mock_urlopen:
                mock_urlopen.side_effect = error

                result = self.run_hook('api_health_check.py', input_data)

                # Always returns 0
                self.assertEqual(result['returncode'], 0)


if __name__ == '__main__':
    unittest.main()
