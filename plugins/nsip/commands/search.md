---
description: Search for animals with optional filters
allowed-tools: [mcp__nsip__nsip_search_animals]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
SEARCH(1)                                            User Commands                                            SEARCH(1)

NAME
    search - Search for animals with optional filters

SYNOPSIS
    /nsip:search [options]

DESCRIPTION
    Search for animals with optional filters

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:search                            
    /nsip:search <options>                  
    /nsip:search --help                     

SEE ALSO
    /nsip:* for related commands

                                                                      SEARCH(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /search - Search Animals with Filters

You are tasked with searching for animals using optional filters.

## Instructions

<step number="1" name="Get Search Criteria">
Prompt user for search criteria (or use provided filters):
- Breed ID (optional)
- Status (optional)
- Traits filters (optional)
- Page number (default: 1)
- Page size (default: 50)
</step>

<step number="2" name="Call MCP Tool">
<mcp_integration>
<tool name="nsip_search_animals">
Call `nsip_search_animals` MCP tool with provided filters
</tool>
</mcp_integration>
</step>

<step number="3" name="Format Search Results">
Format and display search results:
- Total matches found
- Current page / total pages
- Animal list with key details (LPN ID, breed, status)
- Top traits for each animal
</step>

<step number="4" name="Suggest Pagination">
Suggest pagination commands if more results available
</step>

<error_handling>

- If no results found: "No animals match the search criteria. Try adjusting filters."
- If API call fails: "Connection error - check network and API status"
- If invalid filters: Display helpful message about valid filter values
- Successful operation remains silent (FR-016) - only show results

</error_handling>
