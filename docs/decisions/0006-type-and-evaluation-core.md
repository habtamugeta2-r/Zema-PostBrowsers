# Decision Record 0006 — Type and evaluation core: values for absence and failure, checked arithmetic everywhere, matching that is always exhaustive

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 1 / Gate 1 (the semantics half) |
| **Status** | **Proposed** — normative text, unfrozen; E1/E2 must price the checked-arithmetic and closure rules |
| **Evidence label** | **Proposed** (with **Established** citations for prior art) |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); owner ratification of the language decisions pending |
| **Implements** | [`../plain/01-types.md`](../plain/01-types.md), [`../plain/02-evaluation.md`](../plain/02-evaluation.md) |

## Context

Three decisions determine whether a language is *predictable* (Concern 4),
and they interact: how absence and failure are represented, what
arithmetic does at the edges, and what happens when a program is
incomplete. Each has a widely used precedent that ZEMA deliberately does
not follow, and each precedent was chosen for reasons that do not apply
to app developers.

## Options considered

### Overflow and division

| Option | Precedent | Why not (or why) |
|---|---|---|
| A — wrap silently | C, Rust release builds [S1][S2] | Turns a correctness bug into corrupted data; invisible in testing |
| B — check in debug, wrap in release | Rust default [S1][S3] | **Same program, two meanings**; forbids "predictable behavior" outright |
| C — check always, fault on overflow | **chosen** | One meaning in every build; the fault is visible and testable |
| D — every arithmetic op returns `Result` | checked-int styles | Correct but unreadable: `a + b` becomes `a.checked_add(b)?` everywhere, and the common case dominates the code |

`Int.min / -1` and division by zero are treated the same way as
overflow: **fault**, not wrap, not `Result` (E-05, E-06).

### Absence and failure

| Option | Precedent | Assessment |
|---|---|---|
| A — null + exceptions | mainstream OO | Rejected: two failure channels, both invisible in types |
| B — `Option`/`Result` + no exceptions | Elm, Rust [S4][S1] | **Chosen.** Absence and failure are the only channels; both appear in signatures |
| C — `Option`/`Result` **and** catchable exceptions for host faults | Java-shaped | Rejected: catching a fault invites inconsistent state; the reactive transaction model (Phase 2) must discard, not resume (E-31, E-32) |

### Matching

| Option | Precedent | Assessment |
|---|---|---|
| A — statement and expression forms | Kotlin [S5] | Rejected: the same construct has two forms, so the guarantee's strength depends on context and version |
| B — expression-only, always checked | **chosen** | The guarantee cannot be bypassed; `_` must be written explicitly (E-25) |

## Decision

**Adopt the following core, normative in the specification:**

1. **No null, no exception primitives.** Absence is `Option<a>`; failure
   is `Result<a, e>` with the **value first**; `?` propagates only with
   the *same* error type (no implicit conversion).
2. **`Int` is 64-bit, checked in every profile; overflow and
   divide-by-zero fault.** Wrapping and saturating exist under explicit
   names; no optimization may weaken a check (E-05).
3. **Division truncates toward zero; `%` takes the dividend's sign**
   (E-06) — stated because "obvious" semantics differ between languages.
4. **`Float` is not `Eq`**; `Float.compare` gives a documented total
   order (E-08, E-09). This keeps derived equality sound for sets, maps,
   and reactive dependency comparison.
5. **Matching is an expression and is always exhaustive**, with explicit
   `_` where intended (E-23…E-25).
6. **Closures capture immutable bindings by value; capturing `mut` is an
   error** (E-16, E-17). No late-binding capture bug can be written.
7. **Faults terminate the task, never the platform**, discard the
   in-flight transaction, and are not catchable (E-30…E-33).
8. **Records are structural; unions are nominal and closed.** No
   subtyping, so no variance questions (T-06, T-10, T-25).
9. **Inference is local and rank-1; every function signature is
   annotated** (T-21). No higher-rank types, no overloading, no implicit
   conversions, no defaulting except `Int` literals.
10. **Program meaning is independent of build profile**, and a
    conformance fixture asserts it in both configurations (E-36).

## Consequences

- **Positive:** every failure path is in a type; no build-mode
  divergence to reason about; no capture trap; one match form, so
  exhaustiveness cannot depend on context; a reader can answer "what can
  go wrong here?" from the signature.
- **Negative / accepted costs:**
  - **Checked arithmetic costs cycles.** This is a **Hypothesis about
    magnitude**, not a measured fact: E1/E2 must record whether checks
    appear in any measured hot path, and Phase 12 must not accept a
    performance claim produced by disabling them.
  - Explicit `Option`/`Result` plumbing is verbose compared with
    exceptions; `?` reduces but does not remove it.
  - No catchable host failures means some apps must be restarted rather
    than degraded — the supervisor model (Phase 3) has to be good.
  - Rejecting `Float` from `Eq` will surprise users; the diagnostic must
    explain the NaN/`-0.0` reason and point at `Float.compare`.
- **New obligations created:**
  - The **conformance suite** must include: overflow in both build
    profiles, `Int.min / -1`, divide-by-zero, NaN ordering, `-0.0`
    ordering, non-exhaustive match, unreachable arm, `mut` capture, `?`
    with mismatched error types, recursive-record `Eq` rejection.
  - Phase 2 must confirm that fault-discards-transaction is implementable
    in the reactive core; Phase 4 must confirm task termination is clean.
  - Phase 3's interpreter must implement **checked arithmetic from day
    one** rather than retrofitting it, to avoid a performance cliff at
    Gate 3.
- **What would make us revisit this decision:**
  1. E1/E2 show checked arithmetic exceeding the frame budget on the
     reference workload **and** no targeted fix (e.g. hoisting checks,
     proof-carrying unchecked blocks) recovers it. The response is a new
     decision with measured data — **not** a silent build-profile switch.
  2. Phase 2 cannot discard a faulting transaction cleanly.
  3. Phase 8/13 show that `Option`/`Result` verbosity is a measured
     accessibility or productivity problem.

## Evidence

- Citations: Rust RFC 560 and the debug/release divergence [S1][S2][S3];
  Kotlin sealed-class exhaustiveness [S5] (the statement-form gap is C-grade and flagged for verification before Gate 1);
  Elm's "no runtime exceptions" posture [S4]; UAX/UTS only where
  identifiers and text are involved (not here). Full list:
  [`../../research/phase-01-01-language-prior-art.md`](../../research/phase-01-01-language-prior-art.md) §5.
- Experiments: **none yet.** E1 (Phase 2) and E2 (Phase 4) price the
  reactive and allocation consequences; Phase 12 tests every performance
  claim. This record creates obligations for those experiments rather
  than claiming results.
- Related records: [`0005-language-surface-doctrine.md`](./0005-language-surface-doctrine.md),
  [`../plain/03-ambiguities.md`](../plain/03-ambiguities.md) (A-09, A-10, A-11, A-14, A-22).
