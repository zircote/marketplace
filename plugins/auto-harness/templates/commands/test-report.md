---
name: test-report
description: Generate test execution report in various formats
arguments:
  - name: format
    description: Output format (markdown, html, json)
    required: false
  - name: output
    description: Output file path (defaults to stdout)
    required: false
---

# Generate Test Report

Create a comprehensive report of test execution results.

## Report Generation

<step name="check-state">
Verify test state exists:

```bash
if [[ ! -f ".claude/test-state.json" ]]; then
  echo "No test results found. Run /run-tests first."
  exit 1
fi
```
</step>

<step name="generate-report">
Call the runner to generate the report:

```bash
"./tests/functional/runner.sh" report {{#if format}}--format {{format}}{{/if}}
```
</step>

<step name="output-report">
If output path specified, write to file:

```bash
"./tests/functional/runner.sh" report --format {{format}} > {{output}}
```

Otherwise, display in conversation.
</step>

## Report Formats

### Markdown (default)

```markdown
# Test Execution Report

**Generated:** 2024-01-20T15:30:00Z
**Duration:** 5m 23s

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Passed | 48 | 90.6% |
| ❌ Failed | 3 | 5.7% |
| ⏭️ Skipped | 2 | 3.8% |
| **Total** | **53** | **100%** |

## Failed Tests

### search_empty
**Category:** search
**Description:** Search with no results returns empty message

**Expected:**
- contains: "no results"

**Actual Response:**
> Found 0 matches for query

**Failure:** Missing 'no results'

---

### crud_update_invalid
**Category:** crud
**Description:** Update with invalid ID returns error

**Expected:**
- contains: "error"
- contains: "not found"

**Actual Response:**
> Update failed: ID format invalid

**Failure:** Missing 'not found'

## Passed Tests

<details>
<summary>48 tests passed (click to expand)</summary>

- ✅ init_basic
- ✅ init_with_recall
- ✅ crud_create
- ✅ crud_read
...
</details>

## Skipped Tests

- ⏭️ external_api_test (tagged: slow)
- ⏭️ integration_full (depends_on: external_api_test)
```

### HTML

Generates styled HTML with:
- Color-coded status badges
- Collapsible sections
- Syntax highlighting for responses
- Print-friendly styling

### JSON

```json
{
  "generated_at": "2024-01-20T15:30:00Z",
  "duration_seconds": 323,
  "summary": {
    "total": 53,
    "passed": 48,
    "failed": 3,
    "skipped": 2,
    "pass_rate": 0.906
  },
  "results": [
    {
      "id": "init_basic",
      "status": "pass",
      "duration_ms": 1250,
      "timestamp": "2024-01-20T15:25:00Z"
    },
    {
      "id": "search_empty",
      "status": "fail",
      "failures": ["Missing: 'no results'"],
      "actual_response": "Found 0 matches for query",
      "duration_ms": 890,
      "timestamp": "2024-01-20T15:28:30Z"
    }
  ],
  "metadata": {
    "filters": {
      "category": null,
      "tag": null
    },
    "test_file": "tests/functional/tests.yaml",
    "runner_version": "1.0.0"
  }
}
```

## CI Integration

For CI/CD pipelines, use JSON format and check exit code:

```bash
# Generate JSON report
./tests/functional/runner.sh report --format json > test-results.json

# Check for failures
failures=$(jq '.summary.failed' test-results.json)
if [[ "$failures" -gt 0 ]]; then
  echo "Tests failed: $failures"
  exit 1
fi
```

## Historical Reports

Reports are saved to `tests/functional/reports/` by default:

```
tests/functional/reports/
├── 2024-01-20T15-30-00.md
├── 2024-01-20T15-30-00.json
└── latest.md -> 2024-01-20T15-30-00.md
```

Access historical reports:
```bash
ls tests/functional/reports/
cat tests/functional/reports/latest.md
```
