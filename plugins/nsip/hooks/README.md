# NSIP Plugin Hooks

This directory contains Claude Code plugin hooks that enhance the NSIP plugin functionality with automatic logging, caching, validation, error resilience, context enhancement, workflow intelligence, and export capabilities.

## Overview

The NSIP plugin includes **15 high-value hooks** that execute at different stages of tool usage and user interaction:

| Hook Name | Type | Purpose | Status |
|-----------|------|---------|--------|
| API Health Check | SessionStart | Verify API connectivity at session start | Active |
| LPN Validator | PreToolUse | Validate LPN ID format before API calls | Active |
| Breed Context Injector | PreToolUse | Inject breed characteristics for searches | Active |
| Trait Dictionary | PreToolUse | Provide breeding terminology explanations | Active |
| Auto Retry | PostToolUse | Retry failed calls with exponential backoff | Active |
| Fallback Cache | PostToolUse | Provide cached data when API fails | Active |
| Error Notifier | PostToolUse | Track and alert on repeated failures | Active |
| Query Logger | PostToolUse | Log all API calls with timestamps | Active |
| Result Cache | PostToolUse | Cache frequently accessed data | Active |
| CSV Exporter | PostToolUse | Export search results to CSV | Active |
| Pedigree Visualizer | PostToolUse | Generate ASCII art family trees | Active |
| Breeding Report | PostToolUse | Create comprehensive breeding analysis | Active |
| Smart Search Detector | UserPromptSubmit | Detect LPN IDs and suggest tools | Active |
| Comparative Analyzer | UserPromptSubmit | Identify multi-animal comparisons | Active |

## Advanced Features

The hook system provides four key capability areas:

### Error Resilience
- **Auto Retry**: 3-attempt retry with exponential backoff (1s, 2s, 4s delays)
- **Fallback Cache**: Graceful degradation to cached data when API fails
- **Error Notifier**: Alerts on repeated failures with troubleshooting tips

### Context Enhancement
- **Breed Context**: Automatic breed characteristic injection for 6+ breeds
- **Trait Dictionary**: 13+ trait definitions and breeding terminology
- **Smart Detection**: Automatic LPN ID and intent recognition

### Workflow Intelligence
- **Smart Search**: Detects search, lineage, progeny, and comparison intents
- **Comparative Analysis**: Multi-animal comparison workflow suggestions
- **Intent Detection**: Trait focus identification (weight, wool, meat, etc.)

### Data Export
- **CSV Export**: Flattened search result exports
- **Pedigree Trees**: ASCII art visualization of lineage
- **Breeding Reports**: Comprehensive Markdown analysis documents

## Hook Types

### SessionStart Hooks

Execute once when Claude Code session begins.

#### API Health Check (`api_health_check.py`)

**Purpose**: Verify NSIP API is accessible and check database freshness.

**What it does**:
- Calls `http://nsipsearch.nsip.org/api/GetLastUpdate`
- Retrieves database last update timestamp
- Displays warning if API is unavailable
- Timeout: 5 seconds

**Example Output**:
```
NSIP API Status: Connected
Database Last Updated: 2025-10-10
```

**Troubleshooting**:
- If API is down, the hook warns but allows session to continue
- Check connectivity with: `curl http://nsipsearch.nsip.org/api/GetLastUpdate`

---

### PreToolUse Hooks

Execute before tool calls, can prevent execution or modify context.

#### LPN Validator (`lpn_validator.py`)

**Purpose**: Validate LPN ID format before making API calls to prevent errors.

**Triggers on**: `nsip_get_animal`, `nsip_search_by_lpn`, `nsip_get_lineage`, `nsip_get_progeny`

**What it does**:
- Checks LPN ID length and character requirements
- Validates format: numeric with optional `#` placeholders
- Blocks invalid calls and returns clear error messages
- Prevents unnecessary API requests

**Example Scenarios**:
```
Valid:   "6####92020###249" ✓
Valid:   "621879202000024"  ✓
Invalid: "abc123"           ✗ (contains letters)
Invalid: "123"              ✗ (too short)
```

#### Breed Context Injector (`breed_context_injector.py`)

**Purpose**: Enhance searches with breed-specific characteristics and context.

**Triggers on**: `nsip_search_animals`, `nsip_get_trait_ranges`

**What it does**:
- Injects breed-specific characteristics before searches
- Provides context about breed traits, origins, and uses
- Enhances search results with relevant breed information

**Built-in Breed Database**:
- **Merino**: Fine wool, wrinkle-prone, Australian heritage
- **Border Leicester**: Long wool, dual-purpose, terminal sire
- **Poll Dorset**: Aseasonal breeding, meat production
- **White Suffolk**: Terminal sire, heavy muscling, meat quality
- **Dorper**: Hair sheep, meat production, hardiness
- **Corriedale**: Dual-purpose, New Zealand/Australian cross

**Example Enhancement**:
```
User Query: "Find Merino sheep with high fleece weight"

Injected Context:
- Breed: Merino (fine wool specialist)
- Key Traits: Fleece weight, fiber diameter, staple length
- Typical Range: 4-7kg fleece weight, 17-23 micron
```

