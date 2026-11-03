# ZEMA Master Prompt — Directory Guide

This directory holds the improved, recorded editions of ZEMA's two
founding documents: **0. Core Concerns** (*what and why* — the 19 main
problems the project exists to solve) and the **Master Research &
Build Prompt** (*in what order and how* — Phases 0–14).

> **The Reading Age is over. The Service Age has begun.**

## Start here

| # | File | What it is |
|---|---|---|
| 0 | [`00-Core-Concerns.md`](./00-Core-Concerns.md) | **Read first.** The 19 core concerns (3 founding, 12 make-or-break, 4 about running the project), synthesized from research-book Chapters 1–13. Adds no new claims. |
| 1 | [`ZEMA-Master-Research-and-Build-Prompt.md`](./ZEMA-Master-Research-and-Build-Prompt.md) | **The build plan.** Vision, method, Phases 0–14, Gates 0–14, scope rules, and stopping conditions. Start at Phase 0. |
| 2 | [`PHASE-TRACKER.md`](./PHASE-TRACKER.md) | One-page status board for every phase and gate. Update it at each gate review. |
| 3 | [`IMPROVEMENTS.md`](./IMPROVEMENTS.md) | The editorial record: exactly what was improved in each v1.1, why, and what was deliberately left unchanged. |
| 4 | [`templates/`](./templates/) | Ready-to-copy recording templates the prompt itself requires (evidence register, decision record, experiment record, gate review). |

**Current Phase 1 work order:** [`PHASE-01-EXECUTION-PROMPT.md`](./PHASE-01-EXECUTION-PROMPT.md) — conditional build, conformance, and Gate 1 instructions; not an authorization to bypass Gate 0 conditions.

## How to use it

1. **Read** [`00-Core-Concerns.md`](./00-Core-Concerns.md) first (the
   19 concerns), then §1–§3 of the master prompt (vision, the
   five-step loop, evidence labels, principles).
2. **Begin with Phase 0 — already completed** (Gate 0 passed with
   conditions on 2026-11-02; see [`../gates/gate-00.md`](../gates/gate-00.md)).
   Then work the loop for the current phase only:
   *Research → Decide → Build → Measure → Gate.*
3. **Record as you go**, using the templates in [`templates/`](./templates/)
   and the location map in Appendix B of the master prompt.
4. **Do not start the next phase** until the current gate passes — or the
   gate review records a decision to simplify, pivot, or stop.
5. **Update [`PHASE-TRACKER.md`](./PHASE-TRACKER.md)** at every gate.

## The 15 phases at a glance

| Phase | Title | Gate |
|---|---|---|
| 0 | Historical Foundations & Problem Definition | Gate 0 |
| 1 | The Unified Language: "Plain" | Gate 1 |
| 2 | Reactive State Model | Gate 2 |
| 3 | Execution Model & Host Isolation | Gate 3 |
| 4 | Memory Safety & Concurrency | Gate 4 |
| 5 | Security: Capability-Enforced by the Host | Gate 5 |
| 6 | UI, Rendering & Layout | Gate 6 |
| 7 | Text & Internationalization | Gate 7 |
| 8 | Accessibility | **Gate 8 — Release Gate** |
| 9 | Data: Local-First Correctness, Recovery & Replication | Gate 9 |
| 10 | Networking & Protocol Discipline | Gate 10 |
| 11 | Delivery, Identity, Updates & Adoption | **Gate 11 — Delivery Gate** |
| 12 | Performance Benchmarking & Evidence Discipline | **Gate 12 — Evidence Gate** |
| 13 | Developer Experience (Measured Honestly) | Gate 13 |
| 14 | Production Readiness & Scope Discipline | **Gate 14 — Production Gate** |

## Directory layout

```text
docs/zema-master-prompt/
├── README.md                                      ← you are here
├── 00-Core-Concerns.md                            ← document 0: the 19 core concerns (v1.1)
├── ZEMA-Master-Research-and-Build-Prompt.md       ← canonical build plan (v1.1)
├── IMPROVEMENTS.md                                ← v1.1 editorial records
├── PHASE-TRACKER.md                               ← phase/gate status board
├── VERTICAL-TRACE.md                              ← concerns → phases → gates → evidence
└── templates/
    ├── evidence-register.md
    ├── decision-record.md
    ├── experiment-record.md
    └── gate-review.md
```

## Where the phase records live

This folder holds the two **controlled documents** and their editorial
record. Work produced *by* the phases lives outside it, per Appendix B of
the master prompt:

| Record | Location |
|---|---|
| Research findings | [`../../research/`](../../research/) — index in [`../../research/README.md`](../../research/README.md) |
| The frozen problem statement | [`../problem-statement.md`](../problem-statement.md) |
| Evidence register | [`../evidence-register.md`](../evidence-register.md) |
| **Vertical trace** (concern → phase → gate → evidence) | [`VERTICAL-TRACE.md`](./VERTICAL-TRACE.md) — 3 of 19 concerns had an evidence row before it existed |
| Decisions (build / reuse / invent) | [`../decisions/`](../decisions/) — index and status vocabulary in [`../decisions/README.md`](../decisions/README.md) |
| Gate reviews | [`../gates/`](../gates/) |
| Experiments (E1, E2, E4, E5, …) | `experiments/EN-*/` — created when each experiment begins |

Phase 0's records are indexed in [`PHASE-TRACKER.md`](./PHASE-TRACKER.md#phase-records).

## Editing rules

- Both founding documents are **controlled documents**. Changes go
  through the discipline they prescribe: record what changed and why
  (extend `IMPROVEMENTS.md` and each document's Version History
  appendix), and bump the version number.
- Never delete a concern, phase, task, or exit criterion silently. If
  scope must change, record the decision and the gate at which it was
  made. The concern numbers 1–19 are permanent IDs — never renumber
  them.
- Keep exactly **one** canonical copy of each. Copies drift; links do
  not.
