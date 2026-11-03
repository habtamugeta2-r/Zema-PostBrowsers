# ZEMA — Phase & Gate Tracker

> Update this file at every gate review. It is the one-page answer to
> *"Where is the project, and what evidence says so?"*
>
> Status values: `Not started` · `Research` · `Decide` · `Build` ·
> `Measure` · `At gate` · `Passed` · `Stopped / pivoted`

| Phase | Title | Status | Gate | Gate result | Gate review record |
|---|---|---|---|---|---|
| 0 | Historical Foundations & Problem Definition | `Passed` (with conditions C1–C5) | Gate 0 | 🔁 Pass with conditions | [`../gates/gate-00.md`](../gates/gate-00.md) |
| 1 | The Unified Language: "Plain" | `Research` / `Decide` — spec draft v0.2.3; build blocked on C1, C5; A-27/A-38/A-42/A-44 proposed resolved; ratification pending | Gate 1 | — (not attempted: no executable core, no conformance run) | [Readiness packet](../gates/gate-01-readiness.md) |
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
| E3 | 12? | **Undefined in this repo.** `00-Core-Concerns.md` Concern 3 places E1–E3 in the Ch. 9 performance cluster (hypotheses H1–H3). Phase 0 searched the repository and the owner's 10 public repositories and did not find the book, so the definition remains unrecovered. | **Blocked** — book not found (Phase 0 audit) | [`../../research/phase-00-05-book-import-audit.md`](../../research/phase-00-05-book-import-audit.md) |
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
| 2026-11-02 | **Phase 0 executed; Gate 0 passed with conditions C1–C5** ([review](../gates/gate-00.md)). Produced: frozen [problem statement](../problem-statement.md), [browser-services catalog](../../research/phase-00-02-browser-services-catalog.md) (21 services), [coordination-cost research](../../research/phase-00-03-coordination-cost.md), [prior-art review](../../research/phase-00-04-prior-art.md), [book-import audit](../../research/phase-00-05-book-import-audit.md), [evidence register](../evidence-register.md) (63 rows), and decisions 0001–0004. |
| 2026-11-02 | Claim #001 ("world's first post-browser platform") **retracted** at Gate 0; replaced by #048. Decision C **closed as unattested**. Target OS recorded as **Linux (Ubuntu 24.04 LTS)**, status *Proposed* pending owner confirmation (C3). E3 remains `Blocked`. Phase 1 is next: research tasks may start; build tasks wait on C1/C5. |
| 2026-11-02 | **Phase 1 opened: research and decide done, build blocked.** Plain spec **draft v0.1** written (60 normative rules across four documents), **26 derived ambiguities** (21 resolved, 5 deferred), **18 deferrals** with triggers, decisions 0005–0007. No interpreter, no conformance suite → **Gate 1 deliberately not attempted**. Build waits on C1 and C5; C2 (book or retired pointers) is due before Gate 1. |
| 2026-11-03 | **Phase 1 research deepened; draft v0.2.3.** The v0.1 “60 rules” count was historical/incorrect: the four normative docs contained **98** rules; v0.2 has **100** after T-29/T-30. Added primary-source audit, integrated-systems/PlainP audit, specification audit, non-normative small-step semantics draft, source manifest, and decisions 0008–0011. Ambiguities now **44** (39 resolved proposals, 5 deferred, 0 open; decisions 0009–0011, ratification pending); deferrals **20**. Conformance planning target **307** (including one target per active diagnostic code). Evidence register **96 rows**; #057 universal negative retracted. **No build, no fixtures, no Gate 1 attempt.** C1/C5 still block build; C2 due before Gate 1. |

## Phase records

| Phase | Records |
|---|---|
| 0 | [Problem statement](../problem-statement.md) · [Evidence register](../evidence-register.md) · Research: [lineage](../../research/phase-00-01-lineage.md), [browser-services catalog](../../research/phase-00-02-browser-services-catalog.md), [coordination cost](../../research/phase-00-03-coordination-cost.md), [prior art](../../research/phase-00-04-prior-art.md), [book-import audit](../../research/phase-00-05-book-import-audit.md) · Decisions: [0001](../decisions/0001-source-grading.md), [0002](../decisions/0002-target-os-linux.md), [0003](../decisions/0003-browser-service-strategy.md), [0004](../decisions/0004-research-book-missing.md) · [Gate 0 review](../gates/gate-00.md) |
| 1 | Spec draft v0.2.3: [index](../plain/README.md), [lexical & layout](../plain/00-lexical-and-layout.md), [types](../plain/01-types.md), [evaluation](../plain/02-evaluation.md), [derived ambiguities](../plain/03-ambiguities.md), [deferred features](../plain/04-deferred-features.md), [conformance plan](../plain/05-conformance-plan.md), [operational semantics draft](../plain/06-operational-semantics.md) · Research: [language prior art](../../research/phase-01-01-language-prior-art.md), [honest limits](../../research/phase-01-02-honest-limits.md), [primary-source audit](../../research/phase-01-03-primary-source-audit.md), [integrated systems & PlainP](../../research/phase-01-04-integrated-systems-and-plainp.md), [specification audit](../../research/phase-01-05-specification-audit.md), [source manifest](../../research/data/phase-01-source-manifest.json) · Decisions: [0005](../decisions/0005-language-surface-doctrine.md), [0006](../decisions/0006-type-and-evaluation-core.md), [0007](../decisions/0007-deferred-features.md), [0008](../decisions/0008-phase-01-research-and-draft-v02.md), [0009](../decisions/0009-unicode-pin-and-eq-ord-laws.md), [0010](../decisions/0010-gate-1-core-scope.md), [0011](../decisions/0011-unicode-diagnostic-profile.md) · **No gate review yet** |
