---
description: Display MCP server health metrics and performance
allowed-tools: [mcp__nsip__get_server_health]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
HEALTH(1)                                            User Commands                                            HEALTH(1)

NAME
    health - Display MCP server health metrics and performance

SYNOPSIS
    /nsip:health [options]

DESCRIPTION
    Display MCP server health metrics and performance

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:health                            
    /nsip:health <options>                  
    /nsip:health --help                     

SEE ALSO
    /nsip:* for related commands

                                                                      HEALTH(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /health - Display MCP Server Health Metrics

You are tasked with showing server performance metrics and success criteria status.

## Instructions

<step number="1" name="Get Server Health">
<mcp_integration>
<tool name="get_server_health">
Call `get_server_health` MCP tool
</tool>
</mcp_integration>
</step>

<step number="2" name="Extract Metrics">
Extract and display key server performance metrics:
- MCP server startup time
- API response times
- Cache hit rates
- Request success rates
- Data summarization efficiency
</step>

<step number="3" name="Display Metrics">
Display metrics in readable format with context for interpretation
</step>

<error_handling>

- If tool call fails: "Unable to retrieve server health. Check MCP server status."
- Successful operation remains silent (FR-016) - only show metrics

</error_handling>
