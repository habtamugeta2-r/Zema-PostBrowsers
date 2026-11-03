# ZEMA — Phase & Gate Tracker

> Update this file at every gate review. It is the one-page answer to
> *"Where is the project, and what evidence says so?"*
>
> Status values: `Not started` · `Research` · `Decide` · `Build` ·
> `Measure` · `At gate` · `Passed` · `Stopped / pivoted`

| Phase | Title | Status | Gate | Gate result | Gate review record |
|---|---|---|---|---|---|
| 0 | Historical Foundations & Problem Definition | `Passed` (with conditions C1–C5) | Gate 0 | 🔁 Pass with conditions | [`../gates/gate-00.md`](../gates/gate-00.md) |
| 1 | The Unified Language: "Plain" | `Build` — spec draft v0.2.4; C1/C5 owner responses clear authorization; pinned Unicode inputs verified, NFC/NFD corpus test passes, Unicode property accessors and internalSkeleton candidate implementation exist; all 106 rules are now traced to a verification method and a conformance area ([matrix](../plain/07-traceability.md)); Script_Extensions alias input gap blocks security calculations; bidiSkeleton and the whole language core/suite outstanding (0 of 341 fixtures written); A-27/A-38/A-42/A-44/A-45/A-46/A-47 pending; C2 due before Gate 1 | Gate 1 | — (not attempted: no executable core, no conformance run) | [Readiness packet](../gates/gate-01-readiness.md) |
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
| 2026-11-03 | **Phase 1 research deepened; draft v0.2.3.** The v0.1 “60 rules” count was historical/incorrect: the four normative docs contained **98** rules; v0.2 has **100** after T-29/T-30. Added primary-source audit, integrated-systems/PlainP audit, specification audit, non-normative small-step semantics draft, source manifest, and decisions 0008–0011. Ambiguities **44** (39 resolved proposals, 5 deferred, 0 open; decisions 0009–0011, ratification pending); deferrals **20**. Conformance planning target **307**. Evidence register **96 rows**; #057 universal negative retracted. **No build, no fixtures, no Gate 1 attempt.** C1/C5 still block build; C2 due before Gate 1. |
| 2026-11-03 | **Independent Unicode profile audit; draft v0.2.4.** Added Decision 0012 and evidence #097–#100: UTS #39 all-direction identifier guidance, distinction from UTS #55 source-order guidance, missing ZWJ context-B data, and independent out-of-profile warning suppression. Pinned `IndicSyllabicCategory.txt`; all 16 Unicode 17.0.0 Git blob IDs, byte lengths, and SHA-256 values independently verified. Ambiguities **47** (42 proposed-resolved, 5 deferred, 0 open); evidence register **100 rows**; source manifest **58 entries**. No implementation, fixtures, or gate attempt. C1/C5 still block build; C2 due before Gate 1. |
| 2026-11-03 | Recorded Better-back's Arena owner responses: **C1 signed** and **C5 ruled PlainP donor-only**. Phase 1 build is now authorized against the proposed profile; no implementation has started yet. C2 and A-27/A-38/A-42/A-44/A-45/A-46/A-47 ratifications remain due before Gate 1. No gate attempt. |
| 2026-11-03 | Completed initial Phase 1 implementation feasibility research and drafted proposed decisions 0013–0015 (Python oracle, manifest-verified Unicode pipeline, AST/optimized runner profiles). At that point no implementation or Gate 1 attempt had begun; C2 and A-* ratifications still blocked Gate 1. |
| 2026-11-03 | Started authorized Phase 1 build: fetched and verified all 16 pinned Unicode 17 files to ignored cache; implemented project-owned NFC/NFD and passed 20,034 normalization rows / 200,340 assertions. Added an internalSkeleton implementation and recorded five candidate outputs; bidiSkeleton/UAX #9, lexer/parser/typechecker/evaluator, fixtures, and Gate 1 remain outstanding. Evidence #106/#107; experiment EN-unicode17-normalization. |
| 2026-11-03 | Owner selected import for C2 but has not supplied the book; owner selected revise for the A-* proposals but has not specified IDs/replacement wording. These remain Gate 1 blockers; no gate attempt. |
| 2026-11-03 | Continued Unicode property work: 6 source-accessor/alias-guard smoke tests pass. Found that Script_Extensions uses short aliases while Scripts uses long names; drafted proposed decision 0016 to add the missing PropertyValueAliases input. Security-set calculations remain blocked pending owner amendment; no Gate 1 attempt. |
| 2026-11-03 | **Traceability and structure repair; no spec semantics changed.** Added [`07-traceability.md`](../plain/07-traceability.md): all **106** rule IDs (`L-01…L-34`, `T-01…T-30`, `E-01…E-36`, `S-0…S-5`) now carry a verification method and a conformance area, and the 2 rules Gate 1 cannot verify (`E-31` partial, `E-34`) name their owning phase and gate. Repaired [`05-conformance-plan.md`](../plain/05-conformance-plan.md): **14 of 106 rules had no area** (`L-05`, `L-06`, `L-07`, `L-28`, `L-29`, `T-01…T-05`, `T-28`, `E-13`, `E-34`, `E-36`); added 4 areas, budget **307 → 341**. Removed a duplicated normalization result (`research/data/phase-01-normalization-report.json`; the experiment record now owns the only copy). Fixed: split Markdown tables in the evidence register and the ambiguity register, the `S-nn` §9→§8 reference, out-of-ID-order `T-28`/`T-29`/`T-30`, `PL0114`'s dangling owner reference, the execution prompt's dead `§10`/"implementation log" pointers, and stale "C1/C5 still block build" statuses. `tools/audit_phase01.py --check` now **fails** on an untraced rule, an unattributed rule, a declared-vs-summed fixture mismatch, or a duplicated result artifact. Still **0 fixtures, no executable core, no Gate 1 attempt**. Also opened [`../../research/phase-01-07-process-gap-audit.md`](../../research/phase-01-07-process-gap-audit.md) with eight proposed process rules (PR-01…PR-08): one canonical file per measurement, owner-document status facts, rule-level traces, computed-not-typed numbers, and mutation-tested checks. |
| 2026-11-03 | **Process audit, second pass — the audit's own repair was defective and is corrected.** The traceability pass had copied the Gate 1 exclusion list into two files (the defect it was documenting), and the first duplicate-detection check compared rule sets for exact equality, so it could not see a three-row partial copy; found by mutation-testing the check. Rewritten to measure overlap (≥3 shared rules, ≥60% of the smaller set); [`07-traceability.md` §4](../plain/07-traceability.md) now solely owns the exclusion table and the conformance plan links to it. Completed PR-06: all **16** decision records and [`docs/decisions/README.md`](../decisions/README.md) now carry `Status` **and** `Owner ratification`. Corrected three typed numbers: the problem statement's "580 words" → **519 measured** (866 total), the execution prompt's "seven documents" → **eight**, and the audit record's own file counts. Added `audit_phase01.py --verify`, which prints the quantities prose may quote. Evidence #115–#116. Still **0 fixtures, no executable core, no Gate 1 attempt**; C2/C3/C4 and the seven A-* ratifications unchanged. |

