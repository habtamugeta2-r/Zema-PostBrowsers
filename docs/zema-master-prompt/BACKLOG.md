# BACKLOG — the queue the loop reads

| Field | Detail |
|---|---|
| **Document** | The ordered work queue for the autonomous loop |
| **Version** | 1.0.0 |
| **Date** | 2026-11-04 |
| **Status** | Active. The agent may reorder rows; it may not weaken a `Done when` |
| **Read with** | [`AUTONOMOUS-LOOP.md`](./AUTONOMOUS-LOOP.md) (the procedure) and [`PHASE-01-EXECUTION-PROMPT.md`](./PHASE-01-EXECUTION-PROMPT.md) (the authority) |

> **This file is the prompt.** Each row is a self-contained instruction with a
> test that says whether it finished. `continue` takes the first `ready` row
> whose `Blocked by` is satisfied. Nothing else is needed from the owner.

**Status vocabulary:** `ready` · `doing` · `done` · `blocked: owner` ·
`blocked: dep`

---

## A. Owner decisions — the loop cannot start these, but they unblock the most

| # | Item | Done when | Blocked by | Status |
|---|---|---|---|---|
| A1 | Owner ratifies, revises, or rejects the 20 proposed identifiers | `08-diagnostics-and-faults.md` §9 items 1–6 all answered with a dated owner response | owner | **blocked: owner** |
| A2 | Owner decides the gate vocabulary: `Prompt Gate` or `Phase Gate` | One term chosen; a decision record states it | owner | **blocked: owner** |
| A3 | Owner decides whether VT-1…VT-3 enter the gate-review template | Template either amended with a version bump, or the proposal withdrawn | owner | **blocked: owner** |
| A4 | Owner answers C2 — book imported or references retired | `gate-01-readiness.md` §2 shows C2 recorded | owner | **blocked: owner** |
| A5 | Owner states the license (C4) | A license decision record exists | owner | **blocked: owner** |

> **Why these are first.** A1 gates 20 identifiers that every future fixture
> will cite. A2 gates the mechanical rename of 365 references. A3 gates the
> vertical trace becoming enforced rather than documented. None can be done by
> an agent without breaking "silence is not approval."

## B. Verification work — no owner input needed

| # | Item | Done when | Blocked by | Status |
|---|---|---|---|---|
| B1 | Audit the 38 "needs no code" classifications in `08-diagnostics-and-faults.md` §6 against the rule text | Each of the 38 has a `rejection` / `constraint` / `behaviour` verdict recorded in a table, and any misclassification is corrected | — | **done** |
| B2 | Verify the 23 conformance areas actually cover the 50 gate exit criteria | A table maps each of the 50 criteria to ≥1 area or records it as uncovered; uncovered count reported | — | **ready** |
| B3 | Check the 66 research + 62 build tasks for completion against the repo | Each task marked done / not-done with a file citation; the not-done list is the real remaining scope | — | **ready** |
| B4 | Verify every `E` evidence row's cited source actually says what the row claims | A sample of 20 rows re-read against their sources; disagreements corrected with dated notes | — | **ready** |
| B5 | Check the 47 ambiguities for any silently resolved without a decision record | Every `resolved` ambiguity cites a decision; missing ones listed | — | **ready** |

## C. Definition work — no owner input needed

| # | Item | Done when | Blocked by | Status |
|---|---|---|---|---|
| C1 | Define the diagnostic fixture format before any fixture is written | A spec in `docs/plain/` fixes the `.expected` schema, provenance metadata, and how a fixture names its rule ID | — | **ready** |
| C2 | Define the runner contract from decision 0015 as an executable skeleton | `plain test --profile checked --report json` runs against an empty suite and emits a valid report with an uncovered list | — | **ready** |
| C3 | Define the "checked" vs "optimized" profile difference concretely | Decision 0015 gains an exact description of the two execution paths; a flag that changes nothing is explicitly forbidden | — | **ready** |
| C4 | Specify the prelude inventory policy | Every currently-used prelude name traces to a rule ID; untraced names listed as a defect | — | **ready** |

## D. Build work — only after C2 and A1

| # | Item | Done when | Blocked by | Status |
|---|---|---|---|---|
| D1 | Lexer: encoding, NFC, tabs, comments, literals | Fixtures for L-01…L-07 pass; every code raised is one of `PL0001`, `PL0101`–`PL0126` | C2, A1 | **blocked: dep** |
| D2 | Layout engine: indentation, dedent, continuation | L-19…L-27 fixtures pass including both L-22 causes | D1 | **blocked: dep** |
| D3 | Parser and sugar | Every grammar production has a fixture; S-0…S-5 desugarings asserted | D2 | **blocked: dep** |
| D4 | Type checker | T-01…T-30 fixtures pass | D3 | **blocked: dep** |
| D5 | Evaluator with faults and dual profiles | E-01…E-36 pass; `PLFL01`–`PLFL05` asserted by code, not message | D4 | **blocked: dep** |

## E. Housekeeping — safe at any time, low value

| # | Item | Done when | Blocked by | Status |
|---|---|---|---|---|
| E1 | Mechanically disambiguate the 365 bare `Gate N` references | Zero bare references in the 0–5 range; audit check prevents new ones | A2 | **blocked: owner** |
| E2 | Add `[E]`/`[P]` labels to the 100 normative rules | Every rule carries a label; a check enforces it | owner decision on granularity | **blocked: owner** |
| E3 | Make the gate-review template warn about all 8 stopping conditions | Template §"Stopping-condition check" lists all 8 | A3 | **blocked: owner** |

---

## Selection trace — why the queue is in this order

| Phase | Rows | Reasoning |
|---|---|---|
| 1st | B1–B5 | They are verification of claims the project already makes. They need no owner input, they are cheap, and a wrong claim found now is cheaper than after fixtures cite it |
| 2nd | C1–C4 | They are prerequisites for D. Writing a fixture before the fixture format exists would produce 356 fixtures in the wrong shape |
| 3rd | D1–D5 | The build. Large, and gated behind A1 because every fixture cites an identifier |
| Never without the owner | A1–A5, E1–E3 | Each needs a decision the agent may not make |

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-04 | 1.0.0 | Created: 5 owner rows, 5 verification rows, 4 definition rows, 5 build rows, 3 housekeeping rows. B1–B5 and C1–C4 are `ready`. |
