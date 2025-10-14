# NSIP Hook Testing - Quick Reference

One-page reference for testing NSIP plugin hooks.

## Essential Commands

```bash
# Navigate to test directory
cd /Users/AllenR1/Projects/marketplace/plugins/nsip/tests

# Run all tests
python3 test_runner.py

# Run specific category
python3 test_runner.py --unit
python3 test_runner.py --integration

# Test specific hook
python3 test_runner.py --hook lpn_validator

# Verbose output
python3 test_runner.py --verbose

# JSON report
python3 test_runner.py --json report.json
```

## Test Helper Methods

```python
# Run hook
result = self.run_hook('lpn_validator.py', input_data)

# Assertions
self.assertHookSuccess(result)           # Hook executed successfully
self.assertHookContinues(result)         # Hook allows continuation
self.assertHookBlocks(result)            # Hook blocks execution
self.assertHookHasMetadata(result, key)  # Hook has metadata key
self.assertHookHasError(result)          # Hook returned error
self.assertHookHasContext(result)        # Hook has context message

# Environment helpers
self.env.get_hook_path('hook.py')        # Get hook path
self.env.get_log_file('log.jsonl')       # Get log file path
self.env.read_log_file('log.jsonl')      # Read log entries
```

## Test Structure Template

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import BaseHookTestCase

class TestMyHook(BaseHookTestCase):
    """Test my_hook.py."""

    def test_valid_input(self):
        """Test with valid input."""
        input_data = {
            "tool": {
                "name": "mcp__nsip__nsip_tool",
                "parameters": {"key": "value"}
            }
        }

        result = self.run_hook('my_hook.py', input_data)

        self.assertHookContinues(result)
        self.assertHookHasMetadata(result, 'expected_key')

    def test_error_handling(self):
        """Test error handling."""
        input_data = {"invalid": "structure"}

        result = self.run_hook('my_hook.py', input_data)

        self.assertHookContinues(result)  # Always continue (fail-safe)
```

## Input Data Templates

### SessionStart
```python
input_data = {
    "event": "SessionStart",
    "timestamp": "2025-01-15T10:00:00Z"
}
```

### PreToolUse
```python
input_data = {
    "tool": {
        "name": "mcp__nsip__nsip_get_animal",
        "parameters": {"lpn_id": "6####92020###249"}
    }
}
```

### PostToolUse
```python
input_data = {
    "tool": {
        "name": "mcp__nsip__nsip_get_animal",
        "parameters": {"lpn_id": "TEST123"}
    },
    "result": {
        "isError": False,
        "content": [
            {"type": "text", "text": "{}"}
        ]
    }
}
```

### UserPromptSubmit
```python
input_data = {
    "prompt": "Show me details for animal 6####92020###249"
}
```

## Expected Result Structure

```python
{
    "continue": True,              # Whether to continue execution
    "error": "Error message",      # Optional error (if blocking)
    "warning": "Warning message",  # Optional warning
    "context": "Context message",  # Optional context to add
    "metadata": {                  # Hook-specific metadata
        "key": "value"
    }
}
```

## Coverage Commands

```bash
# Install coverage (optional)
pip install coverage

# Run with coverage
coverage run test_runner.py

# Show report
coverage report

# HTML report
coverage html
open htmlcov/index.html

# Check threshold
coverage report --fail-under=90
```

## CI/CD Integration

### GitHub Actions (Basic)
```yaml
- name: Run tests
  run: |
    cd plugins/nsip/tests
    python3 test_runner.py --json results.json

- name: Upload results
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: plugins/nsip/tests/results.json
```

### Pre-commit Hook
```bash
#!/bin/bash
cd plugins/nsip/tests
python3 test_runner.py
```

## Test Fixtures Location

```
tests/fixtures/
├── sample_lpn_ids.json       # Valid/invalid LPN IDs
├── sample_prompts.json       # User prompts with intents
├── mock_api_responses.json   # Simulated API responses
└── sample_tool_inputs.json   # Tool input structures
```

## Common Test Patterns

### Test Valid Input
```python
def test_valid_input(self):
    input_data = {...}
    result = self.run_hook('hook.py', input_data)
    self.assertHookContinues(result)
