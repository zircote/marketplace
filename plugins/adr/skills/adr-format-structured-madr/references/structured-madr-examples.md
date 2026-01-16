# Structured MADR Examples

Real-world examples of well-written Structured MADR ADRs.

## Example 1: Technology Selection (Comprehensive)

```markdown
---
title: "Rust as Implementation Language"
description: "Decision to rewrite the system from Python to Rust for improved performance and distribution."
type: adr
category: architecture
tags:
  - rust
  - language-choice
  - performance
  - rewrite
status: accepted
created: 2025-12-28
updated: 2026-01-04
author: Architecture Team
project: subcog
technologies:
  - rust
  - tokio
  - python
audience:
  - developers
  - architects
---

# ADR-0001: Rust as Implementation Language

## Status

Accepted

## Context

### Background and Problem Statement

The original implementation was written in Python as a proof-of-concept. While it validated the core architecture, it exhibited fundamental limitations that constrain long-term viability as a production tool.

### Current Limitations

1. **Complex Distribution**: Python requires runtime, pip, virtual environments
2. **Startup Latency**: Cold start times exceeding 500ms
3. **GIL Constraints**: Cannot utilize multi-core for CPU-bound operations
4. **Runtime Type Safety**: Type errors manifest at runtime

## Decision Drivers

### Primary Decision Drivers

1. **Single-Binary Distribution**: Must distribute as single executable under 100MB
2. **Sub-10ms Cold Start**: Enable seamless integration with hooks
3. **True Parallelism**: Utilize multiple CPU cores

### Secondary Decision Drivers

1. **Compiler-Enforced Quality**: Clippy lints catch subtle issues
2. **Cross-Platform Compilation**: Build for multiple platforms from one machine

## Considered Options

### Option 1: Rust

**Description**: Complete rewrite using tokio for async, fastembed for embeddings.

**Technical Characteristics**:
- Compiled to native machine code
- Ownership system for memory safety
- Zero-cost abstractions

**Advantages**:
- Single static binary (~60MB)
- Cold start under 10ms
- No garbage collection pauses

**Disadvantages**:
- Steeper learning curve
- Longer compilation times
- Smaller ML ecosystem

**Risk Assessment**:
- **Technical Risk**: Low. Rust is mature and well-documented.
- **Schedule Risk**: Medium. Initial development takes longer.
- **Ecosystem Risk**: Low. Required libraries available.

### Option 2: Go

**Description**: Rewrite using goroutines with CGO bridges for embeddings.

**Technical Characteristics**:
- Compiled to native machine code
- Built-in goroutines and channels
- Garbage collected

**Advantages**:
- Simple syntax
- Fast compilation
- Single binary distribution

**Disadvantages**:
- GC pauses of 10-100ms conflict with sub-10ms requirement
- CGO required for embeddings adds complexity

**Disqualifying Factor**: GC pause times directly conflict with sub-10ms cold start requirement.

**Risk Assessment**:
- **Technical Risk**: Medium. CGO bridges add complexity.
- **Schedule Risk**: Low. Gentle learning curve.
- **Ecosystem Risk**: High. No native embedding library.

## Decision

We will rewrite the entire system in Rust.

The implementation will use:
- **tokio** for async runtime with multi-threaded scheduler
- **rusqlite** for persistence and FTS5 full-text indexing
- **fastembed** for local embedding generation
- **usearch** for HNSW vector search

## Consequences

### Positive

1. **Single Binary Distribution**: Release build produces ~60MB binary with all features
2. **50x Startup Improvement**: Cold start reduced from ~500ms to ~10ms
3. **True Parallelism**: Full multi-core utilization via tokio

### Negative

1. **Extended Development Time**: ~3x longer initial development
2. **Steeper Learning Curve**: Contributors must understand ownership model
3. **Reduced ML Ecosystem**: Fewer libraries than Python

### Neutral

1. **Architecture Already Validated**: Python proof-of-concept validated design

## Decision Outcome

The Rust rewrite achieved primary objectives:
- Distribution: Single binary of ~60MB
- Startup: Cold start under 10ms
- Parallelism: Full multi-core utilization

Mitigations:
- Document ownership patterns for contributors
- Use fastembed for embedding needs

## Related Decisions

- [ADR-0002: Three-Layer Storage](adr_0002.md) - Leverages Rust trait system
- [ADR-0003: Feature Tier System](adr_0003.md) - Enabled by Cargo features

## Links

- [fastembed crate](https://crates.io/crates/fastembed) - Native embedding generation
- [tokio runtime](https://tokio.rs/) - Async runtime

## More Information

- **Date:** 2025-12-28
- **Source:** SPEC-2025-12-28: System Rewrite
- **Related ADRs:** ADR-0002, ADR-0003, ADR-0004

## Audit

### 2026-01-04

**Status:** Compliant

**Findings:**

| Finding | Files | Lines | Assessment |
|---------|-------|-------|------------|
| Rust crate defined | `Cargo.toml` | L1-L22 | compliant |
| tokio async runtime | `src/main.rs` | L15-L30 | compliant |

**Summary:** Implementation confirms language decision.

**Action Required:** None
```

## Example 2: API Design Decision (Concise)

