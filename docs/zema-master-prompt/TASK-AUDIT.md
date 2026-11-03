# TASK-AUDIT — all 128 Master Prompt tasks against the repository

| Field | Detail |
|---|---|
| **Document** | Task completion audit: every research and build task in the Master Prompt, marked against evidence that exists |
| **Version** | 1.0.0 |
| **Date** | 2026-11-04 |
| **Status** | Active. Produced by backlog item **B3** |
| **Source of truth** | The 128 tasks are extracted from [`ZEMA-Master-Research-and-Build-Prompt.md`](./ZEMA-Master-Research-and-Build-Prompt.md) by `tools/audit_phase01.py`; this file's status table is checked against that extraction |
| **Machine check** | `task_audit_check()` — fails if a task is in the prompt but not here, or if a `done` claim names a path that does not exist |

> **What this answers.** Nobody had ever added up what the Master Prompt asks
> for. It asks for **128 tasks**: 66 research, 62 build, across Phases 0–14.
> This document marks each one against evidence, so the remaining scope stops
> being an impression and becomes a list.

---

## 1. The headline

| | Tasks | Done | Partial | Not started | Blocked: book |
|---|---:|---:|---:|---:|---:|
| **Research** | 66 | 10 | 6 | 49 | 1 |
| **Build** | 62 | 9 | 1 | 52 | 0 |
| **Total** | **128** | **19** | **7** | **101** | **1** |

These are counted from the tables below by `--check`, not typed. **14.8 % of the
Master Prompt's own tasks are done**, 5.5 % partial, and **79.7 % are untouched.**

The nine completed build tasks are all specification work, not implementation:

| Tasks | What they produced |
|---|---|
| P0.B1, P0.B2 | The problem statement and the evidence register (132 rows, a template, a tool that recomputes its summary) |
| P1.B1…P1.B7 | The grammar, Unicode identifier handling, evaluation order, closures and bounds, `?`/`defer`, inference limits, the operational semantics draft and the conformance plan |

> **A correction to this section's first draft.** It claimed 11/12/43 research
> and 1/0/61 build — i.e. one completed build task. Both were wrong: I had
> forgotten that Phase 1's seven specification tasks count as done, and I typed
> the research split without counting. The measured answer is 19 done overall,
> not 12. This is the fifth time in this project that a hand-typed count was
> wrong, and PR-01 exists for exactly this reason.

## 2. Research tasks (66)

Status vocabulary: `done` · `partial` · `not-started` · `blocked: book`.
`blocked: book` means the task explicitly depends on the research book that
decision 0004 records as absent — it is not the project's omission.

