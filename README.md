# Zema-PostBrowsers

**ZEMA** — a research-and-build project for a post-browser application
platform: a deliberately constrained, capability-secured client runtime
with one co-designed language ("Plain"), for interactive, data-driven
service applications.

> The Reading Age is over. The Service Age has begun.

## Start here

📘 **[0. Core Concerns](docs/zema-master-prompt/00-Core-Concerns.md)** — *read
first:* the 19 main problems this whole repository exists to solve
(3 founding, 12 make-or-break, 4 about how the project must be run).

📗 **[ZEMA Master Research & Build Prompt](docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md)**
— the build plan: vision, method, Phases 0–14, Gates 0–14, scope
rules, and stopping conditions.

📕 **[Problem Statement (frozen at Gate 0)](docs/problem-statement.md)** —
what ZEMA is, the app class it targets, the class it refuses, and what
success and failure would each look like.

| Document | Purpose |
|---|---|
| [Directory guide](docs/zema-master-prompt/README.md) | How the master-prompt folder is organized and how to work through it |
| [Phase tracker](docs/zema-master-prompt/PHASE-TRACKER.md) | One-page status of every phase, gate, and experiment |
| [Improvement record](docs/zema-master-prompt/IMPROVEMENTS.md) | What was improved in each v1.1 edition, why, and what was left unchanged |
| [Recording templates](docs/zema-master-prompt/templates/) | Evidence register, decision record, experiment record, gate review |

## Where the work stands

**Phase 0 — Historical Foundations & Problem Definition: complete.
Gate 0 passed with conditions (C1–C5).**

**Phase 1 — The Unified Language ("Plain"): draft v0.2.5; build authorized, in progress.** Better-back signed C1 and ruled PlainP a donor only on 2026-11-03 (recorded in [`gate-00.md`](docs/gates/gate-00.md) §10); the Phase 1 build may proceed against the proposed spec. The specification ([`docs/plain/`](docs/plain/README.md)) has 100 numbered rules, 47 derived ambiguities (42 resolved proposals, 5 deferred, 0 open; ratification pending), 20 deferrals, a 356-fixture planning budget, and a **non-normative** small-step semantics draft. Every one of the 106 rule IDs is allocated to a verification method and a conformance area in the [traceability matrix](docs/plain/07-traceability.md); **zero of the 356 fixtures are written.** The Phase 1 build has fetched and verified the 16 pinned Unicode inputs and implemented a project-owned NFC/NFD normalizer that passes all 20,034 rows / 200,340 assertions in the Unicode 17 normalization corpus. The lexer/parser/typechecker/evaluator, bidiSkeleton and full identifier-security algorithms, and conformance suite remain unimplemented; Script_Extensions comparisons are deliberately guarded pending proposed decision 0016 (an A-46 input-lock amendment). **Gate 1 is not attempted**. C2 and A-27/A-38/A-42/A-44/A-45/A-46/A-47 ratifications are required before a Gate 1 attempt.

| Phase 0 artifact | What it records |
|---|---|
| [Problem statement](docs/problem-statement.md) | The target app class (starting with the task list app), eight non-goals, and the success/failure tests — frozen |
| [Browser-services catalog](research/phase-00-02-browser-services-catalog.md) | 21 services the browser provides beyond rendering, each classified **rebuild / interoperate / give up** with its cost |
| [Coordination-cost research](research/phase-00-03-coordination-cost.md) | Published measurements of today's stack, plus what they do *not* prove |
| [Prior-art review](research/phase-00-04-prior-art.md) | Electron, Tauri, Flutter, React Native, PWAs — and the retraction of "world's first" |
| [Book-import audit](research/phase-00-05-book-import-audit.md) | A reproducible negative finding: the research book is not in this repo or the owner's public repos |
| [Evidence register](docs/evidence-register.md) | 116 numbered claims, each labeled Established / Proposed / Hypothesis, with source grades and retractions |
| [Decision records](docs/decisions/) | Source grading · target OS · browser-service strategy · missing research book; index and two-field status vocabulary in [`docs/decisions/README.md`](docs/decisions/README.md) |
| [Gate 0 review](docs/gates/gate-00.md) | The pass, its two retractions, its stopping-condition check, and conditions C1–C5 |
| [Gate 1 readiness packet](docs/gates/gate-01-readiness.md) | Owner/reviewer response blocks for C1/C2/C5 and A-27/A-38/A-42/A-44/A-45/A-46/A-47; preparation only, not a gate attempt |

### Phase 1 records (draft)

