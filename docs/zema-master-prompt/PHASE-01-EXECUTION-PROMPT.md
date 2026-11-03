# ZEMA Phase 1 Execution Prompt — Plain Core Build, Conformance, and Gate 1

| Field | Detail |
|---|---|
| **Document** | Phase 1 execution prompt — the work order that turns draft v0.2.5 into an executable core and a Gate 1 result |
| **Version** | 1.1 (2026-11-03: repaired internal section pointers and refreshed the verified-facts table after the traceability pass; no work package changed) |
| **Date** | 2026-11-03 |
| **Status** | Ready for execution — **conditional on the owner authorizations in §2**. This document is a plan, not an authorization |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner (Better-back) |
| **Evidence label** | **Proposed** for all recommendations; **Established** for quoted repository state and the verified environment facts in §3 |
| **Subordinate to** | [Master Prompt v1.1](./ZEMA-Master-Research-and-Build-Prompt.md), [Gate 0 conditions](../gates/gate-00.md), decisions [0004](../decisions/0004-research-book-missing.md)–[0016](../decisions/0016-script-value-alias-input.md), and the [Plain draft](../plain/README.md) |
| **Location** | `docs/zema-master-prompt/PHASE-01-EXECUTION-PROMPT.md` |

> **Mission.** Build the smallest executable implementation of the
> hermetic Plain core specified in [`docs/plain/`](../plain/README.md),
> write and run the conformance suite planned in
> [`05-conformance-plan.md`](../plain/05-conformance-plan.md), and record
> a Gate 1 result — **"Plain core passed Gate 1"** or **"Plain core did
> not pass Gate 1"** (decision [0010](../decisions/0010-gate-1-core-scope.md)) —
> with every claim labeled and every number reproducible. An honest
> "did not pass," with the uncovered list attached, is a valid outcome.
> A fabricated pass is not.

---

## 0. How to use this prompt

You are the ZEMA research-and-build agent. Execute this prompt in one
phase slice: **Phase 1 → Gate 1**, and nothing else.

**Read first, in this order:**

1. [`00-Core-Concerns.md`](./00-Core-Concerns.md) — the 19 concerns, especially 4, 16, 17, 18, 19.
2. [Master Prompt](./ZEMA-Master-Research-and-Build-Prompt.md) §1–§3 and Phase 1 — the loop, the labels, the gate criteria.
3. [`gate-00.md`](../gates/gate-00.md) — conditions C1–C5 and their consequences.
4. [`gate-01-readiness.md`](../gates/gate-01-readiness.md) — the owner response packet.
5. [`docs/plain/`](../plain/README.md) — all nine documents. Docs 0–4 and 6 are the rule text and the decision registers; **doc 7** ([traceability](../plain/07-traceability.md)) is the work list your fixtures must close out; **doc 8** ([diagnostics and faults](../plain/08-diagnostics-and-faults.md)) names every code a fixture asserts — without it a rejection cannot be fixtured at all. The rule text is the specification you must satisfy; this prompt never overrides it.
6. This file, §2 preflight, before writing any code.

**Conflict precedence:** Master Prompt > Gate 0 conditions and recorded
decisions > Plain draft rule text > this prompt > convenience. Any
conflict you cannot resolve by that order is a **decision record**, not
a silent choice (Master Prompt §3).

**The five-step loop still applies.** The work packages in §5 encode it:
WP-1 is DECIDE (with targeted research), WP-2…WP-9 are BUILD, WP-8/WP-9
are MEASURE (behavior, never speed), WP-10 is GATE. Do not skip ahead;
do not start Phase 2 (directory guide rule 4).

---

## 1. Definition of success

Gate 1's exit criteria, verbatim from the Master Prompt:

- [ ] A safe executable core language is running (interpreter or compiled).
- [ ] The conformance suite passes for all specified semantics.
- [ ] Syntax is frozen for this gate. Scope discipline: no feature creep.

Scoped by decision 0010 (A-42): **the hermetic Plain core only** —
lexical/layout, grammar, types, local evaluation, patterns, closures,
`?`, `defer`, checked arithmetic, deterministic fuel faults, and
diagnostics. Reactive transactions (Phase 2), supervision/isolation
(Phases 3–4), real capabilities (Phase 5), segmentation/shaping
(Phase 7), and durable I/O (Phase 9) are **not** Gate 1 obligations and
are **not waived** by a Gate 1 pass. The gate review must say so
explicitly.

Success additionally requires (conformance plan §1, §3):