**Benefits**:
- More relevant search results
- Better trait interpretation
- Breed-aware recommendations

#### Trait Dictionary (`trait_dictionary.py`)

**Purpose**: Provide comprehensive trait definitions and breeding terminology.

**Triggers on**: All NSIP tools (when trait-related parameters detected)

**What it does**:
- Detects trait mentions in queries
- Provides detailed trait definitions
- Explains breeding terminology
- Offers typical ranges and units

**Comprehensive Trait Coverage** (13+ traits):
- **Weight Traits**: Birth weight, weaning weight, yearling weight, mature weight
- **Wool Traits**: Fleece weight, fiber diameter, staple length, staple strength
- **Meat Traits**: Eye muscle depth, fat depth, loin depth, carcass weight
- **Reproduction**: Number of lambs born, weaning rate, conception rate

**Example Trait Definitions**:
```
Fleece Weight (kg):
  Description: Total wool weight at shearing
  Importance: Primary wool production metric
  Typical Range: 3-8kg (varies by breed)

Fiber Diameter (microns):
  Description: Average wool fiber thickness
  Importance: Determines wool quality and value
  Typical Range: 15-25 microns (finer = higher value)
```

**Benefits**:
- Clear trait understanding
- Proper unit interpretation
- Context-aware breeding decisions

---

### PostToolUse Hooks

Execute after tool calls, enhance results but cannot modify core responses.

#### Auto Retry (`auto_retry.py`)

**Purpose**: Automatically retry failed API calls with exponential backoff.

**Triggers on**: All NSIP tools (when errors, empty results, or timeouts occur)

**What it does**:
- Detects failures: API errors, empty results, timeouts
- Executes up to 3 retry attempts
- Exponential backoff delays: 1s, 2s, 4s
- Logs all retry attempts

**Retry Scenarios**:
1. **Network Error**: Temporary connection issues
2. **Timeout**: API slow to respond
3. **Empty Results**: Potential database issue
4. **Server Error**: 5xx HTTP status codes

**Log Location**: `~/.claude-code/nsip-logs/retry_log.jsonl`

**Example Log Entry**:
```json
{
  "timestamp": "2025-10-13T14:30:45.123Z",
  "tool": "mcp__nsip__nsip_get_animal",
  "parameters": {"lpn_id": "6####92020###249"},
  "attempt": 2,
  "delay_seconds": 2,
  "success": true,
  "total_attempts": 2
}
```

**Troubleshooting**:
- If all 3 attempts fail, check API connectivity
- View retry history: `tail -f ~/.claude-code/nsip-logs/retry_log.jsonl`
- High retry rates indicate API instability

#### Fallback Cache (`fallback_cache.py`)

**Purpose**: Provide cached data as fallback when API is unavailable.

**Triggers on**: All NSIP tools (when API calls fail after retries)

**What it does**:
- Checks for cached data when API fails
- Returns most recent cached result with warning
- Provides graceful degradation
- Displays cache age in warning message

**Fallback Priority**:
1. Try live API call (with auto-retry)
2. If fails, check fallback cache
3. If cache exists, return with warning
4. If no cache, return error

**Log Location**: `~/.claude-code/nsip-logs/fallback_log.jsonl`

**Example Warning**:
```
Warning: NSIP API unavailable. Using cached data from 45 minutes ago.
Data may be outdated. API status: Connection timeout.
```

**Example Log Entry**:
```json
{
  "timestamp": "2025-10-13T14:30:45.123Z",
  "tool": "mcp__nsip__nsip_get_animal",
  "parameters": {"lpn_id": "6####92020###249"},
  "cache_age_minutes": 45,
  "api_error": "Connection timeout",
  "fallback_used": true
}
```

**Benefits**:
- Continues working during API outages
- User aware of data staleness
- Graceful user experience

#### Error Notifier (`error_notifier.py`)

**Purpose**: Track repeated failures and create actionable alerts.

**Triggers on**: All NSIP tools (when errors occur)

**What it does**:
- Tracks errors in 5-minute rolling windows
- Detects patterns: 3+ failures in 5 minutes
- Creates alert files with troubleshooting tips
- Provides actionable remediation steps

**Alert Threshold**: 3+ failures within 5 minutes

**Alert Location**: `~/.claude-code/nsip-logs/ALERT_*.txt`

**Example Alert File** (`ALERT_20251013_143045.txt`):
```
NSIP API Alert - Repeated Failures Detected

Time: 2025-10-13 14:30:45
Failures: 5 in last 5 minutes
Tools Affected: nsip_get_animal, nsip_search_animals

Common Errors:
- Connection timeout (3 occurrences)
- 503 Service Unavailable (2 occurrences)

Troubleshooting Steps:
1. Check API status: curl http://nsipsearch.nsip.org/api/GetLastUpdate
2. Verify internet connectivity
3. Check firewall/proxy settings
4. Try again in 5-10 minutes (possible API maintenance)
5. Review logs: ~/.claude-code/nsip-logs/query_log.jsonl

If problem persists:
- Report to: https://github.com/epicpast/nsip-api-client/issues
- Include: This alert file + query_log.jsonl entries
```