## Phase records

| Phase | Records |
|---|---|
| 0 | [Problem statement](../problem-statement.md) · [Evidence register](../evidence-register.md) · Research: [lineage](../../research/phase-00-01-lineage.md), [browser-services catalog](../../research/phase-00-02-browser-services-catalog.md), [coordination cost](../../research/phase-00-03-coordination-cost.md), [prior art](../../research/phase-00-04-prior-art.md), [book-import audit](../../research/phase-00-05-book-import-audit.md) · Decisions: [0001](../decisions/0001-source-grading.md), [0002](../decisions/0002-target-os-linux.md), [0003](../decisions/0003-browser-service-strategy.md), [0004](../decisions/0004-research-book-missing.md) · [Gate 0 review](../gates/gate-00.md) |
| 1 | Spec draft v0.2.4: [index](../plain/README.md), [lexical & layout](../plain/00-lexical-and-layout.md), [types](../plain/01-types.md), [evaluation](../plain/02-evaluation.md), [derived ambiguities](../plain/03-ambiguities.md), [deferred features](../plain/04-deferred-features.md), [conformance plan](../plain/05-conformance-plan.md), [operational semantics draft](../plain/06-operational-semantics.md), [rule traceability matrix](../plain/07-traceability.md) · Research: [language prior art](../../research/phase-01-01-language-prior-art.md), [honest limits](../../research/phase-01-02-honest-limits.md), [primary-source audit](../../research/phase-01-03-primary-source-audit.md), [integrated systems & PlainP](../../research/phase-01-04-integrated-systems-and-plainp.md), [specification audit](../../research/phase-01-05-specification-audit.md), [implementation feasibility](../../research/phase-01-06-implementation-feasibility.md), [source manifest](../../research/data/phase-01-source-manifest.json) · Decisions: [0005](../decisions/0005-language-surface-doctrine.md), [0006](../decisions/0006-type-and-evaluation-core.md), [0007](../decisions/0007-deferred-features.md), [0008](../decisions/0008-phase-01-research-and-draft-v02.md), [0009](../decisions/0009-unicode-pin-and-eq-ord-laws.md), [0010](../decisions/0010-gate-1-core-scope.md), [0011](../decisions/0011-unicode-diagnostic-profile.md), [0012](../decisions/0012-directional-confusability-and-ucd-completeness.md), [0013](../decisions/0013-phase-1-reference-interpreter.md), [0014](../decisions/0014-unicode-data-pipeline.md), [0015](../decisions/0015-conformance-runner-and-profiles.md), [0016](../decisions/0016-script-value-alias-input.md) · **No gate review yet** |
