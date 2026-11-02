# Plain 3 — Derived Ambiguity Register

| Field | Detail |
|---|---|
| **Version** | 0.1 (draft) |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Active register |
| **Evidence label** | **Proposed** (each resolution is a design decision) |

> **Provenance, stated plainly.** Master Prompt Phase 1 requires resolving
> "all draft ambiguities catalogued in §12.1 of the research book". That
> book is not in this repository and was not found in the owner's public
> repositories ([audit](../../research/phase-00-05-book-import-audit.md)),
> so the original list is **unrecoverable**. This register is **derived**
> from the v0.1 specification and the implementation questions it forces.
> It is *not* the book's list and **MUST NOT** be cited as such
> (decision [0004](../decisions/0004-research-book-missing.md)).
>
> If the book arrives, reconcile the two lists row by row in one reviewed
> change — do not silently replace this one.

---

## 1. Register

| ID | Question | Resolution | Status | Spec ref |
|---|---|---|---|---|
| A-01 | What indentation character and width are legal? | Spaces only; tab in indentation is an error; block columns must be consistent, widths otherwise free; formatter canonicalizes to two spaces | Resolved | L-03, L-20 |
| A-02 | Do blank and comment-only lines affect layout? | No | Resolved | L-23 |
| A-03 | Are tuples in the language? | No. A product is a record; a tuple would be a second notation for the same concept, and positional payloads invite silent field swaps | Resolved | T-06, §10 of doc 0 |
| A-04 | Is destructuring allowed in `let`? | Not in v0.1. Destructuring happens in `when`; records are projected by field. Deferred with trigger | **Deferred** | D-15 |
| A-05 | Positional or named variant payloads? | At most **one** payload per variant; multi-field payloads are records (`Archived({ reason: Text })`). No positional field lists | Resolved | T-09 |
| A-06 | Operator precedence and associativity, and can users add operators? | Fixed table; comparisons non-associative; no user-defined operators or sections | Resolved | L-22 §7, L-28 |
| A-07 | What happens to an integer literal that does not fit? | Compile-time error, never a wrapped value | Resolved | L-18 |
| A-08 | How are numeric literals typed and converted? | Integer literal is `Int`; no implicit `Int`↔`Float`; `Float` needs a decimal point; explicit conversions | Resolved | T-23, E-07 |
| A-09 | Do integers wrap, saturate, or fault — and does the answer depend on build mode? | Checked in **all** profiles; overflow faults; wrapping/saturating live in explicitly named prelude functions | Resolved | E-05, E-36 |
| A-10 | Integer division and remainder semantics for negatives and zero | Truncate toward zero; remainder takes the dividend's sign; divide-by-zero faults | Resolved | E-06 |
| A-11 | `Float` equality, NaN, and `-0.0` | `Float` is not `Eq`; `Float.compare` provides a documented total order; NaN handling specified | Resolved | E-08, E-09 |
| A-12 | Are match guards (`pattern if cond`) allowed? | Not in v0.1; a nested `if` expresses the same thing. Deferred with trigger | **Deferred** | E-26, D-11 |
| A-13 | Generic bound syntax: inline or `where` clauses? | Inline (`<a: Display>`); `where` clauses deferred | Resolved | T-15 |
| A-14 | How can equality be sound for recursive types, and can it fail to terminate? | Recursive **unions** are `Eq` (finite values); a record type that recurses without an indirection is rejected. Occurs-check on the type graph | Resolved (risk accepted) | T-27 |
| A-15 | Is there a `return` or early exit? | No `return` in v0.1; `?` exits a `Result` function with an error; the keyword stays reserved | Resolved | L-09, §10 of doc 0 |
| A-16 | Does `?` convert between error types? | No conversion; the error type must match exactly and be mapped explicitly | Resolved | T-13, E-19 |
| A-17 | Interface coherence: orphans, duplicate impls, overlap, specialization | Orphan rule; one impl per (interface, type); no overlap expressible; no specialization | Resolved | T-18 |
| A-18 | Must identifiers be normalized? | NFC required; non-NFC is an error with the NFC form as a fix | Resolved | L-04 |
| A-19 | How are confusable identifiers handled, and over what scope? | Skeleton collisions among declarations **in the same scope** are errors; mixed-script identifiers warn. Cross-scope (shadowing) collisions are **not** checked — a stated limit, not an oversight | Resolved (partial) | L-10, L-11 |
| A-20 | What is the line-continuation rule? | One rule: leading binary operator, or a trailing operator/comma/open delimiter, plus deeper indentation | Resolved | L-22 |
| A-21 | Is there a module system, and can an app span files? | Not in v0.1: one file, no `import`; the conformance suite is single-file. Multi-file modules and packages are Phase 13 work | **Deferred** | D-10 |
| A-22 | Is shadowing allowed? | Nested-block shadowing allowed (warning); same-block shadowing is an error with the fix "use `mut` or a new name" | Resolved | T-28 |
| A-23 | Do interfaces carry default method bodies? | No | **Deferred** | D-12 |
| A-24 | Is `{}` the unit value or an empty record? | Neither: `{}` is an error pointing at `()`; records need at least one field | Resolved | L-16, T-06 |
| A-25 | Can `when` match on literals and non-union values? | Yes; such a match needs an explicit `_` arm to be exhaustive | Resolved | E-25 |
| A-26 | Are record types width-polymorphic (row polymorphism)? | No in v0.1; functions take the exact record type. Deferred with trigger | **Deferred** | D-13 |

## 2. Summary

| Status | Count | IDs |
|---|---|---|
| Resolved | 21 | A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10, A-11, A-13, A-14, A-15, A-16, A-17, A-18, A-19, A-20, A-22, A-24, A-25 |
| Deferred | 5 | A-04, A-12, A-21, A-23, A-26 |
| Open — requires a decision before Gate 1 | 0 | — |
| **Total** | **26** | A-01 … A-26 |

> Counts are reconciled at every revision; if the table and the summary
> disagree, the table governs and the summary is a defect.

## 3. Rules for this register

1. Every row has a **status** and a **spec reference**. A row with
   neither is open by definition.
2. A **Deferred** row needs a trigger for revisiting — recorded in
   [`04-deferred-features.md`](./04-deferred-features.md), not here.
3. **Resolved** means the specification states the rule and a
   conformance test can assert it. "Resolved" is not "frozen": freezing
   happens at Gate 1.
4. "Resolved (partial)" must say which part is unhandled. Silence is how
   a bounded check becomes a false guarantee.
5. If a new ambiguity is found during implementation, **add a row**; do
   not fix it in code and leave the specification silent.

## 4. Known limits recorded honestly

| Limit | Consequence |
|---|---|
| The original §12.1 list is unrecoverable | Phase 1 pays for re-derivation; the book may contain questions this register missed |
| Confusable detection is character-based | Sequence-level spoofing (`rn` for `m`) is out of scope, as UTS #39 itself notes |
| `Eq` on recursive records is rejected rather than defined | Some legitimate data models must be reshaped; the diagnostic must explain why |
| No subtyping (T-25) | Some reuse patterns need conversion functions instead of implicit widening — deliberate |
| No modules (D-01) | Real apps cannot be structured in v0.1; the interpreter's demo is single-file |

## 5. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 0.1 | Register derived: 26 questions, 21 resolved, 5 deferred, 0 open; provenance and limits stated. |
