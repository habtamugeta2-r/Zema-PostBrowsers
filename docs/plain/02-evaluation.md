# Plain 2 — Evaluation, Numbers, Matching, and Faults

| Field | Detail |
|---|---|
| **Version** | 0.2.4 (draft) — text unchanged since 0.2.3; the version follows the specification's document set, not this file's edit history |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Proposed — normative text, not frozen |
| **Rules** | `E-nn` |

---

## 1. Evaluation order

- **E-01** Evaluation is **strict and call-by-value**. There are no lazy bindings and no thunks visible to the program.
- **E-02** Within a construct, sub-expressions are evaluated **left to right**:
  - function call: callee, then arguments in source order;
  - record literal: fields in source order;
  - list literal: elements in source order;
  - binary operator: left, then right.
- **E-03** A pipe (S-2) inserts its left operand as the **last** argument, so `x |> f(y)` desugars to `f(y, x)` and therefore evaluates `y` before `x`. This order is **defined and deterministic**, even when it is surprising. Tooling **SHOULD** flag a pipe whose operands both call the host; the language does not pretend the order is unspecified.
- **E-04** `if` and `when` evaluate their scrutinee **exactly once** and then exactly one branch.

## 2. Integers

- **E-05** `Int` is 64-bit signed two's complement. Arithmetic is **checked in every build profile** — there is no debug/release divergence (decision [0006](../decisions/0006-type-and-evaluation-core.md)). Overflow is the fault `PLFL01`; `Int.min / -1` is `PLFL02`.
  - overflow of `+`, `-`, `*`, unary `-`, and `Int.min / -1` raises a **fault** (E-30), not a wrapped value and not a compile error;
  - explicit, named alternatives live in the prelude: `Int.wrapping_add`, `Int.saturating_add`, `Int.checked_add -> Option<Int>`;
  - an implementation **MUST NOT** silently optimize a checked operation into a wrapping one. A conformance test asserts that `Int.max + 1` faults in optimized builds.
- **E-06** Integer division truncates **toward zero**; the remainder `%` takes the sign of the **dividend** (`-7 / 2 == -3`, `-7 % 2 == -1`). Division by zero is the fault `PLFL03`; remainder by zero is `PLFL04`.

## 3. Floating point

- **E-07** `Float` is IEEE 754 binary64. No implicit conversion from `Int` exists in either direction; use `Int.to_float` and `Float.to_int` (which returns `Option<Int>` because of range and NaN).
- **E-08** `Float` is **not** an `Eq` type and does not support `==` (`PL0219`). Reason: IEEE equality is not reflexive (`NaN != NaN`) and conflates `-0.0` and `+0.0`, which makes a derived structural equality unsound for sets, maps, and reactive dependency checks (Phase 2).
- **E-09** Ordering is explicit: `Float.compare(a, b) -> Ordering` defines a **total order** — `-0.0 < +0.0`, all NaNs compare `Greater` than every non-NaN and `Equal` to each other. `Float.is_nan`, `Float.abs`, and `Float.round` are prelude functions. This order is **not** IEEE 754 `totalOrder`; it is a Plain-specified ordering. It does **not** make `Float` an `Ord` type: `Ord` requires `Eq`, and `Float` is not `Eq` (decision 0009). Generic ordered collections therefore do not accept `Float` keys/elements; callers may use `Float.compare` explicitly. Map/Set are deferred (D-19).
- **E-10** Floating-point results are not promised to be bit-identical across CPUs beyond IEEE 754 requirements; no fast-math is permitted, and the compiler **MUST NOT** reassociate float arithmetic.

## 4. Text

