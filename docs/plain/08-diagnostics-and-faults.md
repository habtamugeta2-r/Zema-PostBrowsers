# Plain 8 — Diagnostic and Fault Code Catalog

| Field | Detail |
|---|---|
| **Version** | 0.3.2 (draft) |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | **Proposal.** Identifiers and severities only. No message text, span, or fix is ratified |
| **Evidence label** | **Proposed** for every new identifier. The *existence* of each obligation is Established — it is in the rule text; the *identifier* is a new decision |
| **Depends on** | L-30 (stable code on every diagnostic), L-34 (one fixture per active code), E-30 (faults), A-42 (Gate 1 scope) |
| **Owner ratification** | **pending** — a new proposal, not a restatement of an accepted decision |
| **Machine check** | `python3 tools/audit_phase01.py --check` derives the registry from rule text and verifies every code in this catalog is either cited by a rule or is a §5 fault |

> **Why this document had to exist.** Three documents required what this catalog
> provides, and none of them provided it:
>
> - **L-30** requires every diagnostic to carry "a stable code (`PLnnnn` /
>   `PL1nnn`)".
> - The conformance plan §3.3 requires fault fixtures to "assert an **exact fault
>   code**, not a message string".
> - The traceability matrix promised a fixture for each of 52 active codes.
>
> But **E-30 enumerated the core faults and gave them no identifier at all**, and
> **12 rules required refusing a construct while naming no code.** An implementer
> following the specification literally cannot satisfy the runner: the artifacts
> demand identity where the specification supplies only description.
>
> That is the research → build gap in its concrete form — not a missing
> paragraph, but a requirement whose *shape* is specified and whose *identity*
> is not. A specification can look complete and still be unbuildable in exactly
> this way, because completeness was checked by reading, never by implementing.

---

## 1. Identifier scheme

| Kind | Pattern | Severity | Namespace state |
|---|---|---|---|
| **Parse** | `PL00nn` | error | **new in this catalog**; `PL0001` is the generic syntax error |
| **Lexical / layout / identifier** | `PL01nn` | error | closed; `PL0199` is the cascade summary (L-32) |
| **Type / declaration** | `PL02nn` | error | extended here to `PL0236`; next free is `PL0237` |
| **Runtime fault** | `PLFLnn` | **fault** (terminating, uncatchable) | **new in this catalog** |
| **Warning** | `PL11nn` | warning | `PL1101`…`PL1104` |

Rules for the scheme (Proposed):

1. **Codes are permanent.** A retired code keeps its number and is marked
   historical; it is never reissued. `PL0106` is the precedent.
2. **One owner per code.** The owning rule first defines the condition. Another
   rule may *cite* a code (`PL0107`, `PL0114`, `PL0219`, `PL0228` do) but must not
   redefine it.
3. **A fault is not a diagnostic.** Faults terminate the task and app code cannot
   catch them (E-30, T-12), so they get a separate `PLFL` namespace. **This is
   the decision that was missing.** With one shared namespace, the natural wrong
   move is to write a `catch` for a `PL0105`-style code, which the language
   forbids. The namespace makes the distinction structural instead of a footnote.
4. **Severity is part of the identity.** `error` blocks compilation, `fault`
   terminates execution, `warning` permits it. A fixture asserts all three.

## 2. Error codes — lexical, layout, identifiers (`PL01nn`)

