---
description: List animal offspring/progeny
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_get_progeny]
---

# /progeny - List Offspring

You are tasked with retrieving the offspring list for an animal.

## Instructions

1. Prompt user for LPN ID if not provided
2. Validate LPN ID is at least 5 characters
3. Call `nsip_get_progeny` MCP tool with search_string parameter
4. Format and display progeny list:
   - Parent animal: LPN ID, breed
   - Total offspring count
   - For each offspring:
     - LPN ID
     - Breed
     - Birth date (if available)
     - Key breeding values/traits
5. Provide summary statistics if large progeny count (average traits, etc.)

## Error Handling

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If no progeny: "No offspring recorded for this animal."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results
