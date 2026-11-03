# Plain 4 — Deferred Features

| Field | Detail |
|---|---|
| **Version** | 0.2.4 (draft) — text unchanged since 0.2.3; the version follows the specification's document set, not this file's edit history |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Active register — each entry is a **decision not to build**, with a trigger |
| **Rules** | `D-nn` |

> Master Prompt Phase 1 requires studying "the deferred features and
> **why** each is deferred". A deferral without a reason is scope
> erosion; a deferral without a trigger is a feature that never returns.
> Both are recorded for all 20 entries.

**Format:** what it is · why deferred · what its absence costs · trigger
to revisit · owning phase.

---

## Part A — The nine deferrals named by the Master Prompt

### D-01 — Algebraic effect handlers
- **What:** first-class effects with handlers (à la Koka/Eff), letting code declare "I perform effect E" and callers interpret it.
- **Why deferred:** handlers add effect typing, inference, resumption, and diagnostic complexity before the core exists. They are **orthogonal** to host authority: Unison-style handlers interpret effect requests, while a host can still require an opaque capability before performing the underlying operation. Deferral is a scope decision, not a claim that handlers inherently forge authority (research record 04).
- **Cost of absence:** some generic control patterns (async, generators) must be written with explicit types instead of handled effects.
- **Trigger to revisit:** Phase 5 shows a class of host services that cannot be expressed with capability parameters alone.
- **Owner:** Phase 5 / research track.

### D-02 — Refinement types and SMT solving
- **What:** types carrying predicates (`{ n: Int | n > 0 }`) discharged by an SMT solver.
- **Why deferred:** an SMT dependency in the compiler makes diagnostics unpredictable (timeouts, undecidable goals), and Phase 1's promise is *predictable behavior*. Validation belongs in constructors today.
- **Cost of absence:** invariants like "count ≥ 0" are enforced by smart constructors and tests, not by the type checker.
- **Trigger to revisit:** a recurring, measured class of app bugs that smart constructors demonstrably fail to prevent (Phase 13 task logs).
- **Owner:** research track only; never a prerequisite for release.

### D-03 — Const generics
- **What:** type parameters over values (`Vector<3, Float>`), enabling fixed-size arrays.
- **Why deferred:** the target app class works in lists and records, not fixed-size numeric arrays; const generics complicate inference (T-21) for no Gate 1 benefit.
- **Cost of absence:** no statically-sized numeric arrays; `List` is the only sequence.
- **Trigger to revisit:** Phase 6 needs fixed-size buffers for rendering and a list is measurably too slow (E1/Phase 6 data).
- **Owner:** Phase 6.

### D-04 — Hygienic macros
- **What:** compile-time code generation with hygiene guarantees.
- **Why deferred:** macros are the most common way a "small language" stops being readable — the surface becomes user-defined dialects. The co-design bet is that Plain's own notation is enough.
- **Cost of absence:** boilerplate must be written out; prelude/generics must cover the common cases.
- **Trigger to revisit:** Phase 13 finds repeated boilerplate that generics cannot express and that dominates task logs.
- **Owner:** Phase 13 (measured), never speculative.

### D-05 — Content-addressed modules
- **What:** definitions identified by hash, names as metadata (Unison-style).
- **Why deferred:** it changes how source is stored and diffed — a toolchain decision that must follow, not precede, a working toolchain. It also interacts with reproducible builds (Phase 11).
- **Cost of absence:** renames and dependency resolution behave like every mainstream language.
- **Trigger to revisit:** Phase 11's distribution/update work finds content addressing materially simplifies verified updates.
- **Owner:** Phase 11 / research track.

### D-06 — A query DSL
- **What:** a declared query language over app data integrated into Plain.
- **Why deferred:** it is a second language inside the language, and Phase 9's storage contract is SQLite-first with explicit transactions. A DSL before the data model exists would be designed against guesses.
- **Cost of absence:** queries are written as prelude functions over collections or as capability-gated SQL strings with bound parameters.
- **Trigger to revisit:** Phase 9 shows hand-written queries dominate app code and produce measured correctness defects (E5).
- **Owner:** Phase 9.

