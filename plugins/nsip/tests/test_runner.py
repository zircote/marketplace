#!/usr/bin/env python3
"""
NSIP Plugin Test Runner

Standalone test runner for the NSIP Claude Code plugin hooks.
Runs all tests and generates coverage reports.

Usage:
    python test_runner.py                    # Run all tests
    python test_runner.py --unit             # Run unit tests only
    python test_runner.py --integration      # Run integration tests only
    python test_runner.py --hook lpn_validator  # Test specific hook
    python test_runner.py --verbose          # Verbose output
    python test_runner.py --json output.json # JSON output
"""

import argparse
import json
import sys
import time
import unittest
from pathlib import Path
from io import StringIO
from typing import Dict, List, Any


class TestStatistics:
    """Collect and format test statistics."""

    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        self.skipped_tests = 0
        self.start_time = None
        self.end_time = None
        self.failures = []
        self.errors = []

    def start(self):
        """Start timing."""
        self.start_time = time.time()

    def finish(self):
        """Finish timing."""
        self.end_time = time.time()

    def duration(self) -> float:
        """Get test duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

    def add_result(self, result: unittest.TestResult):
        """Add results from a test run."""
        self.total_tests += result.testsRun
        self.failed_tests += len(result.failures)
        self.error_tests += len(result.errors)
        self.skipped_tests += len(result.skipped)
        self.passed_tests = self.total_tests - self.failed_tests - self.error_tests - self.skipped_tests

        self.failures.extend(result.failures)
        self.errors.extend(result.errors)

    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary."""
        return {
            'total': self.total_tests,
            'passed': self.passed_tests,
            'failed': self.failed_tests,
            'errors': self.error_tests,
            'skipped': self.skipped_tests,
            'success_rate': self.success_rate(),
            'duration': self.duration(),
            'failures': [
                {
                    'test': str(test),
                    'traceback': traceback
                }
                for test, traceback in self.failures
            ],
            'errors': [
                {
                    'test': str(test),
                    'traceback': traceback
                }
                for test, traceback in self.errors
            ]
        }

    def print_summary(self):
        """Print summary to console."""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests:    {self.total_tests}")
        print(f"Passed:         {self.passed_tests} ✓")
        print(f"Failed:         {self.failed_tests} ✗")
        print(f"Errors:         {self.error_tests} !")
        print(f"Skipped:        {self.skipped_tests} -")
        print(f"Success Rate:   {self.success_rate():.1f}%")
        print(f"Duration:       {self.duration():.2f}s")
        print("=" * 70)

        if self.failed_tests > 0:
            print("\nFAILURES:")
            for test, traceback in self.failures:
                print(f"\n{test}")
                print(traceback)

        if self.error_tests > 0:
            print("\nERRORS:")
            for test, traceback in self.errors:
                print(f"\n{test}")
                print(traceback)