- every in-scope rule exercised by ≥1 fixture; the runner's uncovered
  list is empty for the declared scope;
- the whole suite passes **twice** — checked and optimized profiles —
  with identical results, including faults (E-36);
- every active diagnostic code in the generated registry has a fixture
  asserting code, span, and fix presence where required (L-30, L-34);
- Unicode 17.0.0 inputs match their recorded SHA-256 values before use;
- C1, C5, C2, and the A-27/A-38/A-42/A-44/A-45/A-46/A-47 ratifications
  are recorded (readiness packet §4). C3 (target OS) is *not* a Gate 1
  precondition; it is due before Phase 5.

---

## 2. WP-0 — Preflight: authorization check (MUST run first)

**This prompt authorizes nothing by itself.** Before any build task,
verify each item below in the repository record. Owner decisions cannot
be made, inferred, or signed by the agent. Silence is not approval.

| Check | Where to verify | If missing |
|---|---|---|
| **C1** — owner signed the frozen problem statement, target class, non-goals | [`gate-00.md`](../gates/gate-00.md) §8 sign-off box and §10 owner response | **Build blocked.** Run **WP-11 (§5)** fallback only |
| **C5** — PlainP ruled superseded / donor / eventual home | A dated owner decision in `docs/decisions/` or the readiness packet §2 | **Build blocked.** Run **WP-11 (§5)** fallback only |
| **C2** — book imported or chapter references retired | Readiness packet §2; decision 0004 successor if retired | Build may proceed; **Gate 1 attempt blocked** until recorded |
| **A-27, A-38, A-42, A-44, A-45, A-46, A-47** ratified or revised | Readiness packet §1 responses, or successor decision records | Build may proceed on the proposed text; **Gate 1 attempt blocked** until recorded. If revised: apply the revision to the rule text **and** the ambiguity register in the same commit, bump the draft version, then build |
| **C4** — project license stated | Gate 0 §5; a license decision record | No vendoring of third-party data/code into Git (§5 WP-2); fetch-on-build with hash verification instead. Public release remains blocked |

Record the preflight outcome — date, what was found, what is missing — as a
dated row in [`PHASE-TRACKER.md`](./PHASE-TRACKER.md)'s change log, and add or
update `docs/gates/gate-01-readiness.md` §2 with the condition you checked.
Then proceed to §5 if C1/C5 are recorded, or to **WP-11 (§5)** if they are not.
**Stop conditions are live at every step** (§7).

---

## 3. Verified environment facts (2026-11-03, this sandbox)

These were checked directly, not assumed. Re-verify at execution time;
if the environment differs, record the difference and revisit WP-1.

| Fact | Verification | Consequence |
|---|---|---|
| Python 3.11.2 present | `python3 --version` | Candidate implementation vehicle |
| Python's `unicodedata` is **Unicode 14.0.0**, not 17.0.0 | `python3 -c "import unicodedata; print(unicodedata.unidata_version)"` → `14.0.0`; matches the [Python 3.11 docs](https://docs.python.org/3.11/library/unicodedata.html) | **MUST NOT** use host `unicodedata` for L-04/L-08/L-10/L-11 properties or NFC. Generate all character data from the pinned 17.0.0 files (WP-2) |
| Node v22.22.3 present; **no Rust toolchain** (`rustc`, `cargo`, `rustup` absent) | `command -v` checks | A Rust implementation cannot be built or tested here without a toolchain this sandbox cannot reach (`static.rust-lang.org` is outside the network allowlist) |
| Network allowlist: `github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org` | Environment constraint | `unicode.org` is unreachable from the sandbox; the pinned GitHub mirror is the data source |
| The pinned Unicode data commit is reachable | `api.github.com` returned HTTP 200 for blob `21a79503…` and commit `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c` (`unicode-org/unicodetools`) | WP-2 fetch-and-verify is feasible here |
| `python3 tools/audit_phase01.py --check` passes | Ran it: 100 L/T/E rules + 6 sugars (106 rule IDs), 47 ambiguities (42/5/0), 20 deferrals, 355 fixture targets, 106/106 rules traced to a verification method and an area, 120 evidence rows, 56 grammar productions, 58 sources, 16 Unicode files, 72 diagnostic codes (63 error / 5 fault / 4 warning) + historical PL0106 | Keep it green; extend it, never hand-edit its outputs |

