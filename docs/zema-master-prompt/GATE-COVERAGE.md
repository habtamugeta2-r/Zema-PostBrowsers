# GATE-COVERAGE — the 50 gate exit criteria against what can discharge them

| Field | Detail |
|---|---|
| **Document** | Coverage map: every gate exit criterion → the artifact that discharges it |
| **Version** | 1.0.1 |
| **Date** | 2026-11-04 |
| **Status** | Active. Produced by backlog item **B2** |
| **Source of truth** | The 50 criteria are extracted from [`ZEMA-Master-Research-and-Build-Prompt.md`](./ZEMA-Master-Research-and-Build-Prompt.md) by `tools/audit_phase01.py`; this file's disposition table is checked against it |
| **Machine check** | `gate_coverage_check()` — fails if a criterion appears in the prompt but not here, or if a `covered` claim names a mechanism that does not exist |

> **What this answers.** [`05-conformance-plan.md`](../plain/05-conformance-plan.md)
> has 23 test areas and a 357-fixture budget. The Master Prompt has 50 gate exit
> criteria across Phases 0–14. Nobody had ever asked whether the first can
> discharge the second. This document answers it, and the answer is not
> comfortable.

---

## 1. The headline

| | Count |
|---|---:|
| Gate exit criteria in the Master Prompt | 50 |
| `covered` — an artifact path that exists today | **8** |
| `future` — a named artifact that **does not exist yet** | **27** |
| `platform` — outside Gate 1 by A-42, owned by a later phase | **8** |
| **`UNCOVERED` — no artifact anywhere would discharge it** | **7** |

These four figures are printed by `--check`, not typed. The first draft of this
section guessed 12 / 22 / 9 / 7; the measured answer is 8 / 27 / 8 / 7, and the
total was the only part I had right. The `covered` count fell because three
criteria I had called covered (G1.1, G1.2, G1.3) are in fact one covered and two
future: a frozen syntax is checkable today, a running interpreter and a passing
suite are not.

**All 23 conformance areas are Phase-1 language areas.** Not one of them
addresses isolation, accessibility, data, networking, delivery, or
developer experience. That is not a defect in the conformance plan — it is
scoped to Gate 1 by decision 0010. The defect is that **no other plan exists**,
so 50 criteria rest on a test plan that can reach 8 of them, and the remaining
42 have either a not-yet-built artifact or nothing at all.

## 2. The disposition of all 50

Disposition vocabulary:

| Disposition | Meaning |
|---|---|
| `covered` | A named conformance area or existing artifact discharges it |
| `future` | A named artifact is planned but **does not exist**; the criterion is safe only if that plan holds |
| `platform` | Outside Gate 1's hermetic core by A-42; owned by a later phase. Not a gap, but it must be listed as untested at Gate 1 |
| **`UNCOVERED`** | **No artifact is named anywhere that would discharge it** |

### 2.1 The disposition table