class TestRunner:
    """Main test runner."""

    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.stats = TestStatistics()

    def discover_tests(self, pattern: str = "test_*.py", start_dir: str = None) -> unittest.TestSuite:
        """
        Discover tests matching pattern.

        Args:
            pattern: Test file pattern
            start_dir: Directory to start discovery

        Returns:
            Test suite
        """
        if start_dir is None:
            start_dir = str(self.test_dir)

        loader = unittest.TestLoader()
        suite = loader.discover(start_dir, pattern=pattern)
        return suite

    def run_tests(self, suite: unittest.TestSuite, verbose: bool = False) -> unittest.TestResult:
        """
        Run test suite.

        Args:
            suite: Test suite to run
            verbose: Verbose output

        Returns:
            Test result
        """
        verbosity = 2 if verbose else 1
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        return result

    def run_unit_tests(self, verbose: bool = False) -> unittest.TestResult:
        """Run unit tests only."""
        print("\n" + "=" * 70)
        print("RUNNING UNIT TESTS")
        print("=" * 70)

        unit_dir = str(self.test_dir / "unit")
        suite = self.discover_tests(start_dir=unit_dir)
        return self.run_tests(suite, verbose)

    def run_integration_tests(self, verbose: bool = False) -> unittest.TestResult:
        """Run integration tests only."""
        print("\n" + "=" * 70)
        print("RUNNING INTEGRATION TESTS")
        print("=" * 70)

        integration_dir = str(self.test_dir / "integration")
        suite = self.discover_tests(start_dir=integration_dir)
        return self.run_tests(suite, verbose)

    def run_hook_tests(self, hook_name: str, verbose: bool = False) -> unittest.TestResult:
        """Run tests for specific hook."""
        print("\n" + "=" * 70)
        print(f"RUNNING TESTS FOR: {hook_name}")
        print("=" * 70)

        # Map hook names to test files
        hook_test_map = {
            'api_health_check': 'test_session_start.py',
            'lpn_validator': 'test_pre_tool_use.py',
            'breed_context_injector': 'test_pre_tool_use.py',
            'auto_retry': 'test_post_tool_use.py',
            'query_logger': 'test_post_tool_use.py',
            'smart_search_detector': 'test_user_prompt_submit.py',
        }

        test_file = hook_test_map.get(hook_name)
        if not test_file:
            print(f"Unknown hook: {hook_name}")
            return unittest.TestResult()

        suite = self.discover_tests(pattern=test_file)
        return self.run_tests(suite, verbose)

    def run_all_tests(self, verbose: bool = False) -> List[unittest.TestResult]:
        """Run all tests."""
        print("\n" + "=" * 70)
        print("NSIP PLUGIN TEST SUITE")
        print("=" * 70)

        results = []

        # Run unit tests
        result = self.run_unit_tests(verbose)
        results.append(result)

        # Run integration tests
        result = self.run_integration_tests(verbose)
        results.append(result)

        return results

    def generate_json_report(self, output_file: str):
        """Generate JSON test report."""
        report = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'statistics': self.stats.to_dict(),
            'test_directory': str(self.test_dir),
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"\nJSON report written to: {output_file}")

    def generate_coverage_report(self):
        """Generate coverage report (placeholder)."""
        print("\n" + "=" * 70)
        print("COVERAGE REPORT")
        print("=" * 70)
        print("Note: Coverage analysis requires the 'coverage' package.")
        print("Install with: pip install coverage")
        print("Run with: coverage run test_runner.py && coverage report")
        print("=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='NSIP Plugin Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py                           # Run all tests
  python test_runner.py --unit                    # Unit tests only
  python test_runner.py --integration             # Integration tests only
  python test_runner.py --hook lpn_validator      # Specific hook
  python test_runner.py --verbose                 # Verbose output
  python test_runner.py --json report.json        # JSON output
        """
    )

    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run unit tests only'
    )

    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run integration tests only'
    )

    parser.add_argument(
        '--hook',
        type=str,
        metavar='HOOK_NAME',
        help='Run tests for specific hook'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--json',
        type=str,
        metavar='FILE',
        help='Generate JSON report'
    )

    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Show coverage information'
    )

    args = parser.parse_args()

    # Create test runner
    runner = TestRunner()
    runner.stats.start()

    # Run tests based on arguments
    results = []

    if args.hook:
        result = runner.run_hook_tests(args.hook, args.verbose)
        results.append(result)
    elif args.unit:
        result = runner.run_unit_tests(args.verbose)
        results.append(result)
    elif args.integration:
        result = runner.run_integration_tests(args.verbose)
        results.append(result)
    else:
        results = runner.run_all_tests(args.verbose)

    # Collect statistics
    runner.stats.finish()
    for result in results:
        runner.stats.add_result(result)

    # Print summary
    runner.stats.print_summary()

    # Generate JSON report
    if args.json:
        runner.generate_json_report(args.json)

    # Show coverage info
    if args.coverage:
        runner.generate_coverage_report()

    # Exit with appropriate code
    if runner.stats.failed_tests > 0 or runner.stats.error_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