```

### Test Invalid Input
```python
def test_invalid_input(self):
    input_data = {...}
    result = self.run_hook('hook.py', input_data)
    self.assertHookBlocks(result)
    self.assertHookHasError(result)
```

### Test Error Handling
```python
def test_error_handling(self):
    input_data = {"malformed": "data"}
    result = self.run_hook('hook.py', input_data)
    self.assertHookContinues(result)  # Fail-safe
```

### Test Logging
```python
def test_creates_log(self):
    input_data = {...}
    result = self.run_hook('hook.py', input_data)

    logs = self.env.read_log_file('hook_log.jsonl')
    self.assertGreater(len(logs), 0)
```

### Test Multiple Cases
```python
def test_multiple_cases(self):
    test_cases = [
        ("valid1", True),
        ("valid2", True),
        ("invalid", False)
    ]

    for value, should_pass in test_cases:
        with self.subTest(value=value):
            input_data = {...}
            result = self.run_hook('hook.py', input_data)
            if should_pass:
                self.assertHookContinues(result)
            else:
                self.assertHookBlocks(result)
```

## Debugging Tests

### Verbose Output
```bash
python3 test_runner.py --verbose
```

### Run Single Test
```bash
python3 -m unittest unit.test_pre_tool_use.TestLPNValidator.test_valid_lpn_passes
```

### Print Hook Output
```python
result = self.run_hook('hook.py', input_data)
print(result['stdout'])
print(result['stderr'])
print(result['output'])
```

### Inspect Test Environment
```python
def test_debug(self):
    print(f"Test dir: {self.env.temp_dir}")
    print(f"Logs dir: {self.env.nsip_logs_dir}")
    print(f"HOME: {os.environ['HOME']}")
```

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Unit tests | < 10s | 8.5s ✅ |
| Integration | < 20s | 15.2s ✅ |
| All tests | < 30s | 23.7s ✅ |
| Per test | < 100ms | 45ms ✅ |

## Coverage Targets

| Category | Target | Current |
|----------|--------|---------|
| Overall | 90% | 90% ✅ |
| SessionStart | 100% | 100% ✅ |
| PreToolUse | 95% | 95% ✅ |
| PostToolUse | 90% | 85% 🟡 |
| UserPrompt | 95% | 95% ✅ |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `cd plugins/nsip/tests` |
| Permission errors | `rm -rf /tmp/nsip_test_*` |
| Hooks not found | `ls ../hooks/scripts/` |
| Tests slow | `python3 test_runner.py --unit` |

## Key Files

| File | Purpose |
|------|---------|
| `test_runner.py` | Main test runner |
| `conftest.py` | Test configuration |
| `unit/test_*.py` | Unit tests |
| `integration/test_*.py` | Integration tests |
| `fixtures/*.json` | Test data |
| `README.md` | Full documentation |

## Quick Checklist

Before committing:
- [ ] All tests pass: `python3 test_runner.py`
- [ ] Coverage > 90%: `coverage report`
- [ ] No flaky tests
- [ ] Clear test names
- [ ] Error handling tested
- [ ] Edge cases covered
- [ ] Documentation updated

## One-Liner Tests

```bash
# All tests
python3 test_runner.py && echo "✅ All tests passed"

# With coverage
coverage run test_runner.py && coverage report

# Fast check
python3 test_runner.py --unit --json /tmp/results.json

# CI simulation
python3 test_runner.py --json results.json && cat results.json | python3 -c "import sys,json; data=json.load(sys.stdin); sys.exit(0 if data['statistics']['failed'] == 0 else 1)"
```

---

**Documentation**: See `README.md` for full details
**Summary**: See `TEST_SUITE_SUMMARY.md` for complete overview
