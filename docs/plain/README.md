# Plain — Language Specification (Draft v0.1)

| Field | Detail |
|---|---|
| **Document** | Plain language specification, index and status |
| **Version** | 0.1 (draft — **not frozen**) |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 1 → Gate 1 (Gate 1 **not attempted**: no executable core, no conformance run) |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Draft. Syntax is **not** frozen. Every normative rule is `Proposed` until the conformance suite passes and Gate 1 signs |
| **Evidence label** | **Proposed** throughout, except where a rule cites an external standard (then **Established** for the standard, **Proposed** for its adoption) |

> **Why this is a draft and not a gate-passing spec.** Gate 1 requires a
> safe executable core *and* a passing conformance suite. Neither exists:
> Phase 1's build tasks are blocked on Gate 0 conditions **C1** (owner
> sign-off of the problem statement) and **C5** (the `PlainP` ruling).
> This specification is the *decide* half of the loop, written so that
> implementation and tests can begin immediately once C1/C5 clear.

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
| `S-nn` | [`00-lexical-and-layout.md`](./00-lexical-and-layout.md) §9 | Sanctioned sugar, each with a defined desugaring |
| `A-nn` | [`03-ambiguities.md`](./03-ambiguities.md) | Derived ambiguity register (the substitute for the missing book's §12.1) |
| `D-nn` | [`04-deferred-features.md`](./04-deferred-features.md) | Deferred features, each with a reason and a revisit trigger |

Rule IDs are permanent. A rule may be revised, never renumbered.

## 3. Document map

| # | Document | Contents |
|---|---|---|
| 0 | [`00-lexical-and-layout.md`](./00-lexical-and-layout.md) | Source encoding, identifiers (UAX #31, UTS #39), literals, comments, layout rules, compact EBNF grammar, sanctioned sugar, diagnostics requirements |
| 1 | [`01-types.md`](./01-types.md) | `let`/`mut`, records, tagged unions, `Option`/`Result`, generics and bounds, interfaces and coherence, `alias` vs `distinct`, inference limits |
| 2 | [`02-evaluation.md`](./02-evaluation.md) | Evaluation order, integer/float/text semantics, equality and ordering, closures and capture, `?` propagation, `defer`, faults, exhaustive matching |
| 3 | [`03-ambiguities.md`](./03-ambiguities.md) | 26 derived ambiguities and how each is resolved, deferred, or left open |
| 4 | [`04-deferred-features.md`](./04-deferred-features.md) | The nine deferrals named by the Master Prompt, plus nine added here, each with a reason, a cost, and a revisit trigger |
| 5 | [`05-conformance-plan.md`](./05-conformance-plan.md) | The Gate 1 test plan: what "passing" means, ≈285 fixtures by area, runner requirements — **plan only, zero fixtures written** |

Research that supports these choices:
[`../../research/phase-01-01-language-prior-art.md`](../../research/phase-01-01-language-prior-art.md)
and
[`../../research/phase-01-02-honest-limits.md`](../../research/phase-01-02-honest-limits.md).
Decisions:
[0005](../decisions/0005-language-surface-doctrine.md) (surface),
[0006](../decisions/0006-type-and-evaluation-core.md) (types and semantics),
[0007](../decisions/0007-deferred-features.md) (deferrals).

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