**Recommendation (Proposed — to be recorded as decision 0013):** the
Gate 1 vehicle is a **Python 3.11 standard-library-only reference
interpreter** ("the oracle"). Rationale: it is buildable and testable in
this environment with zero third-party dependencies; it mirrors the
Python-oracle/Rust-port parity pattern already recorded as a PlainP
donor candidate (research record 04 §3.4) **without adopting any PlainP
code**; and the Master Prompt assigns the production-runtime language
choice to Phase 3 Decision A, not to Gate 1. The Rust port remains a
Phase 3 obligation, and the oracle then becomes its parity target.
Alternatives (Node/TypeScript; waiting for a Rust toolchain) must be
written down and priced in the same decision record.

---

## 4. Non-negotiables (apply to every work package)

1. **Evidence discipline.** Every new claim gets a row in
   [`docs/evidence-register.md`](../evidence-register.md) with
   exactly one label (E/P/H) and a source grade where external. No
   performance claims — Gate 12 owns numbers; this suite asserts
   behavior only.
2. **Rule IDs are permanent.** Revise rule text, never renumber. Any
   spec change updates the rule **and** adds/updates an ambiguity row in
   the same commit (freeze policy, `docs/plain/README.md` §5).
3. **Hermetic core only** (A-42/decision 0010). No reactive graph, no
   host I/O, no network, no wall-clock, no filesystem beyond fixtures.
   Host capabilities in tests are deterministic stubs and prove nothing
   about Phase 5.
4. **No PlainP code** without C4 + C5 + a provenance record (research
   record 04 §3.4). Ideas already recorded as donor candidates may
   inform design; bytes may not be copied.
5. **No silent Unicode bump** (L-08). The profile is Unicode 17.0.0 /
   UAX #31 rev43 / UAX #15 rev57 / UAX #9 rev51 / UTS #39 rev32 /
   UTS #55 rev5, pinned to manifest commit `3ff0e2bb…`. An upgrade needs
   a decision, a data diff, regenerated fixtures, and a rerun.
6. **Checked arithmetic in every profile** (E-05, E-36). The optimized
   profile must not remove checks, wrap silently, or move a runtime
   fault to compile time.
7. **Deterministic faults** (E-33). Fuel/step quotas are fixture inputs;
   results must not depend on GC timing, wall clock, or host recursion
   limits.
8. **The diagnostic registry is generated, not hand-maintained**
   (L-34). Derive it from the rules via the audit tool; retired codes
   stay historical.
9. **Negative results are recorded with the same care as positive
   ones.** A retracted claim is a successful experiment.
10. **One canonical copy.** No parallel specs, no forked fixture lists.

---

## 5. Work packages

### WP-1 — DECIDE: implementation, data, and runner design

**Inputs:** §3 facts; Appendix A research; decisions 0005–0012; the
conformance plan; the rule traceability matrix; the semantics draft.

**Tasks:**
- Research the implementation approaches in Appendix A (test262/Wasm
  conformance practice, SpecTec/Watt semantics-validation practice,
  PLT Redex property testing, tree-walk interpreter structure). Record
  what you adopt and what you reject in `research/phase-01-06-*.md`.
- Write **decision 0013** — implementation vehicle and architecture
  (recommendation in §3), repository layout (§8), and the prelude
  inventory policy: every prelude function must trace to a rule in
  docs 00–02; additions require a decision row, not convenience.
- Write **decision 0014** — Unicode data pipeline: fetch/verify/generate
  strategy, NFC implementation approach, and the NormalizationTest.txt
  acceptance oracle (WP-2).
- Write **decision 0015** — conformance runner design: fixture header
  convention (entry function per T-30, fuel quota, expected outcome
  class), the `.expected` format, the JSON report schema, and what
  "checked" vs "optimized" concretely mean for the oracle. The two
  profiles MUST be genuinely different execution paths (e.g., direct
  AST walk vs. a semantics-preserving optimized pass); a flag that
  changes nothing is a fake pass and is forbidden.

**Acceptance:** three decision records (0013–0015) using
[`templates/decision-record.md`](./templates/decision-record.md), each
with options priced, not just chosen. A fourth, decision 0016, handles the
Script value-alias input and is an owner amendment, not an agent choice. Research record indexed in
[`research/README.md`](../../research/README.md).

### WP-2 — BUILD: Unicode data pipeline

**Inputs:** [`phase-01-source-manifest.json`](../../research/data/phase-01-source-manifest.json)
(16 pinned files; see proposed decision 0016 for a potential A-46 alias-input amendment), decisions 0011/0012/0014/0016, UTS #39 rev32, UTS #55 rev5,
UAX #31 rev43, UAX #15 rev57.