| Code | Owner rule | Condition | New? |
|---|---|---|---|
| `PL0001` | L-28 (owner) | **Generic syntax error** — the parser reached a token no production accepts (chained comparison, unclosed delimiter, misplaced `->`). The only code for a malformed program, and the one L-32 suppresses in cascade | |
| `PL0101` | L-01 | Source is not valid UTF-8, or a BOM is rejected | |
| `PL0102` | L-03 | Tab character in indentation (fix: spaces) | |
| `PL0103` | L-04 | Identifier is not NFC (fix: the NFC form) | |
| `PL0104` | L-07 | Doc comment with no following declaration | |
| `PL0105` | L-10 | Two visible names are directionally confusable | |
| `PL0106` | L-12 | **Historical** — retired case-based naming error; never reissued | historical |
| `PL0107` | L-16 | `{}` used as an empty record (fix: `()`) | |
| `PL0108` | L-18 | Integer literal outside `Int` range | |
| `PL0109` | L-24 | Empty block | |
| `PL0110` | L-27 | Non-`()` value discarded in statement position | |
| `PL0111` | L-29 | `x.f(y)` method-call syntax (fix: `f(x)`) | |
| `PL0112` | S-1 | Record update where the record type is not deducible | |
| `PL0113` | S-3 | Text interpolation of a type with no `Display` | |
| `PL0114` | S-4 | `as` outside the `distinct`↔representation conversion | |
| `PL0115` | S-5 | Forbidden sugar (`+=`, `elif`, ternary, `do`, comprehension, `xs[i]`, method call) | |
| `PL0116` | E-11 | Integer indexing of `Text` | |
| `PL0117` | L-15 | Escape value is not a Unicode scalar value | |
| `PL0118` | L-08 | Identifier does not match the declared profile | **new** |
| `PL0119` | L-09 | Reserved word used as an identifier | **new** |
| `PL0120` | L-13 | Numeric literal malformed (leading/trailing `_`, empty or bad radix digits) | **new** |
| `PL0121` | L-14 | Float literal malformed (`1.`, `.5`, no digits around the point) | **new** |
| `PL0122` | L-20 | Statements in one block do not start at the same column, or the block column does not exceed the introducing line | **new** |
| `PL0123` | L-22 | Continuation line not indented deeper than the statement's first token | **new** |
| `PL0124` | L-25 | Declaration nested inside a function body (D-17) | **new** |
| `PL0125` | L-06 | Unterminated block comment (span opens at `{-`) | **new** |
| `PL0126` | L-02 | U+0085/U+2028/U+2029 used as a hidden line terminator outside a text literal | **new** |
| `PL0199` | L-32 | Cascade-suppression summary: "N further errors in this declaration" | |

## 3. Error codes — types and declarations (`PL02nn`)

| Code | Owner rule | Condition | New? |
|---|---|---|---|
| `PL0201` | T-01 | Assignment to a `let` binding | |
| `PL0202` | T-02 | Assignment target is not a `mut` binding | |
| `PL0203` | T-07 | Nominal mismatch between distinct union types | |
| `PL0204` | T-11 | Recoverable failure not declared as `Result` | |
| `PL0205` | T-13 | `?` outside a `Result` function, or error types differ | |
| `PL0206` | T-14 | Unbound type variable | |
| `PL0207` | T-15 | Interface operation on an unbounded parameter (fix: add the bound) | |
| `PL0208` | T-17 | Incomplete interface implementation | |
| `PL0209` | T-17 | Implementation adds a method not in the interface | |
| `PL0210` | T-18 | Orphan implementation | |
| `PL0211` | T-18 | Duplicate implementation for (interface, type) | |
| `PL0212` | T-18 | Specialization/override attempt | |
| `PL0213` | T-19 | `alias` used where `distinct` semantics were expected (explanatory) | |
| `PL0214` | T-21 | Missing annotation where inference is not allowed | |
| `PL0215` | T-21 | Lambda parameter type not determined by an expected type | |
| `PL0216` | T-22 | A rejected named feature: higher-rank, higher-kinded, implicit parameters, overloading, polymorphic recursion, defaulting, widening | |
| `PL0217` | T-23 | Integer literal in a `Float` position (fix: write `1.0`) | |
| `PL0218` | T-24 | Empty list literal or generic constructor with no expected type (fix: annotate) | |
| `PL0219` | E-08 | `==` or derived equality on a type that is not `Eq` | |
| `PL0220` | T-27 | Non-productive recursive type | |
| `PL0221` | E-17 | Closure captures a `mut` binding | |
| `PL0222` | E-18 | Closure self-reference | |
| `PL0223` | E-21 | `defer` body does not have type `()` | |
| `PL0224` | E-23 | Non-exhaustive `when` (lists the missing variants) | |
| `PL0225` | E-24 | Unreachable arm (names the earlier arm) | |
| `PL0226` | E-28 | Unit-typed `if` in a value position, or branch types differ | |
| `PL0227` | T-28 | Same-block redeclaration (fix: use `mut` or a new name) | |
| `PL0228` | T-13 | `?` inside a `defer` body | |
| `PL0229` | E-26 | Duplicate binder name in one pattern | |
| `PL0230` | T-29 | Top-level `let` initializer not constant or not annotated | |
| `PL0231` | T-26 | User-written `impl Eq` (the interface is sealed) | |
| `PL0232` | T-03 | Use of a `mut` binding outside its block | **new** |
| `PL0233` | T-08 | Union extension attempt after declaration | **new** |
| `PL0234` | T-09 | Variant with more than one payload, or a positional field list | **new** |
| `PL0235` | T-25 | Implicit widening or subtyping attempt (no subtyping exists) | **new** |
| `PL0236` | T-16 | Interface declares a default method body (D-12) | **new** |

## 4. Fault codes — `PLFLnn` (new namespace)

