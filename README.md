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

**Phase 1 — The Unified Language ("Plain"): research and design done,
build blocked.** The specification draft is written
([`docs/plain/`](docs/plain/README.md)): 98 numbered rules, 26 derived
ambiguities, 18 deferrals with triggers, and a ≈285-fixture conformance
plan. There is **no interpreter and no
conformance suite**, so **Gate 1 is deliberately not attempted** — build
tasks wait on owner sign-off (C1) and the `PlainP` ruling (C5), with the
research-book condition (C2) due before Gate 1.

| Phase 0 artifact | What it records |
|---|---|
| [Problem statement](docs/problem-statement.md) | The target app class (starting with the task list app), eight non-goals, and the success/failure tests — frozen |
| [Browser-services catalog](research/phase-00-02-browser-services-catalog.md) | 21 services the browser provides beyond rendering, each classified **rebuild / interoperate / give up** with its cost |
| [Coordination-cost research](research/phase-00-03-coordination-cost.md) | Published measurements of today's stack, plus what they do *not* prove |
| [Prior-art review](research/phase-00-04-prior-art.md) | Electron, Tauri, Flutter, React Native, PWAs — and the retraction of "world's first" |
| [Book-import audit](research/phase-00-05-book-import-audit.md) | A reproducible negative finding: the research book is not in this repo or the owner's public repos |
| [Evidence register](docs/evidence-register.md) | 63 numbered claims, each labeled Established / Proposed / Hypothesis, with source grades |
| [Decision records](docs/decisions/) | Source grading · target OS · browser-service strategy · missing research book |
| [Gate 0 review](docs/gates/gate-00.md) | The pass, its two retractions, its stopping-condition check, and conditions C1–C5 |

### Phase 1 records (draft)

| Artifact | What it records |
|---|---|
| [Plain specification v0.1](docs/plain/README.md) | Index, non-goals, freeze policy — **draft, not frozen** |
| [Conformance plan](docs/plain/05-conformance-plan.md) | What Gate 1 will require: coverage per rule, ≈285 fixtures, runner contract — **plan only** |
| [Lexical structure & layout](docs/plain/00-lexical-and-layout.md) | Unicode identifiers and confusables, literals, the single layout rule, compact EBNF, sanctioned sugar, diagnostics |
| [Types](docs/plain/01-types.md) | `let`/`mut`, structural records, nominal closed unions, `Option`/`Result`, interfaces and coherence, inference limits |
| [Evaluation](docs/plain/02-evaluation.md) | Evaluation order, checked integers everywhere, `Float` and `Eq`, text, closures, `?`, `defer`, exhaustive matching, faults |
| [Derived ambiguities](docs/plain/03-ambiguities.md) | 26 questions: 21 resolved, 5 deferred — the substitute for the missing §12.1 |
| [Deferred features](docs/plain/04-deferred-features.md) | 18 deferrals (9 from the Master Prompt, 9 added), each with cost and trigger |
| [Language prior art](research/phase-01-01-language-prior-art.md) | Elm, Rust, Kotlin, Swift, Unison, Unicode — and what Plain refuses |
| [Honest limits](research/phase-01-02-honest-limits.md) | Five seams removed; ten domains that stay hard |
| [Decisions 0005–0007](docs/decisions/) | Surface doctrine · type and evaluation core · deferral policy |

## Method

For every phase: **Research → Decide → Build → Measure → Gate.**
Reuse before inventing. Prove every claim — or retract it. Every gate
can stop the project, and "an existing solution is better" is a valid
outcome.

**Evidence rules:** every claim carries exactly one label —
**Established** (cited external source, grade A or B), **Proposed**
(decided, not yet verified), or **Hypothesis** (needs measurement or
proof). Retracted claims stay in the register forever.

**Current status (2026-11-02):** Core Concerns v1.1 and Master Prompt
v1.1 recorded; Phase 0 executed and Gate 0 passed with conditions;
Phase 1 research and specification drafting complete as **draft v0.1**.
No ZEMA code exists yet — by design. Next step: **after C1/C5, build the
checked interpreter and the conformance suite**, which is what Gate 1
actually requires.
