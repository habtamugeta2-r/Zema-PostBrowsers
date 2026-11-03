# Plain 3 — Derived Ambiguity Register

| Field | Detail |
|---|---|
| **Version** | 0.2.4 (draft) |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Active register |
| **Evidence label** | **Proposed** (each resolution is a design decision) |

> **Provenance, stated plainly.** Master Prompt Phase 1 requires resolving
> "all draft ambiguities catalogued in §12.1 of the research book". That
> book is not in this repository and was not found in the owner's public
> repositories ([audit](../../research/phase-00-05-book-import-audit.md)),
> so the original list is **unrecoverable**. This register is **derived**
> from the v0.1/v0.2 specification and the implementation questions it forces.
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
| A-06 | Operator precedence and associativity, and can users add operators? | Fixed table; comparisons non-associative; no user-defined operators or sections | Resolved | §7 of doc 0, L-28 |
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
| A-18 | Must identifiers be normalized? | Identifiers: NFC required; non-NFC is an error with the NFC form as a fix. Text literals are not silently normalized | Resolved | L-04, A-28 |
| A-19 | How are confusable identifiers handled, and over what scope? | Versioned UTS #39 skeleton collisions among visible names are errors where the relevant-name set is known; mixed-script checks use identifier chunks. Full cross-module/visible-name analysis is a stated limit | Resolved (partial) | L-10, L-11, A-41 |
| A-20 | What is the line-continuation rule? | One rule: leading binary operator, or a trailing operator/comma/open delimiter, plus deeper indentation | Resolved | L-22 |
| A-21 | Is there a module system, and can an app span files? | Not in v0.1: one file, no `import`; the conformance suite is single-file. Multi-file modules and packages are Phase 13 work | **Deferred** | D-10 |
| A-22 | Is shadowing allowed? | Nested-block shadowing allowed (warning); same-block shadowing is an error with the fix "use `mut` or a new name" | Resolved | T-28 |
| A-23 | Do interfaces carry default method bodies? | No | **Deferred** | D-12 |
| A-24 | Is `{}` the unit value or an empty record? | Neither: `{}` is an error pointing at `()`; records need at least one field | Resolved | L-16, T-06 |
| A-25 | Can `when` match on literals and non-union values? | Yes; open domains need a wildcard or binding pattern, and nested patterns are checked for coverage/reachability | Resolved | E-25, E-27, A-37 |
| A-26 | Are record types width-polymorphic (row polymorphism)? | No in v0.1; functions take the exact record type. Deferred with trigger | **Deferred** | D-13 |