**Alert Management**:
```bash
# View recent alerts
ls -lt ~/.claude-code/nsip-logs/ALERT_*.txt | head -5

# Read latest alert
cat ~/.claude-code/nsip-logs/ALERT_*.txt | head -1

# Clear old alerts (older than 7 days)
find ~/.claude-code/nsip-logs/ -name "ALERT_*.txt" -mtime +7 -delete
```

#### Query Logger (`query_logger.py`)

**Purpose**: Log all API calls for audit, debugging, and analytics.

**Triggers on**: All 5 main NSIP tools

**What it does**:
- Captures timestamps, parameters, and results
- Records success/failure status
- Measures API response times
- Stores in JSONL format for easy parsing

**Log Location**: `~/.claude-code/nsip-logs/query_log.jsonl`

**Example Log Entry**:
```json
{
  "timestamp": "2025-10-13T14:30:45.123Z",
  "tool": "mcp__nsip__nsip_get_animal",
  "parameters": {"lpn_id": "6####92020###249"},
  "success": true,
  "error": null,
  "result_size": 1234,
  "duration_ms": 250
}
```

**Analytics Examples**:
```bash
# Count total queries
wc -l ~/.claude-code/nsip-logs/query_log.jsonl

# Find slow queries (>1000ms)
jq 'select(.duration_ms > 1000)' ~/.claude-code/nsip-logs/query_log.jsonl

# Count errors
jq 'select(.success == false)' ~/.claude-code/nsip-logs/query_log.jsonl | wc -l

# Most used tool
jq -r '.tool' ~/.claude-code/nsip-logs/query_log.jsonl | sort | uniq -c | sort -rn
```

#### Result Cache (`result_cache.py`)

**Purpose**: Cache frequently accessed data to improve performance.

**Triggers on**: `nsip_get_animal`, `nsip_search_by_lpn`, `nsip_get_lineage`, `nsip_get_progeny`

**What it does**:
- Caches animal data, lineage, and progeny
- TTL: 60 minutes
- SHA-256 hashed filenames for privacy
- Automatic cleanup on expiration

**Cache Location**: `~/.claude-code/nsip-cache/`

**Cache Entry Structure**:
```json
{
  "tool": "mcp__nsip__nsip_get_animal",
  "parameters": {"lpn_id": "6####92020###249"},
  "result": {...},
  "cached_at": "2025-10-13T14:30:45.123Z"
}
```

**Benefits**:
- Faster repeated queries
- Reduced API load
- Works offline (within TTL window)

**Cache Management**:
```bash
# View cache statistics
du -sh ~/.claude-code/nsip-cache/
ls ~/.claude-code/nsip-cache/ | wc -l

# Clear cache
rm -rf ~/.claude-code/nsip-cache/*

# Find old cache files (>60 minutes)
find ~/.claude-code/nsip-cache/ -mmin +60
```

#### CSV Exporter (`csv_exporter.py`)

**Purpose**: Export search results to CSV for analysis in spreadsheet tools.

**Triggers on**: `nsip_search_animals`

**What it does**:
- Auto-flattens nested JSON data structures
- Exports to timestamped CSV files
- Handles complex trait data
- Creates human-readable column names

**Export Location**: `~/.claude-code/nsip-exports/`

**Filename Format**: `nsip_search_animals_YYYYMMDD_HHMMSS.csv`

**Example Export**:
```csv
lpn_id,breed_name,sex,birth_weight_kg,fleece_weight_kg,fiber_diameter_micron
6####92020###249,Merino,Male,4.5,5.2,19.5
6####92020###250,Merino,Female,4.1,4.8,18.9
```

**Use Cases**:
- Bulk data analysis
- Breeding program spreadsheets
- Third-party tool integration
- Backup/archival

#### Pedigree Visualizer (`pedigree_visualizer.py`)

**Purpose**: Generate ASCII art family trees from lineage data.

**Triggers on**: `nsip_get_lineage`

**What it does**:
- Creates visual pedigree trees
- Shows parent-offspring relationships
- Multiple format options
- Exports to text files

**Export Location**: `~/.claude-code/nsip-exports/pedigree_*.txt`

**Filename Format**: `pedigree_{lpn_id}_{timestamp}.txt`

**Example Output**:
```
Pedigree for: 6####92020###249 (Merino Ram)
Generated: 2025-10-13 14:30:45

                    ┌─ Grandsire A (6####92018###100)
        ┌─ Sire B (6####92019###150)
        │           └─ Granddam C (6####92018###101)
Animal D (6####92020###249)
        │           ┌─ Grandsire E (6####92018###102)
        └─ Dam F (6####92019###151)
                    └─ Granddam G (6####92018###103)

Statistics:
- Generations: 3
- Total Ancestors: 7
- Breed Consistency: 100% Merino
```

**Format Options**:
- **Tree**: Visual hierarchy (shown above)
- **Compact**: Space-efficient listing
- **Detailed**: With traits and dates

**Use Cases**:
- Breeding decisions
- Genetic diversity analysis
- Documentation
- Presentations

