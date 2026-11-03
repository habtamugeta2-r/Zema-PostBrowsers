# Plain 6 — Core Operational Semantics (Research Draft)

| Field | Detail |
|---|---|
| **Version** | 0.1 (research draft — **non-normative**) |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Candidate small-step model for the hermetic core; not frozen, not implemented, not a proof |
| **Evidence label** | **Proposed** for the model; **Hypothesis** for determinism/soundness conjectures |
| **Depends on** | Draft v0.2 resolutions A-32…A-40; proposed resolutions A-27/A-38/A-42; A-43 resolved in T-30 |

> This document exists because Gate 1 requires a small-step operational
> semantics and v0.1 had none. It is deliberately **non-normative**: the
> prose rules in docs 00–02 remain the candidate specification until the
> open items are resolved and an implementation/conformance run agrees
> with this model. No interpreter, fixture, or theorem is claimed here.

---

## 1. Scope

The model covers the single-file, hermetic core after lexical analysis,
parsing, name resolution, type checking, and desugaring:

- strict call-by-value evaluation;
- immutable `let`, block-local `mut`, records, lists, nominal variants;
- named functions and immutable-capture closures;
- `if`, `when`, patterns, `?`, block-local `defer`;
- checked integer faults and deterministic fuel exhaustion.

It does **not** model reactive graphs, host capabilities, OS isolation,
Unicode segmentation, rendering, persistence, or networking. Those are
later-phase platform contracts. A Gate 1 pass may not silently count this
model as coverage for them (A-42).

## 2. Abstract machine

### 2.1 Values and environments

```text
v ::= int | float | text | ()
    | { l_i = v_i }              -- record, i ≥ 1
    | C | C(v)                   -- nominal variant, at most one payload
    | [v_1, …, v_n]
    | clo(ρ_c, x_1…x_n, body)    -- immutable snapshot closure
    | fun(f)                     -- top-level function value

ρ ::= name → imm(v) | mut(ℓ)
σ ::= ℓ → v                      -- mutable cells, task-local
G ::= name → v                   -- checked top-level constants
F ::= name → (params, body)      -- named functions
```

There are no source-visible references. A `mut` name denotes a cell in
the current task; passing it to a function passes the current value.
Closure creation snapshots only immutable bindings; a free `mut` binding
is rejected before evaluation (E-17).

### 2.2 Configurations

A configuration is:

```text
⟨ σ, frames, focus, κ ⟩
```

- `frames` is a stack of function activations. The top frame owns the
  current environment `ρ` and a stack `β` of active block-defer lists.
- `focus` is the expression or administrative form currently reducing.
- `κ` is the continuation: evaluate an evaluation context, return to a
  caller, unwind defers with a saved result, or terminate the task.

Evaluation contexts are the usual strict, left-to-right contexts for
calls, records, lists, operators, scrutinees, and `?`. Short-circuit
`and`/`or` are not strict in their right operand.

Administrative forms:

```text
block(ρ, ds, seq)       -- ds is a LIFO list of registered defers
unwind(ds, v)           -- run defers, preserving result v
returning(v)            -- early return from the nearest function
fault(code, span)       -- terminal task fault
```

`ds` entries are `(ρ_register, body)`. A defer body runs in the
environment where it was registered, but it is not a closure: it may
access mutable cells in that scope. It may not contain `?` (A-35).

## 3. Selected reduction rules

Rules are written in the dual prose/reduction style used by the
WebAssembly specification: the prose is authoritative for readers; the
reduction is the compact checkable form. Only selected rules are shown;
a Gate 1 version must enumerate every core construct.

### OS-01 — Values and lookup

An immutable name evaluates to its value. A mutable name evaluates to
the current contents of its cell.

```text
ρ(x) = imm(v)
────────────────────────────
⟨σ, …, x, κ⟩ → ⟨σ, …, v, κ⟩

ρ(x) = mut(ℓ)   σ(ℓ) = v
────────────────────────────
⟨σ, …, x, κ⟩ → ⟨σ, …, v, κ⟩
```

### OS-02 — Bindings and assignment

