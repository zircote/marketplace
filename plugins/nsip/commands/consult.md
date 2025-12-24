---
description: Consult with NSIP sheep breeding expert using live data
allowed-tools: [mcp__nsip__nsip_get_animal, mcp__nsip__nsip_search_animals, mcp__nsip__nsip_get_lineage, mcp__nsip__nsip_get_progeny, mcp__nsip__nsip_search_by_lpn, mcp__nsip__nsip_get_trait_ranges, mcp__nsip__nsip_list_breeds]
---

<help_check>
## Help Check

If `$ARGUMENTS` contains `--help` or `-h`:

**Output this help and HALT (do not proceed further):**

<help_output>
```
CONSULT(1)                                           User Commands                                           CONSULT(1)

NAME
    consult - Consult with NSIP sheep breeding expert using live data

SYNOPSIS
    /nsip:consult [options]

DESCRIPTION
    Consult with NSIP sheep breeding expert using live data

OPTIONS
    --help, -h                Show this help message

EXAMPLES
    /nsip:consult                           
    /nsip:consult <options>                 
    /nsip:consult --help                    

SEE ALSO
    /nsip:* for related commands

                                                                      CONSULT(1)
```
</help_output>

**After outputting help, HALT immediately. Do not proceed with command execution.**
</help_check>

---

# /consult - Expert NSIP Breeding Consultation

This command provides expert sheep breeding advice using live NSIP data through the shepherd agent.

## How It Works

**ALWAYS invoke the nsip:shepherd agent** for this command:

1. Use the Task tool with `subagent_type: "nsip:shepherd"`
2. Pass the user's question/request as the prompt
3. The shepherd agent will:
   - Use NSIP MCP tools to gather relevant data
   - Provide expert interpretation and recommendations
   - Explain breeding values, genetics, and selection strategies
   - Give actionable advice for sheep farm operations

## Example Usage

```
/nsip:consult I'm looking for a terminal sire ram with good growth rates
```

The shepherd agent will:
1. Search NSIP database for terminal breeds
2. Filter by growth trait performance (YWT, PWWT)
3. Analyze top candidates
4. Provide selection recommendations with explanations

## When to Use

- **Breeding decisions**: Ram/ewe selection, genetic evaluation
- **Health questions**: Diagnosis, treatment, prevention
- **Nutrition planning**: Feed programs, supplementation
- **Flock management**: Culling decisions, optimization
- **NSIP data interpretation**: Understanding breeding values, trait tradeoffs

## Instructions

<step number="1" name="Invoke Shepherd Agent">
ALWAYS start by invoking the shepherd agent:

```
Use Task tool:
- subagent_type: "nsip:shepherd"
- description: "NSIP breeding consultation"
- prompt: "[User's complete question including any LPN IDs, breed preferences, or specific concerns]"
```

The agent has access to all NSIP tools and will handle the complete consultation.
</step>