#### Breeding Report (`breeding_report.py`)

**Purpose**: Create comprehensive Markdown breeding analysis reports.

**Triggers on**: `nsip_search_animals`, `nsip_get_animal`, `nsip_get_lineage`

**What it does**:
- Analyzes trait distributions
- Provides breeding recommendations
- Compares animals
- Generates formatted reports

**Export Location**: `~/.claude-code/nsip-exports/breeding_report_*.md`

**Filename Format**: `breeding_report_{timestamp}.md`

**Example Report Structure**:
```markdown
# Breeding Analysis Report
Generated: 2025-10-13 14:30:45

## Search Summary
- Query: Merino sheep, fleece weight > 5kg
- Results: 45 animals
- Breeds: Merino (100%)

## Trait Analysis

### Fleece Weight (kg)
- Mean: 5.8
- Range: 5.1 - 7.2
- Std Dev: 0.6
- Top 10%: > 6.5kg

### Fiber Diameter (microns)
- Mean: 19.2
- Range: 17.5 - 21.8
- Std Dev: 1.2
- Finer than average: 23 animals (51%)

## Breeding Recommendations

### For Wool Production
**Top Candidates** (fleece weight + fiber quality):
1. 6####92020###249 - 7.2kg @ 18.5μ
2. 6####92020###250 - 6.9kg @ 18.9μ
3. 6####92020###251 - 6.7kg @ 19.1μ

### Genetic Diversity
- Recommend: Cross different bloodlines
- Avoid: Inbreeding coefficient > 0.25

## Notes
- Data current as of: 2025-10-10
- All measurements: 12-month benchmarks
```

**Report Sections**:
- Search summary
- Trait distributions
- Top performers
- Breeding recommendations
- Genetic notes
- Caveats/limitations

**Use Cases**:
- Breeding program planning
- Animal selection
- Client reports
- Documentation

---

### UserPromptSubmit Hooks

Execute when users submit prompts, before Claude processes them. Enable workflow intelligence and proactive assistance.

#### Smart Search Detector (`smart_search_detector.py`)

**Purpose**: Detect LPN IDs in user prompts and suggest appropriate tools.

**Triggers on**: All user prompt submissions

**What it does**:
- Scans prompts for LPN ID patterns
- Detects user intent: search, lineage, progeny, comparison
- Suggests most relevant NSIP tools
- Logs detected IDs for tracking

**Detection Patterns**:
```
LPN ID Formats:
- Full: "6####92020###249"
- Partial: "621879202000024"
- Multiple: "Compare 6####92020###249 and 6####92020###250"
```

**Intent Detection**:
- **Search Intent**: "find", "search", "lookup"
- **Lineage Intent**: "parents", "ancestry", "pedigree", "lineage"
- **Progeny Intent**: "offspring", "children", "progeny", "descendants"
- **Comparison Intent**: Multiple LPN IDs mentioned

**Log Location**: `~/.claude-code/nsip-logs/detected_ids.jsonl`

**Example Detection**:
```
User Prompt: "Show me the lineage for 6####92020###249"

Detected:
- LPN ID: 6####92020###249
- Intent: lineage
- Suggested Tool: nsip_get_lineage
- Confidence: High
```

**Example Log Entry**:
```json
{
  "timestamp": "2025-10-13T14:30:45.123Z",
  "prompt": "Show me the lineage for 6####92020###249",
  "detected_lpns": ["6####92020###249"],
  "intent": "lineage",
  "suggested_tool": "nsip_get_lineage",
  "confidence": "high"
}
```

**Benefits**:
- Faster workflow execution
- Reduced user friction
- Better tool utilization
- Proactive assistance

**Troubleshooting**:
```bash
# View detection history
tail -f ~/.claude-code/nsip-logs/detected_ids.jsonl

# Count detections by intent
jq -r '.intent' ~/.claude-code/nsip-logs/detected_ids.jsonl | sort | uniq -c

# Find misdetections (review confidence scores)
jq 'select(.confidence == "low")' ~/.claude-code/nsip-logs/detected_ids.jsonl
```

#### Comparative Analyzer (`comparative_analyzer.py`)

**Purpose**: Identify multi-animal comparison requests and suggest workflows.

**Triggers on**: User prompts mentioning 2+ animals

**What it does**:
- Detects multiple animal references
- Identifies comparison intent keywords
- Determines trait focus (weight, wool, meat, etc.)
- Suggests comparison workflows

**Comparison Detection**:
```
Keywords: "compare", "versus", "vs", "better", "which"
Patterns: 2+ LPN IDs, breed names, or animal descriptors
```

**Trait Focus Detection**:
- **Weight Focus**: birth weight, weaning weight, growth
- **Wool Focus**: fleece weight, fiber diameter, staple
- **Meat Focus**: eye muscle, fat depth, carcass
- **Overall**: multiple trait categories or general comparison

**Example Scenarios**:

**Scenario 1: Direct LPN Comparison**
```
User Prompt: "Compare 6####92020###249 vs 6####92020###250 for wool production"

Detected:
- LPN IDs: 2 animals
- Intent: comparison
- Trait Focus: wool (fleece weight, fiber diameter)
- Suggested Workflow:
  1. Get animal data for both LPNs
  2. Extract wool traits
  3. Generate comparison table
  4. Provide recommendations
```

