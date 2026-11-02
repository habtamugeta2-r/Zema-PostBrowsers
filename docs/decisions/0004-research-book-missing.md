# Decision Record 0004 — The research book is missing: keep chapter pointers unresolved, block E3, close Decision C

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 / Gate 0 |
| **Status** | **Accepted** (interim; superseded the moment the book is imported) |
| **Evidence label** | **Proposed** |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); project owner must supply the book or approve retirement at Gate 1 (condition C2) |
| **Input** | [`../../research/phase-00-05-book-import-audit.md`](../../research/phase-00-05-book-import-audit.md) |

## Context

Master Prompt v1.1 and Core Concerns v1.1 both cite a longer research
book — Chapters 1–13, §12.1's ambiguity catalog, Ch. 6's benchmark
protocol, Ch. 7's evidence register (R1–R29), and Ch. 9's experiments
(E1–E5) and decisions (A, B, D). That book is **not in this repository**.

Phase 0's task was to locate or import it, or to mark it missing
explicitly. A reproducible search (owner's 10 public repositories, file
trees, full-text search for the book's distinctive markers) found it in
neither — see the audit record for commands and raw results.

The project therefore faces a fork: fabricate the missing content
(fatal to evidence discipline), silently drop the references (fatal to
traceability), or proceed with the references visibly unresolved.

## Options considered

### Option A — Reuse: import the book now

- What it is: owner supplies the text; commit under `research/book/` with
  a version and visibility note.
- Security cost: none.
- Performance cost: none.
- Fit: **preferred**, and still possible at any time. It requires an
  action only the owner can take.

### Option B — Build on existing foundations: reconstruct only what a
phase actually needs, clearly labeled as *this repository's* text

- What it is: e.g. write a new benchmark protocol for Phase 12 derived
  from the Master Prompt's summary, never attributed to the book.
- Cost: real work, and a permanent attribution hazard.
- Fit: acceptable **only** where a phase blocks; not a substitute for the
  book.

### Option C — Retire the cross-references

- What it is: annotate every "Ch. N" pointer as retired and rely solely on
  Master Prompt v1.1 / Core Concerns v1.1.
- Cost: loses detail the summaries compress (notably §12.1's ambiguity
  list and Ch. 6's protocol).
- Fit: acceptable fallback at **Gate 1** if no book arrives.

### Option D — Ignore the gap and cite chapters as if available

- Fit: **rejected.** It invites fabricated authority and would fail the
  project's own Gate 12 audit.

## Decision

**Choose Option A as the goal, with Option B narrowly permitted and
Option C as the Gate 1 fallback.** Concretely, as of Gate 0:

1. **Chapter pointers stay in the founding documents as unresolved
   pointers.** They are not sources. No claim may cite a chapter as
   evidence (Concern 16 already says a reference establishes background
   at most).
2. **E3 stays `Blocked`.** It is not redefined, renumbered, or deleted.
   Its existence is attested only by a synthesis that "adds no new
   claims", so even its existence is uncertain.
3. **Decision C is closed as unattested.** Only A, B, and D appear
   anywhere. It reopens only if the book names it.
4. **This repository's evidence register is canonical** for what would
   establish each claim (it replaces the book's Ch. 7 role in practice).
5. **The owner has until Gate 1** to import the book (Option A) or
   approve retirement of the pointers (Option C).

## Consequences

- **Positive:** nothing is invented; the gap is auditable by a stranger;
  Phase 1 can start without waiting for a private document.
- **Negative / accepted costs:** §12.1's pre-catalogued ambiguities are
  unavailable, so Phase 1 must derive its own ambiguity list — more work,
  and possibly re-discovering known problems. Phase 12 loses the book's
  fuller benchmark protocol and must use the Master Prompt's summary.
- **New obligations created:**
  - Phase 1 must open its specification with a **derived** ambiguity
    register, marked as derived (not the book's).
  - Phase 12 must record which protocol elements came from the summary
    and which were designed here.
  - `PHASE-TRACKER.md` must keep the E3 row `Blocked` until a gate
    changes it.
- **What would make us revisit this decision:** the book arrives (then
  this record is superseded by a new one, and every reference is
  reconciled against it in a single reviewed change).

## Evidence

- Citations: [`../../research/phase-00-05-book-import-audit.md`](../../research/phase-00-05-book-import-audit.md) §1 (commands and raw results, reproducible); `IMPROVEMENTS.md` §5 items 1–3 (the open items this closes or narrows).
- Experiments: none — this is a provenance decision.
- Related records: [`0001-source-grading.md`](./0001-source-grading.md) (weak sources) and this record (absent sources) are the same discipline applied to two different failures.