**Tasks:**
- Fetch the 16 files from the pinned GitHub commit into a **gitignored
  cache** (Gate 0 condition C4-safe default; vendoring into Git requires
  the C4 license decision). Verify git blob SHA-1, byte length, and
  SHA-256 against the manifest **before any use**; fail closed on
  mismatch. Commit the verification log, not the data.
- Generate compact property tables: XID_Start/XID_Continue, NFC
  decomposition/composition data (incl. combining classes and composition
  exclusions), Script/Script_Extensions, General_Category, Bidi_Class,
  confusables mappings, Identifier_Status/Type, ArabicShaping,
  IndicSyllabicCategory, and the UTS #39 General Security Profile inputs.
- Implement NFC and validate it against **every row** of the pinned
  `NormalizationTest.txt` before anything depends on it. Record the
  pass/fail counts as raw output.
- Implement UTS #39 rev32 §4 `internalSkeleton` exactly (NFD, remove
  Default_Ignorable_Code_Point characters, map through `confusables.txt`,
  NFD); implement `bidiSkeleton` for LTR/RTL/FS using UAX #9 L2/L3/L4
  before `internalSkeleton`; implement compatibility `skeleton` as
  `bidiSkeleton(LTR, X)`. Implement UTS #55 §5.1.2 chunking and the full
  C4 test; implement the §3.1.1.1 ZWJ/ZWNJ context rules including the
  global single-script/NFC restrictions and Indic context-B data.
- **Blocking input issue discovered during execution:** before any
  Script_Extensions/resolved-script-set comparison, resolve decision
  0016. `Scripts.txt` uses long Script names while `ScriptExtensions.txt`
  uses ISO short aliases; do not compare these raw strings. If the owner
  approves the proposed amendment, add and hash-pin
  `PropertyValueAliases.txt` and update A-46/source-manifest counts. Until
  then, keep the code path guarded and do not claim PL1101/C4 results.

**Acceptance:** hash verification log green; NormalizationTest 100%
pass; skeleton/bidiSkeleton outputs for the decision-0012 example pairs
(`aא1`/`a1א`, `Строкa`, `Δt`, `HTTPसर्वер`) **computed from the pinned
data and recorded** — decision 0012 forbids asserting Plain outcomes
for these pairs before the values are established.

### WP-3 — BUILD: lexer and layout engine

**Inputs:** `00-lexical-and-layout.md` L-01…L-27; WP-2 tables.

**Tasks:** UTF-8/BOM/CRLF handling; NFC identifier check with fix;
space-only indentation; comments incl. nesting and doc-comment
attachment; literals (L-13…L-18, incl. `Int` range check at compile
time); the single layout rule (blocks, dedent, L-22 continuations,
blank/comment lines, empty-block rejection, tail expressions,
non-`()` discard rejection); reserved words; confusable-declaration
detection (L-10) and the L-11 warning suite.

**Acceptance:** L- and identifier-area fixtures pass (WP-8); hostile
inputs (BOM, invalid UTF-8, tab indentation, non-NFC `é`, U+2028/29
outside literals, bidi controls) produce the exact registered codes.

### WP-4 — BUILD: parser and sugar

**Inputs:** grammar §6 (56 productions, audit-verified closed), the
closed precedence table, S-0…S-5.

**Tasks:** recursive-descent parser producing the full AST; non-
associative comparisons; `x.f(y)` rejection (L-29); desugaring printer
for S-1…S-4 (the compiler MUST print the desugared form); forbidden-
sugar diagnostics naming the canonical form (S-5).

**Acceptance:** every grammar production exercised by ≥1 fixture; each
sanctioned sugar has a desugaring-print assertion; each forbidden form
has a diagnostic fixture.

### WP-5 — BUILD: resolver and type checker

**Inputs:** `01-types.md` T-01…T-30; L-12 name roles; E-23…E-27
coverage rules.

**Tasks:** contextual name roles; structural records vs nominal closed
unions; `let`/`mut`/shadowing rules; generics with inline bounds;
interface coherence (orphan, uniqueness, no overlap, no specialization);
`alias` vs `distinct`; local rank-1 monomorphic inference with the
T-21…T-25 limits; derived/sealed `Eq`, `Ord`-requires-`Eq`, `Float`
neither; productive-recursion check (T-27); exhaustiveness and
unreachability over nested patterns and open domains; top-level
constant-only `let` (T-29); no implicit entry point (T-30).