**Scenario 2: Breed Comparison**
```
User Prompt: "Which is better for meat: Dorper or White Suffolk?"

Detected:
- Breeds: Dorper, White Suffolk
- Intent: comparison
- Trait Focus: meat (eye muscle, carcass weight)
- Suggested Workflow:
  1. Search animals by breed
  2. Calculate trait averages
  3. Compare breed performance
  4. Provide breeding recommendations
```

**Scenario 3: Trait-Specific Comparison**
```
User Prompt: "Show me rams with better fleece weight than 6####92020###249"

Detected:
- Reference LPN: 6####92020###249
- Intent: comparison (better than)
- Trait Focus: wool (fleece weight)
- Suggested Workflow:
  1. Get reference animal traits
  2. Search for rams with higher fleece weight
  3. Filter by breed if specified
  4. Return ranked results
```

**Workflow Suggestions**:

The hook provides structured workflow suggestions based on comparison type:

```json
{
  "comparison_type": "direct",
  "workflow": [
    {
      "step": 1,
      "tool": "nsip_get_animal",
      "parameters": ["lpn_id_1", "lpn_id_2"],
      "description": "Fetch data for both animals"
    },
    {
      "step": 2,
      "tool": "internal",
      "action": "extract_traits",
      "focus": ["fleece_weight", "fiber_diameter"],
      "description": "Extract wool-related traits"
    },
    {
      "step": 3,
      "tool": "internal",
      "action": "generate_comparison",
      "format": "table",
      "description": "Create side-by-side comparison"
    },
    {
      "step": 4,
      "tool": "breeding_report",
      "description": "Generate recommendation report"
    }
  ]
}
```

**Benefits**:
- Intelligent workflow routing
- Trait-aware comparisons
- Structured analysis
- Breeding recommendations

**Troubleshooting**:
```bash
# View comparison detection log
tail -f ~/.claude-code/nsip-logs/comparative_analysis.jsonl

# Common issues:
# 1. Single animal mentioned - not enough for comparison
# 2. Ambiguous trait focus - hook suggests general comparison
# 3. Invalid LPN IDs - caught by LPN Validator in PreToolUse
```

---

## Hook Locations

```
plugins/nsip/hooks/
├── README.md                           # This file
├── hooks.json                          # Hook configuration
└── scripts/
    ├── api_health_check.py             # SessionStart
    ├── lpn_validator.py                # PreToolUse
    ├── breed_context_injector.py       # PreToolUse
    ├── trait_dictionary.py             # PreToolUse
    ├── auto_retry.py                   # PostToolUse
    ├── fallback_cache.py               # PostToolUse
    ├── error_notifier.py               # PostToolUse
    ├── query_logger.py                 # PostToolUse
    ├── result_cache.py                 # PostToolUse
    ├── csv_exporter.py                 # PostToolUse
    ├── pedigree_visualizer.py          # PostToolUse
    ├── breeding_report.py              # PostToolUse
    ├── smart_search_detector.py        # UserPromptSubmit
    └── comparative_analyzer.py         # UserPromptSubmit
```

## Data Locations

### Query Logs
- **Path**: `~/.claude-code/nsip-logs/query_log.jsonl`
- **Format**: JSONL (one JSON object per line)
- **Rotation**: None (manual cleanup required)
- **Size Management**: Monitor with `du -sh ~/.claude-code/nsip-logs/`

### Retry Logs
- **Path**: `~/.claude-code/nsip-logs/retry_log.jsonl`
- **Purpose**: Track auto-retry attempts
- **Retention**: Recommend 30 days

### Fallback Logs
- **Path**: `~/.claude-code/nsip-logs/fallback_log.jsonl`
- **Purpose**: Track fallback cache usage
- **Retention**: Recommend 7 days

### Alert Files
- **Path**: `~/.claude-code/nsip-logs/ALERT_*.txt`
- **Pattern**: `ALERT_YYYYMMDD_HHMMSS.txt`
- **Purpose**: Critical error notifications
- **Action Required**: Review and resolve issues
- **Cleanup**: Delete after resolution (or 7 days)

### Detection Logs
- **Path**: `~/.claude-code/nsip-logs/detected_ids.jsonl`
- **Purpose**: Smart search detection tracking
- **Retention**: Recommend 30 days

### Cache Files
- **Path**: `~/.claude-code/nsip-cache/`
- **Format**: JSON files with SHA-256 hashed filenames
- **TTL**: 60 minutes
- **Cleanup**: Automatic on expiration

### CSV Exports
- **Path**: `~/.claude-code/nsip-exports/`
- **Format**: CSV with flattened nested data
- **Naming**: `{tool_name}_{timestamp}.csv`
- **Cleanup**: Manual

### Pedigree Visualizations
- **Path**: `~/.claude-code/nsip-exports/pedigree_*.txt`
- **Format**: ASCII art text files
- **Naming**: `pedigree_{lpn_id}_{timestamp}.txt`
- **Cleanup**: Manual

