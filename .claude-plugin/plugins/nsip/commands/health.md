---
description: Display MCP server health metrics and performance
allowed-tools: [mcp__nsip__get_server_health]
---

# /health - Display MCP Server Health Metrics

You are tasked with showing server performance metrics and success criteria status.

## Instructions

1. Call `get_server_health` MCP tool
2. Extract and display key server performance metrics:
   - MCP server startup time
   - API response times
   - Cache hit rates
   - Request success rates
   - Data summarization efficiency
3. Display metrics in readable format with context for interpretation

## Error Handling

- If tool call fails: "Unable to retrieve server health. Check MCP server status."
- Successful operation remains silent (FR-016) - only show metrics