`let` binds a value. `mut` allocates a fresh task-local cell. Assignment
updates the cell; a field path updates the aggregate value stored at the
mutable root. No alias to the cell is created.

```text
fresh ℓ
──────────────────────────────────────────────
⟨σ, mut x = v; rest, κ⟩ → ⟨σ[ℓ↦v], rest, κ⟩
with ρ(x)=mut(ℓ)

ρ(x)=mut(ℓ)
──────────────────────────────────────────────
⟨σ, x = v; rest, κ⟩ → ⟨σ[ℓ↦v], rest, κ⟩
```

A field path `x.a.b = v` is valid only when `x` is a mutable root and
each intermediate projection is a record. The update replaces the root
value with the path-updated aggregate. Attempting to assign through an
immutable root is a static error.

### OS-03 — Calls and closures

Evaluate callee, then arguments in source order. A closure body runs in
a new frame whose environment is the captured immutable snapshot plus
parameter bindings. A top-level function uses `F` and `G`, not a mutable
caller environment.

```text
v_f = clo(ρ_c, x_1…x_n, body)
ρ' = ρ_c[x_i ↦ imm(v_i)]
──────────────────────────────────────────────────────────────
⟨σ, caller, v_f(v_1…v_n), κ⟩ →
⟨σ, push(ρ', caller, κ), block(ρ', [], body), done⟩
```

When the new frame produces a value, pop it and resume the caller with
that value. Arity mismatch is static, not a runtime fault.

### OS-04 — Pipes

Pipes are desugared before evaluation. `x |> f(y)` becomes `f(y, x)`,
so OS-03 evaluates `f`, then `y`, then `x`. This order is surprising but
defined; it is not undefined behavior.

```text
x |> f(y)  ⇒  f(y, x)
```

A chained pipe desugars left-associatively. Any future change to
input-first ordering is a semantic change, not a formatter change.

### OS-05 — Blocks and defer registration

A block executes its statements in order and then its tail. Registering
a defer adds it to the current block’s LIFO list; it does not run yet.

```text
────────────────────────────────────────────────────────────
⟨σ, block(ρ, ds, defer b; rest), κ⟩ →
⟨σ, block(ρ, ds ++ [(ρ,b)], rest), κ⟩
```

When a block reaches a value, it begins unwinding its own defers:

```text
────────────────────────────────────────────────────────────
⟨σ, block(ρ, ds, v), κ⟩ → ⟨σ, focus(unwind(ds, v)), κ⟩
```

### OS-06 — Defer unwind

Defers run last-registered first. Each body must produce `()`. The saved
result is threaded through unchanged.

```text
────────────────────────────────────────────────────────────
⟨σ, unwind((ρ_d,b)::ds, v), κ⟩ →
⟨σ, execute_in_current_function(ρ_d, b, unwind(ds, v)), κ⟩

────────────────────────────────────────────────────────────
⟨σ, unwind([], v), κ⟩ → ⟨σ, v, κ⟩
```

If a defer body faults, the task faults; remaining defers are not
guaranteed. If a defer body contains `?`, the program is rejected before
evaluation.

### OS-07 — `?` and nearest-function return

`?` evaluates its operand once. `Ok(v)` continues with `v`. `Err(e)`
starts an early return from the nearest function activation, including a
lambda; it never returns from the caller’s caller.

```text
────────────────────────────────────────────────────────────
⟨σ, Ok(v)?, κ⟩ → ⟨σ, v, κ⟩

────────────────────────────────────────────────────────────
⟨σ, Err(e)?, κ⟩ → ⟨σ, returning(Err(e)), κ⟩
```

`returning(v)` unwinds all active block-defer lists in the current
function, innermost first, then pops the function frame and resumes the
caller with `v`. It does not unwind caller frames.

### OS-08 — Conditionals and matching

`if` and `when` evaluate the scrutinee once. Matching is a partial
function:

```text
match(p, v) = none | some(ρ_bindings)
```

Bindings exist only after a successful match and are scoped to the arm.
A failed arm leaves no bindings. Arms are tried top to bottom; the first
successful arm’s block runs in the current environment extended with the
bindings.