**Acceptance:** all T-area fixtures pass, including the rejection
fixtures (orphan impl, duplicate impl, cross-`distinct` conversion,
higher-rank rejection, `impl Eq` rejection `PL0231`, recursive-record
`Eq` rejection, int-literal-as-`Float` error).

### WP-6 — BUILD: evaluator, faults, dual profiles

**Inputs:** `02-evaluation.md` E-01…E-36; the approved WP-1 decisions.

**Tasks:** implement strict left-to-right call-by-value evaluation;
pipe appends its value as the final argument; checked signed 64-bit
`Int` arithmetic; binary64 `Float` with the specified `Float.compare`
total order (not host equality/order); structural equality only where
specified; `Option`/`Result` and nearest-function `?`; block-local LIFO
`defer`; immutable snapshot closures; pattern matching; task-local
termination and deterministic fuel faults. No exceptions/null, host
I/O, wall-clock, network, or nondeterministic host behavior.

**Traps that MUST be tested:**
- Python integers are unbounded: explicitly range-check every `Int`
  operation, including `Int.min / -1`, division truncation toward zero,
  and remainder sign. Overflow is a runtime fault in **both** profiles.
- `Float` is not `Eq` or `Ord`; implement `Float.compare` explicitly
  for NaN and signed zero per E-09. Never rely on Python float comparison.
- A constant-folding optimization MUST NOT turn an E-05/E-30 runtime
  overflow into an L-18 literal diagnostic or a compile-time error.
- `defer` runs LIFO on normal block exit and on `?`; it is not promised
  on a fault. `?` is nearest-function and forbidden inside `defer`.
- Closures snapshot immutable bindings; no self-reference; mutable
  capture is rejected.
- Every evaluation and optimization pass must have deterministic fuel
  accounting and yield the same specified result/fault code.

**Acceptance:** E-area fixtures pass in both profiles with byte-for-byte
equivalent normalized results, including exact fault codes; adversarial
fuel tests are repeatable across runs.

### WP-7 — BUILD: diagnostics and source locations

**Inputs:** L-30…L-34; [`../plain/08-diagnostics-and-faults.md`](../plain/08-diagnostics-and-faults.md)
(the authoritative catalog: 71 active codes — 66 error/warning, 5 fault — plus
`PLFL06`–`PLFL08` reserved for later phases, and PL0106 historical); the derived
`diagnostic_registry` in `research/data/phase-01-document-audit.json`; all
errors/warnings surfaced by WP-3…WP-6. Fault codes use the `PLFL` namespace and
must not be catchable (T-12).

**Tasks:** implement source spans in the spec's coordinate convention,
caret lines, normalized diagnostic objects, safe quoting of bidi/control
characters, no-cascade behavior, terminology, and required fixes. Keep
emission deterministic. Extend `tools/audit_phase01.py` only if the
specification needs new mechanical checks; outputs stay generated.

**Acceptance:** each active diagnostic code has at least one fixture;
assert code, severity, span, and required fix presence; diagnostic
fixtures are included in both profiles. Historical PL0106 is not
required to be emitted unless a recorded spec change reactivates it.

### WP-8 — MEASURE: fixtures, runner, and coverage report

**Inputs:** [conformance plan](../plain/05-conformance-plan.md),
[rule traceability matrix](../plain/07-traceability.md), and
decision 0015. The planned budget is **341**, not a cap and not proof of
coverage. The matrix, not the budget, is what you close out: every one of the
106 rule IDs must end with a real fixture path beside it.

**Tasks:**
- Write fixtures at `conformance/<area>/<id>_<slug>.plain` and adjacent
  `.expected` files, with outcomes (value, exact fault code, or
  diagnostic object) and enough metadata to attribute coverage to rule
  IDs. Raw test inputs that cannot live inline go beside the suite with
  a README and license/provenance.
- Implement `plain test conformance/ --profile checked|optimized --report json`.
  Report per-rule pass/fail/uncovered and a machine-readable uncovered
  ID list. Fault assertions compare codes, not prose; diagnostics use
  normalized objects (code, severity, span, fix presence).
- Run every fixture under both profiles; execute the suite twice from a
  clean state and retain the JSON reports and exact commands/environment.
- Add generative/property tests where valuable (e.g. parser rejection,
  normalization idempotence, deterministic evaluation), with fixed
  seeds and saved minimized counterexamples. Property testing augments,
  never replaces, rule-attributed fixtures.