| Artifact | What it records |
|---|---|
| [Plain specification v0.2.4](docs/plain/README.md) | Index, non-goals, freeze policy — **draft, not frozen** |
| [Conformance plan](docs/plain/05-conformance-plan.md) | Gate 1 core vs platform scope, 356 allocated fixture targets, runner requirements — **plan only** |
| [Rule traceability matrix](docs/plain/07-traceability.md) | All 106 rule IDs → verification method → conformance area; the 2 rules Gate 1 cannot verify, with owners — **allocation, not coverage** |
| [Operational semantics draft](docs/plain/06-operational-semantics.md) | Non-normative small-step core model, conjectures, trace obligations |
| [Lexical structure & layout](docs/plain/00-lexical-and-layout.md) | Unicode identifiers and confusables, literals, the single layout rule, compact EBNF, sanctioned sugar, diagnostics |
| [Types](docs/plain/01-types.md) | `let`/`mut`, structural records, nominal closed unions, `Option`/`Result`, interfaces and coherence, inference limits |
| [Evaluation](docs/plain/02-evaluation.md) | Evaluation order, checked integers everywhere, `Float` and `Eq`, text, closures, `?`, `defer`, exhaustive matching, faults |
| [Derived ambiguities](docs/plain/03-ambiguities.md) | 47 questions: 42 resolved (proposed), 5 deferred, 0 open — the substitute for the missing §12.1 |
| [Deferred features](docs/plain/04-deferred-features.md) | 20 deferrals (9 from the Master Prompt, 11 added), each with cost and trigger |
| [Language prior art](research/phase-01-01-language-prior-art.md) | Elm, Rust, Kotlin, Swift, Unison, Unicode — and what Plain refuses |
| [Honest limits](research/phase-01-02-honest-limits.md) | Five seams removed; eleven domains that stay hard |
| [Primary-source audit](research/phase-01-03-primary-source-audit.md) | Kotlin/Swift/Rust/Elm/Unicode corrections and UTS #55 source-handling profile |
| [Integrated systems & PlainP](research/phase-01-04-integrated-systems-and-plainp.md) | Newspeak/Monte/Unison/Lamdera/Dark/Skip/Flutter matrix and read-only PlainP audit |
| [Specification audit](research/phase-01-05-specification-audit.md) | 29 findings, counterexamples, count corrections, Unicode data lock, Gate 1 readiness |
| [Implementation feasibility](research/phase-01-06-implementation-feasibility.md) | Python reference vehicle proposal, C1/C5 authorization state, and Unicode implementation progress |
| [Process-gap audit](research/phase-01-07-process-gap-audit.md) | The research-and-build process gap: 14 rules unlinked to any test, 3 broken invariants, 11 stale statuses — root cause, repair, and the checks that now fail on regression |
| [Source manifest](research/data/phase-01-source-manifest.json) | 58 versioned sources including 16 hash-pinned Unicode 17.0.0 data/test inputs |
| [Unicode input verification](research/data/phase-01-unicode-verification.json) | Fetch-time Git blob, byte-length, and SHA-256 checks for all 16 pinned files |
| [Internal skeleton candidates](research/data/phase-01-internal-skeleton-examples.json) | Computed UTS #39 internalSkeleton only; not bidiSkeleton or final Plain results |
| [Unicode property tests](tests/test_unicode17_properties.py) | Six source-accessor smoke tests; Script_Extensions comparisons are guarded without the pending alias input |
| [Normalization experiment](research/experiments/EN-unicode17-normalization/README.md) | Project-owned NFC/NFD implementation passes the complete pinned Unicode 17 normalization corpus |
| [Decisions 0005–0016](docs/decisions/) | Language doctrine, types/evaluation, scope, Unicode, proposed Python/data/runner implementation, and Script alias input decision |

## Method

For every phase: **Research → Decide → Build → Measure → Gate.**
Reuse before inventing. Prove every claim — or retract it. Every gate
can stop the project, and "an existing solution is better" is a valid
outcome.

**Structural rules (from the 2026-11-03 process audit):** one canonical file per
measurement; a status fact has one owning document and every other mention links
to it; every rule ID is traced to a verification method and a fixture area; every
number in prose is computed by the audit tool, not typed. Enforced by
`tools/audit_phase01.py --check` and `tests/test_document_invariants.py`; see the
[process-gap audit](research/phase-01-07-process-gap-audit.md) §6.

**Evidence rules:** every claim carries exactly one label —
**Established** (cited external source, grade A or B), **Proposed**
(decided, not yet verified), or **Hypothesis** (needs measurement or
proof). Retracted claims stay in the register forever.

**Current status (2026-11-03):** Phase 0 passed with conditions; Phase 1
draft v0.2.4. C1/C5 were resolved by owner responses; build is authorized
and initial Unicode acquisition/normalization work is complete. A partial
Unicode subsystem now exists, but there is no lexer/parser/typechecker/
evaluator or conformance suite. Next: continue the proposed implementation;
obtain owner/reviewer ratification of A-27/A-38/A-42/A-44/A-45/A-46/A-47
and resolve C2 before Gate 1. Gate 1 is not attempted.
