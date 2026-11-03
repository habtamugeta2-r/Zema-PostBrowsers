# Decision Record 0015 — Conformance Runner and Dual Execution Profiles

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — owner/reviewer acceptance not recorded; runner and profiles not implemented |
| **Owner ratification** | **pending** — see [`README.md`](./README.md) for the status vocabulary |
| **Evidence label** | Established for the existing conformance-plan requirements; Proposed for runner design |
| **Deciders** | ZEMA research agent; owner Better-back has not ratified this decision |

## Context

`docs/plain/05-conformance-plan.md` defined a 307-fixture planning budget at the time of this record (now 341 after the 2026-11-03 traceability repair; see [`../../research/phase-01-07-process-gap-audit.md`](../../research/phase-01-07-process-gap-audit.md)), rule-attributed fixtures, the command `plain test conformance/ --profile checked|optimized --report json`, an empty in-scope uncovered list, exact fault-code assertions, normalized diagnostic assertions, and checked/optimized parity. Gate 1 cannot pass when any in-scope rule is uncovered. The draft also requires actual profile equivalence, not merely a flag that selects the same path.

## Options considered

### Option A — Reuse: an existing generic test framework without a Plain adapter contract

- **What it is, who maintains it, license:** A generic unit-test/discovery framework installed as a dependency; none selected.
- **Security cost / attack surface:** Adds dependency and license/provenance review; generic discovery does not automatically prove rule attribution or completeness.
- **Performance cost:** Not measured; not a Gate 1 criterion.
- **Fit for ZEMA's defined app class:** Could support reporting, but would require a custom adapter and careful controls to keep the report schema and fixture semantics stable.

### Option B — Build on existing foundations: project-owned standard-library fixture runner

- **What it is, who maintains it, license:** A small runner in the Python standard library. Discover `.plain` fixtures and adjacent `.expected` data, run profiles, and emit deterministic JSON with per-rule pass/fail/uncovered results.
- **Security cost / attack surface:** Avoids plugin loading and third-party runner code; fixture parsing and expected-value comparison remain project code requiring tests.
- **Performance cost:** Not measured; no benchmark requirement for this gate.
- **Fit for ZEMA's defined app class:** Directly represents the project's rule IDs, exact diagnostic/fault outcomes, and hermetic constraints.

### Option C — Invent: two independent implementations from the start

- **What it is, who maintains it, license:** Build an AST interpreter and a separate compiler/VM implementation with independently written front ends.
- **Security cost / attack surface:** Independent implementations reduce shared-code risk but multiply unreviewed implementation surface and delay core coverage.
- **Performance cost:** Not measured.
- **Fit for ZEMA's defined app class:** Valuable as future differential validation, but disproportionate for an initial Gate 1 oracle; no second implementation currently exists.

## Decision

**Proposed selection: Option B.** Build a project-owned standard-library runner using rule IDs declared in fixture metadata or an equivalent auditable mapping. A fixture has a `.plain` source file, adjacent `.expected` data, one or more rule IDs, and an explicit outcome class (value, exact fault code, diagnostic object, or desugared output). The JSON report records commands/profile, fixture totals, per-rule outcomes, uncovered IDs, and profile differences. The checked profile evaluates typed AST nodes. The optimized profile lowers the same typed AST to an instruction form and runs a separate instruction evaluator; any optimizer must preserve specified errors, fuel, and observable behavior. A mere configuration flag is not a distinct profile. Do not claim independent implementation validation: both paths share the front end and type checker.

## Consequences

- **Positive:** The suite is directly traceable to the specification and detects missing coverage; report output is reproducible and machine-readable.
- **Negative / accepted costs:** The instruction evaluator introduces a parity obligation and is not fully independent of the AST front end; a custom runner itself needs tests and review.
- **New obligations created:** Each normative in-scope rule must map to at least one fixture; every active diagnostic code must be tested; report must name all uncovered rules; execute from clean state under both profiles; retain raw reports and exact commands.
- **What would make us revisit this decision:** The fixture contract becomes unmaintainable, the JSON schema cannot capture the spec's outcomes, or a separate independent reference implementation becomes feasible and meaningfully improves validation.

## Evidence

- Citations: `docs/plain/05-conformance-plan.md` §§1–6 and `docs/zema-master-prompt/templates/experiment-record.md` / `gate-review.md`.
- Experiments: none yet — runner, fixture format, and profile parity are not implemented or measured.
- Related records: decision 0010 (Gate 1 scope); research `phase-01-06-implementation-feasibility.md`.
