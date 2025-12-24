---
description: Validate NSIP API connectivity and configuration
allowed-tools: [mcp__nsip__nsip_get_last_update]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
TEST_API(1)                                          User Commands                                          TEST_API(1)

NAME
    test-api - Validate NSIP API connectivity and configuration

SYNOPSIS
    /nsip:test-api [options]

DESCRIPTION
    Validate NSIP API connectivity and configuration

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:test-api                          
    /nsip:test-api <options>                
    /nsip:test-api --help                   

SEE ALSO
    /nsip:* for related commands

                                                                      TEST_API(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /test-api - Validate NSIP API Connectivity

You are tasked with validating NSIP API connection.

**Note**: The NSIP API is public and requires no authentication.

## Instructions

<step number="1" name="Test API Connectivity">
<mcp_integration>
<tool name="nsip_get_last_update">
Call `nsip_get_last_update` MCP tool (simple API call to test connectivity)
</tool>
</mcp_integration>
</step>

<step number="2" name="Display Success">
If successful, display:
- "✓ NSIP API connectivity verified"
- "Database last updated: [date]"
- "API endpoint: [base_url from NSIP_BASE_URL or default]"
</step>

<step number="3" name="Display Failure">
If fails, display:
- "✗ NSIP API connection failed"
- "Possible causes:"
  - "- Network connectivity issues"
  - "- NSIP API temporarily unavailable"
  - "- Custom NSIP_BASE_URL misconfigured (if set)"
- "Default API: http://nsipsearch.nsip.org/api"
- "To use custom endpoint: export NSIP_BASE_URL=your-url"
</step>

<error_handling>

- Provide helpful diagnostics for connection issues
- Suggest checking network connectivity
- Mention NSIP_BASE_URL only if relevant (custom endpoint)
- Successful operation displays result (not silent for this diagnostic command)

</error_handling>