### Breeding Reports
- **Path**: `~/.claude-code/nsip-exports/breeding_report_*.md`
- **Format**: Markdown
- **Naming**: `breeding_report_{timestamp}.md`
- **Cleanup**: Manual

## Hook Execution Flow

### Validation Flow (PreToolUse)

```
Tool Call Request
    ↓
LPN Validator Hook → Validate format
    ↓
Breed Context Injector → Add breed characteristics
    ↓
Trait Dictionary → Add trait definitions
    ↓
Valid? → Yes → Continue to API
    ↓
    No → Block Call → Return Error
```

### Error Resilience Flow (PostToolUse)

```
Tool Call Completes
    ↓
Auto Retry Hook → Retry if failed (3 attempts)
    ↓
Fallback Cache Hook → Use cache if still failed
    ↓
Error Notifier Hook → Track failures, create alerts
    ↓
Return Result to User
```

### Logging & Export Flow (PostToolUse)

```
Tool Call Completes
    ↓
Query Logger Hook → Log to JSONL
    ↓
Result Cache Hook → Cache if applicable
    ↓
CSV Exporter Hook → Export if search
    ↓
Pedigree Visualizer → Generate tree if lineage
    ↓
Breeding Report → Create analysis if applicable
    ↓
Return Result to User
```

### User Prompt Flow (UserPromptSubmit)

```
User Submits Prompt
    ↓
Smart Search Detector → Detect LPN IDs & intent
    ↓
Comparative Analyzer → Detect comparison requests
    ↓
Suggest Tools/Workflows
    ↓
Claude Processes Prompt
```

### Health Check Flow (SessionStart)

```
Claude Code Session Starts
    ↓
API Health Check Hook
    ↓
Call: http://nsipsearch.nsip.org/api/GetLastUpdate
    ↓
Success? → Yes → Continue silently
    ↓
    No → Display warning → Continue anyway
```

## Error Handling

All hooks follow fail-safe principles:

1. **Never block execution on hook errors** (except PreToolUse validation)
2. **Log errors but continue**
3. **Return metadata about hook status**
4. **Graceful degradation**

Example error response:
```json
{
  "continue": true,
  "metadata": {
    "logged": false,
    "error": "Permission denied writing to log file"
  }
}
```

## Performance Impact

| Hook | Overhead | When | Notes |
|------|----------|------|-------|
| API Health Check | ~100ms | Once per session | Timeout at 5s |
| LPN Validator | <1ms | Before validated calls | Regex check only |
| Breed Context Injector | <5ms | Before searches | In-memory lookup |
| Trait Dictionary | <2ms | On trait detection | In-memory lookup |
| Auto Retry | 0-7s | On failures only | 3 attempts max |
| Fallback Cache | <10ms | On API failure | File I/O |
| Error Notifier | <5ms | On errors only | File write |
| Query Logger | <5ms | After all calls | Async write |
| Result Cache | <2ms | After cached calls | SHA-256 + write |
| CSV Exporter | 10-50ms | After searches only | Data flattening |
| Pedigree Visualizer | 20-100ms | After lineage calls | Tree generation |
| Breeding Report | 50-200ms | After analysis calls | MD generation |
| Smart Search Detector | <5ms | Every prompt | Regex scanning |
| Comparative Analyzer | <10ms | Every prompt | Multi-pattern match |

**Total overhead**: <2% for typical usage (excluding retry delays on failures)

## Installation

Hooks are automatically loaded when the NSIP plugin is installed. No manual setup required.

```bash
/plugin install nsip
```

## Configuration

Hook configuration is stored in `hooks.json`:

```json
{
  "PreToolUse": [
    "lpn_validator.py",
    "breed_context_injector.py",
    "trait_dictionary.py"
  ],
  "PostToolUse": [
    "auto_retry.py",
    "fallback_cache.py",
    "error_notifier.py",
    "query_logger.py",
    "result_cache.py",
    "csv_exporter.py",
    "pedigree_visualizer.py",
    "breeding_report.py"
  ],
  "SessionStart": [
    "api_health_check.py"
  ],
  "UserPromptSubmit": [
    "smart_search_detector.py",
    "comparative_analyzer.py"
  ]
}
```

## Debugging Hooks

### Enable verbose logging

```bash
# Check query log
tail -f ~/.claude-code/nsip-logs/query_log.jsonl

# Check retry log
tail -f ~/.claude-code/nsip-logs/retry_log.jsonl

# Check fallback log
tail -f ~/.claude-code/nsip-logs/fallback_log.jsonl

# Check detection log
tail -f ~/.claude-code/nsip-logs/detected_ids.jsonl

# View cache statistics
ls -lh ~/.claude-code/nsip-cache/
du -sh ~/.claude-code/nsip-cache/

# Check exports
ls -lt ~/.claude-code/nsip-exports/

# View recent alerts
ls -lt ~/.claude-code/nsip-logs/ALERT_*.txt | head -5
```

### Test individual hooks

