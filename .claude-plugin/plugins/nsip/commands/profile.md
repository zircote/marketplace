---
description: Get complete animal profile (details, lineage, progeny)
argument-hint: "[LPN ID]"
allowed-tools: [mcp__nsip__nsip_search_by_lpn]
---

# /profile - Get Complete Animal Profile

You are tasked with retrieving comprehensive profile (details + lineage + progeny).

## Instructions

1. Prompt user for LPN ID if not provided
2. Validate LPN ID is at least 5 characters
3. Call `nsip_search_by_lpn` MCP tool (this combines details, lineage, progeny)
4. Format and display comprehensive profile:
   - Animal: LPN ID, Breed
   - Pedigree: Sire LPN ID, Dam LPN ID
   - Progeny: Total count
   - Top Traits: Top 3 by accuracy

## Error Handling

- If LPN ID invalid: "Please provide valid LPN ID (minimum 5 characters)"
- If not found: "Animal not found. Verify LPN ID and try again."
- If API call fails: "Connection error - check network and API status"
- Successful operation remains silent (FR-016) - only show results