- Audit every normative rule against fixtures. If a rule is deliberately
  outside A-42, list it as excluded with the later phase/gate that owns
  it; do not silently count it as covered.

**Acceptance:** all in-scope normative rules have ≥1 fixture; uncovered
list empty; all fixture targets accounted for or deviations justified
by evidence and recorded; checked/optimized normalized results agree;
reproduction command and reports checked into the repo.

### WP-9 — MEASURE: semantics cross-check and promotion review

**Inputs:** [operational semantics](../plain/06-operational-semantics.md),
which is currently draft/non-normative; WP-3…WP-8; research Appendix A.

**Tasks:** independently compare executable behavior against the
operational semantics and the prose rules. Treat the interpreter as an
implementation, **not** as self-authenticating truth. Select properties
whose statements are independently reviewed (e.g. determinism on
well-typed closed terms, normalization idempotence, profile parity),
then run fixed-seed randomized testing and preserve failures plus
minimized cases. Review whether the semantics is precise enough to
promote; do not silently make it normative, and do not use the same
implementation to generate both expected results and pass verdicts.
Record mismatches as experiments (including negative results), file
ambiguities for underspecified behavior, and change rules only under the
freeze policy. If unresolved discrepancies can affect a Gate 1 exit
criterion, the gate cannot pass.

**Acceptance:** experiment records use
[`templates/experiment-record.md`](./templates/experiment-record.md),
with hypothesis, confirmation/retraction criteria, raw data, and
reproduction commands; semantics promotion is an explicit, reviewed
decision or is deferred with a named owner and reason.

### WP-10 — GATE: review packet, tracker, and final audit

**Preconditions:** C1/C5 recorded; C2 recorded; all required A-* items
ratified or revised and reflected in the spec; build and conformance
acceptance satisfied; no unresolved Gate 1-blocking discrepancy.

**Tasks:**
1. Create `docs/gates/gate-01.md` from
   [`templates/gate-review.md`](./templates/gate-review.md). Copy the
   three Gate 1 exit criteria from §1 **verbatim**; attach evidence links
   to each checked item. State the decision-0010 scope and excluded
   later-phase obligations explicitly.
2. Include both profile reports, the uncovered list, fixture-to-rule
   matrix, diagnostic-code coverage, Unicode verification and
   normalization logs, fixed-seed experiment results, independent
   reviewer identity, claims audit (confirmed/retracted/open), and
   stopping-condition check. The implementer cannot be the only reviewer.
3. Update `PHASE-TRACKER.md`, `docs/evidence-register.md`,
   `docs/plain/README.md`, and `README.md` in the **same commit** as the
   gate review. Record version changes and reasons; keep one canonical
   spec. Do not edit the two controlled founding prompt docs except
   with their prescribed version bump and `IMPROVEMENTS.md` entry.
4. Run `python3 tools/audit_phase01.py --check`; fix discrepancies at
   their source, regenerate outputs via the tool, rerun, and record the
   exact command and result. Add tests to the audit tool only where the
   existing checks fail to enforce a documented invariant.
5. State exactly one result: **"Plain core passed Gate 1"**,
   **"Plain core passed Gate 1 with conditions"**, or **"Plain core did
   not pass Gate 1"**. A failed or blocked gate is a valid result and
   must not be relabeled as a pass.

**Acceptance:** a reviewer who did not implement the core can reproduce
the result from the repository and supplied commands; all linked
artifacts are committed; no platform-level claim is inferred from a
core-only pass.

### WP-11 — STOP / research-only fallback

If C1 or C5 is absent, **do not write implementation code, fixtures,
Unicode tables, or adopt PlainP code**. Do only work that can resolve
those blockers without committing to a build: obtain owner decisions
through the readiness packet, clarify the exact PlainP ruling, compare
implementation-language options, maintain external-source research,
and write decision/experiment drafts clearly marked **Proposed**. Do
not invent owner sign-off or use a draft decision as authorization.

If blocked only on C2 or A-* ratification, code may be built only after
C1/C5 and only against the currently proposed spec; label all results
provisional. Do not create or claim a Gate 1 pass. Avoid irreversible
vendor or release actions until C4 is settled.

---

## 6. Recording map