```text
match(p_i, v) = some(ρ_i)
────────────────────────────────────────────────────────────
⟨σ, when v { p_1:b_1; …; p_n:b_n }, κ⟩ →
⟨σ, block(ρ+ρ_i, [], b_i), κ⟩
```

Static coverage must prove that some arm matches every value of the
scrutinee type. Finite closed unions are covered variant-by-variant;
records by the product of their listed field patterns; `Int`, `Text`,
and other open domains require a wildcard or binding pattern. A later
arm whose pattern set is empty is a static error.

### OS-09 — Checked integer faults

Checked integer operations either produce an `Int` value or a terminal
fault. The fault is not a `Result` and cannot be caught.

```text
a + b ∈ Int64
────────────────────────────────────────────────────────────
⟨σ, a + b, κ⟩ → ⟨σ, int(a+b), κ⟩

a + b ∉ Int64
────────────────────────────────────────────────────────────
⟨σ, a + b, κ⟩ → fault(arithmetic_overflow, span)
```

Division by zero and `Int.min / -1` follow the same terminal path.
Optimization may remove a check only when it preserves this observable
behavior.

### OS-10 — Fuel and task termination

The hermetic model uses a deterministic instruction/fuel counter, not a
wall-clock timeout. Fuel exhaustion is a fault. Host wall-clock policy
belongs to Phase 3 and must not change core conformance results.

```text
fuel = 0
────────────────────────────────────────────────────────────
⟨σ, focus, κ⟩ → fault(quota_exceeded, span)
```

A fault terminates the current task. In the hermetic core, the task’s
local store is discarded. External host effects are not rolled back by
this rule; Phase 5/9 must define mediation, durability, and compensation.

## 4. Static obligations before evaluation

The evaluator assumes these checks have already passed:

1. Every name is resolved; every function signature is annotated.
2. Local bindings are monomorphic; declaration type parameters are
   explicit and rank-1 (A-33).
3. Top-level user `let` initializers are constant expressions; there are
   no top-level initialization effects or cycles (A-32).
4. `mut` capture in closures is rejected; `?` occurs only in a function
   returning `Result` with the same error type; `?` is absent from
   `defer` bodies.
5. `when` is exhaustive and has no unreachable arm; pattern binders are
   unique within a pattern.
6. `defer` bodies have type `()`.
7. Eq/Ord constraints follow proposed decision 0009: `Ord` requires
   `Eq`; `Float` has an explicit compare function but is not `Ord`. Generic
   collection APIs remain deferred (D-19).

## 5. Conjectures, not theorems

| ID | Conjecture | What would establish it |
|---|---|---|
| H-OS-1 | For a closed, well-typed hermetic core program with fixed fuel and no host calls, at most one reduction rule applies to a configuration. | Rule-overlap review plus differential conformance traces |
| H-OS-2 | A well-typed core program either produces a value of the expected type or terminates in a defined fault; it does not get stuck on an undefined state. | Progress/preservation proof for the core calculus and an executable checker/evaluator pair |
| H-OS-3 | Defer unwind preserves the saved result on normal and `?` return, and runs registered defers LIFO within the stated boundary. | Trace fixtures for nested blocks, lambdas, early return, and fault |
| H-OS-4 | Immutable snapshot closures cannot observe later mutation of an enclosing binding. | Fixtures plus a capture-check proof |

No security, memory-safety, race-freedom, accessibility, or performance
claim follows from these conjectures.

## 6. Conformance trace obligations

When build work is authorized, each reduction rule needs at least one
observable trace, not only a final value:

- OS-03/04: argument-order probe with a test-only effect logger;
- OS-05/06: nested defer LIFO and result preservation;
- OS-07: `?` inside lambda vs named function; defer rejection;
- OS-08: failed nested pattern leaves no binding; unreachable arm error;
- OS-09: overflow/division faults in checked and optimized profiles;
- OS-10: deterministic fuel exhaustion and local-state discard.

These are **requirements for future fixtures**, not fixtures written in
this pass.

## 7. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 0.1 | Non-normative small-step core draft created; open items and conjectures recorded. |
