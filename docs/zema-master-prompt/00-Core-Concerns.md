# 0. Core Concerns — What This Whole Repository Is About

| Field | Detail |
|---|---|
| **Document** | 0. Core Concerns — the main problems ZEMA exists to solve |
| **Version** | 1.1 (improved and recorded edition) |
| **Date** | 2026-11-01 |
| **Status** | Synthesis of the full research book (Chapters 1–13 plus the two READMEs). **This file adds no new claims.** It distills what the book repeatedly treats as the main problems to solve. |
| **Read it** | **First.** This document says *what and why*. Its companion, the [Master Research & Build Prompt](./ZEMA-Master-Research-and-Build-Prompt.md), says *in what order and how* (Phases 0–14). |
| **Location** | `docs/zema-master-prompt/00-Core-Concerns.md` |

> **Implementation status — read before anything else**
>
> Nothing here is implemented yet. In the original research-book
> repository, every `Plain` code block was illustrative pseudocode
> (root README). In *this* repository, as recorded on 2026-11-01, the
> research book itself has not yet been imported — locating or
> importing it is an explicit Phase 0 task. Until then, all chapter
> references below are pointers to that book, and **no statement in
> this file should be read as describing working software.**

**Names:** **ZEMA** is the repository/project name. **Plain** is the
working name of the proposed language + runtime.

---

## Table of Contents

