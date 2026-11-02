# Phase 1 · Record 02 — The Honest Limits of One Language

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-01-02-honest-limits.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for Gate 1 research |
| **Evidence label** | Mostly **Proposed** interpretation over **Established** facts |

> Master Prompt Phase 1 requires an explicit catalog of limits: *"unified
> syntax still contains multiple semantic domains (queries, layout, text,
> GPU). One language removes seams; it does not eliminate domain
> complexity."* This record says where that line is, because a founding
> document that oversells unification will be quoted against the project
> at Gate 12.

---

## 1. What unification actually removes

| # | Seam removed | Why it is real | Label |
|---|---|---|---|
| R1 | **The type boundary between client and server** for the same data shape | One declaration instead of a DB row, an API schema, a client type, and a validator | P |
| R2 | **The build step as a separate language** | No transpiler, bundler, CSS preprocessor, or template compiler in the core loop | P |
| R3 | **Duplicated accessibility semantics** | Role, name, and state are derived from the same declaration that draws the control — if the compiler requires them | P |
| R4 | **Style/structure mismatch** | Layout is expressed in the same tree that carries state, so "the CSS says otherwise" cannot happen | P |
| R5 | **Formatter/linter dialect wars** | One canonical formatting; no per-project style configuration | P |

## 2. What unification does **not** remove

| # | Domain that stays hard | Why no language can absorb it | Consequence for ZEMA |
|---|---|---|---|
| H1 | **Text and internationalization** | Bidi, shaping, line breaking, and font fallback are algorithms over data (UAX #9/#14/#29, HarfBuzz-class shaping), not syntax | Phase 7 must integrate proven libraries and test scripts; syntax cannot help |
| H2 | **Layout** | Constraint solving and box models are numerical problems with genuine trade-offs and conflicts | Phase 6 owns the layout engine; Plain only gives it a notation |
| H3 | **Rendering and GPU** | Device capabilities, drivers, and frame scheduling are outside the language | Phase 6; software fallback is mandatory |
| H4 | **Data correctness** | Transactions, conflict resolution, and durability depend on storage and network behavior | Phase 9/10; CRDT honesty rules already recorded |
| H5 | **Security** | Authority comes from the host, not from types (Concern 8) | Phase 5; no type system can grant or revoke a capability |
| H6 | **Performance** | Cost is a property of the implementation and the workload, not the syntax | Phase 12; E1/E2 measure it |
| H7 | **Accessibility conformance** | Only testing with assistive technology establishes it | Phase 8; compiler warnings are aids, not proof |
| H8 | **Domain knowledge** | An accounting rule, a clinical constraint, or a tax schedule is not made simple by notation | The language can only avoid *adding* accidental complexity |
| H9 | **Migration of existing apps** | Rewriting is a cost no syntax eliminates | Adoption risk (Gate 11) |
| H10 | **Tooling** | LSP, debugger, formatter, profiler, package manager are products with their own roadmaps | Phase 13; explicitly "not a free consequence of unification" |

## 3. The specific promises Plain must not make

| Promise | Why it is forbidden | Where it would be caught |
|---|---|---|
| "You won't need to think about layout" | H2 — layout is a real design space | Phase 6 review |
| "It's fast because it's compiled" | H6 — no measurement | Gate 12 |
| "Accessibility comes for free" | H7 — warnings ≠ conformance | Gate 8 |
| "One language means one mental model" | H1–H4 each have their own model | Concern 2's honest limit |
| "You can't write a security bug" | H5 — authority is the host's | Gate 5 audit |
| "Rewrite once, never migrate again" | H9 — schema and data outlive syntax | Phase 9 review |

## 4. How the limits are carried into the design

1. **The specification states its own non-goals** (`docs/plain/README.md`
   §4), not only the project's.
2. **Every deferred feature carries a reason and a revisit trigger**
   ([`../docs/plain/04-deferred-features.md`](../docs/plain/04-deferred-features.md)),
   so "the language is small" is a recorded choice rather than an excuse.
3. **Domain complexity is named in the phase that owns it** (H1→7,
   H2→6, H4→9, H5→5, H6→12, H7→8), so no phase can assume another phase
   absorbed it.
4. **The Gate 1 review must reject any claim of the form "Plain makes X
   easy" without a task-log or a measurement.** Proposed as a review
   rule.

## 5. Sources

| # | Source | Grade |
|---|---|---|
| S1 | Master Prompt v1.1, Phase 1 research tasks (honest limits) and Phase 7/8/12 obligations: [`../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md`](../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md) | A (project record) |
| S2 | Core Concerns v1.1, Concern 2 ("one language removes *seams*; it does not make those problems disappear") and Concern 15 (tooling is not free): [`../docs/zema-master-prompt/00-Core-Concerns.md`](../docs/zema-master-prompt/00-Core-Concerns.md) | A (project record) |
| S3 | Unicode UAX #9 (bidi), #14 (line breaking), #29 (segmentation) — referenced as the algorithm family Phase 7 must integrate; exact versions to be pinned in Phase 7: <https://www.unicode.org/reports/> | A |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: 5 removed seams, 10 irreducible domains, 6 forbidden promises, 4 hand-offs. |
