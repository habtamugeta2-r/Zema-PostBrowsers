# Plain 7 — Rule Traceability Matrix

| Field | Detail |
|---|---|
| **Version** | 0.2.4 |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | **Matrix only.** It allocates every normative rule to a verification method and a conformance area. It is **not** coverage evidence: zero fixtures exist, and a row here is a promise, not a result |
| **Scope** | All 106 normative rule IDs: `L-01`…`L-34`, `T-01`…`T-30`, `E-01`…`E-36`, `S-0`…`S-5` |
| **Evidence label** | **Proposed.** The allocation is a design decision; the counts it reports are repository observations |

> **Why this document exists.** The specification had stable rule IDs and the
> conformance plan had fixture *budgets by area*, but nothing joined them. The
> plan named ranges (`L-08…L-12`, `T-21…T-25`) that omitted **14 of the 106
> rules**, and there was no way for a reviewer to ask "where is `E-34` tested?"
> and get an answer. A fixture budget by area can be met while individual rules
> stay untouched — exactly the failure mode the plan's own §1 forbids
> ("a rule with no fixture is reported as uncovered").
>
> This matrix is the join. `tools/audit_phase01.py --check` now fails if any
> normative rule is missing from this file, if an ID here does not exist, or if
> an area in the [conformance plan](./05-conformance-plan.md) is left unowned.

---

## 1. Verification method legend

| Code | Method | What it proves | What it does not prove |
|---|---|---|---|
| **FX** | Executable conformance fixture (`.plain` + `.expected`) | The implementation produces the specified observable outcome for that input | Anything about inputs not written |
| **RT** | Rejection fixture: the construct **must** be refused with a named code | The language keeps a promise to refuse | That all ways of writing the construct are caught |
| **DZ** | Diagnostic fixture: code, severity, span, fix presence | The diagnostic contract of L-30…L-34 | Message prose quality (review obligation) |
| **EM** | Emitted-desugaring fixture (§8 / S-0…S-4) | The compiler can print the desugared form | Formatter equivalence (Phase 13) |
| **AX** | Axiom: verified by **reading the artifact**, not by running Plain | The file/record exists and says what is claimed | Any runtime behavior |
| **SR** | Structured review against an external standard, recorded as an experiment | A reviewer compared rule text to the pinned clause | That the implementation matches the rule |
| **PT** | Property/generative test with fixed seed and saved minimized counterexample | Falsification on sampled inputs | Completeness |
| **NV** | **Not verifiable at Gate 1 — and this is recorded, not hidden.** The rule makes a claim about something the hermetic core cannot exhibit | Nothing, yet | It must never be counted as covered |

**Rule.** A rule whose only method is **NV** **MUST** appear in §4 with the
owning phase and gate that will verify it. Marking a rule NV without that
entry is a defect the audit rejects.

## 2. Matrix

Columns: **Rule** — the normative text · **Method** — from §1 · **Area** — the
conformance-plan area that carries the fixture · **Target** — the Gate 1
verification that must exist before Gate 1 can be attempted.

### 2.1 Lexical structure and layout (`docs/plain/00-lexical-and-layout.md`)