| # | Criterion (abridged) | Disposition | What discharges it |
|---|---|---|---|
| G0.1 | Problem statement reviewed and frozen | covered | [`problem-statement.md`](../problem-statement.md), frozen at Gate 0 |
| G0.2 | Target app class defined, starting with the task list | covered | `problem-statement.md` §target class |
| G0.3 | Non-goals documented and agreed | covered | `problem-statement.md` §non-goals |
| G1.1 | A safe executable core is running | future | The interpreter — **does not exist** (0 lines of lexer/parser/checker/eval) |
| G1.2 | Conformance suite passes for all specified semantics | future | 357 planned fixtures — **0 written** |
| G1.3 | Syntax frozen for this gate; no feature creep | covered | Can be checked now: the 100 rules and the grammar are frozen in `docs/plain/00`–`02` |
| G2.1 | Reactive state passes correctness tests: no glitches, no stale reads | future | Phase 2 reactive model — **does not exist** |
| G2.2 | E1 measurements recorded with raw data | UNCOVERED | **Experiment E1 is named but never defined.** No protocol, no baseline, no record directory |
| G2.3 | No performance claim without an equivalent-workload baseline | future | Bench harness — **does not exist** |
| G3.1 | Untrusted app code runs in isolation with enforced quotas | platform | Prompt Gate 3; not Gate 1 (A-42) |
| G3.2 | Terminating a misbehaving app does not affect others | platform | Prompt Gate 3 |
| G3.3 | Security review of the execution boundary completed | platform | Prompt Gate 3 |
| G4.1 | Memory safety verified for the checked subset | platform | Prompt Gate 4 |
| G4.2 | E2 measurements recorded | UNCOVERED | **E2 named, never defined** |
| G4.3 | Concurrency model specified with formal guarantees | platform | Prompt Gate 4 |
| G5.1 | Capability broker passes a security audit | platform | Prompt Gate 5 |
| G5.2 | A malicious test app cannot escalate privileges | platform | Prompt Gate 5 |
| G5.3 | Network policy verified against DNS-rebinding | platform | Prompt Gate 5 |
| G6.1 | Retained scene graph renders on GPU | future | Phase 6 renderer — **does not exist** |
| G6.2 | Pipeline-stage measurements recorded separately | future | Phase 6 harness — **does not exist** |
| G6.3 | Virtualized lists preserve identity, focus, scroll | future | Phase 6 UI — **does not exist** |
| G7.1 | Every script in the test matrix renders correctly | future | Phase 7 script matrix — **does not exist** |
| G7.2 | Bidirectional text displays correctly | future | Phase 7 — **does not exist** |
| G7.3 | IME composition works for CJK input | future | Phase 7 — **does not exist** |
| G7.4 | E4 results recorded | UNCOVERED | **E4 named, never defined** |
| G8.1 | The task list app runs with full accessibility | future | The app — **does not exist** |
| G8.2 | Manual testing with real assistive technology passes | future | No AT test procedure exists |
| G8.3 | WCAG 2.2 / WCAG2ICT used as references | covered | Policy stated in the Master Prompt; references are public standards |
| G8.4 | Accessibility gaps block release | covered | Policy, recorded in evidence #041 |
| G9.1 | Local data survives crash recovery with zero loss | future | Phase 9 storage — **does not exist** |
| G9.2 | Offline operations sync after reconnection | future | Phase 9 sync — **does not exist** |
| G9.3 | E5 results recorded | UNCOVERED | **E5 named, never defined** |
| G10.1 | App communicates over HTTPS with correct TLS | future | Phase 10 — **does not exist** |
| G10.2 | Retries idempotent; network failure causes no data loss | future | Phase 10 — **does not exist** |
| G10.3 | QUIC evaluation documented in a decision record | future | Decision record — **not written** |
| G11.1 | App installs, updates, launches, measured cold start | future | Phase 11 — **does not exist** |
| G11.2 | Signature verification works, including key rotation | future | Phase 11 — **does not exist** |
| G11.3 | Distribution-channel decision documented | future | Decision record — **not written** |
| G12.1 | Every headline claim confirmed or retracted, raw data published | future | The evidence register exists; the *benchmarks to populate it* do not |
| G12.2 | Per-metric comparison tables for web/PWA and native baselines | future | Benchmarks — **do not exist** |
| G12.3 | No composite scores, no unverified numbers | covered | Enforced by `audit_phase01.py --verify` (PR-01), which is why this project's counts are computed |
| G13.1 | Developer task-log study completed | UNCOVERED | No study protocol, no participant plan, no task list |
| G13.2 | Core tooling (LSP, formatter, debugger) functional | future | Phase 13 tooling — **does not exist** |
| G13.3 | Productivity claims backed by task logs | UNCOVERED | Depends on G13.1, which has no protocol |
| G14.1 | The app ships on one desktop OS with full accessibility | future | Depends on G8, G9, G11 |
| G14.2 | All performance claims verified, raw data published | future | Depends on G12 |
| G14.3 | Security audit passed, re-verified for release | future | Depends on G5 |
| G14.4 | Developer-experience study complete | UNCOVERED | Depends on G13.1 |
| G14.5 | Distribution and updates work end to end | future | Depends on G11 |
| G14.6 | Every deferred feature documented as a research track | covered | [`04-deferred-features.md`](../plain/04-deferred-features.md) — 20 deferrals, each with reason/cost/trigger |