```bash
# Test LPN validator
echo '{"tool":{"name":"nsip_get_animal","parameters":{"lpn_id":"123"}}}' | \
  python3 scripts/lpn_validator.py

# Test API health check
python3 scripts/api_health_check.py

# Test smart search detector
echo '{"prompt":"Show me lineage for 6####92020###249"}' | \
  python3 scripts/smart_search_detector.py

# Test comparative analyzer
echo '{"prompt":"Compare 6####92020###249 vs 6####92020###250"}' | \
  python3 scripts/comparative_analyzer.py
```

### Common Issues

#### Hooks not executing
- Check: `hooks.json` syntax is valid
- Check: Scripts have execute permissions
- Check: Python 3 is available
- Verify: `python3 --version`

#### Permission denied errors
- Check: `~/.claude-code/` directory permissions
- Solution: `chmod 755 ~/.claude-code/`
- Check subdirectories: `nsip-logs/`, `nsip-cache/`, `nsip-exports/`

#### Cache not working
- Check: Available disk space (`df -h ~`)
- Check: `~/.claude-code/nsip-cache/` exists and is writable
- Clear cache: `rm -rf ~/.claude-code/nsip-cache/*`
- Test write: `touch ~/.claude-code/nsip-cache/test.txt`

#### Retry failures
- Check retry log: `tail ~/.claude-code/nsip-logs/retry_log.jsonl`
- Verify API connectivity: `curl http://nsipsearch.nsip.org/api/GetLastUpdate`
- Check timeout settings (default: 5s per attempt)

#### Alert overload
- Too many alerts: Check if API is actually down
- Clear old alerts: `rm ~/.claude-code/nsip-logs/ALERT_*.txt`
- Review patterns: `grep "Common Errors" ~/.claude-code/nsip-logs/ALERT_*.txt`

#### Export file accumulation
- Large exports directory: Review and archive old files
- Compress old exports: `gzip ~/.claude-code/nsip-exports/*.csv`
- Archive: `mv ~/.claude-code/nsip-exports/old_*.* ~/nsip-archives/`

#### Prompt detection issues
- False positives: Review detection log for patterns
- Missed LPNs: Check format variations in log
- Intent misclassification: Review confidence scores

## Maintenance

### Clear cache

```bash
# Clear all cache
rm -rf ~/.claude-code/nsip-cache/*

# Clear old cache (>24 hours)
find ~/.claude-code/nsip-cache/ -mtime +1 -delete
```

### Archive logs

```bash
# Archive query log
mv ~/.claude-code/nsip-logs/query_log.jsonl \
   ~/.claude-code/nsip-logs/query_log.$(date +%Y%m%d).jsonl

# Archive retry log
mv ~/.claude-code/nsip-logs/retry_log.jsonl \
   ~/.claude-code/nsip-logs/retry_log.$(date +%Y%m%d).jsonl

# Archive detection log
mv ~/.claude-code/nsip-logs/detected_ids.jsonl \
   ~/.claude-code/nsip-logs/detected_ids.$(date +%Y%m%d).jsonl

# Compress old logs
gzip ~/.claude-code/nsip-logs/*.jsonl.*
```

### Clear old alerts

```bash
# Remove alerts older than 7 days
find ~/.claude-code/nsip-logs/ -name "ALERT_*.txt" -mtime +7 -delete

# Archive resolved alerts
mkdir -p ~/.claude-code/nsip-logs/resolved/
mv ~/.claude-code/nsip-logs/ALERT_*.txt ~/.claude-code/nsip-logs/resolved/
```

### Manage exports

```bash
# List exports by size
ls -lhS ~/.claude-code/nsip-exports/

# Archive old exports (>30 days)
find ~/.claude-code/nsip-exports/ -mtime +30 -exec mv {} ~/nsip-archives/ \;

# Compress old exports
gzip ~/.claude-code/nsip-exports/*_2025*.csv
```

### View statistics

```bash
# Cache statistics
du -sh ~/.claude-code/nsip-cache/
ls ~/.claude-code/nsip-cache/ | wc -l

# Log statistics
wc -l ~/.claude-code/nsip-logs/*.jsonl

# Export statistics
ls ~/.claude-code/nsip-exports/ | wc -l
du -sh ~/.claude-code/nsip-exports/

# Error statistics
jq 'select(.success == false)' ~/.claude-code/nsip-logs/query_log.jsonl | \
  jq -r '.error' | sort | uniq -c | sort -rn
```

## Development

### Adding New Hooks

1. Create Python script in `scripts/`
2. Add entry to `hooks.json`
3. Follow hook interface (see below)
4. Test thoroughly
5. Document in this README

### Hook Interface

**Input** (stdin):
```json
{
  "tool": {
    "name": "mcp__nsip__nsip_get_animal",
    "parameters": {"lpn_id": "..."}
  },
  "result": {...},  // PostToolUse only
  "metadata": {...},
  "prompt": "..."   // UserPromptSubmit only
}
```

**Output** (stdout):
```json
{
  "continue": true,  // or false to block (PreToolUse only)
  "error": "...",    // if continue=false
  "warning": "...",  // optional warning message
  "metadata": {...}, // custom metadata
  "suggestions": {   // UserPromptSubmit only
    "tools": [...],
    "workflow": [...]
  }
}
```

