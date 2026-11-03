# AMBIGUITY-DECISION-AUDIT — does every `resolved` ambiguity have an author?

| Field | Detail |
|---|---|
| **Document** | Ambiguity-resolution audit: whether each `Resolved` row traces to a recorded decision |
| **Version** | 1.0.0 |
| **Date** | 2026-11-04 |
| **Status** | Active. Produced by backlog item **B5** |
| **Machine check** | `ambiguity_decision_check()` — counts recorded vs unrecorded rows and deferral leaks; reported by `--check`. Informational, not gating: the defect is historical and the repair is an owner decision (§5) |
| **Scope** | All 47 ambiguity rows; the 42 `Resolved` ones in full |

> **The question B5 asks.** "Check the 47 ambiguities for any silently resolved
> without a decision record." The register answers a *different* question well:
> it says whether a resolution is written down. It never says who chose it. All
> 42 resolved rows pass the written-down test — each cites rule IDs that exist.
> **35 of them have no decision record behind them**, and the 7 that do are
> exactly the 7 the owner has been asked about.

---

## 1. The measured split

| | Rows |
|---|---:|
| Ambiguity rows | 47 |
| `Resolved` (any flavour) | **42** |
| …with a decision record naming the A-ID in its **Resolves** field | **7** |
| …with no route to any decision record | **35** |
| `Deferred` (with a `D-##` trigger) | 5 |

The 7 recorded rows are `A-27, A-38, A-42, A-44, A-45, A-46, A-47` — declared by
decisions 0009–0012. The 35 unrecorded rows carry the statuses `Resolved` (32),
`Resolved (partial)` (2), `Resolved (risk accepted)` (1).

### 1.1 The status word is correlated with the gap, exactly

| Status | Rows | Recorded |
|---|---:|---:|
| `Resolved (proposed)` | 7 | **7** |
| `Resolved` | 32 | **0** |
| `Resolved (partial)` | 2 | **0** |
| `Resolved (risk accepted)` | 1 | **0** |

This correlation is perfect and is not a coincidence. `Resolved (proposed)` was
introduced *by the decision records* — it marks a row a decision made. Plain
`Resolved` marks a row the **specification draft** made, and it never got a
record.

That gives the gap a precise meaning: **32 rows claim to be settled, in a status
word that no decision record can produce.**

### 1.2 The seven "silently resolved" rows are the only ones with an audience

The gate-1 readiness packet puts exactly 7 A-IDs to the owner
(`gate-01-readiness.md` §1). They are the 7 recorded rows. **All 35 unrecorded
rows have never been put to the owner at all** — the owner cannot ratify a
question that was never asked, and the readiness packet is the only channel
that asks.

The owner's recorded response to that packet was **Revise** for all seven,
without naming which or with what wording — so the seven are *asked and
unsettled*, and the 35 are *unasked*. Nothing in the register's summary
distinguishes those two states.

## 2. The 24 that are decided somewhere — they just do not say so

