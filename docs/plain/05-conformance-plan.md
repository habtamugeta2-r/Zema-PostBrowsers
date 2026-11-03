# Plain 5 — Conformance Plan (plan only: zero fixtures written)

| Field | Detail |
|---|---|
| **Version** | 0.2.4 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | **Plan only.** No test file exists yet; this document exists so the build task has a specification to satisfy |
| **Rules covered** | L-01…L-34, S-0…S-5, T-01…T-30, E-01…E-36 — full rule-level allocation is in [`07-traceability.md`](./07-traceability.md) |

> Gate 1 requires "a conformance test suite with passing results". This is
> the plan for that suite, not the suite. Writing fixtures is a **build**
> task; C1/C5 were resolved on 2026-11-03, so it is authorized, and none of
> it has been written.
>
> **Every rule is allocated to an area here and to a verification method in
> [`07-traceability.md`](./07-traceability.md).** That second document is
> the one to consult when asking "is rule X tested?" — an area with a
> fixture budget can be satisfied while an individual rule stays untouched.

---

## 1. What "passing" will mean

- Every normative rule in the **Gate 1 scope** (A-42) **MUST** be exercised by at least one fixture. Later-phase platform obligations are listed separately and are not silently waived.
- Fixtures are grouped by rule prefix and named `conformance/<area>/<id>_<slug>.plain` with an adjacent `.expected` file (stdout value, fault code, or diagnostic code + span).
- The whole suite **MUST** pass twice: once with checking/assertions enabled and once with an optimizing configuration, with identical results (E-36).
- Diagnostics fixtures **MUST** assert code, span, and the presence of a fix where L-30 requires one.
- A rule with no fixture is reported as **uncovered** by the runner; the Gate 1 review **MUST** refuse a suite with uncovered rules.

## 2. Test areas and coverage targets

| Area | Rules | Fixture count (target) | Notes |
|---|---|---|---|
| Lexical: encoding, NFC, tabs, tables of literals | L-01…L-04, L-13…L-18 | 18 | Includes hostile inputs: BOM, invalid UTF-8, tab indentation, non-NFC `é` |
| Comments and doc comments | L-05…L-07 | 6 | Line comment ends at newline; `--` inside a literal is data; nested block comment; unterminated block comment; doc comment attaches; dangling doc comment is `PL0104` |
| Identifiers: syntax, reserved words, confusables, naming | L-08…L-12 | 14 | Includes LTR/RTL/FS UTS #39 collision candidates, including `aא1` / `a1א`; UTS #55 C4 cases `Строкa`/`Δt`/`HTTPसर्वер`; valid Persian ZWNJ; `PL1104` profile warning |
| Layout: blocks, dedent, continuation, empty block, discard | L-19…L-27 | 20 | Includes "dedent that closes two blocks" and each of L-22's two continuation causes |
| Grammar: every production | §6, L-28, L-29 | 29 | Records need ≥1 field; `{}`; chained comparison; missing `else`; no user-defined operators or sections (L-28); `x.f(y)` rejection and field-access-only `.` (L-29) |
| Sugar and forbidden sugar | S-0…S-5 | 12 | Each sanctioned sugar has a desugaring-print assertion; each forbidden form has a diagnostic |
| Bindings, mutability, and prelude basics | T-01…T-05, T-28 | 16 | `let` immutability (`PL0201`); `mut` assignment rule (`PL0202`); block-local `mut`; no index syntax and `List.get` returns `Option`; `Bool` as an ordinary union with short-circuit keywords; same-block shadowing (`PL0227`) vs nested-block warning (`PL1102`) |
| Types: records, unions, nominality, closure of unions, top-level constants, entry point | T-06…T-10, T-29, T-30 | 14 | Two identical-shaped unions must not be interchangeable |
| Absence/failure: `Option`, `Result`, `?` | T-11…T-13, E-19 | 12 | Includes mismatched error type and `?` outside `Result` |
| Generics, bounds, interfaces, coherence | T-14…T-18 | 18 | Orphan impl, duplicate impl, incomplete impl, extra method |
| `alias` / `distinct` / `as` | T-19, T-20, S-4 | 8 | Includes rejected cross-distinct conversion |
| Inference limits | T-21…T-25 | 16 | Missing signature, ambiguous `[]`, int-literal-as-Float, higher-rank rejection |
| Equality and ordering | T-26, T-27, E-14, E-15 | 12 | NaN, `-0.0`, function comparison, recursive record `Eq` rejection, recursive union `Eq` success, user `impl Eq` rejection (`PL0231`), `Ord` requires `Eq`; law statements are review obligations, not statically provable |
| Numbers | E-05…E-10 | 20 | Overflow, `Int.min / -1`, divide-by-zero, truncation, `%` sign, total order of NaN/±0 |
| Text | E-11, E-12 | 10 | Concat/equal/compare, non-NFC preservation, no integer indexing; graphemes/scalars deferred D-20 |
| Logic and short-circuit | E-13 | 4 | `and`/`or` do not evaluate a right operand that cannot change the result; `not` is strict; left-to-right order |
| Evaluation order and determinism | E-01…E-04, E-35, E-36 | 14 | Order-of-effects probes with a test capability; pipe order (E-03); every one of these fixtures is also run under both profiles, which is how E-36 is established |
| Closures and capture | E-16…E-18 | 8 | `mut` capture rejection, snapshot semantics, no self-reference |
| `defer` | E-20…E-22 | 8 | LIFO order, non-`()` defer rejection, runs on `?`, not guaranteed on fault |
| Matching | E-23…E-27 | 14 | Missing variant, unreachable arm, explicit `_`, literal match with `_` |
| `if` | E-28, E-29 | 6 | Unit-typed `if` without `else`; mismatched branch types |
| Faults and termination | E-30…E-33 | 10 | Core arithmetic/fuel faults and task-local discard; supervisor/other-task survival is a Phase 3 platform fixture |
| Diagnostics quality | L-30…L-34 | 52+ | Generated registry ([`../../research/data/phase-01-document-audit.json`](../../research/data/phase-01-document-audit.json), `diagnostic_registry`): every active code, span, caret line, safe bidi quoting, no cascade, terminology; 20 is a floor, not a cap |
| **Currently allocated** | — | **341 fixtures** | Sum of the rows above; a planning budget, **not** a coverage proof. The 52 minimum is the current active diagnostic-code registry; new rules and A-42 scope may increase it. `E-34` is deliberately **not** in this table: it is a cost claim that Gate 12 owns (see §5) |

