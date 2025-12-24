---
description: List animal offspring/progeny
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_get_progeny]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
PROGENY(1)                                           User Commands                                           PROGENY(1)

NAME
    progeny - List animal offspring/progeny

SYNOPSIS
    /nsip:progeny [LPN ID]

DESCRIPTION
    List animal offspring/progeny

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:progeny                           
    /nsip:progeny --help                    

SEE ALSO
    /nsip:* for related commands

                                                                      PROGENY(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /progeny - List Offspring

You are tasked with retrieving the offspring list for an animal.

## Instructions

<step number="1" name="Get LPN ID">
Prompt user for LPN ID if not provided
</step>

<step number="2" name="Validate LPN ID">
Validate LPN ID is at least 5 characters
</step>

<step number="3" name="Call MCP Tool">
<mcp_integration>
<tool name="nsip_get_progeny">
Call `nsip_get_progeny` MCP tool with search_string parameter
</tool>
</mcp_integration>
</step>

<step number="4" name="Format Progeny List">
Format and display progeny list:
- Parent animal: LPN ID, breed
- Total offspring count
- For each offspring:
  - LPN ID
  - Breed
  - Birth date (if available)
  - Key breeding values/traits
</step>

<step number="5" name="Provide Summary Statistics">
Provide summary statistics if large progeny count (average traits, etc.)
</step>

<error_handling>

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If no progeny: "No offspring recorded for this animal."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results

</error_handling>
