"""
Integration Tests for Hook Workflows

Tests complete hook execution chains and interactions.
"""

import json
import sys
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase


class TestToolCallLifecycle(BaseHookTestCase):
    """Test complete tool call lifecycle with multiple hooks."""

    def test_complete_get_animal_workflow(self):
        """Test PreToolUse -> Tool Call -> PostToolUse workflow."""

        # Step 1: PreToolUse - LPN Validation
        pre_input = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "6####92020###249"}
            }
        }

        pre_result = self.run_hook('lpn_validator.py', pre_input)
        self.assertHookContinues(pre_result)

        # Step 2: Simulate API call result
        post_input = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "6####92020###249"}
            },
            "result": {
                "isError": False,
                "content": [
                    {
                        "type": "text",
                        "text": '{"lpn_id": "6####92020###249", "name": "Test Animal"}'
                    }
                ]
            }
        }

        # Step 3: PostToolUse - Query Logger
        post_result = self.run_hook('query_logger.py', post_input)
        self.assertHookContinues(post_result)

        # Verify logging occurred
        log_entries = self.env.read_log_file('query_log.jsonl')
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0]['tool'], 'mcp__nsip__nsip_get_animal')

    def test_search_workflow_with_context_injection(self):
        """Test search workflow with breed context injection."""

        # Step 1: PreToolUse - Breed Context Injector
        pre_input = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "1"}
            }
        }

        pre_result = self.run_hook('breed_context_injector.py', pre_input)
        self.assertHookContinues(pre_result)
        self.assertTrue(
            pre_result['output']['metadata']['context_injected']
        )

        # Step 2: PostToolUse - Query Logger
        post_input = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "1"}
            },
            "result": {
                "isError": False,
                "content": [
                    {"type": "text", "text": '[{"lpn_id": "A1"}]'}
                ]
            }
        }

        post_result = self.run_hook('query_logger.py', post_input)
        self.assertHookContinues(post_result)

    def test_invalid_lpn_blocks_execution(self):
        """Test that invalid LPN blocks execution early."""

        # PreToolUse with invalid LPN
        pre_input = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "abc"}
            }
        }

        pre_result = self.run_hook('lpn_validator.py', pre_input)
        self.assertHookBlocks(pre_result)
        self.assertHookHasError(pre_result)

        # In real execution, PostToolUse hooks would not run
        # because the tool call was blocked


class TestErrorResilienceFlow(BaseHookTestCase):
    """Test error handling and resilience workflows."""

    def test_retry_then_log_workflow(self):
        """Test auto-retry followed by logging."""

        # Step 1: PostToolUse - Auto Retry (on failure)
        retry_input = {
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

        retry_result = self.run_hook('auto_retry.py', retry_input)
        self.assertHookContinues(retry_result)
        self.assertTrue(
            retry_result['output']['metadata'].get('retry_needed', False)
        )

        # Verify retry log
        retry_log = self.env.read_log_file('retry_log.jsonl')
        self.assertGreater(len(retry_log), 0)

        # Step 2: PostToolUse - Query Logger (logs the failure)
        logger_result = self.run_hook('query_logger.py', retry_input)
        self.assertHookContinues(logger_result)

        # Verify query log
        query_log = self.env.read_log_file('query_log.jsonl')
        self.assertEqual(len(query_log), 1)
        self.assertFalse(query_log[0]['success'])

    def test_multiple_failures_tracked(self):
        """Test that multiple failures are properly tracked."""

        # Simulate multiple failed calls
        for i in range(3):
            input_data = {
                "tool": {
                    "name": "mcp__nsip__nsip_get_animal",
                    "parameters": {"lpn_id": f"TEST{i}"}
                },
                "result": {
                    "isError": True,
                    "error": "Connection error",
                    "content": []
                }
            }

            # Run through retry handler
            retry_result = self.run_hook('auto_retry.py', input_data)
            self.assertHookContinues(retry_result)

            # Run through logger
            logger_result = self.run_hook('query_logger.py', input_data)
            self.assertHookContinues(logger_result)

        # Verify all failures logged
        retry_log = self.env.read_log_file('retry_log.jsonl')
        query_log = self.env.read_log_file('query_log.jsonl')

        self.assertGreater(len(retry_log), 0)
        self.assertEqual(len(query_log), 3)


class TestPromptToToolWorkflow(BaseHookTestCase):
    """Test UserPromptSubmit to tool execution workflows."""

    def test_prompt_detection_to_tool_call(self):
        """Test prompt detection suggesting appropriate tools."""

        # Step 1: UserPromptSubmit - Smart Search Detector
        prompt_input = {
            "prompt": "Show me details for animal 6####92020###249"
        }

        detector_result = self.run_hook('smart_search_detector.py', prompt_input)
        self.assertHookContinues(detector_result)
        self.assertHookHasContext(detector_result)

        detected_ids = detector_result['output']['metadata'].get('detected_ids', [])
        self.assertGreater(len(detected_ids), 0)

        # Step 2: Simulate user acting on suggestion - PreToolUse
        lpn_id = detected_ids[0] if detected_ids else "6####92020###249"
        tool_input = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": lpn_id}
            }
        }

        validator_result = self.run_hook('lpn_validator.py', tool_input)
        self.assertHookContinues(validator_result)

    def test_lineage_prompt_workflow(self):
        """Test lineage prompt detection to lineage tool."""

        # Step 1: Detect lineage intent
        prompt_input = {
            "prompt": "Show me the pedigree for 6####92020###249"
        }

        detector_result = self.run_hook('smart_search_detector.py', prompt_input)
        self.assertHookContinues(detector_result)

        intents = detector_result['output']['metadata'].get('intents', {})
        self.assertTrue(intents.get('get_lineage', False))

        # Suggestion should mention lineage
        context = detector_result['output'].get('context', '')
        self.assertIn('lineage', context.lower())

    def test_comparison_prompt_workflow(self):
        """Test comparison prompt detection."""

        # Step 1: Detect comparison intent with multiple IDs
        prompt_input = {
            "prompt": "Compare animals 6####92020###249 and NSWK123456"
        }

        detector_result = self.run_hook('smart_search_detector.py', prompt_input)
        self.assertHookContinues(detector_result)

        # Should detect multiple IDs
        ids_detected = detector_result['output']['metadata'].get('ids_detected', 0)
        self.assertGreaterEqual(ids_detected, 2)

        # Should detect comparison intent
        intents = detector_result['output']['metadata'].get('intents', {})
        self.assertTrue(intents.get('compare_traits', False))


