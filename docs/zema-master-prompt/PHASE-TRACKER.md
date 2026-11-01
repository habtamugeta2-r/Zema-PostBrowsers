# ZEMA — Phase & Gate Tracker

> Update this file at every gate review. It is the one-page answer to
> *"Where is the project, and what evidence says so?"*
>
> Status values: `Not started` · `Research` · `Decide` · `Build` ·
> `Measure` · `At gate` · `Passed` · `Stopped / pivoted`

| Phase | Title | Status | Gate | Gate result | Gate review record |
|---|---|---|---|---|---|
| 0 | Historical Foundations & Problem Definition | Not started | Gate 0 | — | — |
| 1 | The Unified Language: "Plain" | Not started | Gate 1 | — | — |
| 2 | Reactive State Model | Not started | Gate 2 | — | — |
| 3 | Execution Model & Host Isolation | Not started | Gate 3 | — | — |
| 4 | Memory Safety & Concurrency | Not started | Gate 4 | — | — |
| 5 | Security: Capability-Enforced by the Host | Not started | Gate 5 | — | — |
| 6 | UI, Rendering & Layout | Not started | Gate 6 | — | — |
| 7 | Text & Internationalization | Not started | Gate 7 | — | — |
| 8 | Accessibility | Not started | **Gate 8 — Release Gate** | — | — |
| 9 | Data: Local-First Correctness, Recovery & Replication | Not started | Gate 9 | — | — |
| 10 | Networking & Protocol Discipline | Not started | Gate 10 | — | — |
| 11 | Delivery, Identity, Updates & Adoption | Not started | **Gate 11 — Delivery Gate** | — | — |
| 12 | Performance Benchmarking & Evidence Discipline | Not started | **Gate 12 — Evidence Gate** | — | — |
| 13 | Developer Experience (Measured Honestly) | Not started | Gate 13 | — | — |
| 14 | Production Readiness & Scope Discipline | Not started | **Gate 14 — Production Gate** | — | — |

## Experiment register

| ID | Phase | Question it answers | Status | Record |
|---|---|---|---|---|
| E1 | 2 | What does a reactive update cost vs. affected node count, compared with web-framework baselines? | Not started | — |
| E2 | 4 | What are the allocation patterns, GC pauses (if any), and concurrent-task throughput? | Not started | — |
| E3 | 12? | **Undefined in this repo.** `00-Core-Concerns.md` Concern 3 places E1–E3 in the Ch. 9 performance cluster (hypotheses H1–H3); E3's exact definition must be recovered when the research book is imported in Phase 0. | Blocked — awaiting book | — |
| E4 | 7 | Does text render accurately across the full script matrix (Arabic, Hebrew, Indic, Ethiopic, CJK, …)? | Not started | — |
| E5 | 9 | Does local data survive crashes, resolve conflicts correctly, and sync within acceptable latency? | Not started | — |

> **Note (recorded 2026-11-01):** There is no E3 in the master prompt.
> Phase 0 must confirm whether E3 (and "Decision C") exist in the
> research book or whether the numbering should be closed up. See
> `IMPROVEMENTS.md` §5.
>
> **Update (2026-11-01, on recording `00-Core-Concerns.md`):** the
> Core Concerns synthesis confirms E3 exists in the book's Ch. 9
> performance cluster (H1–H3, E1–E3) — so its definition, not its
> existence, is what Phase 0 must recover. "Decision C" remains
> unattested (Decisions A, B, D only). See `00-Core-Concerns.md`
> Appendix A.

## Rules

- A phase may move to `Passed` **only** when its gate review record
  exists and every exit criterion in the master prompt is checked.
- `Stopped / pivoted` is a respectable final state — the gate review
  must say what was learned and where the evidence lives.
- Never edit history: if a passed gate is later reopened, add a new
  dated note below instead of changing the original result silently.

## Change log

| Date | Change |
|---|---|
| 2026-11-01 | Tracker created alongside master prompt v1.1. All phases `Not started`; next action is Phase 0. |
| 2026-11-01 | `00-Core-Concerns.md` v1.1 recorded. E3 row added as *Blocked — awaiting book* (existence confirmed by Concern 3; definition pending Phase 0 book import). Phases unchanged. |