| Artifact | Canonical location / rule |
|---|---|
| Research notes and source grades | `research/phase-01-06-*.md`; index in `research/README.md`; use E/P/H labels and source grades from Master Prompt §2 |
| Decision records 0013–0015 | `docs/decisions/`; copy `templates/decision-record.md`; record alternatives, evidence, consequences, reversibility, and review date |
| Experiments | `research/experiments/`; copy `templates/experiment-record.md`; raw data beside experiment README; every hypothesis copied from the evidence register |
| Implementation | `src/plain/` or a layout justified by decision 0013; standard library only unless a reviewed decision and license permit otherwise |
| Generated Unicode tables/cache | Under a gitignored data/cache location; pin commit and manifest; do not commit source data before C4 review |
| Conformance suite | `conformance/<area>/<id>_<slug>.plain` and `.expected`; fixture README describes format and provenance |
| Rule→fixture traceability | [`../plain/07-traceability.md`](../plain/07-traceability.md); update the row for a rule **in the same commit** as its first fixture |
| Runner reports/raw results | `research/data/phase-01-...`; commit compact reproducible outputs, not redundant or huge generated artifacts |
| Gate review | `docs/gates/gate-01.md`, derived from gate-review template |
| Norm/evidence/status updates | Update rule + ambiguity record together; evidence register + tracker + relevant README in same gate-result commit |
| Audit | `python3 tools/audit_phase01.py --check`; do not hand-edit `phase-01-document-audit.json` |

Paths are proposals until decision 0013; adjust once, record why, and
update this table before implementation proliferates.

---

## 7. Stop conditions and change control

Stop the affected work package and record the issue if any of these
occurs:

- C1/C5 absent or revoked; proposed resolutions cannot be treated as
  owner approval.
- A required Gate 1 ambiguity changes the language's observable
  behavior and lacks a ratified resolution.
- Unicode blob hash, byte count, or source-manifest commit does not
  match; no fallback to host Unicode libraries.
- A rule cannot be implemented without contradicting another rule, or
  two profiles disagree on a specified result/fault.
- A security property in L-08…L-11 cannot be tested from the pinned
  source data; do not weaken it to make fixtures pass.
- The operational model and prose disagree on an in-scope behavior and
  a reviewed decision cannot resolve it.
- A new dependency, host capability, language feature, platform
  obligation, or performance target is proposed: out of scope unless a
  decision and the proper phase/gate explicitly authorize it.
- Research finds a materially better existing solution or invalidates
  the project's core premise: invoke Master Prompt Phase 14; do not
  keep building to defend sunk cost.

Record blocker, evidence, affected rules, safe next action, and whether
other work packages can continue. No silent scope changes. Apply
version/change rules in `docs/plain/README.md` and the directory guide.

---

## 8. Operational semantics and language invariants checklist

Before closing WP-6/WP-8, explicitly review these rules against the
source and fixtures; this list is an index, **not a replacement for the
spec**:

- Strict CBV, left-to-right; pipe adds the piped value as final argument.
- Checked signed 64-bit `Int`; overflow faults in all profiles. `Float`
  is binary64, has no `Eq`/`Ord`, and has a dedicated total comparison.
- Structural records with at least one field; nominal closed unions
  with at most one payload; `Option`/`Result`, no null/exceptions.
- `?` returns through nearest function, forbidden in `defer`; block-local
  `defer` is LIFO and is not guaranteed on a fault.
- Immutable closures capture snapshots; rank-1 monomorphic local
  inference; constants only at top level; no `main` keyword/implicit
  entry point (T-29/T-30).
- Spaces-only indentation; enforce sugar S-0…S-4 and reject S-5.
- Pattern exhaustiveness/reachability; no invented support for the 20
  deferred D-01…D-20 features.
- Exact Unicode profile and source pins; implement normalization and
  security behavior only from the manifest-backed Unicode 17 data.
- Deterministic fuel-based faults; both profiles must agree including
  fault codes; no benchmark or speed claim.

Any conflict with the rule documents is a stop-and-record issue, not an
invitation to reinterpret the spec.

---

## 9. Definition of done

This prompt's execution is complete only when one of these is true:

1. **Gate 1 reviewed:** all preconditions in WP-10 are met, an
   independent reviewer has signed a reproducible `gate-01.md`, and the
   result has been recorded as pass, conditional pass, or did-not-pass;
   or
2. **Work stopped honestly:** a blocker or stop condition is documented
   with evidence and next action, the tracker accurately says blocked
   or stopped, and no Gate 1 pass or platform capability is claimed.