class TestMultiHookInteraction(BaseHookTestCase):
    """Test interactions between multiple hooks."""

    def test_all_hooks_execute_independently(self):
        """Test that hooks can all execute without interference."""

        # Prepare inputs
        session_input = {
            "event": "SessionStart",
            "timestamp": "2025-01-15T10:00:00Z"
        }

        pre_input = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "1"}
            }
        }

        post_input = {
            "tool": {
                "name": "mcp__nsip__nsip_search_animals",
                "parameters": {"breed_id": "1"}
            },
            "result": {
                "isError": False,
                "content": [{"type": "text", "text": "[]"}]
            }
        }

        prompt_input = {
            "prompt": "Search for Merino sheep"
        }

        # Execute all hook types - they should all succeed independently
        breed_result = self.run_hook('breed_context_injector.py', pre_input)
        self.assertHookContinues(breed_result)

        logger_result = self.run_hook('query_logger.py', post_input)
        self.assertHookContinues(logger_result)

        detector_result = self.run_hook('smart_search_detector.py', prompt_input)
        self.assertHookContinues(detector_result)

        # All hooks should complete successfully and not interfere with each other

    def test_hooks_share_filesystem_safely(self):
        """Test that hooks can safely share log/cache directories."""

        # Multiple hooks writing to different files
        log_input = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST1"}
            },
            "result": {"isError": False, "content": []}
        }

        retry_input = {
            "tool": {
                "name": "mcp__nsip__nsip_get_animal",
                "parameters": {"lpn_id": "TEST2"}
            },
            "result": {"isError": True, "content": []}
        }

        prompt_input = {
            "prompt": "Test prompt with 6####92020###249"
        }

        # Execute hooks that write to different files
        self.run_hook('query_logger.py', log_input)
        self.run_hook('auto_retry.py', retry_input)
        self.run_hook('smart_search_detector.py', prompt_input)

        # Verify all files exist independently
        query_log = self.env.read_log_file('query_log.jsonl')
        retry_log = self.env.read_log_file('retry_log.jsonl')
        detected_log = self.env.read_log_file('detected_ids.jsonl')

        self.assertGreater(len(query_log), 0, "Query log should contain entries")
        self.assertGreater(len(retry_log), 0, "Retry log should contain entries")
        self.assertGreater(len(detected_log), 0, "Detection log should contain entries")


if __name__ == '__main__':
    unittest.main()