| A-27 | Which Unicode/UTS #39 data version and identifier profile does Plain pin? | Initial pin: Unicode 17.0.0 / UAX #31 rev43 / UAX #15 rev57 / UAX #9 rev51 / UTS #39 rev32 / UTS #55 rev5; declared R1-2 `_` profile; upgrades require decision, data diff, fixtures, and rerun | Resolved (proposed) | L-04, L-08, L-10, decision 0009 |
| A-28 | Are text literals normalized like identifiers? | No. Identifiers are NFC; text literals preserve scalar data. Concatenation does not normalize | Resolved | L-04, E-11 |
| A-29 | Can naming roles depend solely on case? | No. Roles come from declaration/resolution context; case conventions are warnings and do not exclude unicameral scripts | Resolved | L-12 |
| A-30 | How are type/value/constructor names resolved? | The lexer emits names; the resolver assigns roles. Types/interfaces and values/constructors occupy separate resolution categories; qualified prelude names are paths, not method calls | Resolved | L-12, L-29, grammar §6 |
| A-31 | Does a trailing `:` continue an expression or open a block? | It opens a block. Continuations are only the closed operator/comma/open-delimiter cases | Resolved | L-19, L-22 |
| A-32 | What is the order of top-level `let` initialization? | User top-level `let` is constant-only; no effects, calls, forward references, or cycles | Resolved | T-29 |
| A-33 | Do local bindings generalize? | No. Local bindings and lambdas are monomorphic; explicit declaration type parameters are the rank-1 entry point | Resolved | T-21 |
| A-34 | Is pipe side-effect order unspecified? | No. The pipe inserts its left operand as the last argument, so callee, explicit arguments, then piped operand are evaluated in that defined order; tooling may warn about host calls on both sides | Resolved | E-03, S-2 |
| A-35 | Which function does `?` exit, and may `defer` use it? | Nearest function activation, including lambdas; `?` is forbidden in `defer` | Resolved | T-13, E-19, E-21 |
| A-36 | What is the scope of `defer` on early return? | Block-local LIFO; `?` unwinds active blocks in the returning function only; faults do not guarantee defers | Resolved | E-20, E-22 |
| A-37 | Are pattern bindings irrefutable, and how is coverage computed? | Matching is partial; bindings exist only after success. Coverage is variant/product/open-domain analysis; duplicate binders are rejected | Resolved | E-26, E-27 |
| A-38 | What are the `Eq`/`Ord` laws and collection key constraints? | Eq is derived/sealed; Ord requires Eq and equality-consistent total-order laws; Float is neither Eq nor Ord; Map/Set deferred to Phase 9 | Resolved (proposed) | T-26, E-08, E-09, D-19, decision 0009 |
| A-39 | Does fault rollback cover external effects? | No. Core rollback is task-local state only; durable/external effects need Phase 9 mediation/compensation | Resolved | E-32 |
| A-40 | Are wall-clock timeouts part of deterministic core faults? | No. Core conformance uses deterministic fuel/step quotas; wall-clock policy is Phase 3 host scheduling | Resolved | E-30, E-33 |
| A-41 | How are bidi/invisible controls shown in diagnostics? | Quote source with directional/invisible controls escaped or visibly marked; full editor rendering is Phase 13 | Resolved (partial) | L-02, L-31 |
| A-42 | What exactly does Gate 1 cover? | Hermetic Plain core only; later platform obligations remain binding in their named phases and are not waived (decision 0010); owner/reviewer ratification required before Gate 1 | Resolved (proposed) | 05-conformance-plan.md, decision 0010 |
| A-43 | Is there a `main` entry point? | No core keyword. Fixtures name the function to evaluate; application hosts define exported entry later | Resolved | T-30 |
| A-44 | What exact Unicode security diagnostics and data sources does Plain use? | UTS #55 rev5 chunk boundaries and C4 test; separate UTS #39 General Security Profile warning; exact Unicode 17.0.0 inputs in the source manifest (decisions 0011/0012) | Resolved (proposed) | L-08…L-11, decisions 0011/0012 |
| A-45 | Which directional skeletons define identifier confusability? | For Plain, identifiers are confusable if any UTS #39 rev32 `bidiSkeleton` value for LTR, RTL, or FS matches; applies to PL0105 and proposed PL1101 C4 relation (decision 0012) | Resolved (proposed) | L-10/L-11, UTS #39 rev32 §4, UTS #55 rev5 §§5.1.1–5.1.2.2, decision 0012 |
| A-46 | Does the pinned Unicode 17.0.0 data lock cover all identified inputs for joining contexts and diagnostics? | Add `IndicSyllabicCategory.txt` for UTS #39 rev32 §3.1.1.1(B); map 16 data/test inputs to adopted profile operations (decision 0012) | Resolved (proposed) | L-08/L-11, decision 0012 and source manifest |
| A-47 | Can an out-of-profile warning be suppressed independently from confusable diagnostics? | UTS #55 rev5 §5.1.3 recommends independent suppression; propose `PL1104` enabled by default and independently suppressible from `PL0105`/`PL1101`, with the exact configuration mechanism deferred to the tooling/configuration phase (decision 0012) | Resolved (proposed) | L-11, UTS #55 rev5 §5.1.3, decision 0012 |

## 2. Summary

| Status | Count | IDs |
|---|---|---|
| Resolved (proposed) | 42 | A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10, A-11, A-13, A-14, A-15, A-16, A-17, A-18, A-19, A-20, A-22, A-24, A-25, A-27, A-28, A-29, A-30, A-31, A-32, A-33, A-34, A-35, A-36, A-37, A-38, A-39, A-40, A-41, A-43, A-44, A-45, A-46, A-47 |
| Deferred | 5 | A-04, A-12, A-21, A-23, A-26 |
| Open — requires a decision before Gate 1 | 0 | — |
| **Total** | **47** | A-01 … A-47 |

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
| Confusable detection is a mitigation, not a guarantee | Skeletons are sequence-aware but versioned and incomplete; full visible-name analysis is Phase 13 tooling work |
| `Eq` on recursive records is rejected rather than defined | Some legitimate data models must be reshaped; the diagnostic must explain why |
| No subtyping (T-25) | Some reuse patterns need conversion functions instead of implicit widening — deliberate |
| No modules (D-10) | Real apps cannot be structured in v0.1; the interpreter's demo is single-file |

## 5. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 0.1 | Register derived: 26 questions, 21 resolved, 5 deferred, 0 open; provenance and limits stated. |
| 2026-11-03 | 0.2 | Audit added A-27…A-43; corrected A-06/A-18/A-19/A-25 and limits; 43 total, 35 resolved, 5 deferred, 3 open. |
| 2026-11-03 | 0.2.1 | Decision 0009 proposed resolutions for A-27/A-38; 43 total, 37 resolved, 5 deferred, 1 open (A-42). |
| 2026-11-03 | 0.2.2 | Decision 0010 proposes hermetic core-only Gate 1 with later obligations unwaived; 43 total, 38 resolved, 5 deferred, 0 open. Owner/reviewer ratification remains a gate condition. |
| 2026-11-03 | 0.2.3 | Decision 0011 specifies UTS #55 chunk diagnostics, out-of-profile warning, and pins the initial 15 Unicode 17.0.0 data/test inputs. |
| 2026-11-03 | 0.2.4 | Decision 0012 proposes direction-aware LTR/RTL/FS confusability and adds the missing joining-context data input; 47 total, 42 resolved (proposed), 5 deferred, 0 open. |
