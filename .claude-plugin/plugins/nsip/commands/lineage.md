---
description: Get animal pedigree tree (lineage/ancestry)
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_get_lineage]
---

# /lineage - Get Pedigree Tree

You are tasked with retrieving the pedigree tree (ancestry) for an animal.

## Instructions

1. Prompt user for LPN ID if not provided
2. Validate LPN ID is at least 5 characters
3. Call `nsip_get_lineage` MCP tool with search_string parameter
4. Format and display pedigree tree:
   - Animal (subject): LPN ID, breed
   - Sire: LPN ID, breed, key traits
   - Dam: LPN ID, breed, key traits
   - Grandparents (if available):
     - Paternal: Sire's sire and dam
     - Maternal: Dam's sire and dam
5. Display tree structure with clear hierarchy visualization

## Error Handling

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If lineage incomplete: Display available information with note about missing data
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results