### D-07 — CRDTs
- **What:** conflict-free replicated data types as a first-class data model.
- **Why deferred:** the project's own honesty rule (Concern 12) — CRDTs converge but do not preserve business invariants, privacy, or authorization. v1 is server-authoritative offline, not multi-writer replication.
- **Cost of absence:** real-time multi-user collaboration is out of scope for v1; conflicts are resolved explicitly (E5).
- **Trigger to revisit:** a Phase 9 research track where the app class demonstrably needs concurrent multi-writer editing **and** the invariants survive without a server.
- **Owner:** Phase 9 research track.

### D-08 — LLVM, Wasm, and custom-VM back ends
- **What:** alternative code-generation targets.
- **Why deferred:** Phase 3's provisional runtime is a small checked interpreter; a back end is an optimization decision that requires profiles (E1/E2) to justify. A custom VM also adds a verifier — new attack surface (Decision A).
- **Cost of absence:** interpreted performance until a back end is justified; no AOT distribution.
- **Trigger to revisit:** Phase 12 measurements show the interpreter misses a stated budget on a metric that a back end can fix without changing semantics.
- **Owner:** Phase 3 (decision), Phase 12 (evidence).

### D-09 — Self-hosting
- **What:** writing the Plain compiler in Plain.
- **Why deferred:** bootstrapping is a milestone, not a foundation; it needs a stable language, a toolchain, and a distribution story. Self-hosting also couples language stability to compiler velocity.
- **Cost of absence:** the compiler stays in its host language (Rust for the runtime, per Phase 3).
- **Trigger to revisit:** Gate 14 (production) and only with a staffing plan for a second implementation.
- **Owner:** post-Gate 14 research track.

---

## Part B — Eleven additions this specification defers

### D-10 — Modules, multi-file apps, packages
- **What:** `import`, module namespaces, package resolution.
- **Why deferred:** a module system is a *tooling and distribution* design (visibility, cycles, versioning) and Phase 1's job is a frozen core. The conformance suite runs single files.
- **Cost of absence:** real apps cannot be structured across files in v0.1; the demo app is one file.
- **Trigger:** before Phase 13 (developer experience) or as soon as the reference app exceeds a single file.
- **Owner:** Phase 13.

### D-11 — Guard clauses in match arms
- **What:** `Some(v) if v > 0:` as an arm-level condition.
- **Why deferred:** guards interact with exhaustiveness (a guarded arm does not cover its variant) and would complicate E-23 for a capability a nested `if` already provides.
- **Cost of absence:** slightly deeper nesting in some matches.
- **Trigger:** Phase 13 task logs show guard-free matching is a measured readability problem.
- **Owner:** Phase 13.

### D-12 — Interface default method bodies
- **What:** a default implementation inside an `interface` declaration.
- **Why deferred:** defaults create a second place behavior can live, and coherence questions (T-18) around overriding them. v0.1 requires explicit implementations, so every behavior is where a reader looks.
- **Cost of absence:** some duplication across `impl` blocks.
- **Trigger:** duplication is measured as a maintenance cost in Phase 13.
- **Owner:** Phase 13.

### D-13 — Row polymorphism (record width)
- **What:** functions that accept "a record with at least these fields".
- **Why deferred:** inference for row types is a significant step up (T-21 explicitly limits inference) and structural records already cover the app-class need with exact types.
- **Cost of absence:** helper functions must name exact record types; some duplication.
- **Trigger:** Phase 6/13 shows record-shape duplication dominating component signatures.
- **Owner:** Phase 6 / 13.