- **E-11** `Text` is immutable UTF-8. There is **no** integer indexing, slicing, or `length` returning bytes (`PL0116`). The prelude exposes intent-named operations only:
  - `Text.concat(parts: List<Text>) -> Text` — concatenation does **not** normalize; the result may be non-NFC even if every part is NFC ([UAX #15 revision 57](https://www.unicode.org/reports/tr15/tr15-57.html));
  - `Text.equal(a, b) -> Bool` and `Text.compare(a, b) -> Ordering` — code-point equality/order, documented as *not* locale collation (Phase 7 owns collation);
  - interpolation uses `Display.display`, not a second `Text.from` notation (S-3).
  `Text.graphemes` and `Text.scalars` are **deferred to Phase 7** (D-20); they are not Gate 1 core obligations.
- **E-12** Concatenating user-derived text is never assumed localizable; translation and formatting belong to Phase 7, not to the language.

## 5. Logic

- **E-13** `and` and `or` are keywords with **short-circuit** semantics, left to right; `not` is strict. A right operand is not evaluated when the left determines the result. Their precedence is the closed table in `00-lexical-and-layout.md` §7.

## 6. Equality and ordering

- **E-14** `==` and `!=` are available only on `Eq` types (T-26) and are **structural**: records by field, unions by variant and payload, `List` element-wise in order, `Text` by code-point equality. Functions are never comparable. `!=` is exactly `not (a == b)` with short-circuit on the first difference.
- **E-15** `<`, `<=`, `>`, `>=` require `Ord`. Records and unions are **not** `Ord` by default; `Ord` must be implemented explicitly, so no accidental lexicographic ordering of app data can appear in a sort.

## 7. Closures

- **E-16** A closure captures **immutable** bindings **by value at creation**. Later changes to the enclosing `mut` binding are not observed.
- **E-17** Capturing a `mut` binding in a closure is an **error** (`PL0221`) with the fix "bind a `let` snapshot first". This removes the classic late-binding loop-capture bug by construction.
- **E-18** A closure **MUST NOT** refer to itself; recursion requires a named top-level function (`PL0222`). Anonymous recursion via combinators remains possible where the prelude provides it.

## 8. `?` propagation

- **E-19** `expr?` evaluates `expr` once.
  - If it is `Ok(v)`, the expression's value is `v`.
  - If it is `Err(e)`, the **nearest function activation** (named function or lambda) returns immediately with `Err(e)`, after unwinding active block defers in that function (E-22). It does not return from the caller’s caller.
  - The error type is not converted and the enclosing return type must match exactly (T-13).
  - `?` inside `defer` is rejected (`PL0228`).

## 9. `defer`

- **E-20** `defer:` registers a block that runs when its **enclosing block** exits, in **LIFO** order, before the block’s value is produced. On a `?`-early-return, active blocks in the returning function unwind innermost-first; caller blocks are not unwound.
- **E-21** A `defer` block **MUST** have type `()` (`PL0223`), **MUST NOT** contain `?` (`PL0228`), and **MUST NOT** change the enclosing block’s saved result. It may mutate cells in scope; it cannot rebind the result expression.
- **E-22** `defer` blocks run on normal exit **and** on `?`-early-return, because that is still a normal return of a value. They are **not** guaranteed to run when the task is torn down by a **fault** (E-30, E-31). Programs **MUST NOT** rely on `defer` for resource release that security depends on; the host owns resource teardown (Phase 5).

## 10. Pattern matching

- **E-23** `when` is an **expression** and is always **checked for exhaustiveness** (`PL0224`), listing the missing variants. There is no match *statement*. This is a simplicity choice; current Kotlin already requires exhaustiveness for enum/sealed/Boolean `when` statements (research record 03).
- **E-24** Arms are tried top to bottom. A later arm that can never match is an **error** (`PL0225`) naming the earlier arm.
- **E-25** A `_` arm is permitted and must be written explicitly; it suppresses the missing-variant list but not unreachability checks.
- **E-26** Patterns are: wildcard `_`, binding names, variant patterns with nested patterns, record patterns (`{ done: True }`), unit, `Int`/`Text` literals, and negative `Int` literals. A record pattern may list a subset of fields, each exactly once; unlisted fields are ignored for matching. Duplicate binder names in one pattern are an error (`PL0229`). Guard clauses (`when x if cond:`) are **deferred** (A-12) — v0.1 expresses the same thing with a nested `if`.
- **E-27** Pattern matching is a **partial** operation: `match(pattern, value)` either fails or returns bindings. Bindings are produced only after the whole pattern succeeds and are scoped to that arm. A failed arm leaves no bindings. Exhaustiveness/reachability checking must account for nested patterns and open domains (`Int`, `Text`, `Float`, `List`); finite literals alone never cover an open domain.

## 11. `if`

- **E-28** `if cond:` without `else` has type `()` and **MUST** be used where `()` is expected (`PL0226`). An `if` used as a value **MUST** have an `else`, and both branches **MUST** have the same type.
- **E-29** `else:` followed by a nested `if` is the only way to chain conditions (no `elif`, S-5).

## 12. Faults

- **E-30** A **fault** is a terminating condition that app code cannot catch or convert. The v0.2 list separates **core faults** from later platform faults. Core faults are closed:
  1. integer overflow or divide-by-zero (E-05, E-06);
  2. deterministic fuel/step quota exceeded in the hermetic core (E-33).
  Later platform contracts add host quota exceeded (Phase 3), capability revoked/misused (Phase 5), and unrecoverable host I/O failure (Phase 9). Those are not Gate 1 core conformance obligations unless explicitly included by A-42.
- **E-31** A fault **terminates the current task**, not the platform. The observable effects are: the in-flight reactive transaction is discarded (Phase 2), the task's supervisor is notified with a diagnostic code and span, and other tasks continue (Phase 3, Gate 3).
- **E-32** A fault **MUST NOT** leave partial **task-local core state**: the provisional interpreter discards in-memory mutations of the faulting task. This rule does **not** roll back external host effects. Durable writes, external I/O, compensation, and transactional visibility are Phase 9 obligations, not a claim that all effects are atomic.
- **E-33** Core faults are deterministic under the same inputs and **deterministic fuel/step quotas**. Wall-clock timeouts are host scheduling policy (Phase 3), not core semantic inputs; a conformance result **MUST NOT** depend on GC timing or wall-clock scheduling. Exhausting the deterministic fuel/step quota is the fault `PLFL05`.
- **E-34** `Int.max + 1` faulting rather than wrapping is a **Proposed** choice with a measurable cost; E1/E2 (Phase 2/4) must record whether checked arithmetic appears in any measured hot path, and Gate 12 must not accept a performance claim that quietly disabled the checks.

## 13. Determinism

- **E-35** Evaluation is deterministic: no ambient host authority, no uninitialized values, no implicit randomness, no wall-clock access from the language. All nondeterminism enters through capability-gated host calls (Phase 5) and is visible in the signature that takes the capability.
- **E-36** Program meaning **MUST NOT** depend on build profile (decision 0006). A conformance test runs the suite in both a non-optimized and an optimized configuration and requires identical results, including faults.