**Not authorized by this prompt:** Phase 2 reactive runtime; Phase 3
production Rust runtime or supervisor; Phase 4 isolation; Phase 5 real
capabilities; Phase 7 text shaping/segmentation; Phase 9 durable I/O;
third-party code/data adoption without license/provenance review; a
public release; performance comparisons; or a claim that ZEMA is
"world's first." The Python oracle is a Phase 1 verification vehicle,
not a change to the Phase 3 production-runtime decision.

---

## Appendix A — Research notes for the executor

These sources informed the work order; they are methodological models,
not evidence that Plain is correct or that ZEMA is better than existing
systems. Recheck versions and applicability before relying on them.

| Source | Finding applied | Limitation / guardrail |
|---|---|---|
| [TC39 Test262](https://github.com/tc39/test262) | Feature-tagged, per-test fixtures and several independent runners are a useful model for mapping tests to rules and validating runner portability | A large suite does not prove completeness; use explicit per-rule coverage and do not claim full language conformance beyond scoped rules |
| [SpecTec / Watt et al.](https://conrad-watt.github.io/papers/youn2024.pdf) | Executable semantics can act as an oracle and validate against an independent official suite; reported work found specification bugs | ZEMA has no independent official suite yet; do not treat the interpreter as its own oracle; use independently reviewed properties and reviewers |
| [WebAssembly mechanization and differential testing](https://www.cl.cam.ac.uk/~caw77/papers/mechanising-and-verifying-the-webassembly-specification.pdf) | Differential testing and mechanized semantics can expose mismatches | No proof claim transfers to Plain; a future independent implementation is needed for true cross-implementation differential tests |
| [PLT Redex](https://redex.racket-lang.org/) | Randomized falsification of semantics properties can complement directed examples | Oracle correctness is itself a risk; fixed seeds, saved counterexamples, independent property statements, and fixtures are mandatory |
| [Crafting Interpreters](https://craftinginterpreters.com/) | Scanner → parser → resolver → interpreter is a practical staged tree-walk architecture; a later VM can be compared against a simpler oracle | Architecture inspiration only; no code or license assumptions transferred |
| [Python 3.11 `unicodedata`](https://docs.python.org/3.11/library/unicodedata.html) | Confirms Python 3.11 uses UCD 14.0.0 | Explicitly disqualifies it as a source for the pinned Unicode 17.0.0 profile |
| [Unicode 17.0.0 release](https://www.unicode.org/versions/Unicode17.0.0/) | Version/date baseline: Unicode 17.0.0 released 2025-09-09; UAX #31 rev43 and versioned security data | Sandbox cannot reach unicode.org; use manifest-pinned GitHub mirror and verify hashes |
| [UTS #39 rev32](https://www.unicode.org/reports/tr39/tr39-32.html) and [UTS #55](https://www.unicode.org/reports/tr55/) | Identifier security, skeletons, bidi-aware checks, and identifier-type guidance that decisions 0011/0012 map into the draft | Implement the exact pinned revisions; do not simplify or claim compliance without its prescribed data and tests |
| [Solid signals package](https://www.npmjs.com/package/@solidjs/signals) and [Svelte 5 runes](https://svelte.dev/docs/svelte/$state) | Potential reference material for the explicitly deferred Phase 2 reactive research | Not a Phase 1 dependency or authorization; research later under Phase 2, not here |

**Research conclusion:** the immediate high-risk unknowns are not whether
a tree-walk interpreter can be written; they are authorization (C1/C5),
faithful implementation of the 47-ambiguity draft (especially Unicode and
numeric edge cases), an independently trustworthy conformance oracle,
and precise owner/reviewer ratification. The correct next action is
therefore WP-0, followed by WP-1 decisions—not immediate coding.

---

## Appendix B — External source references

- Unicode UAX #15, Unicode Normalization Forms: <https://www.unicode.org/reports/tr15/>
- Unicode UAX #31, Unicode Identifiers and Syntax: <https://www.unicode.org/reports/tr31/>
- Unicode UAX #9, Unicode Bidirectional Algorithm: <https://www.unicode.org/reports/tr9/>
- UTS #39, Unicode Security Mechanisms: <https://www.unicode.org/reports/tr39/tr39-32.html>
- UTS #55, Unicode Source Code Handling: <https://www.unicode.org/reports/tr55/>
- Pinned data repository: <https://github.com/unicode-org/unicodetools/tree/3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c>
- All live findings checked 2026-11-03; refer to `research/data/phase-01-source-manifest.json` for the definitive per-file URL, hash, byte count, and pinned commit.
