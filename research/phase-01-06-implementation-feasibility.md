# Phase 1 Research 06 — Implementation Vehicle and Build Feasibility

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 preparation |
| **Status** | **Proposed** — research/decision support only; no language implementation or conformance result is claimed here |
| **Evidence label** | Established for the cited repository/environment facts and primary-source findings; Proposed for recommendations |
| **Author** | ZEMA research agent on behalf of Better-back |

## Question

What can be implemented and validated in this checkout without violating the frozen Phase 1 scope, the Unicode 17.0.0 input lock, license/provenance rules, or current environment constraints? Which execution architecture could provide meaningfully independent checked and optimized profiles?

## Findings

1. **Established — build authorization.** Better-back recorded C1 sign-off and ruled PlainP a donor only on 2026-11-03 through Arena owner responses. The responses are transcribed in `docs/gates/gate-00.md` §9 and `docs/gates/gate-01-readiness.md` §2. This clears C1/C5 for Phase 1 build work; it does not resolve C2, C3/C4, ratify A-27/A-38/A-42/A-44/A-45/A-46/A-47, or authorize Gate 1.
2. **Established — environment.** Python 3.11.2 and Node v22.22.3 are available; Rust/Cargo are absent. Python's `unicodedata` is UCD 14.0.0, so it cannot supply the locked Unicode 17.0.0 normalization or identifier properties. The audit tool passes and reports 100 normative L/T/E rules, 47 ambiguities (42 resolved-proposed, 5 deferred), 20 deferrals, 307 planned fixtures, 56 grammar productions, and 58 manifest sources including 16 Unicode data/test inputs. Source: direct environment checks and `tools/audit_phase01.py --check` on 2026-11-03.
3. **Established — suite design prior art.** Test262 uses feature metadata and a large per-test suite; this supports explicit rule-to-fixture traceability, not a claim that a finite suite proves completeness [S1].
4. **Established — semantics validation prior art.** SpecTec/Wasm research demonstrates executable semantics can be checked against an independently maintained official test suite and can expose specification defects [S2]. ZEMA has no equivalent independent official Plain suite, so an interpreter cannot authenticate itself; use reviewed properties, independent fixture expectations where possible, and a reviewer who did not implement it.
5. **Established — oracle architecture prior art.** A staged scanner/parser/resolver/interpreter architecture is a practical implementation teaching pattern [S3]. It informs decomposition only; no implementation code is adopted.
6. **Proposed — vehicle.** Use Python 3.11 standard library for a reference interpreter and data tooling. It is executable in this sandbox and supports explicit integer/fault semantics, but host Unicode APIs must be excluded from locked Unicode behavior. Reconsider this choice if a reproducible Rust toolchain becomes available or if a concrete requirement cannot be met in Python.
7. **Proposed — differential profiles.** Use checked AST evaluation as the simple reference path and a separately lowered instruction representation with its own evaluator for optimized mode. Keep the same typed AST, observable diagnostics, fault codes, and fuel semantics. Profile parity is still an obligation, not a result.
8. **Established — Unicode source access.** The manifest pins the 16 Unicode 17 files to `unicode-org/unicodetools` commit `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c`; a GitHub API blob and commit were reachable (HTTP 200). The sandbox cannot fetch from `unicode.org`. The input bytes must be fetched from the pinned GitHub blobs and validated against git blob SHA-1, manifest byte count, and SHA-256 before use.
9. **Established — initial Unicode pipeline result.** `tools/fetch_unicode17.py` fetched all 16 pinned inputs through GitHub's API, verified each Git blob SHA-1, manifest byte length, and SHA-256, and wrote only to the ignored cache; the compact verification log is `research/data/phase-01-unicode-verification.json`. The project-owned normalizer in `src/plain/unicode17.py` (no `unicodedata` import) passed all 20,034 rows / 200,340 NFC+NFD assertions in the pinned NormalizationTest corpus, zero failures; see experiment EN-unicode17-normalization and its raw report. This establishes the result for that corpus only, not full Unicode correctness.
10. **Proposed — next sequence.** Generate remaining properties and implement bidi/skeleton/security algorithms; continue language stages in conformance-plan order. Keep all build outputs provisional while C2 and A-* ratifications remain unresolved; no Gate 1 attempt until those are recorded.

## Options and cost notes

| Option | Fit / cost | Disposition |
|---|---|---|
| Reuse a third-party parser/interpreter framework | Could reduce parser/evaluator work, but adds dependency, license, and provenance review; dependency semantics may not match the draft. No benchmark or compatibility experiment exists. | Not selected for the initial oracle; revisit only with a decision and license review. |
| Build a custom reference interpreter in Python stdlib | Available now; no new runtime dependency; host integer behavior must be constrained and Unicode tables generated explicitly. More implementation burden; no speed claim. | Proposed. |
| Use Node/TypeScript | Available runtime; JavaScript numeric behavior and a second toolchain/package ecosystem increase semantic adaptation and dependency review. No comparative experiment exists. | Retained alternative, not selected. |
| Wait for Rust / implement production runtime immediately | Rust toolchain absent and rustup host is outside sandbox allowlist; production runtime is Phase 3, not Gate 1. | Not feasible in this environment; production port remains later work. |

## Open risks / unresolved authorizations

- **C2** book import or retirement authorization is outstanding and required before Gate 1.
- **A-27/A-38/A-42/A-44/A-45/A-46/A-47** remain proposed; build can proceed on the draft but final Gate 1 cannot.
- No C4 license decision is recorded. Do not commit or adopt third-party source data/code; default to a gitignored cache and include license/provenance review before any future vendoring.
- No Plain lexer/parser/typechecker/evaluator, language fixtures, Unicode bidi/skeleton/security implementation, dual-profile parity result, or full conformance run exists yet.

## Sources

- **[S1]** TC39 Test262, official project repository, https://github.com/tc39/test262 — grade A for project structure/practice; accessed 2026-11-03.
- **[S2]** Andreas Rossberg et al., SpecTec / executable WebAssembly semantics, https://conrad-watt.github.io/papers/youn2024.pdf — grade B (academic paper); accessed 2026-11-03.
- **[S3]** Robert Nystrom, *Crafting Interpreters*, https://craftinginterpreters.com/ — grade B (technical book); accessed 2026-11-03.
- Python 3.11 `unicodedata` documentation, https://docs.python.org/3.11/library/unicodedata.html — grade A; accessed 2026-11-03.
- PLT Redex, https://redex.racket-lang.org/ — grade A for tool documentation; accessed 2026-11-03.
- Project records: `docs/gates/gate-00.md`, `docs/gates/gate-01-readiness.md`, `docs/plain/05-conformance-plan.md`, and `research/data/phase-01-source-manifest.json` — grade A.

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Initial feasibility research after C1/C5 owner responses. Recommendations remain Proposed; no full-language implementation or conformance result claimed. |
| 2026-11-03 | Added verified Unicode 17 fetch/cache and full NormalizationTest corpus result; remaining Unicode security algorithms and Plain implementation are still outstanding. |
