---
description: Get detailed animal information by LPN ID
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_get_animal]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
LOOKUP(1)                                            User Commands                                            LOOKUP(1)

NAME
    lookup - Get detailed animal information by LPN ID

SYNOPSIS
    /nsip:lookup [LPN ID]

DESCRIPTION
    Get detailed animal information by LPN ID

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:lookup                            
    /nsip:lookup --help                     

SEE ALSO
    /nsip:* for related commands

                                                                      LOOKUP(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /lookup - Get Animal Details by LPN ID

You are tasked with retrieving detailed information about a specific animal.

## Instructions

<step number="1" name="Get LPN ID">
Prompt user for LPN ID if not provided (or use argument if given)
</step>

<step number="2" name="Validate LPN ID">
Validate LPN ID is at least 5 characters
</step>

<step number="3" name="Call MCP Tool">
<mcp_integration>
<tool name="nsip_get_animal">
Call `nsip_get_animal` MCP tool with the search_string parameter
</tool>
</mcp_integration>
</step>

<step number="4" name="Format and Display Results">
Format and display results:
- Animal basics: LPN ID, breed, status
- Top 3 traits by accuracy
- Breeding values summary
</step>

<error_handling>

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results

</error_handling>
