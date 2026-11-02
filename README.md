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
Gate 0 passed with conditions (C1–C5).** Phase 1 — *The Unified
Language: "Plain"* — is next; its research tasks may start now, its
build tasks wait on owner sign-off (C1) and the `PlainP` ruling (C5).

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
v1.1 recorded; Phase 0 executed and Gate 0 passed with conditions. No
ZEMA code exists yet — by design. Next step: **Phase 1 — research the
language, then (after C1/C5) build the safe executable core.**