A decision record does not have to name an A-ID to have decided it. Reading the
11 `Decision` sections against the 35 found **24 rows whose answer is stated
verbatim in a decision record**, most of them decision 0008 §2 ("Adopt Plain
draft v0.2 corrections") or the corresponding bullet in decisions 0005/0006.

Every row below carries a **verbatim quote from the record's Decision section**.
A test re-verifies each quote against the file, so this table cannot rot.

| Row | Decision | Strength | The record's own words |
|---|---|---|---|
| A-03 | 0005 | decides | "A product is a record; positional payloads are rejected (T-09)" |
| A-05 | 0005 | partial | "positional payloads are rejected (T-09)" |
| A-06 | 0005 | decides | "No user-defined operators, no compound assignment, no `elif`, no ternary, no index syntax" |
| A-07 | 0006 | partial | "overflow and divide-by-zero fault" |
| A-08 | 0006 | partial | "no implicit conversions, no defaulting except `Int` literals" |
| A-09 | 0006 | decides | "checked in every profile" |
| A-10 | 0006 | decides | "Division truncates toward zero; `%` takes the dividend's sign" |
| A-11 | 0006 | decides | "`Float` is not `Eq`" |
| A-15 | 0006 | partial | "No null, no exception primitives" |
| A-16 | 0006 | decides | "propagates only with the *same* error type (no implicit conversion)" |
| A-18 | 0008 | decides | "identifiers are NFC; text literals are not silently normalized" |
| A-19 | 0012 | decides | "compare distinct semantic names that are simultaneously visible under L-10" |
| A-25 | 0006 | partial | "Matching is an expression and is always exhaustive" |
| A-28 | 0008 | decides | "text literals are not silently normalized" |
| A-29 | 0008 | decides | "case conventions do not exclude unicameral scripts" |
| A-30 | 0008 | decides | "name roles are contextual" |
| A-31 | 0005 | decides | "One block introducer, `:`" |
| A-32 | 0008 | decides | "top-level user `let` is constant-only" |
| A-33 | 0008 | decides | "local bindings are monomorphic" |
| A-35 | 0008 | decides | "`?` targets the nearest function and is forbidden in `defer`" |
| A-36 | 0008 | decides | "`defer` is block-local LIFO" |
| A-37 | 0008 | decides | "pattern matching is partial and coverage-aware" |
| A-39 | 0008 | decides | "fault rollback is task-local, not external-effect rollback" |
| A-40 | 0008 | decides | "core determinism uses fuel/step quotas, not wall-clock semantics" |

`decides` = the record states the whole answer. `partial` = the record states
one clause of a multi-clause answer and the rest exists only in the rule text.

**These 24 are not a decision gap. They are a *linkage* gap** — the same shape
as B4's finding one layer down. The decision exists; the register does not
point at it.

## 3. The 11 that are genuinely unrecorded

| Row | Status | Rule | What the register decided with no record | The consequence |
|---|---|---|---|---|
| A-01 | Resolved | L-03, L-20 | Spaces only; tab is an error; widths free | Covered — but **by a different route than its neighbours**: the conformance plan's Layout area names the range `L-19…L-27`, which excludes both of A-01's rules; only the traceability matrix catches them (§5.1) |
| A-02 | Resolved | L-23 | Blank and comment-only lines do not affect layout | Covered by the Layout area; decision absent |
| A-13 | Resolved | T-15 | Inline bounds; `` `where` `` clauses deferred | **Deferral leak** (§4). No `D-##` entry, so no trigger, no owning phase |
| A-14 | Resolved (*risk accepted*) | T-27 | Recursive unions are `Eq`; a record cycle is rejected | **No record of the risk.** "Risk accepted" is a status word with nobody's name on it |
| A-17 | Resolved | T-18 | Orphan rule, one impl per pair, no overlap, no specialization | Covered by the Grammar area; decision absent |
| A-20 | Resolved | L-22 | The two continuation causes | Covered by the Layout area; decision absent |
| A-22 | Resolved | T-28 | Nested shadowing warns; same-block shadowing errors | Covered; decision absent |
| A-24 | Resolved | L-16, T-06 | `{}` errors pointing at `()` | Covered; decision absent |
| A-34 | Resolved | E-03, S-2 | Pipe appends its operand as the **last** argument | Covered; decision absent — and this is the one that makes `y` evaluate before `x`, a semantic consequence stated only in a parenthetical |
| A-41 | Resolved (*partial*) | L-02, L-31 | Escaped/visible bidi controls in quoted source | Covered; the unhandled part ("full editor rendering is Phase 13") names no phase document |
| A-43 | Resolved | T-30 | No core entry point; fixtures name the function | Covered; decision absent |

Eight of these are ordinary specification decisions that were simply never
written up — the drafts predate the decision-record practice. Three are
different:

- **A-14** accepts a risk in a status word. The register's rule 4 already
  demands that "(partial)" say which part is unhandled; *risk accepted* has no
  such rule, so it says nothing about who accepted it or what it costs.
- **A-34** has a consequence (operand evaluation order diverges from reading
  order) that appears nowhere outside the register cell and rule E-03.
- **A-01** is the one case where the *unrecorded* status and a *coverage* wrinkle
  coincide, though not for the reason it first appears: the rule is covered, but
  the plan's range notation misses it (§5.1).

## 4. Two deferrals living outside the deferral register

`03-ambiguities.md` §3 rule 2 says every `Deferred` row needs a trigger,
"recorded in [`04-deferred-features.md`], not here". Resolution 0007 makes the
deferral register normative and says a deferral without a trigger is a silent
scope change. Measured:

| Row | Defers | Cites a `D-##` | In the deferral register |
|---|---|---|---|
| A-13 | `` `where` `` clauses | none | **no** |
| A-47 | the configuration mechanism | none (defers to "the tooling/configuration phase") | **no** |
| A-38 | Map/Set/Hash | `D-19` | yes |

Both are `Resolved`, not `Deferred`, so no check looks at them and the
deferral register's rule never fires. **A deferral parked in a resolution cell
has no trigger and no owning phase, which is exactly the "later" that decision
0007 forbids.**

A-13 is the more consequential: the deferral register holds 20 entries and none
of them is `where` clauses, so a reader of `04-deferred-features.md` would
conclude Plain has no deferred syntax for generic bounds.

## 5. Verified honest: the register's own arithmetic

Not everything here is a defect. Checked and sound:

- **All 47 rows resolve to something real.** Every `L/T/E/S` rule ID cited in
  the `Spec ref` column exists; every `§N of doc 0` section exists (1–10); the
  file references exist. `cross_reference_check` enforces this and it is green.
- **The 5 `Deferred` rows all cite a defined `D-##`** with a trigger.
- **The counts reconcile**: 42 + 5 + 0 = 47, and the summary's ID list matches
  the table exactly.
- **The register does not overclaim provenance.** Its preamble states plainly
  that the book's §12.1 list is unrecoverable, that this list is derived, and
  that it *MUST NOT* be cited as the book's. Decision 0004 backs it. This is the
  one place in the project where an absent source is stated rather than implied.

### 5.1 A coverage wrinkle this audit found by being wrong

A-01's rules are `L-03` and `L-20`. The conformance plan's Layout area names the
range `L-19…L-27` — which **excludes both**. Reading the plan alone, indentation
character and block-column rules have no fixture area.

They are covered anyway, and the reason matters: `07-traceability.md` assigns
both to `Layout` by ID, per rule, and `conformance_area_coverage` fails if any
rule is unattributed. So the safety net is the matrix, and the *plan* — the
document a reader consults to answer "how many fixtures for layout?" — is
incomplete for those two rules.

This is worth recording as a measurement, not a defect: the plan uses ranges as
shorthand, the matrix uses explicit IDs, and the two disagree in exactly one
place out of 106. The matrix is the authority (it is the one with a check), the
plan is the summary. Ranges are why the plan could not be the authority. A
reviewer reading "L-19…L-27" would not know they were reading a summary.

## 6. Proposed remedy (AD)

| # | Proposal | Why it is a proposal, not an action |
|---|---|---|
| **AD-1** | Backfill the forward edge for the 24 rows in §2: add `decision NNNN` to each row's `Spec ref` cell, and add the A-IDs to the corresponding record's **Resolves** field | It is a 24-row edit to the register plus an edit to four decision records. It changes what four records claim to have decided, which is the owner's record to amend |
| **AD-2** | Write the 11 records in §3, or mark them explicitly `Resolved (agent)` with a pointer to this audit | Backfilling decisions retroactively would invent a decision trail the project does not have. Naming the status honestly is the cheaper and more truthful option |
| **AD-3** | Add `D-21 — `where` clauses` and `D-22 — diagnostic configuration mechanism`, or move both to `Deferred` with a trigger | Touches the normative deferral register and its count (20 → 22), which every count-bearing document quotes |
| **AD-4** | Give `Resolved (risk accepted)` the same disclosure rule as `Resolved (partial)`: it must name the risk, the cost, and who accepted it | A new register rule, and A-14 is the only row affected |
| **AD-5** | Put the 35 unrecorded rows in front of the owner, or state in the readiness packet that they are delegated to the specification draft and why | This is the substantive one: 35 language decisions are currently settled without the owner ever having been asked |

## 7. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-04 | 1.0.0 | Created by backlog item B5. Measured: 42 resolved, **7 recorded** (all `Resolved (proposed)`, all in the readiness packet), **35 unrecorded**. 24 of the 35 are decided verbatim in a decision record and need a link, not a decision; 11 are genuinely unrecorded. Found the perfect status/record correlation (§1.1), two deferrals living outside the deferral register (§4), and that the risks in `Resolved (risk accepted)` are attributed to nobody (§3). Proposes AD-1…AD-5. |
