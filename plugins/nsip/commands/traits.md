---
description: Get trait value ranges for a specific breed
argument-hint: "[breed ID]"
allowed-tools: [mcp__nsip__nsip_get_trait_ranges]
---

# /traits - Get Trait Ranges for Breed

You are tasked with retrieving trait value ranges for a specific breed.

## Instructions

1. Prompt user for breed ID if not provided
2. Validate breed ID is numeric
3. Call `nsip_get_trait_ranges` MCP tool with breed_id parameter
4. Format and display trait ranges:
   - Breed name and ID
   - For each trait:
     - Trait name
     - Minimum value
     - Maximum value
     - Unit of measurement (if applicable)
5. Provide context on how to interpret trait ranges for breeding decisions

## Error Handling

- If breed ID invalid: "Please provide a valid numeric breed ID"
- If breed not found: "Breed not found. Use /discover to list available breeds."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results
