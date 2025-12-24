---
description: Discover available NSIP breeds, statuses, and database info
allowed-tools: [mcp__nsip__nsip_get_last_update, mcp__nsip__nsip_list_breeds, mcp__nsip__nsip_get_statuses]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
DISCOVER(1)                                          User Commands                                          DISCOVER(1)

NAME
    discover - Discover available NSIP breeds, statuses, and database ...

SYNOPSIS
    /nsip:discover [options]

DESCRIPTION
    Discover available NSIP breeds, statuses, and database info

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:discover                          
    /nsip:discover <options>                
    /nsip:discover --help                   

SEE ALSO
    /nsip:* for related commands

                                                                      DISCOVER(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /discover - Discover Available NSIP Data

**IMPORTANT**: Before performing this task, invoke the `nsip:shepherd` agent for expert context:
```
Use the Task tool with subagent_type "nsip:shepherd" to provide expert sheep breeding context for this discovery operation.
```

You are tasked with discovering and displaying available NSIP sheep breeding data with expert interpretation.

## Instructions

<step number="1" name="Get Database Update Date">
<mcp_integration>
<tool name="nsip_get_last_update">
Call the `nsip_get_last_update` MCP tool to get database update date
- Returns: `{'success': true, 'data': '2025-09-23T00:14:00'}`
- Extract the date from the `data` field
</tool>
</mcp_integration>
</step>

<step number="2" name="Get Breed Groups">
<mcp_integration>
<tool name="nsip_list_breeds">
Call the `nsip_list_breeds` MCP tool to get all breed groups and individual breeds
- Returns: `{'success': true, 'data': {'breed_groups': [{'id': 61, 'name': 'Range', 'breeds': [{'id': 486, 'name': 'South African Meat Merino'}, ...]}, ...]}}`
- Extract the breed_groups list from `data.breed_groups`
</tool>
</mcp_integration>
</step>

<step number="3" name="Get Available Statuses">
<mcp_integration>
<tool name="nsip_get_statuses">
Call the `nsip_get_statuses` MCP tool to get available statuses
- Returns: `{'success': true, 'data': {'statuses': ['CURRENT', 'SOLD', ...]}}`
- Extract the statuses list from `data.statuses`
</tool>
</mcp_integration>
</step>

<step number="4" name="Format and Display Results">
Format and display the results:

**NSIP Database**
- Last Updated: [date from step 1]
- Breed Groups:
  - [Group Name] (ID: [group_id])
    - Individual Breeds: [breed1 (ID: X), breed2 (ID: Y), ...]
  - Note: Individual breed IDs are needed for `/traits` command
- Statuses: [comma-separated list from step 3]
</step>

<error_handling>

- If any tool call fails, display helpful error message with diagnostic guidance
- Suggest checking `/health` or `/test-api` for diagnostic information
- Successful execution remains silent (FR-016) - only show results

</error_handling>
