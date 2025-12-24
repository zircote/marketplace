---
description: Get trait value ranges for a specific breed
argument-hint: "[breed ID]"
allowed-tools: [mcp__nsip__nsip_get_trait_ranges]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
TRAITS(1)                                            User Commands                                            TRAITS(1)

NAME
    traits - Get trait value ranges for a specific breed

SYNOPSIS
    /nsip:traits [breed ID]

DESCRIPTION
    Get trait value ranges for a specific breed

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:traits                            
    /nsip:traits --help                     

SEE ALSO
    /nsip:* for related commands

                                                                      TRAITS(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /traits - Get Trait Ranges for Breed

You are tasked with retrieving trait value ranges for a specific breed.

## Instructions

<step number="1" name="Get Breed ID">
Prompt user for breed ID if not provided
</step>

<step number="2" name="Validate Breed ID">
Validate breed ID is numeric
</step>

<step number="3" name="Call MCP Tool">
<mcp_integration>
<tool name="nsip_get_trait_ranges">
Call `nsip_get_trait_ranges` MCP tool with breed_id parameter
</tool>
</mcp_integration>
</step>

<step number="4" name="Format Trait Ranges">
Format and display trait ranges:
- Breed name and ID
- For each trait:
  - Trait name
  - Minimum value
  - Maximum value
  - Unit of measurement (if applicable)
</step>

<step number="5" name="Provide Context">
Provide context on how to interpret trait ranges for breeding decisions
</step>

<error_handling>

- If breed ID invalid: "Please provide a valid numeric breed ID"
- If breed not found: "Breed not found. Use /discover to list available breeds."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results

</error_handling>