### D-14 — Blanket implementations and specialization
- **What:** `impl Display for List<a> where a: Display` and more-specific overrides.
- **Why deferred:** both break the "one implementation per (interface, type)" guarantee (T-18) and make error messages depend on global search. Coherence is worth more than convenience in a language whose selling point is predictability.
- **Cost of absence:** `List` display is a named function, not an interface impl.
- **Trigger:** a demonstrated case where absence produces measured defects (not just verbosity).
- **Owner:** Phase 13.

### D-15 — Destructuring bindings (`let { a, b } = r`)
- **What:** pattern binding outside `when`.
- **Why deferred:** it is a second binding notation; `when` covers destructuring and field projection covers the common case.
- **Cost of absence:** a throwaway `when` for multi-field extraction.
- **Trigger:** Phase 13 task logs show a frequent, awkward pattern.
- **Owner:** Phase 13.

### D-16 — User-defined operators
- **What:** custom infix/prefix operators with declared precedence.
- **Why deferred:** unparseable-to-a-newcomer code, precedence conflicts, and a smuggling route for DSLs (D-06). The fixed table (§7 of doc 0, L-28) is closed.
- **Cost of absence:** matrix/monadic-style code reads as function calls.
- **Trigger:** none planned; this is the deferral most likely to stay permanent.
- **Owner:** not scheduled.

### D-17 — Nested/local declarations
- **What:** `type` and `fn` declared inside a function body.
- **Why deferred:** local types interact with inference limits and with the Eq recursion rule (T-27); local functions duplicate lambdas plus `let`.
- **Cost of absence:** helpers must be top-level (single file, D-10) or lambdas.
- **Trigger:** Phase 13, if top-level-only proves a measured obstacle.
- **Owner:** Phase 13.

### D-18 — Multi-line string literals
- **What:** `"""` blocks for embedded text.
- **Why deferred:** indentation-sensitive multi-line strings need their own dedent rules that interact with layout (L-19…L-23); v0.1 uses `\n` escapes.
- **Cost of absence:** verbose escaped strings for embedded text/JSON fixtures.
- **Trigger:** Phase 13, or the first conformance fixture that needs embedded multi-line text.
- **Owner:** Phase 13.

### D-19 — `Map`, `Set`, and `Hash`
- **What:** ordered/hash collections and the `Hash` interface.
- **Why deferred:** the draft mentions `Map`/`Set` without a complete API or a settled key law set. `Float` has a specified compare order but is not `Eq` or `Ord` (decision 0009). The Gate 1 law set is settled, but collection APIs, hash laws, and performance remain Phase 9 work.
- **Cost of absence:** Gate 1 uses `List` and records; lookup tables are explicit lists until Phase 9.
- **Trigger:** Phase 9 storage/query work needs keyed collections, with conformance fixtures for the decision-0009 key laws and any future Hash laws.
- **Owner:** Phase 9.

### D-20 — Unicode segmentation APIs in the core prelude
- **What:** `Text.graphemes`, `Text.scalars`, and related segmentation operations.
- **Why deferred:** extended grapheme clusters require UAX #29 data/version pinning and Phase 7 text work; they are not needed to freeze arithmetic, matching, closures, and faults.
- **Cost of absence:** Gate 1 text operations are concat/equal/compare only; user-visible segmentation arrives with the text phase.
- **Trigger:** Phase 7 text layout/input work, with a pinned UAX #29 version and fixtures.
- **Owner:** Phase 7.

---

## Register summary

| Part | Count | IDs |
|---|---|---|
| Named by the Master Prompt | 9 | D-01 … D-09 |
| Added by this specification | 11 | D-10 … D-20 |
| With a concrete owning phase | 20 | all |
| Permanently unscheduled | 1 | D-16 |

## Rules

1. A deferral **MUST** name a trigger. "Later" is not a trigger.
2. A deferred feature **MUST NOT** appear in the grammar, in examples, or
   in diagnostics as if it existed (README §4 non-goal 7).
3. Implementing a deferred feature requires: a decision record, a Gate 1
   (or later) revision, new ambiguity rows, and new conformance tests.
   There is no fast path.
