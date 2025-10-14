---
description: Search for animals with optional filters
allowed-tools: [mcp__nsip__nsip_search_animals]
---

# /search - Search Animals with Filters

You are tasked with searching for animals using optional filters.

## Instructions

1. Prompt user for search criteria (or use provided filters):
   - Breed ID (optional)
   - Status (optional)
   - Traits filters (optional)
   - Page number (default: 1)
   - Page size (default: 50)
2. Call `nsip_search_animals` MCP tool with provided filters
3. Format and display search results:
   - Total matches found
   - Current page / total pages
   - Animal list with key details (LPN ID, breed, status)
   - Top traits for each animal
4. Suggest pagination commands if more results available

## Error Handling

- If no results found: "No animals match the search criteria. Try adjusting filters."
- If API call fails: "Connection error - check network and API status"
- If invalid filters: Display helpful message about valid filter values
- Successful operation remains silent (FR-016) - only show results
