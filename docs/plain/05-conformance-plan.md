# Plain 5 — Conformance Plan (plan only: zero fixtures written)

| Field | Detail |
|---|---|
| **Version** | 0.1 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | **Plan only.** No test file exists yet; this document exists so the build task has a specification to satisfy |
| **Rules covered** | L-01…L-34, S-0…S-5, T-01…T-28, E-01…E-36 |

> Gate 1 requires "a conformance test suite with passing results". This is
> the plan for that suite, not the suite. Writing fixtures is a **build**
> task and is blocked on Gate 0 conditions C1/C5.

---

## 1. What "passing" will mean

- Every normative rule **MUST** be exercised by at least one fixture.
- Fixtures are grouped by rule prefix and named `conformance/<area>/<id>_<slug>.plain` with an adjacent `.expected` file (stdout value, fault code, or diagnostic code + span).
- The whole suite **MUST** pass twice: once with checking/assertions enabled and once with an optimizing configuration, with identical results (E-36).
- Diagnostics fixtures **MUST** assert code, span, and the presence of a fix where L-30 requires one.
- A rule with no fixture is reported as **uncovered** by the runner; the Gate 1 review **MUST** refuse a suite with uncovered rules.

## 2. Test areas and coverage targets

| Area | Rules | Fixture count (target) | Notes |
|---|---|---|---|
| Lexical: encoding, NFC, tabs, tables of literals | L-01…L-04, L-13…L-18 | 18 | Includes hostile inputs: BOM, invalid UTF-8, tab indentation, non-NFC `é` |
| Identifiers: syntax, reserved words, confusables, naming | L-08…L-12 | 14 | Includes a Cyrillic/Latin skeleton collision and a mixed-script warning |
| Layout: blocks, dedent, continuation, empty block, discard | L-19…L-27 | 20 | Includes "dedent that closes two blocks" and each of L-22's three continuation causes |
| Grammar: every production | §6 | 25 | Records need ≥1 field; `{}`; `x.f(y)`; chained comparison; missing `else` |
| Sugar and forbidden sugar | S-0…S-5 | 12 | Each sanctioned sugar has a desugaring-print assertion; each forbidden form has a diagnostic |
| Types: records, unions, nominality, closure of unions | T-06…T-10 | 14 | Two identical-shaped unions must not be interchangeable |
| Absence/failure: `Option`, `Result`, `?` | T-11…T-13, E-19 | 12 | Includes mismatched error type and `?` outside `Result` |
| Generics, bounds, interfaces, coherence | T-14…T-18 | 18 | Orphan impl, duplicate impl, incomplete impl, extra method |
| `alias` / `distinct` / `as` | T-19, T-20, S-4 | 8 | Includes rejected cross-distinct conversion |
| Inference limits | T-21…T-25 | 16 | Missing signature, ambiguous `[]`, int-literal-as-Float, higher-rank rejection |
| Equality and ordering | T-26, T-27, E-14, E-15 | 12 | NaN, `-0.0`, function comparison, recursive record `Eq` rejection, recursive union `Eq` success |
| Numbers | E-05…E-10 | 20 | Overflow, `Int.min / -1`, divide-by-zero, truncation, `%` sign, total order of NaN/±0 |
| Text | E-11, E-12 | 10 | Grapheme vs scalar counts, no integer indexing, code-point ordering documented |
| Evaluation order and determinism | E-01…E-04, E-35 | 10 | Order-of-effects probes with a test capability; pipe order (E-03) |
| Closures and capture | E-16…E-18 | 8 | `mut` capture rejection, snapshot semantics, no self-reference |
| `defer` | E-20…E-22 | 8 | LIFO order, non-`()` defer rejection, runs on `?`, not guaranteed on fault |
| Matching | E-23…E-27 | 14 | Missing variant, unreachable arm, explicit `_`, literal match with `_` |
| `if` | E-28, E-29 | 6 | Unit-typed `if` without `else`; mismatched branch types |
| Faults and termination | E-30…E-33 | 10 | Fault discards transaction; other tasks survive (needs Phase 3 harness) |
| Diagnostics quality | L-30…L-34 | 20 | Code, span, caret line, no cascade, terminology check |
| **Total target** | — | **≈ 285 fixtures** | Deliberately over-provisioned: Gate 1 must not need "we'll add tests later" |

## 3. Runner requirements

1. **CLI**: `plain test conformance/ --profile checked|optimized --report json`.
2. **Report**: per-rule pass/fail/uncovered, plus a machine-readable list of uncovered rule IDs.
3. **Fault fixtures** assert an exact fault code, not a message string.
4. **Diagnostic fixtures** compare against a normalized diagnostic object (code, severity, span, fix presence).
5. **Hermetic**: no network, no clock, no filesystem beyond fixtures. Host capabilities are stubbed by a test capability broker (Phase 3 stub, Phase 5 real).

## 4. Order of work once C1/C5 clear

1. Lexer + layout engine → L- and S- fixtures.
2. Parser → grammar fixtures.
3. Type checker → T- fixtures.
4. Evaluator → E- fixtures, including both build profiles.
5. Diagnostics pass → L-30…L-34 fixtures last, because they depend on every earlier code.
6. Gate 1 review only when the uncoverable list is empty and both profiles agree.

## 5. What this plan deliberately does not cover

- **Reactive semantics** (E1), **concurrency** (E2), **rendering**, **text shaping**, **capabilities**: later phases, own experiments and gates.
- **Performance**: this suite asserts *behavior*, never speed (Gate 12 owns numbers).
- **Formatting equivalence**: the formatter's canonical output is Phase 13; until then, S-0 is tested by the parser, not by a formatter round-trip.