## 3. Runner requirements

1. **CLI**: `plain test conformance/ --profile checked|optimized --report json`.
2. **Report**: per-rule pass/fail/uncovered, plus a machine-readable list of uncovered rule IDs.
3. **Fault fixtures** assert an exact fault code, not a message string.
4. **Diagnostic fixtures** compare against a normalized diagnostic object (code, severity, span, fix presence).
5. **Hermetic**: no network, no wall-clock semantics, no filesystem beyond fixtures. Core faults use deterministic fuel/step quotas. Host capabilities are stubbed by a test broker only for explicitly included platform fixtures (Phase 3 stub, Phase 5 real).

## 4. Order of work (C1/C5 cleared 2026-11-03; build authorized)

1. Lexer + layout engine → L- and S- fixtures.
2. Parser → grammar fixtures.
3. Type checker → T- fixtures.
4. Evaluator → E- fixtures, including both build profiles.
5. Diagnostics pass → L-30…L-34 fixtures last, because they depend on every earlier code.
6. Gate 1 review only when the in-scope uncovered list is empty, both profiles agree, the proposed resolutions for A-27/A-38/A-42/A-44/A-45/A-46/A-47 have been ratified or revised by the owner/reviewer, and C2 is recorded.

## 5. Gate 1 scope versus later platform obligations (A-42; decision 0010)

**Proposed Gate 1 core (requires owner/reviewer ratification):** lexical/layout, grammar, types, local evaluation,
patterns, closures, `?`, `defer`, checked arithmetic, deterministic fuel
faults, diagnostics, and the non-normative reduction traces in
[`06-operational-semantics.md`](./06-operational-semantics.md) once that
model is promoted.

**Not covered by a hermetic core pass:** reactive transactions (Phase 2),
task supervision/isolation (Phase 3/4), real capability issuance/revocation
(Phase 5), grapheme segmentation/shaping (Phase 7), durable I/O and
external-effect compensation (Phase 9). Each remains an explicit later
gate obligation. A Gate 1 signature must say “Plain core passed Gate 1,” not “the
platform passed.” Later obligations are not waived.

**Normative rules this suite cannot verify.** Four rules in docs 00–02 resist a
hermetic core fixture; each has a named owner and a later gate that verifies it.
The list lives in exactly one place — [`07-traceability.md` §4](./07-traceability.md#4-rules-gate-1-cannot-fully-verify) —
and is deliberately **not** repeated here. `tools/audit_phase01.py --check`
requires every rule to appear in an area above **or** in that table, so a new
rule cannot fall between the two.

## 6. What this plan deliberately does not cover

- **Performance**: this suite asserts *behavior*, never speed (Gate 12 owns numbers).
- **Formatting equivalence**: the formatter's canonical output is Phase 13; until then, S-0 is tested by the parser, not by a formatter round-trip.
- **Proof**: the operational-semantics conjectures are not discharged by fixtures alone; they need a separate argument/review.
