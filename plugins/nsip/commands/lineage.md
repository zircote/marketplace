---
description: Get animal pedigree tree (lineage/ancestry)
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_get_lineage]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
LINEAGE(1)                                           User Commands                                           LINEAGE(1)

NAME
    lineage - Get animal pedigree tree (lineage/ancestry)

SYNOPSIS
    /nsip:lineage [LPN ID]

DESCRIPTION
    Get animal pedigree tree (lineage/ancestry)

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:lineage                           
    /nsip:lineage --help                    

SEE ALSO
    /nsip:* for related commands

                                                                      LINEAGE(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /lineage - Get Pedigree Tree

You are tasked with retrieving the pedigree tree (ancestry) for an animal.

## Instructions

<step number="1" name="Get LPN ID">
Prompt user for LPN ID if not provided
</step>

<step number="2" name="Validate LPN ID">
Validate LPN ID is at least 5 characters
</step>

<step number="3" name="Call MCP Tool">
<mcp_integration>
<tool name="nsip_get_lineage">
Call `nsip_get_lineage` MCP tool with search_string parameter
</tool>
</mcp_integration>
</step>

<step number="4" name="Format Pedigree Tree">
Format and display pedigree tree:
- Animal (subject): LPN ID, breed
- Sire: LPN ID, breed, key traits
- Dam: LPN ID, breed, key traits
- Grandparents (if available):
  - Paternal: Sire's sire and dam
  - Maternal: Dam's sire and dam
</step>

<step number="5" name="Display Tree Visualization">
Display tree structure with clear hierarchy visualization
</step>

<error_handling>

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If lineage incomplete: Display available information with note about missing data
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results

</error_handling>