## 3. The seven genuinely uncovered

These are the finding. Each names an obligation and **no artifact anywhere**
that would discharge it:

| # | Criterion | Why nothing discharges it |
|---|---|---|
| G2.2 | E1 measurements with raw data | Experiment E1 is cited seven times and **defined nowhere.** Concern 3 says the book's Ch. 9 holds it; the book is absent (decision 0004) |
| G4.2 | E2 measurements | Same — E2 is named, never specified |
| G7.4 | E4 results | Same — E4 is named, never specified |
| G9.3 | E5 results | Same — E5 is named, never specified |
| G13.1 | Developer task-log study | No protocol, no participants, no task list, no metric |
| G13.3 | Productivity claims backed by task logs | Derivative of G13.1 |
| G14.4 | Developer-experience study complete | Derivative of G13.1 |

**Four of seven are one defect**: the experiments E1–E5 are referenced as if
defined, and their definitions live in the missing book. This is decision 0004
reaching a gate criterion instead of a citation.

That is a sharper statement than "the book is missing." The book's absence was
recorded as a *traceability* problem. It is also a **delivery** problem: four
gate criteria cannot be attempted, by anyone, until either the book arrives or
the experiments are re-specified from scratch and that re-specification is
recorded as an owner decision.

## 4. What this means for Gate 1, specifically

Gate 1 has three criteria. Measured:

| # | Criterion | Located where | State |
|---|---|---|---|
| G1.1 | A safe executable core is running | §2, `future` | **0** of the lexer/parser/checker/evaluator exists |
| G1.2 | Conformance suite passes for all specified semantics | §2, `future` | **0** of 357 fixtures written |
| G1.3 | Syntax frozen; no feature creep | §2, `covered` | **Achievable now** — the 100 rules and grammar are stable |

So Gate 1 is 1/3 reachable today and 0/3 passed. The readiness packet is
honest about this; the new information here is that **G1.3 is the only
criterion the repository can currently evidence**, and it is the one nobody
has written down as done.

## 5. Proposed remedy (P)

| # | Proposal | Why |
|---|---|---|
| **GC-1** | The experiments **E1, E2, E4, E5** must each have a protocol record under `research/experiments/EN-*/` **before** the phase that needs them begins. A protocol states the hypothesis, the baseline, the metric, the sample size, and the raw-data location | Four gate criteria are unopenable without this, and the definitions live in an absent book |
| **GC-2** | The developer-experience study (G13.1) needs the same treatment: protocol first, results second | It is the only uncovered criterion that is *not* blocked by the missing book, so it is squarely the project's own omission |
| **GC-3** | Every gate review restates **all 50 criteria** with a disposition, not only its own phase's | Today a reviewer sees 3–6 criteria and cannot see that the other 44 exist |
| **GC-4** | A criterion may not be marked `covered` unless this file names an artifact **path** that exists | Prevents the `future`/`covered` confusion that let 22 criteria look settled |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-04 | 1.0.1 | Corrected §1 to the measured disposition counts (8 covered / 27 future / 8 platform / 7 uncovered) after typing 12 / 22 / 9 / 7 from impression. The check itself was order-dependent in its first version and was scoped to §2. |
| 2026-11-04 | 1.0.0 | Created by backlog item B2. Maps all 50 gate exit criteria to a disposition. Records that all 23 conformance areas are Phase-1 language areas. Proposes GC-1…GC-4. |