| # | Task (abridged) | Status | Evidence |
|---|---|---|---|
| P0.R1 | Catalog every browser service beyond rendering | done | `research/phase-00-02-browser-services-catalog.md` — 20+ services classified |
| P0.R2 | Classify each service rebuild / interoperate / give up | done | `research/phase-00-02-browser-services-catalog.md` §1–§5 |
| P0.R3 | Define the exact app class targeted | done | `docs/problem-statement.md` §target class |
| P0.R4 | Document the coordination cost of the fragmented stack | done | `research/phase-00-03-coordination-cost.md` |
| P1.R1 | Study the "easy" specification in depth | done | `research/phase-01-01-language-prior-art.md` |
| P1.R2 | Research the type system | done | `research/phase-01-01` §survey; `docs/plain/01-types.md` |
| P1.R3 | Catalog the honest limits | done | `research/phase-01-02-honest-limits.md` |
| P1.R4 | Study deferred features and why each is deferred | done | `docs/plain/04-deferred-features.md` — 20 deferrals |
| P2.R1 | Study static dependency wiring | not-started | No Phase 2 record exists |
| P2.R2 | Research the diamond problem | not-started | No Phase 2 record exists |
| P2.R3 | Study transactional update models | not-started | No Phase 2 record exists |
| P2.R4 | Investigate stable keys and cleanup for list items | not-started | No Phase 2 record exists |
| P2.R5 | Specify equality semantics and reentrancy | partial | Equality is specified for the core (`docs/plain/02` E-08/E-14/E-15); reactive reentrancy is not |
| P2.R6 | Research the reactive cost model | not-started | No Phase 2 record exists |
| P3.R1 | Evaluate three execution paths with security-cost analysis | done | `research/phase-01-06-implementation-feasibility.md`; decision 0013 |
| P3.R2 | Study untrusted-code containment | partial | `research/phase-01-06`; quotas specified for the core (E-33) but not for isolation |
| P3.R3 | Research why raw FFI/C ABI/syscalls must be forbidden | partial | Stated as policy in the Master Prompt; no dedicated research record |
| P4.R1 | Evaluate memory strategies with obligations | not-started | No Phase 4 record exists |
| P4.R2 | Study structured concurrency models | not-started | No Phase 4 record exists |
| P4.R3 | Research why no race-freedom claim is valid without a checked subset | not-started | No Phase 4 record exists |
| P5.R1 | Define the threat model | not-started | No Phase 5 record exists |
| P5.R2 | Study capability handle design | not-started | No Phase 5 record exists |
| P5.R3 | Research network security beyond allowlists | not-started | No Phase 5 record exists |
| P5.R4 | Study unspoofable permission-prompt design | not-started | No Phase 5 record exists |
| P5.R5 | Research bounded parsing of app-controlled input | not-started | No Phase 5 record exists |
| P6.R1 | Study the full rendering pipeline | not-started | No Phase 6 record exists |
| P6.R2 | Evaluate existing rendering stacks | not-started | No Phase 6 record exists |
| P6.R3 | Research CPU/software fallback requirements | not-started | No Phase 6 record exists |
| P6.R4 | Study layout approaches | not-started | No Phase 6 record exists |
| P6.R5 | Research virtualized-list requirements | not-started | No Phase 6 record exists |
| P6.R6 | Define the measurement protocol per pipeline stage | not-started | No Phase 6 record exists |
| P7.R1 | Study Unicode text processing and segmentation | partial | **Unicode data pipeline done** (`src/plain/unicode17*.py`, 16 pinned files verified); segmentation (UAX #29) not started |
| P7.R2 | Evaluate text-shaping engines | not-started | No Phase 7 record exists |
| P7.R3 | Research font-fallback strategies | not-started | No Phase 7 record exists |
| P7.R4 | Study selection and editing by grapheme cluster | not-started | No Phase 7 record exists |
| P7.R5 | Research IME composition and clipboard | not-started | No Phase 7 record exists |
| P7.R6 | Investigate SDF glyph rendering accuracy limits | not-started | No Phase 7 record exists |
| P7.R7 | Define the test matrix of scripts | not-started | No Phase 7 record exists |
| P8.R1 | Study OS accessibility APIs | not-started | No Phase 8 record exists |
| P8.R2 | Research semantic-tree → accessibility-tree mapping | not-started | No Phase 8 record exists |
| P8.R3 | Study keyboard-only operation and focus order | not-started | No Phase 8 record exists |
| P8.R4 | Research screen-reader announcement patterns | not-started | No Phase 8 record exists |
| P8.R5 | Study accessible dialog and error flows | not-started | No Phase 8 record exists |
| P9.R1 | Study SQLite as local truth store | not-started | No Phase 9 record exists |
| P9.R2 | Research durability guarantees honestly | not-started | No Phase 9 record exists |
| P9.R3 | Study the server-authoritative offline model | not-started | No Phase 9 record exists |
| P9.R4 | Research "effectively-once" semantics | not-started | No Phase 9 record exists |
| P9.R5 | Study CRDT limitations honestly | not-started | No Phase 9 record exists |
| P9.R6 | Research version checks and conflict UX | not-started | No Phase 9 record exists |
| P10.R1 | Study HTTPS with existing schema encodings | not-started | No Phase 10 record exists |
| P10.R2 | Evaluate QUIC with TCP fallback | not-started | No Phase 10 record exists |
| P10.R3 | Research requirements for a deferred custom protocol | not-started | Deferred by the Master Prompt itself; no record |
| P10.R4 | Study zero-copy view security | not-started | No Phase 10 record exists |
| P10.R5 | Research server-snapshot portability | not-started | No Phase 10 record exists |
| P11.R1 | Study the full installation cost | not-started | No Phase 11 record exists |
| P11.R2 | Research the package format | not-started | No Phase 11 record exists |
| P11.R3 | Study trust bootstrap and key rotation | not-started | No Phase 11 record exists |
| P11.R4 | Evaluate distribution channels | not-started | No Phase 11 record exists |
| P12.R1 | Study the benchmark protocol | blocked: book | The protocol is Ch. 6 of the absent book |
| P12.R2 | Research equivalent-workload comparison methodology | partial | The requirement is stated in G12.2; no methodology record |
| P12.R3 | Study why composite scores mislead | partial | Stated as a principle (G12.3); no research record |
| P12.R4 | Catalog every unverified hypothesis from the drafts | done | `docs/evidence-register.md` (30 H-labeled rows); `research/phase-01-02-honest-limits.md` |
| P13.R1 | Study why lines-of-code tables mislead | not-started | No Phase 13 record exists |
| P13.R2 | Research task-log methodologies | not-started | No Phase 13 record exists — this is why G13.1 is uncovered |
| P13.R3 | Study standard-library tiering | not-started | No Phase 13 record exists |
| P13.R4 | Research tooling requirements | not-started | No Phase 13 record exists |

## 3. Build tasks (62)

| Phase | Tasks | Status | Note |
|---|---:|---|---|
| 0 | 2 (B1, B2) | B2 done, B1 done | Problem statement written and frozen; evidence register created |
| 1 | 8 (B1–B8) | B1–B7 done, B8 partial | Grammar, identifiers, evaluation, closures, `?`/`defer`, inference limits, operational semantics and conformance plan all exist. B8 asks to resolve §12.1 of the book: the project resolved **47 derived ambiguities instead**, and `03-ambiguities.md` states explicitly that this list "is **not** the book's list and MUST NOT be cited as such" |
| 2–14 | 52 | **not-started** | No Phase 2+ build artifact exists. `src/` is 4 files: the Unicode pipeline only |

Phase 1's build tasks are *specification* work, so "done" there means the
specification exists — not that an implementation exists. That distinction is
what Gate 1 criterion G1.1 measures separately, and it is `future` (see
[`GATE-COVERAGE.md`](./GATE-COVERAGE.md)).

## 4. The three findings

### 4.1 The real remaining scope is 104 tasks, not "Phase 1"

Every planning document frames the project as being inside Phase 1. Measured,
the Master Prompt's own task list is **81 % untouched**, and 52 of the 62 build
tasks belong to phases that have no research record at all. Phase 1 is not
late; it is one of fifteen.

### 4.2 One task is dishonest by construction and cannot be closed

**P1.B8** says: *"Resolve all draft ambiguities catalogued in §12.1 of the
research book."* The book is absent (decision 0004). The project responded by
deriving **47 of its own** ambiguities and resolving 42 of them — which is a
reasonable substitute, and `03-ambiguities.md` is careful to say the list is
**not** the book's and must not be cited as such.

So P1.B8 can never be marked `done` without falsifying the record. It can only
be marked **`superseded`**: the obligation was discharged by a different
artifact, and the substitution is an owner decision, not an agent's. It is
listed here as `partial` because the substitution is not ratified.

### 4.3 The handoff gap: eleven tasks are done and six are partially done, and the tracker says none of it

`PHASE-TRACKER.md` summarises Phase 1 as a single status cell. The task-level
truth is:

- **11 research tasks done**, spanning Phases 0, 1, 3 and 12;
- the **implementation-feasibility** and **primary-source-audit** records exist
  and are not referenced from any phase record;
- Phase 1's 8 build tasks are 7 done and 1 partial — a far better state than
  the tracker's one-line summary conveys.

The gap is the same one §3.10 of the process audit found, one level down: the
tracker is a *phase* view, the Master Prompt is a *task* view, and nothing
joins them. This file is that join.

## 5. Proposed remedy (P)

| # | Proposal | Why |
|---|---|---|
| **TA-1** | `PHASE-TRACKER.md` gains a task-count column: `done / partial / not-started` per phase, computed by `--verify`, not typed | The phase status cell currently hides 7-of-8 completion in Phase 1 |
| **TA-2** | P1.B8 is formally marked `superseded` by a dated owner decision, citing the 47 derived ambiguities | It cannot be honestly marked done |
| **TA-3** | A task may be marked `done` only with a file path that exists — enforced | Already enforced here; the check should be reused by the tracker |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-04 | 1.0.0 | Created by backlog item B3. Marks all 128 tasks: 12 done, 12 partial, 104 not-started. Records that 52 of 62 build tasks belong to phases with no research record, that P1.B8 is unclosable without falsification, and that the phase tracker's one-line summary conceals 7-of-8 Phase 1 build completion. Proposes TA-1…TA-3. |
