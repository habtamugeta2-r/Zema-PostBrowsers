# Plain 1 — Types

| Field | Detail |
|---|---|
| **Version** | 0.1 (draft) |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Proposed — normative text, not frozen |
| **Rules** | `T-nn` |

---

## 1. Bindings and mutability

- **T-01** `let` introduces an immutable binding. It **MUST NOT** be reassigned (`PL0201`).
- **T-02** `mut` introduces a mutable binding. Only a `mut` binding may appear on the left of `=` (`PL0202`). Mutability is a property of the *binding*, not of the value: there are no reference types in the core, so no mutable aliasing exists.
- **T-28** **Shadowing:** a `let` or `mut` in the **same block** that redeclares an existing name in that block is an error (`PL0227`, fix: use `mut` or a new name). A **nested** block **MAY** shadow an outer name; this produces a warning (`PL1102`) and never changes which binding an earlier line referred to.
- **T-03** `mut` bindings are **block-local**. Passing a `mut` binding to a function passes its current value. There is no borrowing, no shared mutability, and therefore no data race inside the language (concurrency safety is Phase 4's problem at task boundaries).

## 2. The type universe

| Type | Kind | Notes |
|---|---|---|
| `Int` | primitive | 64-bit signed two's complement (E-05) |
| `Float` | primitive | IEEE 754 binary64 (E-07) |
| `Text` | primitive | immutable UTF-8; no integer indexing (E-11) |
| `Unit` | primitive | the only value is `()` |
| `List<a>` | prelude union | finite, ordered |
| `Option<a>` | prelude union | `None \| Some(a)` — **absence** |
| `Result<a, e>` | prelude union | `Ok(a) \| Err(e)` — **failure**, value first |
| `Ordering` | prelude union | `Less \| Equal \| Greater` |
| `Bool` | prelude union | `False \| True` — not a keyword primitive |
| `Map<k, v>` | prelude | requires `Ord` on `k` (T-15; ordering in E-15) |
| user `type` | nominal union | closed set of variants |

- **T-04** `List` provides no indexing syntax. Bounds-safe access is `List.get(xs, i) -> Option<a>`; the out-of-bounds case is a value, not a fault.
- **T-05** `Bool` is declared in the prelude as an ordinary union, so `if`/`when` need no special boolean type. `and`, `or`, and `not` remain **keywords with short-circuit semantics** because a strict function cannot express them (E-09).

## 3. Records (structural) and unions (nominal)

- **T-06** A record type is written `{ field: Type, … }` and is **structural**: two record types with identical field names and types are the same type, and there is no record declaration form. Records **MUST** have at least one field (`{}` is `PL0107`; use `()`).
- **T-07** A record value is written `{ field: expr, … }`; every field of the type **MUST** be present exactly once (`PL0203`). Field order in a literal **MUST NOT** matter for typing; it does determine evaluation order (E-02).
- **T-08** A union type **MUST** be declared: `type Status = Active | Done | Archived({ reason: Text })`. Unions are **nominal** — two identically-shaped unions are different types — and **closed**: a value is one of the declared variants, permanently (T-10).
- **T-09** A variant carries **at most one** value: either a single type (`Some(a)`) or a record when more than one field is needed (`Archived({ reason: Text })`). There is **no positional field list**, so there is no field-order/field-swap hazard, and matching reuses record patterns rather than inventing a second one (A-05).
- **T-10** A union **MUST NOT** be extended after declaration. Modelling "one more case" requires a new union; this is what makes exhaustive matching (E-14) a real guarantee.

## 4. Absence, failure, and errors

- **T-11** There is **no null**: absence is `Option<a>`. There are **no exception primitives**: failure is `Result<a, e>`. A function that can fail **MUST** say so in its return type (`PL0204`).
- **T-12** Faults are not errors: integer overflow, division by zero, host revocation, and out-of-memory **terminate the current task** and are not catchable by app code (E-16). App code cannot represent them as `Result`.
- **T-13** `?` **MUST** appear only in a function whose return type is `Result<a, e>` (or in a block whose tail is such a call), and the operand **MUST** be `Result<b, e>` with the **same** `e` (`PL0205`). There is no implicit error-type conversion in v0.1; map explicitly with `Result.map_error` (A-16).

## 5. Records, generics, interfaces

- **T-14** A type parameter **MUST** be declared in the declaration that uses it: `fn map<a, b>(xs: List<a>, f: fn(a) -> b) -> List<b>`. Unbound type variables are `PL0206`.
- **T-15** Generic code **MUST** declare the interfaces it relies on as bounds: `fn display_all<a: Display>(xs: List<a>) -> List<Text>`. A method call on an unbounded parameter is `PL0207` with the missing bound as a fix. Prelude interfaces: `Eq`, `Ord`, `Display`, `Hash` (the last deferred until Phase 9 needs it).
- **T-16** An interface declares signatures only: `interface Display<a>:` with `fn display(value: a) -> Text`. Interfaces carry no default bodies in v0.1.
- **T-17** An implementation is `impl Display for Task:` followed by the required functions. Implementations **MUST** be complete (`PL0208`) and **MUST NOT** add functions beyond the interface (`PL0209`).
- **T-18** **Coherence rules (normative):**
  1. **Orphan rule** — an `impl` **MUST** live in the module that declares the type or the interface (`PL0210`).
  2. **Uniqueness** — at most one implementation per (interface, type) pair (`PL0211`).
  3. **No overlap** — blanket implementations are not expressible in v0.1 (D-14), so overlap cannot arise; if it ever does, it is an error, not a warning.
  4. **No specialization** — a more specific implementation never overrides a general one (`PL0212`).
- **T-19** `alias Name = Type` is **transparent**: `Name` and `Type` are interchangeable everywhere (`PL0213` explains this in diagnostics when it surprises someone).
- **T-20** `distinct Name = Type` is **nominal** and zero-cost: no implicit conversion in either direction; `expr as Name` and `name as Type` (S-4) are the only conversions (`PL0114`). Use it for identifiers that must not be confused (`User_id` vs `Order_id`), which is the target app class's most common silent bug.

## 6. Inference and its limits

- **T-21** Inference is **local, rank-1, and non-global**. Specifically:
  - Function signatures **MUST** be fully annotated (parameters and return type). No signature inference crosses a declaration boundary (`PL0214`).
  - `let` and `mut` bindings **MAY** omit their type; the type is inferred from the initialiser within the enclosing block.
  - Lambda parameters **MAY** omit types when an expected function type exists; otherwise they **MUST** be annotated (`PL0215`).
  - Type declarations, interface signatures, and `impl` function signatures **MUST** be annotated.
  - Recursive functions **MUST** have an annotated signature.
- **T-22** The following are **not** in the language and **MUST** be rejected by name rather than by accident: higher-rank polymorphism, higher-kinded types, implicit parameters, ad-hoc overloading (one name, many types), polymorphic recursion, defaulting beyond T-23, and implicit numeric widening (`PL0216`).
- **T-23** Numeric literals: an integer literal has type `Int` unless the expected type is `Float`, in which case it is a **compile error**, not a conversion (`PL0217`); write `1.0`. There is no other defaulting.
- **T-24** An empty list literal with no expected type **MUST** be an error asking for an annotation (`PL0218`). Guessing the element type is how "it compiles but the data is wrong" starts.
- **T-25** There is **no subtyping** in v0.1 — not for records, not for unions, not for interfaces. Variance questions do not exist because there is no subtyping relation to be variant about.

## 7. Equality and ordering types

- **T-26** Structural equality is derived automatically for any type whose components are all equality-capable. `Float` and function types are **not** equality-capable (E-07), so a type containing them is not `Eq` (`PL0219`), and it cannot be an element of a `Set` or a key of a `Map`.
- **T-27** A type is equality-capable only if its definition is not **recursively reachable without an indirection** through `List`, `Option`, or a declared union variant. Recursive unions are fine (`type Tree = Leaf | Node(Tree, Tree)` is `Eq`); a recursive *record* type would create an equality that may not terminate and is rejected (`PL0220`). Rationale and trade-off: A-14.

## 8. Open items owned by this document

| ID | Question | Status |
|---|---|---|
| A-05 | Variant payload style | **Resolved:** named fields only |
| A-13 | Generic bound syntax (`<a: Display>` vs `where`) | **Resolved:** inline bounds; `where` clauses deferred |
| A-16 | `?` error conversion | **Resolved:** none in v0.1 |
| A-17 | `Eq` on functions/floats | **Resolved:** T-26 |
| A-23 | Interface default methods | **Deferred** (D-12) |
| A-26 | Row polymorphism for records | **Deferred** (D-13) |