| Rule | Method | Area | Target |
|---|---|---|---|
| L-01 | RT + DZ | Lexical | Invalid UTF-8 file rejected; a valid file with a BOM is rejected as `PL0101`, not silently stripped |
| L-02 | FX + RT | Lexical | CRLF source parses identically to LF; U+2028 outside a text literal does not terminate a line and is either data or an error, never layout |
| L-03 | RT + DZ | Layout | Tab in indentation is `PL0102` with a fix; tab inside a text literal is data |
| L-04 | RT + DZ | Identifiers | Non-NFC identifier is `PL0103` with the NFC form as fix; a non-NFC **text literal** is accepted and preserved byte-for-byte through evaluation |
| L-05 | FX | Lexical | Line comment ends at newline; a `--` sequence inside a text literal does not start a comment |
| L-06 | FX + RT | Lexical | Nested block comment closes correctly; an unterminated one is an error with a span at the opening delimiter |
| L-07 | FX + DZ | Lexical | Doc comment attaches to the next declaration; a dangling doc comment is `PL0104` |
| L-08 | FX + RT | Identifiers | XID_Start/XID_Continue accept/reject boundary code points from the pinned tables, incl. `_` as Start and lone `_` as wildcard; every rejection names the profile version |
| L-09 | RT + DZ | Identifiers | Each reserved word is refused as a declaration name; `return` is reserved though unused in expressions |
| L-10 | RT + DZ | Identifiers | Directional collision pair (LTR/RTL/FS) is `PL0105`; a repeated reference to the **same** declaration is not a collision |
| L-11 | RT + DZ + SR | Identifiers | Chunk boundaries, C4 warning `PL1101`, out-of-profile warning `PL1104`, and allowed ZWNJ/ZWJ contexts behave per the pinned clauses; the mixed-script heuristic is absent |
| L-12 | FX + DZ | Identifiers | Name roles resolve from declaration context, not case; style violation is warning `PL1103`; no case-based check on a unicameral-script name |
| L-13 | FX + RT | Lexical | Decimal/hex/binary literals; leading and trailing `_` are errors |
| L-14 | FX + RT | Lexical | `1.5` and `1.5e3` are `Float`; `1.` and `.5` are errors; `1` is `Int` |
| L-15 | FX + RT | Lexical | Every documented escape decodes; surrogate and out-of-range `\u{…}` are `PL0117`; literal contents are not normalized |
| L-16 | FX + RT | Grammar | `()` is unit; `{}` is `PL0107` pointing at `()` |
| L-17 | FX | Grammar | List literals, empty `[]`, and trailing commas in all four positions parse |
| L-18 | RT + DZ | Lexical | Integer literal that does not fit `Int` is `PL0108` at compile time, never a wrapped value |
| L-19 | FX | Layout | Block opens on a trailing `:` and closes at `DEDENT` |
| L-20 | RT + DZ | Layout | Uneven block columns are an error; block column greater than the opener's column is required |
| L-21 | FX + RT | Grammar | `pattern:` opens a block; `->` appears only in return types |
| L-22 | FX + RT | Layout | Both continuation causes accepted; a trailing `:` is not a continuation; under-indented continuation is rejected |
| L-23 | FX | Layout | Blank and comment-only lines do not change indentation analysis |
| L-24 | RT + DZ | Layout | Empty block is `PL0109` |
| L-25 | RT | Grammar | Nested local declarations are rejected (D-17) |
| L-26 | FX | Evaluation | Block value is its tail expression; a block ending in a statement is `()` |
| L-27 | RT + DZ | Layout | Discarding a non-`()` value is `PL0110` |
| L-28 | RT | Grammar | No user-defined operators, no operator sections; the precedence table is closed |
| L-29 | RT + DZ | Grammar | `.` is field access only; `x.f(y)` is `PL0111` recommending `f(x)` |
| L-30 | DZ | Diagnostics | Every emitted diagnostic carries code, severity, span, message, cause, and fix-where-mechanical |
| L-31 | DZ | Diagnostics | Caret line is present; bidi/format controls in quoted source are escaped or visibly marked |
| L-32 | DZ | Diagnostics | After an unrecoverable error in a declaration, later errors in that declaration are suppressed and summarized (`PL0199`); no cascade |
| L-33 | DZ + AX | Diagnostics | Diagnostic wording uses language terms; a reviewer check confirms no internal AST/IR vocabulary in registered messages |
| L-34 | DZ + AX | Diagnostics | Every **active** registry code has a fixture; retired codes (PL0106) are marked historical, not deleted |

### 2.2 Types (`docs/plain/01-types.md`)

| Rule | Method | Area | Target |
|---|---|---|---|
| T-01 | RT + DZ | Bindings | Reassigning a `let` is `PL0201` |
| T-02 | RT + DZ | Bindings | Assigning to a non-`mut` target is `PL0202`; mutability is a property of the binding |
| T-03 | FX + RT | Bindings | A `mut` binding is block-local; passing it passes the current value; no aliasing is expressible |
| T-04 | FX + RT | Types | No index syntax; `List.get` out-of-bounds yields `Option` `None`, not a fault |
| T-05 | FX | Types | `Bool` is an ordinary prelude union usable in `if`/`when`; `and`/`or`/`not` remain keywords |
| T-06 | FX + RT | Types | Records need ≥1 field; record types are structural |
| T-07 | FX + RT | Types | Unions are nominal and closed; two identically shaped unions are not interchangeable |
| T-08 | FX + RT | Types | Union closure holds: no variant may be added outside the declaring type |
| T-09 | RT | Types | At most one variant payload; a positional field list is rejected |
| T-10 | FX + RT | Types | `Option`/`Result` are ordinary prelude unions with the specified constructors |
| T-11 | RT + DZ | Absence | No `null`; a recoverable failure must be in the return type as `Result` (`PL0204`); no exception primitive parses |
| T-12 | RT | Faults | A fault cannot be caught or converted into `Result` by app code |
| T-13 | FX + RT + DZ | Absence | `?` only in a `Result` function, same error type (`PL0205`); forbidden in `defer` (`PL0228`); targets nearest activation incl. a lambda |
| T-14 | RT + DZ | Generics | Unbound type variable is `PL0206` |
| T-15 | RT + DZ | Generics | Interface operation on an unbounded parameter is `PL0207` with the missing bound as fix; `Ord` requires `Eq` |
| T-16 | FX + RT | Generics | Interfaces declare signatures only; a default body is rejected (D-12) |
| T-17 | RT + DZ | Coherence | Incomplete impl is `PL0208`; extra method is `PL0209` |
| T-18 | RT + DZ | Coherence | Orphan `PL0210`, duplicate `PL0211`, specialization `PL0212`; overlap is not expressible |
| T-19 | FX | Types | `alias` is transparent in both directions |
| T-20 | FX + RT | Distinct | No implicit conversion either way; only `as` converts; other `as` use is `PL0114` |
| T-21 | RT | Inference | Declaration without the required annotation is rejected |
| T-22 | RT | Inference | Ambiguous `[]` is `PL0218` |
| T-23 | RT + DZ | Inference | Integer literal in a `Float` position is `PL0217`, never a conversion |
| T-24 | RT | Inference | Higher-rank use is rejected; only rank-1 declaration parameters exist |
| T-25 | RT | Types | No subtyping for records, unions, or interfaces |
| T-26 | FX + RT + DZ | Equality | Derived structural equality; user `impl Eq` is `PL0231`; `Float`/function-containing type is not `Eq` (`PL0219`); `Ord` requires `Eq` |
| T-27 | FX + RT + DZ | Types | Productive recursion accepted; a cycle solely through record fields is `PL0220`; recursive-union equality terminates |
| T-28 | FX + RT + DZ | Bindings | Same-block redeclaration is `PL0227`; nested-block shadowing warns `PL1102` and does not change earlier references |
| T-29 | FX + RT + DZ | Constants | Constant-only top-level `let`; a call, host effect, mutable read, or forward/cyclic reference is `PL0230` |
| T-30 | AX + FX | Entry point | No `main` keyword or implicit entry; a fixture names the function to evaluate |