- [How to Read This Document](#how-to-read-this-document)
- [The 19 Concerns at a Glance](#the-19-concerns-at-a-glance)
- [Part A — The Three Founding Concerns](#part-a--the-three-founding-concerns)
  - [1. A post-browser application platform](#1-a-post-browser-application-platform)
  - [2. One easy, unified language — not a disconnected stack](#2-one-easy-unified-language--not-a-disconnected-stack)
  - [3. High performance and low resource use](#3-high-performance-and-low-resource-use)
- [Part B — Make-or-Break Concerns](#part-b--make-or-break-concerns-without-these-concerns-13-fail)
  - [4. Correct, predictable language semantics](#4-correct-predictable-language-semantics)
  - [5. Reactive state that is correct before it is fast](#5-reactive-state-that-is-correct-before-it-is-fast)
  - [6. Execution model and host isolation](#6-execution-model-and-host-isolation)
  - [7. Memory safety and concurrency safety](#7-memory-safety-and-concurrency-safety)
  - [8. Security: capabilities enforced by the host, not by types alone](#8-security-capabilities-enforced-by-the-host-not-by-types-alone)
  - [9. UI, rendering and layout](#9-ui-rendering-and-layout)
  - [10. Text and internationalization as a platform requirement](#10-text-and-internationalization-as-a-platform-requirement)
  - [11. Accessibility from the first vertical slice (release gate)](#11-accessibility-from-the-first-vertical-slice-release-gate)
  - [12. Data: local-first correctness, recovery and replication](#12-data-local-first-correctness-recovery-and-replication)
  - [13. Networking and protocol discipline](#13-networking-and-protocol-discipline)
  - [14. Delivery, identity, updates and adoption](#14-delivery-identity-updates-and-adoption)
  - [15. Developer experience measured honestly](#15-developer-experience-measured-honestly)
- [Part C — Concerns About How the Project Itself Must Be Run](#part-c--concerns-about-how-the-project-itself-must-be-run)
  - [16. Evidence discipline](#16-evidence-discipline)
  - [17. Stage gates instead of calendar promises](#17-stage-gates-instead-of-calendar-promises)
  - [18. Named risks and stopping conditions](#18-named-risks-and-stopping-conditions)
  - [19. Scope discipline](#19-scope-discipline)
- [One-Line Summary](#one-line-summary)
- [Appendix A — Core Concerns ↔ Master Prompt Map](#appendix-a--core-concerns--master-prompt-map)
- [Appendix B — Research-Book Gates ↔ Master-Prompt Gates](#appendix-b--research-book-gates--master-prompt-gates)
- [Appendix C — Improvement Record & Version History](#appendix-c--improvement-record--version-history)

---

## How to Read This Document

The 19 concerns fall into three groups:

- **Part A (Concerns 1–3) — the founding concerns.** Everything else
  in the book exists to serve, test, or constrain these three.
- **Part B (Concerns 4–15) — the make-or-break concerns.** Without
  these, Concerns 1–3 fail.
- **Part C (Concerns 16–19) — concerns about how the project itself
  must be run:** evidence, gates, risks, and scope.

**The numbers 1–19 are permanent IDs.** Cite them as "Concern 8,"
"Concern 16," and so on. (This numbering is also the source of the
`(1) … (4–15) … (16–19)` references in the original drafts' one-line
summary — see [One-Line Summary](#one-line-summary).)

Each concern ends with a **Book sources** line. Those citations
establish *background* only; under Concern 16, they never establish
Plain's own performance.

---

## The 19 Concerns at a Glance

| # | Concern | Part | Master Prompt phase(s) |
|---|---|---|---|
| 1 | A post-browser application platform | A — Founding | 0, 11, 14 |
| 2 | One easy, unified language — not a disconnected stack | A — Founding | 1, 13 |
| 3 | High performance and low resource use | A — Founding | 12 (and 2, 4, 6) |
| 4 | Correct, predictable language semantics | B — Make-or-break | 1 |
| 5 | Reactive state that is correct before it is fast | B — Make-or-break | 2 |
| 6 | Execution model and host isolation | B — Make-or-break | 3 |
| 7 | Memory safety and concurrency safety | B — Make-or-break | 4 |
| 8 | Security: capabilities enforced by the host | B — Make-or-break | 5 (stub in 3) |
| 9 | UI, rendering and layout | B — Make-or-break | 6 |
| 10 | Text and internationalization | B — Make-or-break | 7 |
| 11 | Accessibility from the first vertical slice | B — Make-or-break | 8 |
| 12 | Data: local-first correctness, recovery, replication | B — Make-or-break | 9 |
| 13 | Networking and protocol discipline | B — Make-or-break | 10 |
| 14 | Delivery, identity, updates and adoption | B — Make-or-break | 11 |
| 15 | Developer experience measured honestly | B — Make-or-break | 13 |
| 16 | Evidence discipline | C — Running the project | 12, and every phase |
| 17 | Stage gates instead of calendar promises | C — Running the project | Every gate; 14 |
| 18 | Named risks and stopping conditions | C — Running the project | 14 |
| 19 | Scope discipline | C — Running the project | 14, and every phase |

---

## Part A — The Three Founding Concerns

*Everything else in the book exists to serve, test, or constrain these
three.*

### 1. A post-browser application platform

**The concern.** Can a deliberately constrained, capability-secured
client runtime replace the browser for a *defined class* of
interactive, data-driven apps — not for general document browsing?

**The book's research question** (verbatim in substance):

> For that class of apps, can an integrated language/runtime deliver a
> better *measured* combination of developer effort, responsiveness,
> resource use, security, accessibility, and distribution than
> comparable web and native alternatives?

**What must not be forgotten.** The browser is also a *distribution
and security platform*, not just a renderer. A post-browser platform
must explicitly **rebuild, interoperate with, or admit giving up**
each of the following:

- URLs and links
- standards and the installed base
- origins and isolation
- security updates
- accessibility APIs
- developer tools
- search

**The honest baseline.** Comparisons must be against the *modern* web
— Wasm, WebGPU, HTTP/3, PWAs, CSP — not a caricature of it.

**Non-goals for the first prototype:**

- replacing general browsing
- rendering arbitrary HTML
- full offline collaboration
- a new internet protocol
- every-OS compatibility

**Book sources:** Ch. 1; Ch. 11; book README.

---

### 2. One easy, unified language — not a disconnected stack

**The concern.** Today, one app mixes markup, style, client code,
server code, schemas, a query language, build tooling, and deployment
configuration — and that separation imposes coordination costs. The
bet is **co-design**: one typed application language designed
*together with* its runtime, state model, and UI. (The book README
calls this the draft's strongest idea.)

**"Easy" is specified, not vibes:**

- a small core, with one notation for each feature before syntactic
  sugar;
- readable diagnostics with error spans;
- predictable behavior;
- local type inference, with annotations required at public
  boundaries;
- immutable `let` + explicit `mut`;
- records and tagged unions, with exhaustive matching;
- `Option`/`Result` — no null, and no unchecked exceptions in the
  core;
- checked integer overflow.

> **The honest limit, stated in the book:** unified syntax still
> contains multiple semantic domains (queries, layout, text, GPU, …).
> One language removes *seams*; it does not make those problems
> disappear. And tooling — package manager, LSP, debugger, formatter,
> documentation, profiler — is **not** a free consequence of
> unification.

**Guardrail — explicitly deferred** so the "easy" core stays easy:
algebraic effect handlers; refinement types / SMT solving; const
generics; hygienic macros; content-addressed modules; a query DSL;
CRDTs; LLVM/Wasm/custom-VM back ends; self-hosting.

**Book sources:** Ch. 1; Ch. 2 (esp. §2.5); Ch. 8; Ch. 11; Ch. 12
(esp. §12.5).

---

### 3. High performance and low resource use

**The concern.** Responsiveness and efficiency across the *whole
path*, not one microbenchmark — as defined by the Ch. 6 benchmark
protocol:

- cold and warm startup;
- interaction-to-present latency;
- missed frames at 60/120 Hz (frame budgets of ≈16.67 ms / ≈8.33 ms);
- CPU and GPU time;
- memory;
- install and update size, **including the shared runtime**;
- network bytes;
- energy.

**Where the hoped-for wins live** (hypotheses H1–H3, experiments
E1–E3 in Ch. 9):

- no DOM layer;
- compile-time-wired reactive dependencies;
- a retained scene graph instead of re-rendering;
- cheap allocation strategies;
- GPU rendering;
- small app packages amortizing a shared runtime.

> **The book's hard correction:** every number in the original drafts
> — "100×," fixed per-signal costs, battery savings, the 70/25/5
> allocation split, million-item lists at 120 fps, … — is an
> **unverified hypothesis, not a result.** The cost of a reactive
> update is proportional to the affected work; there is **no blanket
> O(1) promise**. Success means reproducible, equivalent-workload
> measurements against web/PWA and native/Flutter baselines, published
> **per metric, with raw data** — never a composite "100×" score.

**Book sources:** Ch. 1 §1.3; Ch. 2–4; Ch. 6 (esp. §6.2); Ch. 7
(evidence register); Ch. 9; Ch. 13.

---

## Part B — Make-or-Break Concerns (Without These, Concerns 1–3 Fail)

### 4. Correct, predictable language semantics

The following must be **defined before any compatibility promise** is
made:

- grammar and indentation rules;
- Unicode identifiers and confusable detection;
- evaluation order;
- overflow, division, and floating-point behavior;
- closures and capture semantics;
- generic bounds;
- nominal vs. structural interfaces, and coherence;
- alias vs. newtype;
- `?` propagation and `defer` cleanup semantics;
- inference limits — no unqualified "full Hindley–Milner +
  everything."

**What this requires:** a normative grammar, a small-step operational
semantics, and a conformance suite. Known draft ambiguities are
catalogued in §12.1 of the book and must all be resolved.

**Book sources:** Ch. 2; Ch. 8; Ch. 12 (esp. §12.1).

---

### 5. Reactive state that is correct before it is fast

- **Static dependency wiring** where the graph is provably known at
  compile time.
- **Explicit dependencies** — or a *tracked dynamic mechanism*, which
  is an experiment, not an assumption — for data-dependent branches,
  collections, and higher-order calls.
- **Transactional updates:** queue writes → update derived nodes
  *once*, in dependency order → reject cycles.
- **No glitches:** no observer may see a mix of old and new values
  (the *diamond problem*).
- **Stable keys and cleanup** for list items.
- **Specified behavior** for equality, reentrancy, and error
  propagation.

**Book sources:** Ch. 2 §2.3; Ch. 8 §8.6; §12.2; Ch. 9, experiment E1.

---

### 6. Execution model and host isolation

**The open decision** (Ch. 9, Decision A) — priced in security, not
only in speed:

| Option | Note |
|---|---|
| A small checked interpreter in Rust | The provisional first path |
| An existing, mature Wasm engine | Evaluate before inventing anything |
| A new custom bytecode VM | A new verifier is new attack surface: bounds, control flow, stack types, budgets, malformed input |

**Non-negotiable containment rules**, whichever option is chosen:

- untrusted code runs under **quotas and timeouts**;
- a misbehaving app **can be terminated** without harming other apps
  or the host;
- **no raw FFI, C ABI, or syscalls** for untrusted guests.

**Book sources:** Ch. 5; Ch. 8 §8.7; §12.4; Ch. 9, Decision A.

---

### 7. Memory safety and concurrency safety

Ownership, aliasing, lifetimes, destruction, and FFI must be
**specified before any safety claim is made**. Each candidate memory
strategy carries its own obligation:

| Candidate strategy | Obligation it creates |
|---|---|
| Scoped arenas / regions | Escape proofs |
| Reference counting / Perceus | A cycle strategy — handles detect staleness but do not reclaim cycles |
| Generational handles | A defined answer to generation wraparound |
| Tracing garbage collection | Pause-time and retained-memory measurement |
| Explicit graph owner + weak edges | Destructor and resource-cleanup rules |

**Concurrency model:**

- structured scopes that own their child tasks;
- cooperative cancellation at defined points;
- bounded channels with backpressure;
- **no race-freedom claim without a checked shared-memory model.**

**Book sources:** Ch. 4; §12.3; Ch. 9, experiment E2.

---

### 8. Security: capabilities enforced by the host, not by types alone

**Threat model.** Apps, package bytes, remote responses, fonts,
images, and persisted state are **all untrusted — including signed
malicious apps**.

**The central rule:**

> Effects in type signatures give *auditability*. Authority comes
> **only** from opaque, non-forgeable, host-issued capability
> handles — checked on every sensitive call, with attenuation and
> revocation.

**Supporting requirements:**

- OS sandboxing and process separation, plus quotas;
- network checks *beyond* a domain allowlist: redirects, DNS
  rebinding, IP/port and proxy handling, TLS identity verification;
- unspoofable system permission prompts;
- bounded parsing of all app-controlled input (UI content, text,
  images, fonts).

**Book sources:** Ch. 2 §2.2; Ch. 3 §3.5; Ch. 5; Ch. 8 §8.4.

---

### 9. UI, rendering and layout

**The pipeline to retain:**

```text
input → semantic view tree → layout → retained scene → renderer → display
                                      ↳ accessibility tree, fed from the same semantics
```

**Rules from the book:**

- **Prototype on maintained stacks** (e.g., winit/wgpu with a Vello
  back-end family) instead of writing a GPU engine.
- Provide a **CPU/software fallback**.
- **Measure each stage separately** — event, state, layout, scene,
  presentation. *A fast signal write is not fast visible pixels.*
- **Layout starts simple:** row/column/stack plus virtualized lists.
  Cassowary-style constraints are a *separate experiment* requiring
  specified conflict behavior.
- **Virtualized lists must preserve** item identity, focus, scroll
  anchors, and off-screen accessibility.

**Book sources:** Ch. 3; §13.1; Ch. 9, Decision B.

---

### 10. Text and internationalization as a platform requirement

Text is a **platform requirement, not an afterthought**:

- Unicode segmentation, bidirectional layout, and line breaking
  (UAX #29 / #9 / #14);
- shaping via a proven engine (**HarfBuzz**);
- font fallback across scripts;
- selection and editing by **grapheme cluster**;
- clipboard integration and IME composition;
- emoji and color fonts; high-DPI displays.

**The test matrix explicitly includes:** Arabic, Hebrew, Indic
scripts, Ethiopic, CJK, combining marks, and mixed-direction text.

**Caution:** SDF glyph rendering is **not** assumed to be universally
accurate for all scripts.

**Book sources:** Ch. 3 §3.3; Ch. 9, experiment E4.

---

### 11. Accessibility from the first vertical slice (release gate)

- Every interactive control exposes **role, name, state, value, and
  actions** through the OS accessibility API.
- **Keyboard-only operation**, with correct focus order and focus
  restoration.
- **Screen-reader announcements** for dynamic changes.
- Accessible dialogs and error/conflict flows; high contrast, text
  scaling, and reduced-motion support.

**The gate:** compiler warnings and semantic-tree snapshots are
*aids, not proof*. **Manual testing** — with screen readers,
keyboard only, magnification, and IME, **including
assistive-technology users as testers** — gates the release on each
OS. WCAG 2.2 / WCAG2ICT are references, not conformance by citation.

**Book sources:** Ch. 3 §3.4; Ch. 8 §8.6; Ch. 10 §10.6.

---

### 12. Data: local-first correctness, recovery and replication

**Local truth: SQLite transactions**, with:

- per-app isolation and quotas;
- migrations, backup, and deletion;
- encryption and clear key ownership;
- honesty about durability: it is only as strong as the configured
  synchronous/WAL settings and the underlying filesystem and
  hardware.

**The offline extension (Ch. 10) is server-authoritative:**

- durable operation IDs;
- **one local transaction** covering the pending operation *and* its
  optimistic projection;
- idempotent retries after lost responses — "effectively-once"
  *only within* a defined deduplication scope and retention window;
- version checks and **explicit conflict UX**;
- server-side authorization on **every** write.

> **CRDT honesty:** CRDTs, if ever used, give convergence *under
> stated assumptions only*. They do not by themselves preserve
> business invariants (payments, stock levels, uniqueness), privacy,
> or authorization — and Hybrid Logical Clock timestamps alone
> cannot detect concurrency.

**Book sources:** Ch. 5 §5.5; Ch. 10; §13.3; Ch. 9, experiment E5.

---

### 13. Networking and protocol discipline

- **Start with HTTPS** plus existing schema encodings.
- **QUIC is an evaluation, with a TCP fallback.** Its 0-RTT early
  data is replayable, so **no non-idempotent mutations** may be sent
  in it.
- **The custom "PlainProto" protocol is deferred.** Before *any*
  wire format is designed, the following must be specified:
  negotiation; framing and size limits; authentication; backpressure;
  ordering; timeouts; retries and idempotency; schema evolution;
  cancellation.
- **Zero-copy views still require** bounds checking and UTF-8
  validation.
- **Server snapshots carry portable data only** — never pointers,
  never capabilities.

**Book sources:** Ch. 5 §5.4; §13.2.

---

### 14. Delivery, identity, updates and adoption

**The platform must be installed and trusted — and that cost is part
of every comparison:** runtime download, app package size, updates,
cold start, privacy, power, maintenance, and device support.

**Packages require:**

- versioned manifests and publisher identity;
- digests and signatures — remembering that *a signature
  authenticates a key, not the safety of the code*;
- trust bootstrap;
- key rotation and compromise recovery;
- revocation and expiry;
- anti-rollback protection;
- reproducible builds (with TUF — The Update Framework — as prior
  art).

**The distribution decision** — standalone runtime vs.
browser-hosted Wasm vs. native packaging — must be compared on:
install friction, deep links, copy/paste, file opening, identity,
accessibility, updates, and current app-store rules on downloaded
code.

**Book sources:** Ch. 1 §1.4; Ch. 5 §5.3; Ch. 9, Decision D.

---

### 15. Developer experience measured honestly

- **Productivity claims are unverified until measured.** The drafts'
  lines-of-code tables prove nothing: an honest comparison controls
  for feature parity, tests, migrations, accessibility, error
  handling, schema, configuration, and runtime code. Prefer **task
  logs and maintainability exercises** over line counts.
- **The standard library is tiered:** a pure foundation / granted
  host services / scoped concurrency / platform services / optional
  replication.
- **Cryptography comes from reviewed implementations only** — never
  hand-rolled.
- **Content hashes support caching.** They do **not** prove semantic
  or version compatibility.

**Book sources:** Ch. 12 §12.4–12.5; §13.4.

---

## Part C — Concerns About How the Project Itself Must Be Run

### 16. Evidence discipline

Three labels govern **every** statement the project makes:

| Label | Meaning |
|---|---|
| **Established** | Backed by a cited external source |
| **Proposed** | A decision that has been made but needs implementation |
| **Hypothesis** | Needs a measurement or a formal proof |

**Rules:**

- A reference (Ch. 7, R1–R29) establishes *background* — **never**
  Plain's own performance.
- The Ch. 7 **evidence register** lists what would actually establish
  each headline claim.
- Direct source inspection so far is **README-level only** (§13.5) —
  a limitation to state, not to hide.

**Book sources:** Ch. 7; §13.5.

---

### 17. Stage gates instead of calendar promises

The research book runs the project by **milestone gates**, each
independently reviewable and each able to terminate the project:

| Book gate | Meaning |
|---|---|
| **Gate 0** | Discovery and specification |
| **Gate 1** | A safe, executable core |
| **Gate 2** | An accessible, single-device slice — the task list (add/toggle/filter/restart, local storage, capability broker; the Ch. 8 contract) |
| **Gate 3** | Delivery, plus a measured comparison against baselines |
| **Gate 4** | Optional research branches |
| **Gate 5** | Production readiness |

> **Numbering caution:** these are the *book's* six milestone gates.
> The companion Master Prompt numbers its fifteen *phase* gates
> Gate 0–Gate 14. The two systems are reconciled in
> [Appendix B](#appendix-b--research-book-gates--master-prompt-gates).
> When in doubt, write "Book Gate 2" or "Prompt Gate 8" — never a
> bare "Gate 2."

**Book sources:** Ch. 6.

---

### 18. Named risks and stopping conditions

| Risk | Agreed response if it materializes |
|---|---|
| Adoption / install friction is too high | Pivot (e.g., browser-hosted Wasm) or stop |
| Security-maintenance capacity is insufficient | Stop — do not ship an insecure platform |
| Accessibility gaps remain | **Block the release** |
| A performance hypothesis fails | **Publish the result**, then simplify or stop |
| Language scope explodes | Freeze the syntax per gate |
| Offline data loss occurs | Disable sync |
| Platform / app-store restrictions apply | Re-evaluate distribution |

And overarching all of them:

> **"An existing web/PWA/Wasm/native solution meets the problem
> better" is an explicitly valid outcome of this research.**

**Book sources:** Ch. 1 §1.4; Ch. 9 §9.3.

---

### 19. Scope discipline

- **One workload:** the task list app.
- **One desktop OS.**
- **Local data + HTTP first.**
- **Reuse existing libraries before inventing:** the renderer, text
  shaping, SQLite, a Wasm engine, CRDT libraries.
- **Everything else is a research track** — a custom protocol, a
  custom VM/LLVM back end, self-hosting, effect handlers,
  refinement types, distributed sync, a public registry — each with
  its own hypothesis, baseline, security review, and decision
  record, and **never a prerequisite** for the first release.

**Book sources:** book README; Ch. 6; Ch. 9 §9.4; Ch. 12.

---

## One-Line Summary

> Build a post-browser platform **(1)** where apps are written in one
> small, easy, unified typed language co-designed with its runtime/UI
> **(2)**, that is measurably faster and lighter than equivalent
> web/native apps **(3)** — while holding the line on semantics,
> reactivity correctness, memory/concurrency safety, host-enforced
> capability security, rendering/text/accessibility, local-first data
> recovery, networking, secure delivery/updates and adoption
> **(4–15)** — and prove every claim through gated, reproducible
> experiments with explicit stopping conditions **(16–19)**.

*The numbers are the concern IDs in this document. In the companion
Master Prompt, the same sentence is rewritten using phase numbers;
both forms say the same thing.*

---

## Appendix A — Core Concerns ↔ Master Prompt Map

| Concern | Master Prompt phase(s) | Key experiments / decisions |
|---|---|---|
| 1. Post-browser platform | 0, 11, 14 | Decision D (distribution) |
| 2. One unified language | 1, 13 | — |
| 3. Performance | 12 (inputs from 2, 4, 6) | Hypotheses H1–H3; experiments E1–E3 |
| 4. Language semantics | 1 | Conformance suite (Gate 1) |
| 5. Reactive correctness | 2 | E1 |
| 6. Execution & isolation | 3 | Decision A |
| 7. Memory & concurrency | 4 | E2 |
| 8. Capability security | 5 (broker stub in 3) | Security audit (Gate 5) |
| 9. UI / rendering / layout | 6 | Decision B |
| 10. Text & i18n | 7 | E4 |
| 11. Accessibility | 8 | Manual AT testing (Prompt Gate 8) |
| 12. Data & replication | 9 | E5 |
| 13. Networking | 10 | QUIC decision record |
| 14. Delivery & adoption | 11 | Decision D |
| 15. Developer experience | 13 | Task-log study |
| 16. Evidence discipline | 12, and every phase | Evidence register |
| 17. Stage gates | Every gate; 14 | Gate reviews |
| 18. Risks & stopping conditions | 14 | Risk table review at every gate |
| 19. Scope discipline | 14, and every phase | Research-track decision records |

> **Open numbering items (for Phase 0):** this synthesis confirms
> that experiments **E1–E3** belong to the Ch. 9 performance cluster
> (H1–H3), but the Master Prompt defines build tasks only for E1,
> E2, E4, and E5 — **E3's definition must be recovered from the book
> when it is imported.** Likewise, Decisions A, B, and D are cited
> here with no Decision C. Both items are tracked in
> [`PHASE-TRACKER.md`](./PHASE-TRACKER.md).

---

## Appendix B — Research-Book Gates ↔ Master-Prompt Gates

The book's six *milestone* gates (Concern 17) are each **composed
of** one or more of the Master Prompt's fifteen *phase* gates. The
prompt's numbering is the operational one used day to day; the
book's gates remain the milestone vocabulary of Ch. 6.

| Book milestone gate | Satisfied by Prompt gate(s) | Notes |
|---|---|---|
| Book Gate 0 — Discovery / spec | Prompt Gate 0 (and the specification half of Gate 1) | Problem frozen; language specified |
| Book Gate 1 — Safe executable core | Prompt Gates 1, 3, 4 | Language runs safely, isolated, memory-safe |
| Book Gate 2 — Accessible single-device slice | Prompt Gates 2, 5, 6, 7, 8, 9 (local data) | The Ch. 8 task-list contract, fully accessible |
| Book Gate 3 — Delivery + measured comparison | Prompt Gates 10, 11, 12, 13 | Installable, updatable, honestly benchmarked |
| Book Gate 4 — Optional research branches | *No phase gate* — parallel research tracks | Each track needs its own hypothesis, baseline, security review, and decision record (Concern 19) |
| Book Gate 5 — Production readiness | Prompt Gate 14 | Final go / no-go |

---

## Appendix C — Improvement Record & Version History

### What was improved in v1.1 (2026-11-01)

The v1.0 text was substantively complete and carefully hedged; the
improvement pass was therefore presentational and integrative. **No
concern, requirement, caveat, or source citation was removed.**

| Change | Why |
|---|---|
| Added a document-control header, table of contents, and "read this first" positioning as document **0** | v1.0 arrived as unheaded plain text with no version, status framing, or navigation. |
| Converted each concern's single long paragraph into headed sub-points, lists, and (for Concerns 6, 7, 17, 18) tables | The 19 concerns are reference material; they must be scannable and citable ("Concern 7's table"), not only readable start-to-finish. |
| Moved every trailing `(Ch. …)` citation to a uniform **Book sources** line per concern | In v1.0 the citations were embedded mid-sentence, which hid them and broke up the argument. They are now findable at a glance. |
| Extracted the research question (Concern 1), the "honest limit" (Concern 2), the performance correction (Concern 3), the capability rule (Concern 8), and the CRDT warning (Concern 12) into blockquotes | These five sentences carry the project's intellectual honesty. They should be impossible to skim past. |
| Added the [19 Concerns at a Glance](#the-19-concerns-at-a-glance) table and Appendices A–B mapping concerns to Master Prompt phases and reconciling the two gate-numbering systems | v1.0 used the *book's* Gate 0–5 milestone numbering with no warning that the companion prompt numbers gates differently — the single most likely source of future confusion. The maps are editorial additions and are labeled as appendices so they cannot be mistaken for book claims. |
| Recorded the two open numbering gaps (experiment E3, Decision C) as Phase 0 items instead of silently closing the sequences | This synthesis locates E3 in the Ch. 9 performance cluster but does not define it; inventing a definition would violate Concern 16. |
| Corrected the status framing for *this* repository | v1.0 said "the repository contains only the research book." In this repository the book has not yet been imported, so the header now says so plainly and makes the import a Phase 0 task. |
| Fixed grammar and typography: "Retained the pipeline" → "The pipeline to retain"; `division/ floating-point` spacing; `plain` → `Plain` where the language is meant | Small errors in a founding document get copied everywhere. |
| Normalized spelling to US English (*internationalization, authorization, color*) to match Master Prompt v1.1 | Two founding documents in two dialects would drift further with every edit. (The meaning of every affected sentence is unchanged.) |

### What was deliberately **not** changed

- **The 19-concern structure and numbering** — including the A/B/C
  grouping and the one-line summary that depends on it.
- **Every caveat.** The unverified-number warnings, the "no blanket
  O(1)" correction, the CRDT and SDF limits, the "aids, not proof"
  accessibility rule, and "an existing solution may be better" all
  stand verbatim in substance.
- **The synthesis claim itself:** this file still adds no new
  technical claims. Appendices A–B are cross-references between two
  existing documents, not new assertions about ZEMA.

### Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-01 | Original synthesis of research-book Chapters 1–13 plus the two READMEs: 19 concerns in three parts, written as continuous prose. |
| 1.1 | 2026-11-01 | Improved and recorded edition (this file): document control, TOC, scannable structure, per-concern source lines, at-a-glance table, Master Prompt cross-maps (Appendices A–B), and this record. No substance removed. |

---

**Next step:** [Master Research & Build Prompt, Phase 0](./ZEMA-Master-Research-and-Build-Prompt.md#phase-0--historical-foundations--problem-definition)
— *research deeply, record everything, build one thing at a time, and
prove it before moving on.*
