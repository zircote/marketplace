---
description: Get complete animal profile (details, lineage, progeny)
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_search_by_lpn]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
PROFILE(1)                                           User Commands                                           PROFILE(1)

NAME
    profile - Get complete animal profile (details, lineage, progeny)

SYNOPSIS
    /nsip:profile [LPN ID]

DESCRIPTION
    Get complete animal profile (details, lineage, progeny)

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:profile                           
    /nsip:profile --help                    

SEE ALSO
    /nsip:* for related commands

                                                                      PROFILE(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /profile - Get Complete Animal Profile

You are tasked with retrieving comprehensive profile (details + lineage + progeny).

## Instructions

<step number="1" name="Get LPN ID">
Prompt user for LPN ID if not provided
</step>

<step number="2" name="Validate LPN ID">
Validate LPN ID is at least 5 characters
</step>

<step number="3" name="Call MCP Tool">
<mcp_integration>
<tool name="nsip_search_by_lpn">
Call `nsip_search_by_lpn` MCP tool (this combines details, lineage, progeny)
</tool>
</mcp_integration>
</step>

<step number="4" name="Format Profile">
Format and display comprehensive profile:
- Animal: LPN ID, Breed
- Pedigree: Sire LPN ID, Dam LPN ID
- Progeny: Total count
- Top Traits: Top 3 by accuracy
</step>

<error_handling>

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results

</error_handling>
