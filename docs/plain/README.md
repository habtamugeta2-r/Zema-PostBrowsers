# Plain — Language Specification (Draft v0.2.5)

| Field | Detail |
|---|---|
| **Document** | Plain language specification, index and status |
| **Version** | 0.2.5 (draft — **not frozen**) |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 (Gate 1 **not attempted**: no executable core, no conformance run) |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Draft. Syntax is **not** frozen. Every normative rule is `Proposed` until the conformance suite passes and Gate 1 signs |
| **Evidence label** | **Proposed** throughout, except where a rule cites an external standard (then **Established** for the standard, **Proposed** for its adoption) |

> **Why this is a draft and not a gate-passing spec.** Gate 1 requires a
> safe executable core *and* a passing conformance suite. Neither exists.
> Gate 0 conditions **C1** (owner sign-off) and **C5** (the `PlainP`
> ruling) were **resolved by the owner on 2026-11-03**, so Phase 1 build
> is authorized and has begun; what remains before a Gate 1 attempt is
> **C2** (the research book) and ratification of the seven proposed
> decisions A-27/A-38/A-42/A-44/A-45/A-46/A-47. This specification is the
> *decide* half of the loop.

---

## 1. What this specification is

Plain is ZEMA's single application language. It is co-designed with the
runtime, the reactive state model, and the UI pipeline. This folder
defines the **core language only** — the part that must be frozen at
Gate 1. Everything about state propagation, layout, text, and
capabilities belongs to later phases and arrives as prelude types and
host grants, not as new syntax.

## 2. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and
**MAY** are interpreted as in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Rules carry stable IDs so that conformance tests, diagnostics, and the
ambiguity register can cite them:

| Prefix | Document | Meaning |
|---|---|---|
| `L-nn` | [`00-lexical-and-layout.md`](./00-lexical-and-layout.md) | Lexical structure, identifiers, layout (indentation), blocks, grammar |
| `T-nn` | [`01-types.md`](./01-types.md) | Type system, records, unions, generics, interfaces, aliases, inference limits |
| `E-nn` | [`02-evaluation.md`](./02-evaluation.md) | Evaluation order, numeric semantics, equality, closures, `?`, `defer`, faults, exhaustiveness |
| `S-nn` | [`00-lexical-and-layout.md`](./00-lexical-and-layout.md) §8 | Sanctioned sugar, each with a defined desugaring |
| `A-nn` | [`03-ambiguities.md`](./03-ambiguities.md) | Derived ambiguity register (the substitute for the missing book's §12.1) |
| `D-nn` | [`04-deferred-features.md`](./04-deferred-features.md) | Deferred features, each with a reason and a revisit trigger |

Rule IDs are permanent. A rule may be revised, never renumbered.

## 3. Document map

| # | Document | Contents |
|---|---|---|
| 0 | [`00-lexical-and-layout.md`](./00-lexical-and-layout.md) | Source encoding, identifiers (UAX #31, UTS #39), literals, comments, layout rules, compact EBNF grammar, sanctioned sugar, diagnostics requirements |
| 1 | [`01-types.md`](./01-types.md) | `let`/`mut`, records, tagged unions, `Option`/`Result`, generics and bounds, interfaces and coherence, `alias` vs `distinct`, inference limits |
| 2 | [`02-evaluation.md`](./02-evaluation.md) | Evaluation order, integer/float/text semantics, equality and ordering, closures and capture, `?` propagation, `defer`, faults, exhaustive matching |
| 3 | [`03-ambiguities.md`](./03-ambiguities.md) | 47 derived ambiguities: 42 resolved (proposed), 5 deferred, 0 open |
| 4 | [`04-deferred-features.md`](./04-deferred-features.md) | 20 deferrals: nine named by the Master Prompt plus eleven added here, each with a reason, cost, and revisit trigger |
| 5 | [`05-conformance-plan.md`](./05-conformance-plan.md) | The Gate 1 test plan: core vs platform scope, 357 allocated fixture targets, runner requirements — **plan only, zero fixtures written** |
| 6 | [`06-operational-semantics.md`](./06-operational-semantics.md) | **Non-normative** small-step core reduction draft, conjectures, and trace obligations |
| 7 | [`07-traceability.md`](./07-traceability.md) | Rule→verification matrix: all 106 rule IDs allocated to a method and an area; the rules Gate 1 cannot verify, with owners — **allocation, not coverage** |
| 8 | [`08-diagnostics-and-faults.md`](./08-diagnostics-and-faults.md) | The diagnostic and fault catalog: four code namespaces (`PL01nn`, `PL02nn`, **`PLFLnn` faults**, `PL11nn`), 73 active codes, and the 38 rules that correctly need no code — **proposal, owner ratification pending** |

Research that supports these choices:
[`../../research/phase-01-01-language-prior-art.md`](../../research/phase-01-01-language-prior-art.md)
and
[`../../research/phase-01-02-honest-limits.md`](../../research/phase-01-02-honest-limits.md),
[`../../research/phase-01-03-primary-source-audit.md`](../../research/phase-01-03-primary-source-audit.md),
[`../../research/phase-01-04-integrated-systems-and-plainp.md`](../../research/phase-01-04-integrated-systems-and-plainp.md),
and
[`../../research/phase-01-05-specification-audit.md`](../../research/phase-01-05-specification-audit.md).
Decisions:
[0005](../decisions/0005-language-surface-doctrine.md) (surface),
[0006](../decisions/0006-type-and-evaluation-core.md) (types and semantics),
[0007](../decisions/0007-deferred-features.md) (deferrals),
[0008](../decisions/0008-phase-01-research-and-draft-v02.md) (research continuation and v0.2 corrections),
[0009](../decisions/0009-unicode-pin-and-eq-ord-laws.md) (Unicode and Eq/Ord proposals),
[0010](../decisions/0010-gate-1-core-scope.md) (Gate 1 scope proposal),
[0011](../decisions/0011-unicode-diagnostic-profile.md) (initial Unicode diagnostic/data profile),
[0012](../decisions/0012-directional-confusability-and-ucd-completeness.md) (direction-aware confusability and completed Unicode data lock),
[0013](../decisions/0013-phase-1-reference-interpreter.md) (Python reference-interpreter vehicle),
[0014](../decisions/0014-unicode-data-pipeline.md) (manifest-verified Unicode pipeline),
[0015](../decisions/0015-conformance-runner-and-profiles.md) (conformance runner and dual profiles), and
[0016](../decisions/0016-script-value-alias-input.md) (Script value-alias input; proposed A-46 amendment).

## 4. The language's own non-goals

These are *language* non-goals, distinct from the project's
([`../../docs/problem-statement.md`](../../docs/problem-statement.md) §4):

1. **No general-purpose programming.** Plain targets interactive,
   data-driven service apps; it is not a systems language, not a
   scripting language, and not a replacement for Rust.
2. **No metaprogramming.** No macros, no compile-time code execution, no
   user-defined operators, no reflection.
3. **No implicit conversions**, numeric or otherwise. Widening is
   explicit; `distinct` types never convert silently.
4. **No exceptions and no null.** Failure is a value (`Result`), absence
   is a value (`Option`).
5. **No mode-dependent semantics.** A program's meaning MUST NOT depend
   on debug/release flags.
6. **No second way to say the same thing.** Sugar is sanctioned only
   with a defined desugaring (`S-nn`).
7. **No undocumented syntax.** If a rule is not in this folder, it is
   not Plain — including anything in examples or prototypes.
8. **No silent Unicode rewriting of data.** Identifiers are normalized;
   text literals are not. Case conventions do not exclude unicameral
   scripts.

## 5. Freeze policy

- Syntax freezes at **Gate 1**, and only after the conformance suite
  passes (Gate 1 exit criteria).
- Until then, changes MUST update the rule text **and** add a row to the
  ambiguity register, in the same commit.
- After freeze, a syntax change requires a dated revision, a decision
  record, and a gate — no exceptions (Core Concerns Concern 19).
- The formatter's canonical output is normative for *layout*, not for
  semantics; the formatter ships with the toolchain (Phase 13).

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 0.1 | Initial draft: four normative documents (98 numbered rules + 5 sanctioned sugars), 26 derived ambiguities (21 resolved, 5 deferred), 18 deferred features, a conformance plan, and **no executable implementation**. |
| 2026-11-03 | 0.2 | Research audit applied: 100 numbered rules (T-29/T-30 added), 43 ambiguities (35 resolved, 5 deferred, 3 open at that snapshot), 20 deferrals, corrected grammar/Unicode/defer/fault rules, non-normative semantics draft. Still **no executable implementation and no gate attempt**. |
| 2026-11-03 | 0.2.2 | Proposed decisions 0009/0010 resolve the three remaining ambiguity questions as proposals; 38 resolved, 5 deferred, 0 open. Owner/reviewer ratification pending. No implementation, fixtures, or gate attempt. |
| 2026-11-03 | 0.2.3 | Decision 0011 specifies UTS #55 chunk diagnostics and pins the initial 15 Unicode 17.0.0 data/test inputs; the active diagnostic fixture floor raises the planning sum to 307. No data vendored, no implementation, no fixtures, no gate attempt. |
| 2026-11-03 | 0.2.5 | **Diagnostic-identity pass.** Added [`08-diagnostics-and-faults.md`](./08-diagnostics-and-faults.md): five code namespaces (including the new `PL00nn` parse range and `PLFLnn` fault range), 20 new identifiers inserted into the normative rule text (15 errors, 5 faults), and the 38 rules recorded as correctly needing no code. No rule's *meaning* changed; only unnamed rejection conditions acquired names. Diagnostics floor 52 → 67 error/warning codes; fixture budget 341 → 356. Registry 53 → 73 codes. Proposal — owner ratification pending. |
| 2026-11-03 | 0.2.4 | Decision 0012 distinguishes UTS #55 source-order advice from UTS #39 all-direction guidance, proposes LTR/RTL/FS confusability, and adds `IndicSyllabicCategory.txt`; 47 ambiguities (42 proposed-resolved, 5 deferred, 0 open); A-47 proposes independent suppression of PL1104, 16 inputs verified. No implementation, fixtures, or gate attempt. |
| 2026-11-03 | 0.2.4 (rc) | Structure pass, no rule text changed. Added [`07-traceability.md`](./07-traceability.md) and repaired [`05-conformance-plan.md`](./05-conformance-plan.md) so every one of the 106 rule IDs is allocated to a conformance area and a verification method (14 rules had none); fixture budget 307 → 341. Fixed the `S-nn` section reference (§9 → §8), put `T-01…T-03` back in ID order, and moved the out-of-order `T-28`/`T-29`/`T-30` next to the rules they qualify with an explicit note that IDs are not renumbered. Recorded the two rules Gate 1 cannot verify (`E-31` partial, `E-34`) with owners. |