```markdown
---
title: "Score Normalization to 0.0-1.0 Range"
description: "Use linear normalization for intuitive relevance scores."
type: adr
category: search
tags:
  - normalization
  - scoring
  - user-experience
status: accepted
created: 2026-01-02
updated: 2026-01-04
author: Search Team
project: subcog
technologies:
  - rust
audience:
  - developers
---

# ADR-0035: Score Normalization to 0.0-1.0 Range

## Status

Accepted

## Context

### Background and Problem Statement

The RRF implementation produces scores in range 0.0-0.033. Users expect 0.0-1.0 where higher means more relevant.

### Current Limitations

Raw RRF scores are unintuitive and not user-friendly.

## Decision Drivers

### Primary Decision Drivers

1. **User Experience**: Intuitive score interpretation
2. **Simplicity**: Easy to implement and understand

### Secondary Decision Drivers

1. **Debugging**: Preserve raw scores for analysis

## Considered Options

### Option 1: Linear Normalization

**Description**: Scale to 0.0-1.0 based on maximum score.

**Advantages**:
- Users see intuitive scores
- Top result always scores 1.0
- Preserves relative ordering

**Disadvantages**:
- Scores not comparable across queries
- May mask quality differences

**Risk Assessment**:
- **Technical Risk**: Low
- **Schedule Risk**: Low
- **Ecosystem Risk**: Low

### Option 2: No Normalization

**Description**: Return raw RRF scores.

**Advantages**:
- Scores comparable across queries
- No information loss

**Disadvantages**:
- Unintuitive for users
- Requires documentation

**Risk Assessment**:
- **Technical Risk**: Low
- **Schedule Risk**: Low
- **Ecosystem Risk**: Low

## Decision

We will use linear normalization based on maximum score in result set.

```rust
fn normalize(results: &[SearchHit]) -> Vec<SearchResult> {
    let max = results.iter().map(|r| r.score).fold(0.0, f32::max);
    results.iter().map(|r| SearchResult {
        score: if max > 0.0 { r.score / max } else { 0.0 },
        raw_score: r.score,
    }).collect()
}
```

## Consequences

### Positive

1. **Intuitive Scores**: Users understand 0.0-1.0 range
2. **Clear Top Result**: Best match always shows 1.0

### Negative

1. **Cross-Query Comparison**: Scores not comparable between queries

### Neutral

1. **Raw Score Available**: Debugging still possible via `raw_score`

## Decision Outcome

Linear normalization provides best UX for within-query relevance.

Mitigations:
- Return `raw_score` alongside normalized score
- Add `--raw` CLI flag for power users

## Related Decisions

None currently documented.

## Links

- [RRF Algorithm](https://example.com/rrf) - Background on ranking

## More Information

- **Date:** 2026-01-02
- **Source:** SPEC-2026-01-02: Search Improvements

## Audit

### 2026-01-04

**Status:** Compliant

**Findings:**

| Finding | Files | Lines | Assessment |
|---------|-------|-------|------------|
| normalize_scores scales max to 1.0 | `src/services/recall.rs` | L736-L782 | compliant |

**Summary:** Normalization implemented as specified.

**Action Required:** None
```

## Example 3: Migration Decision (Simple)

```markdown
---
title: "Fresh Start - No Migration of Legacy Data"
description: "Take fresh start with no automatic migration of legacy data."
type: adr
category: migration
tags:
  - migration
  - fresh-start
  - breaking-change
status: accepted
created: 2026-01-03
updated: 2026-01-04
author: Architecture Team
project: subcog
audience:
  - developers
related:
  - adr_0039.md
---

# ADR-0050: Fresh Start - No Migration of Legacy Data

## Status

Accepted

## Context

### Background and Problem Statement

There are 645 memories in existing storage from earlier tooling. Migration would require significant effort.

### Current Limitations

Earlier tooling used incompatible storage format.

## Decision Drivers

### Primary Decision Drivers

1. **Development Effort**: Migration code is complex
2. **Data Quality**: Legacy data may be corrupted

### Secondary Decision Drivers

1. **User Request**: Fresh start is acceptable per user feedback

## Considered Options

### Option 1: Fresh Start

**Description**: No automatic migration.

**Advantages**:
- No complex migration code
- No risk of data corruption
- Clean slate

**Disadvantages**:
- Historical data not immediately available
- Manual re-capture needed

**Risk Assessment**:
- **Technical Risk**: Low
- **Schedule Risk**: Low
- **Ecosystem Risk**: Low

### Option 2: Build Migration Tooling

**Description**: Extract and re-import legacy data.

**Advantages**:
- Preserve historical decisions

**Disadvantages**:
- Complex to build
- Risk of data corruption

**Risk Assessment**:
- **Technical Risk**: High
- **Schedule Risk**: High
- **Ecosystem Risk**: Low

## Decision

We will take a fresh start - no automatic migration of legacy data.

## Consequences

### Positive

1. **No Migration Code**: Eliminates maintenance burden
2. **Clean Architecture**: Known-good data from start

### Negative

1. **Manual Effort**: Users must re-capture important memories

### Neutral

1. **Legacy Preserved**: Old data remains accessible in history

## Decision Outcome

Fresh start eliminates migration complexity and ensures data quality.

Mitigations:
- Legacy data remains in repository history
- Future "import" command possible if demand exists

## Related Decisions

- [ADR-0039: Backward Compatibility](adr_0039.md) - Now moot

## Links

None.

## More Information

- **Date:** 2026-01-03
- **Source:** SPEC-2026-01-03: Storage Simplification

## Audit

### 2026-01-04

**Status:** Compliant

**Findings:**

| Finding | Files | Lines | Assessment |
|---------|-------|-------|------------|
| No legacy migration code | `src/commands/` | all | compliant |

**Summary:** No legacy migration as specified.

**Action Required:** None
```
