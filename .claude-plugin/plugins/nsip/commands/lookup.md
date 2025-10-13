---
description: Get detailed animal information by LPN ID
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_get_animal]
---

# /lookup - Get Animal Details by LPN ID

You are tasked with retrieving detailed information about a specific animal.

## Instructions

1. Prompt user for LPN ID if not provided (or use argument if given)
2. Validate LPN ID is at least 5 characters
3. Call `nsip_get_animal` MCP tool with the search_string parameter
4. Format and display results:
   - Animal basics: LPN ID, breed, status
   - Top 3 traits by accuracy
   - Breeding values summary

## Error Handling

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results