### 2.3 Evaluation (`docs/plain/02-evaluation.md`)

| Rule | Method | Area | Target |
|---|---|---|---|
| E-01 | FX | Order | Strict left-to-right call-by-value, observed via effects |
| E-02 | FX | Order | Callee evaluated before arguments; argument evaluation order is fixed |
| E-03 | FX | Order | Pipe appends the piped value as the **last** argument; callee, explicit args, then piped value |
| E-04 | FX | Order | No ambient authority, no uninitialized value, no implicit randomness in evaluation |
| E-05 | FX | Numbers | Checked signed 64-bit arithmetic; overflow faults in **both** profiles |
| E-06 | FX | Numbers | Division truncates toward zero; remainder takes the dividend's sign; divide-by-zero faults |
| E-07 | FX | Numbers | No implicit `Int`↔`Float`; explicit conversions only |
| E-08 | FX + RT | Equality | `Float` has no `Eq`; NaN and `-0.0` are not equal-comparable |
| E-09 | FX | Equality | `Float.compare` provides the specified total order over NaN and signed zeros |
| E-10 | FX | Numbers | `Int.min / -1` faults; boundary values behave as specified in both profiles |
| E-11 | FX | Text | Concat, equal, compare on `Text` operate on scalar values; a non-NFC literal survives unchanged |
| E-12 | AX | Text | No localization or formatting is implied by concatenation (review obligation, no fixture) |
| E-13 | FX | Logic | `and`/`or` short-circuit left-to-right; `not` is strict; a right operand is not evaluated when the left decides |
| E-14 | FX | Equality | `==` is structural by record field / variant / list order / scalar; functions never comparable |
| E-15 | RT + DZ | Equality | `<`/`>`/`<=`/`>=` require `Ord`; records and unions are not `Ord` by default |
| E-16 | FX + RT | Closures | Closures capture immutable snapshots |
| E-17 | RT + DZ | Closures | Mutable capture is rejected; no self-reference |
| E-18 | FX | Closures | A snapshot taken before a later rebinding still sees the old value |
| E-19 | FX + RT | Absence | `?` propagates the error and exits the nearest function only |
| E-20 | FX | Defer | Block-local `defer` runs LIFO on normal exit |
| E-21 | FX + RT | Defer | Non-`()` defer is rejected; `?` inside `defer` is `PL0228` |
| E-22 | FX | Defer | Defers run on `?` unwinding; not guaranteed on a fault |
| E-23 | RT + DZ | Matching | Non-exhaustive `when` is `PL0224` listing the missing variants |
| E-24 | RT + DZ | Matching | An unreachable arm is `PL0225` naming the earlier arm |
| E-25 | FX | Matching | Explicit `_` suppresses the missing-variant list but not unreachability |
| E-26 | FX + RT | Matching | Pattern forms incl. record subsets and negative literals; duplicate binder is `PL0229`; guards do not parse (D-11) |
| E-27 | FX | Matching | Matching is partial; bindings exist only after full success and are arm-scoped; open domains need a wildcard |
| E-28 | FX + RT + DZ | If | `if` without `else` is `()` and rejected in a value position (`PL0226`); branches must agree |
| E-29 | FX | If | `else:` + nested `if` is the only chaining form; `elif` is refused by S-5 |
| E-30 | FX | Faults | The closed set of core faults: overflow, divide-by-zero, fuel exhaustion |
| E-31 | AX + NV | Faults | Task termination only; supervisor notification and other-task survival are **Phase 3** (Gate 3) |
| E-32 | FX | Faults | A fault leaves no partial task-local core state |
| E-33 | FX + PT | Faults | Fuel/step quotas are fixture inputs; identical results across runs, with no wall-clock or GC dependence |
| E-34 | NV | — | Checked-arithmetic cost is measured by **E1/E2 (Phases 2 and 4)** and is a Gate 12 evidence obligation |
| E-35 | FX + PT | Determinism | Deterministic evaluation; nondeterminism enters only through a capability-gated host call |
| E-36 | FX | Determinism | Checked and optimized profiles agree on every fixture, including fault codes |

