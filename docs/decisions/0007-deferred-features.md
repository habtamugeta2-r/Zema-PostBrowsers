# Decision Record 0007 — Defer 18 features, each with a cost and a trigger, and make the deferral list part of the frozen spec

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — ratifies the register; individual triggers are revisited at the phases named |
| **Evidence label** | **Proposed** |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); owner sign-off pending (C1/C5) |
| **Implements** | [`../plain/04-deferred-features.md`](../plain/04-deferred-features.md) |

## Context

Master Prompt Phase 1 asks for "the deferred features and **why** each is
deferred", and Phase 14 makes the same list a release condition. Core
Concerns Concern 19 calls scope discipline a founding concern, and
Concern 2 names the guardrail: the "easy" core stays easy only if
features that would complicate it are explicitly excluded.

The failure mode this decision prevents is familiar: a language starts
small, each feature is "just one more", and three years later the spec
describes a language nobody can hold in their head — while the original
app class was never served better.

## Options considered

### Option A — Build features as users ask

- What it is: responsive scope; add what the demo needs.
- Cost: no defensible boundary; every addition is locally reasonable.
- Fit: **rejected** — contradicts Concern 19 and the Gate 1 freeze.

### Option B — Defer everything not needed for the task list, with a written register

- What it is: a closed list of 18 deferrals, each with: what it is, why
  deferred, what its absence costs, a trigger, an owning phase.
- Cost: some genuinely useful features are unavailable in v1; some
  duplication in app code.
- Fit: **chosen.**

### Option C — Defer nothing (declare the full language up front)

- Fit: **rejected.** It makes Gate 1 unreachable and re-introduces the
  scope explosion the project names as a stopping condition.

## Decision

**Choose Option B.** The register in
[`../plain/04-deferred-features.md`](../plain/04-deferred-features.md) is
normative and part of the frozen specification at Gate 1:

- **9 deferrals come from the Master Prompt**: algebraic effect handlers,
  refinement types/SMT, const generics, hygienic macros, content-addressed
  modules, a query DSL, CRDTs, LLVM/Wasm/custom-VM back ends,
  self-hosting.
- **9 are added by this specification** because the implementation forced
  the question: modules/multi-file apps, match guards, interface
  defaults, row polymorphism, blanket impls/specialization, `let`
  destructuring, user-defined operators, local declarations, multi-line
  strings.

Three rules make the register binding rather than decorative:

1. **Every deferral names a trigger.** "Later" is not a trigger; a phase
   or a measurement is.
2. **No deferred feature may appear in the grammar, in examples, or in
   diagnostics as if it existed.** A test asserts that each deferred
   construct produces a "not in Plain" diagnostic naming the deferral
   (S-5, L-29, L-28).
3. **Implementing a deferral requires a decision record, a spec
   revision, new ambiguity rows, and new conformance tests** — no fast
   path exists, even for a "small" feature.

## Consequences

- **Positive:** Gate 1 can actually freeze; the language stays readable;
  scope arguments become "which trigger fired?" rather than taste; and
  the deferral list doubles as the research-track list Phase 14 requires.
- **Negative / accepted costs:**
  - v0.1 **cannot express a multi-file app** (D-10) or a guarded match
    (D-11); the reference app must fit one file, and the interpreter demo
    must respect that.
  - Some app code will duplicate record-shape helpers (D-13) and display
    functions (D-14).
  - Deferring self-hosting and back ends keeps the implementation in a
    host language longer than enthusiasts will like.
- **New obligations created:**
  - Phase 13 must **measure** whether the deferral list caused real
    productivity loss (task logs), not merely whether developers wanted
    features. Desire is not evidence.
  - Each owning phase must, at its gate, state whether its trigger fired.
    A trigger that fires without a decision is a silent scope change.
  - The conformance suite must include a "not in Plain" fixture per
    deferred construct that could plausibly be typed by mistake.
- **What would make us revisit this decision:** a deferral whose absence
  causes a **measured** defect class (not verbosity) at its owning phase.
  Revisiting does not mean implementing: it means recording a new
  decision, which may still say no.

## Evidence

- Citations: Master Prompt Phase 1 (deferred-features research task) and
  Phase 14 (research tracks) — [`../zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md`](../zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md);
  Core Concerns Concerns 2 and 19 — [`../zema-master-prompt/00-Core-Concerns.md`](../zema-master-prompt/00-Core-Concerns.md).
  Prior art for the deferral *costs*: Elm (small core, no exceptions) [S1]
  and Unison (content addressing deferred) [S6], in
  [`../../research/phase-01-01-language-prior-art.md`](../../research/phase-01-01-language-prior-art.md).
- Experiments: none — this is a scope decision. Its effects are measured
  in Phase 13 and reported at Gate 14.
- Related records: [`0005-language-surface-doctrine.md`](./0005-language-surface-doctrine.md),
  [`0006-type-and-evaluation-core.md`](./0006-type-and-evaluation-core.md).
