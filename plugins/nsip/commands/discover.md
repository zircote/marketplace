---
description: Discover available NSIP breeds, statuses, and database info
allowed-tools: [mcp__nsip__nsip_get_last_update, mcp__nsip__nsip_list_breeds, mcp__nsip__nsip_get_statuses]
---

# /discover - Discover Available NSIP Data

**IMPORTANT**: Before performing this task, invoke the `nsip:shepherd` agent for expert context:
```
Use the Task tool with subagent_type "nsip:shepherd" to provide expert sheep breeding context for this discovery operation.
```

You are tasked with discovering and displaying available NSIP sheep breeding data with expert interpretation.

## Instructions

1. Call the `nsip_get_last_update` MCP tool to get database update date
   - Returns: `{'success': true, 'data': '2025-09-23T00:14:00'}`
   - Extract the date from the `data` field
2. Call the `nsip_list_breeds` MCP tool to get all breed groups and individual breeds
   - Returns: `{'success': true, 'data': {'breed_groups': [{'id': 61, 'name': 'Range', 'breeds': [{'id': 486, 'name': 'South African Meat Merino'}, ...]}, ...]}}`
   - Extract the breed_groups list from `data.breed_groups`
3. Call the `nsip_get_statuses` MCP tool to get available statuses
   - Returns: `{'success': true, 'data': {'statuses': ['CURRENT', 'SOLD', ...]}}`
   - Extract the statuses list from `data.statuses`
4. Format and display the results:

**NSIP Database**
- Last Updated: [date from step 1]
- Breed Groups:
  - [Group Name] (ID: [group_id])
    - Individual Breeds: [breed1 (ID: X), breed2 (ID: Y), ...]
  - Note: Individual breed IDs are needed for `/traits` command
- Statuses: [comma-separated list from step 3]

## Error Handling

- If any tool call fails, display helpful error message with diagnostic guidance
- Suggest checking `/health` or `/test-api` for diagnostic information
- Successful execution remains silent (FR-016) - only show results