### 2.4 Sugar (`docs/plain/00-lexical-and-layout.md` §8)

| Rule | Method | Area | Target |
|---|---|---|---|
| S-0 | EM | Sugar | Trailing commas are removed by the parser; the emitted desugaring has none |
| S-1 | EM + RT | Sugar | Record update prints as a full record literal; an undeducible record type is `PL0112` |
| S-2 | EM | Sugar | `x \|> f` prints as `f(x)`; `x \|> f(y)` prints as `f(y, x)` |
| S-3 | EM + RT | Sugar | Interpolation prints as `Text.concat` with `Display.display`; an unknown type is `PL0113` |
| S-4 | EM + RT | Distinct | `as` is identity at runtime; any other use is `PL0114` |
| S-5 | RT + DZ | Sugar | Compound assignment, `elif`, ternary, `do`, comprehensions, `xs[i]`, and method calls are refused with `PL0115` naming the canonical form |

## 3. Coverage arithmetic (a ledger, not a result)

| Quantity | Count | Source |
|---|---:|---|
| Normative rule IDs (`L`+`T`+`E`) | 100 | `tools/audit_phase01.py` |
| Sanctioned-sugar IDs (`S-0`…`S-5`) | 6 | §8 of doc 0 |
| **Total rule IDs in this matrix** | **106** | §2 above |
| Rules attributable to a conformance-plan area | 106 | plan §2, after the gap repair |
| Rules that are **NV** at Gate 1 | 2 | `E-31` (partial), `E-34` |
| Planned fixture budget | 341 | conformance plan §2 |
| Fixtures written | **0** | repository observation, 2026-11-03 |
| Rule-level coverage now provable | **0 %** | there is nothing to run |

> **Read this table the right way.** 106/106 rules are *allocated*, which is
> what a plan can achieve before code exists. 0/106 are *verified*. The distance
> between allocation and verification is the entire remaining Phase 1 build.
> Anyone quoting "341 fixtures" as progress is quoting a budget.

## 4. Rules Gate 1 cannot verify

| Rule | Why not at Gate 1 | Owner | Verified by |
|---|---|---|---|
| E-31 (task-survival clause) | There is no task, scheduler, or supervisor in a hermetic single-task core | Phase 3 | Gate 3 supervision fixtures |
| E-34 (cost of checked arithmetic) | It is a performance claim; Gate 12 owns all numbers and Gate 1 asserts behavior only | Phases 2, 4, 12 | E1, E2, Gate 12 |
| E-12 (no implied localization) | A design constraint, not an observable; enforced by review and by the absence of formatting APIs | Phase 7 | Gate 7 review |
| L-33 (diagnostic wording) | Partly mechanical (banned-vocabulary check) and partly editorial | Phase 13 | Gate 13 tooling review |

Every other rule in §2 is verifiable by an executable fixture inside the
hermetic core (decision 0010), which is exactly the scope A-42 proposes.

## 5. How this matrix stays true

1. **Adding a rule** without adding a row here fails `tools/audit_phase01.py --check`.
2. **Adding a row** for a rule that does not exist fails the same check.
3. **Changing the conformance plan's areas** so that a rule loses its area fails the check.
4. When a fixture is written, its metadata names the rule ID **and** the fixture
   path is recorded in the area's row here. That step turns a row from
   *allocated* into *implemented* and is the only way a rule becomes covered.
5. This file is regenerated-and-verified by the audit tool; the narrative
   columns are hand-written and reviewed, the ID set is mechanical.

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 0.2.4 | Created. Closes the rule→fixture traceability gap: 14 of 106 rules (`L-05`, `L-06`, `L-07`, `L-28`, `L-29`, `T-01`…`T-05`, `T-28`, `E-13`, `E-34`, `E-36`) had no conformance-plan area. Records the 2 rules Gate 1 cannot verify and their owners. |