### Testing Hooks

```bash
# Run hook with test input
cat test_input.json | python3 scripts/query_logger.py

# Check exit code
echo $?  # Should be 0

# Validate JSON output
cat test_input.json | python3 scripts/query_logger.py | jq .

# Test all hooks
for hook in scripts/*.py; do
  echo "Testing $hook..."
  cat test_input.json | python3 "$hook" | jq .
done
```

### Hook Development Best Practices

1. **Fail-safe**: Never crash on invalid input
2. **Fast**: Keep overhead <10ms for common operations
3. **Logged**: Log important operations for debugging
4. **Tested**: Include test cases and example inputs
5. **Documented**: Clear docstrings and README updates
6. **Typed**: Use type hints for parameters and returns
7. **Validated**: Validate all inputs before processing
8. **Graceful**: Return meaningful errors, don't throw exceptions

## Security Considerations

- **No sensitive data**: NSIP API requires no authentication
- **Local file access**: All data stored in user's home directory
- **No network calls**: Except API health check to public endpoint
- **No data transmission**: Hooks operate locally only
- **File permissions**: Respect user's umask settings
- **Path traversal**: All paths validated and sanitized
- **Input validation**: All hook inputs validated before processing

## Troubleshooting Guide

### Scenario: All hooks not working

**Symptoms**: No logs, no cache, no exports

**Diagnosis**:
```bash
# Check directory exists
ls -la ~/.claude-code/

# Check permissions
ls -la ~/.claude-code/ | grep nsip

# Test write access
touch ~/.claude-code/test.txt && rm ~/.claude-code/test.txt
```

**Solutions**:
1. Create directory: `mkdir -p ~/.claude-code/{nsip-logs,nsip-cache,nsip-exports}`
2. Fix permissions: `chmod -R 755 ~/.claude-code/`
3. Check disk space: `df -h ~`

### Scenario: Hooks working but performance slow

**Symptoms**: Noticeable delays in responses

**Diagnosis**:
```bash
# Check cache size
du -sh ~/.claude-code/nsip-cache/

# Check export count
ls ~/.claude-code/nsip-exports/ | wc -l

# Check log sizes
ls -lh ~/.claude-code/nsip-logs/
```

**Solutions**:
1. Clear old cache: `find ~/.claude-code/nsip-cache/ -mtime +1 -delete`
2. Archive exports: `mv ~/.claude-code/nsip-exports/*.csv ~/archives/`
3. Rotate logs: See maintenance section above

### Scenario: Frequent retries and alerts

**Symptoms**: Multiple ALERT files, slow responses

**Diagnosis**:
```bash
# Check API status
curl -w "\n%{http_code}\n" http://nsipsearch.nsip.org/api/GetLastUpdate

# Review retry log
tail -20 ~/.claude-code/nsip-logs/retry_log.jsonl

# Count recent failures
jq -r '.timestamp' ~/.claude-code/nsip-logs/retry_log.jsonl | \
  grep $(date +%Y-%m-%d) | wc -l
```

**Solutions**:
1. If API down: Wait for service restoration
2. If network issue: Check firewall/proxy settings
3. If persistent: Report to NSIP API maintainers

### Scenario: Exports not generating

**Symptoms**: No CSV/pedigree/report files created

**Diagnosis**:
```bash
# Check export directory
ls -la ~/.claude-code/nsip-exports/

# Check query log for export attempts
grep "csv_exporter\|pedigree_visualizer\|breeding_report" \
  ~/.claude-code/nsip-logs/query_log.jsonl | tail -10
```

**Solutions**:
1. Verify tool called correctly (e.g., `nsip_search_animals` for CSV)
2. Check write permissions: `touch ~/.claude-code/nsip-exports/test.txt`
3. Review hook logs for errors

### Scenario: Smart detection missing LPNs

**Symptoms**: LPN IDs in prompts not detected

**Diagnosis**:
```bash
# Check detection log
tail ~/.claude-code/nsip-logs/detected_ids.jsonl

# Test detector manually
echo '{"prompt":"Get data for 6####92020###249"}' | \
  python3 scripts/smart_search_detector.py | jq .
```

**Solutions**:
1. Verify LPN format matches patterns (see hook documentation)
2. Check detection log for patterns
3. Use explicit tool calls if detection unreliable

## Support

For issues or questions:
- **Repository**: https://github.com/epicpast/marketplace
- **NSIP API**: https://github.com/epicpast/nsip-api-client
- **Plugin Issues**: https://github.com/epicpast/marketplace/issues

## Version

Current hooks version: **2.0.0**

**Changelog**:
- **2.0.0**: Added 10 new hooks (15 total), UserPromptSubmit lifecycle
  - New: Auto Retry, Fallback Cache, Error Notifier
  - New: Breed Context Injector, Trait Dictionary
  - New: Pedigree Visualizer, Breeding Report
  - New: Smart Search Detector, Comparative Analyzer
- **1.0.0**: Initial release with 5 hooks

Compatible with NSIP plugin version: **1.3.0+**

## License

Same license as the NSIP plugin and marketplace repository.
