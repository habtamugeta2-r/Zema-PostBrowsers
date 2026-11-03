# Decision Record 0013 — Phase 1 Reference Interpreter Vehicle and Architecture

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — owner/reviewer acceptance not recorded; build may use this as the current working proposal only |
| **Evidence label** | Established for environment facts; Proposed for the selected architecture |
| **Deciders** | ZEMA research agent; owner Better-back has not ratified this decision |

## Context

C1 and C5 were resolved by Better-back on 2026-11-03, authorizing Phase 1 build work. Gate 1 evaluates the hermetic Plain core; the production runtime choice belongs to Phase 3. The current sandbox has Python 3.11.2 and Node v22.22.3 but no Rust toolchain. Python's built-in Unicode database is version 14.0.0, while Plain's proposed input lock is Unicode 17.0.0. C2 and the listed A-* ratifications remain outstanding, so any build result is provisional and Gate 1 is not yet eligible.

## Options considered

### Option A — Reuse: third-party parser/interpreter framework

- **What it is, who maintains it, license:** A mature host-language parsing or interpretation package selected after a package-by-package audit; none selected or adopted by this record.
- **Security cost / attack surface:** Adds transitive dependencies and implementation behavior outside the repository's control; package/license/provenance and parser behavior require review.
- **Performance cost:** Not measured; no performance comparison is relevant to Gate 1.
- **Fit for ZEMA's defined app class:** Could accelerate scaffolding, but its type/evaluation semantics may conflict with Plain's draft and could obscure behavior under test.

### Option B — Build on existing foundations: Python 3.11 standard-library reference interpreter

- **What it is, who maintains it, license:** Use Python as implementation language, but write the Plain lexer/parser/type checker/evaluator and data pipeline in this repository using only the Python standard library. Python is maintained by the Python Software Foundation community; the interpreter itself remains project code.
- **Security cost / attack surface:** Avoids third-party runtime dependencies, but host semantics must be contained: Python integers are unbounded, float behavior differs from Plain's laws, recursion/GC are host mechanisms, and Unicode 14 APIs must not implement Unicode 17 rules.
- **Performance cost:** Not measured; no speed target or claim is made at Gate 1.
- **Fit for ZEMA's defined app class:** Buildable and testable in the current sandbox; can serve as a simple oracle for a later Rust implementation without selecting Phase 3's runtime.

### Option C — Invent: implement a custom VM/compiler immediately

- **What it is, who maintains it, license:** A new bytecode VM and execution/compiler stack written in a language available here.
- **Security cost / attack surface:** More new machinery before the language semantics are validated; separate optimizer/VM correctness obligation.
- **Performance cost:** Not measured; inventing a VM has no Gate 1 evidence of benefit.
- **Fit for ZEMA's defined app class:** Unnecessary to demonstrate the hermetic core and would enlarge the initial semantic/debugging surface. No evidence shows the existing staged interpreter approach is inadequate.

## Decision

**Proposed selection: Option B.** Implement a standard-library-only Python 3.11 reference interpreter for Phase 1. Keep it distinct from the Phase 3 production-runtime decision. Use generated tables from the pinned Unicode 17.0.0 files for all locked Unicode operations; never use Python's Unicode 14.0.0 properties or normalization for normative behavior. The checked profile will evaluate a typed AST; the optimized profile will execute a separately lowered instruction representation. Both must preserve exact observable values, diagnostics, and fault codes, including deterministic fuel behavior. This proposal is not owner-ratified and is not evidence of correctness or conformance.

## Consequences

- **Positive:** Build is feasible in the verified sandbox; no package installation or third-party code adoption is required; a simple implementation can later act as a parity target.
- **Negative / accepted costs:** Two execution paths create a parity obligation; Python host behavior must be explicitly fenced; no performance claim follows.
- **New obligations created:** Test Python integer boundaries, Float total ordering, fuel determinism, and all profile parity; use the manifest-pinned Unicode table pipeline; review any added dependencies/license before adoption.
- **What would make us revisit this decision:** A verified Rust toolchain; inability to meet a normative requirement in Python; a materially safer/clearer alternative supported by experiments; or owner/reviewer direction.

## Evidence

- Citations: Python 3.11 `unicodedata` documentation, https://docs.python.org/3.11/library/unicodedata.html (UCD 14.0.0); project environment checks dated 2026-11-03.
- Experiments: none yet — implementation and performance are untested.
- Related records: research [`phase-01-06-implementation-feasibility.md`](../../research/phase-01-06-implementation-feasibility.md); decisions 0009–0012; conformance plan `docs/plain/05-conformance-plan.md`.
