---
description: Validate NSIP API connectivity and configuration
allowed-tools: [mcp__nsip__nsip_get_last_update]
---

# /test-api - Validate NSIP API Connectivity

You are tasked with validating NSIP API connection.

**Note**: The NSIP API is public and requires no authentication.

## Instructions

1. Call `nsip_get_last_update` MCP tool (simple API call to test connectivity)
2. If successful, display:
   - "✓ NSIP API connectivity verified"
   - "Database last updated: [date]"
   - "API endpoint: [base_url from NSIP_BASE_URL or default]"
3. If fails, display:
   - "✗ NSIP API connection failed"
   - "Possible causes:"
     - "- Network connectivity issues"
     - "- NSIP API temporarily unavailable"
     - "- Custom NSIP_BASE_URL misconfigured (if set)"
   - "Default API: http://nsipsearch.nsip.org/api"
   - "To use custom endpoint: export NSIP_BASE_URL=your-url"

## Error Handling

- Provide helpful diagnostics for connection issues
- Suggest checking network connectivity
- Mention NSIP_BASE_URL only if relevant (custom endpoint)
- Successful operation displays result (not silent for this diagnostic command)