Every fault is **terminating** and **uncatchable** (E-30, T-12). A fixture asserts
the exact code; no message is compared.

| Code | Owner rule | Condition | Gate 1? |
|---|---|---|---|
| `PLFL01` | E-05 | Signed 64-bit overflow in `+`, `-`, `*`, unary `-` | **yes** |
| `PLFL02` | E-05 | Overflow in `Int.min / -1` | **yes** |
| `PLFL03` | E-06 | Division by zero | **yes** |
| `PLFL04` | E-06 | Remainder by zero | **yes** |
| `PLFL05` | E-33 | Deterministic fuel/step quota exhausted | **yes** |
| `PLFL06` | E-30 | *Reserved* — host quota exceeded | no (Phase 3) |
| `PLFL07` | E-30 | *Reserved* — capability revoked or misused | no (Phase 5) |
| `PLFL08` | E-30 | *Reserved* — unrecoverable host I/O | no (Phase 9) |

**Only `PLFL01`–`PLFL05` are Gate 1 obligations.** `PLFL06`–`PLFL08` are reserved
so numbering does not shift when Phases 3/5/9 arrive. A Gate 1 fixture must not
assert them and a Gate 1 pass must not imply them (A-42).

## 5. Warning codes — `PL11nn`

| Code | Owner rule | Condition |
|---|---|---|
| `PL1101` | L-11 | Identifier chunk meets the UTS #55 C4 confusability test |
| `PL1102` | T-28 | Nested-block shadowing (allowed; never changes earlier references) |
| `PL1103` | L-12 | Name-case style violation in a bicameral script (fix suggested) |
| `PL1104` | L-11 | Identifier outside the UTS #39 General Security Profile (independently suppressible) |

## 6. Rules that need **no** code, and why

Carrying a `MUST` does not imply a diagnostic. These rules are semantic
obligations verified by behavior, or implementation constraints verified by
review. Listing them prevents the opposite error — inventing a code for
something that must simply *happen*.

| Rule | Obligation | Why no code | Verified by |
|---|---|---|---|
| L-05 | `--` starts a line comment | Nothing is refused | behavior fixture |
| L-17 | Trailing commas accepted | Nothing is refused | parser fixture (S-0) |
| L-19 | Block opens on a trailing `:` | Nothing is refused | layout fixture |
| L-21 | `pattern:` opens a block; `->` only in return types | Its violations are `PL0122`/`PL0123` | parser fixture |
| L-23 | Blank/comment lines do not affect indentation | Its violation *is* a column error (`PL0122`) | layout fixture |
| L-26 | A block's value is its tail expression | Nothing is refused | evaluation fixture |
| L-28 | No user-defined operators; precedence closed | The syntax is refused as `PL0115` | rejection fixture |
| L-30, L-31, L-33, L-34 | The diagnostic *contract* itself | They govern all codes above; they are not conditions | applies to every code |
| T-04 | `List.get` out of bounds returns `None` | A value, not a fault (T-04) | behavior fixture |
| T-05 | `Bool` is an ordinary union | Nothing is refused | type fixture |
| T-10 | Unions are closed | Its violation is `PL0233` | behavior fixture |
| T-12 | Faults are not catchable | No `catch` syntax parses at all | rejection fixture |
| T-18 (rule 3 only) | No blanket implementations, so overlap cannot arise | The construct is not expressible (D-14); **rules 1, 2, 4 raise `PL0210`/`PL0211`/`PL0212`** and are not in this list | parser fixture |
| T-30 | No implicit entry point | Nothing is refused; a fixture names its function | runner fixture |
| E-01…E-04, E-07, E-09, E-14…E-16, E-20, E-25, E-27, E-29, E-31, E-35 | Order, numeric semantics, closures, `?`/`defer`, matching, fault propagation, determinism | Behavior, not rejection | behavior fixtures |
| E-19 (except its last clause) | `?` evaluates its operand once and unwinds to the nearest activation | Behavior — **but the final clause, "`?` inside `defer` is rejected", raises `PL0228`** and is not codeless | behavior + rejection fixture |
| **E-10, E-22, E-32, E-36** | Compiler/implementation constraints (no fast-math; `defer` not guaranteed on fault; no partial state; no profile-dependent meaning) | No *user program* can violate these; a violating **implementation** is non-conforming | `SR` — structured review + the dual-profile run |
| E-33 (except its fuel clause) | Faults are deterministic given the same inputs | Implementation constraint. **Its fuel clause is not codeless: quota exhaustion is the fault `PLFL05`** | `SR` + the fuel fixture |

## 7. Skeleton message shape (illustrative, not ratified)

L-30 fixes the fields, not the wording. One example so that L-33 (language terms)
and L-31 (safe quoting) have something concrete to be tested against:

```text
error[PL0122]: statements in this block do not line up
  --> task.plain:4:6
   |
 3 |     count = 1
 4 |      total = 2
   |      ^^^^^^^
   |
   = this line starts at column 6; the block starts at column 5
   = fix: indent line 4 to column 5
```

This example exists to be checked against four rules: one-line message plus cause,
a `line:column` span with a caret underline (L-30), exactly one machine-applicable
fix (L-30), language terms only — "block", "line", "column", never AST vocabulary
(L-33), and no raw bidi controls inside quoted source (L-31).

## 8. What this catalog changes (computed, not counted by hand)

`python3 tools/audit_phase01.py --verify` prints every figure in this table from
the files themselves. If prose and tool disagree, the tool is right.

| Quantity | Before | After |
|---|---:|---:|
| Codes in the registry (`diagnostic_codes`) | 53 | **73** |
| — error | 49 | **64** (+15) |
| — fault | 0 | **5** (+5, new namespace) |
| — warning | 4 | 4 |
| — historical | 1 | 1 (`PL0106`) |
| **Active codes (L-34 fixtures)** | **52** | **72** — 67 error/warning + 5 fault |
| New identifiers introduced here | 0 | **20** (15 errors + 5 faults) |
| Codes with no owning rule | — | **0** |
| Rules requiring rejection that name no code | 12 | **0** |
| Fault identifiers reserved for later phases | 0 | 3 (`PLFL06`–`PLFL08`) |
| Total conformance budget | 341 | **356** |

> **This section's first two drafts were wrong, and both are recorded.**
> Draft one claimed +16 error codes, +8 fault codes, 68 active codes. Draft two
> claimed 62 and 60. Both were estimated before anything was counted — the same
> defect this audit exists to catch, committed inside the audit itself. The
> table above is generated by `--verify`, and the tool is the authority.
>
> The lesson is the finding: **a count typed into prose is a claim, not a fact**,
> and the only durable fix is to compute it. That is process rule PR-01.

## 9. Deliberately left open

| # | Item | Why |
|---|---|---|
| 1 | Exact wording for all 72 codes | Editorial; L-30/L-33 constrain it and fixtures will pin it |
| 2 | Span convention for multi-token diagnostics (where a caret starts) | Needs the lexer; `line:column` alone does not decide a judgement call |
| 3 | Whether `PL0105` and `PL1101` may both fire on one identifier | Depends on A-47's suppression mechanism, deferred to tooling |
| 4 | Review of every name in this catalog | **Owner ratification pending.** Names are the cheapest thing to change now and the most expensive once fixtures cite them |
| 5 | Whether `PL0213` should be a warning rather than an error | It is explanatory, not a rejection; needs a decision, not a guess |
| 6 | Whether `PLFL05` (fuel) belongs in the fault namespace at all | Fuel is deterministic and fixture-controlled, so it may read better as a diagnostic; either choice is defensible and the current text is not decisive |

## 10. How this catalog is kept honest

Three mechanisms, because this document's own history shows prose drifting:

1. **The registry is derived, not listed.** `tools/audit_phase01.py`
   `diagnostic_registry()` reads every `PL` code out of the normative rule text
   and records which rule cites it. This catalog is checked *against* that
   registry; it does not maintain a parallel list that could drift from it.
2. **`--check` fails** if a rule demands a refusal without a code and without an
   entry in §6; if the registry gains a code with no owning rule; if a §6 row
   claims a rule is codeless while the registry records it as owning one; and if
   a code is introduced as *the fault* outside the `PLFL` namespace.
3. **Every count in §8 is printed by `--verify`.** No figure here may be typed
   from memory — that is exactly how its first two drafts went wrong.

## 11. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 0.3.2 | Added `PL0001`, the generic syntax error the spec twice referred to without naming. §6 audited against the registry: five rules were listed as codeless while owning a code, and are now marked as *partially* coded with the code named. Counts 73 codes / 72 active / budget 356. |
| 2026-11-03 | 0.3.1 | Corrected §8 to measured values after two wrong hand-counted drafts: 72 registry codes (63 error / 5 fault / 4 warning), 71 active, 19 new identifiers, budget 341 → 355. Added §10. |
| 2026-11-03 | 0.3.0 | Created. Records the two gaps (E-30 had no fault identifiers; 12 rules required rejection with no code), defines the `PLFL` fault namespace, proposes 14 new error codes and 5 Gate 1 fault codes, lists the 38 rules that correctly need no code, corrects its own first-draft counts downward, and leaves 6 items open for owner ratification. |
