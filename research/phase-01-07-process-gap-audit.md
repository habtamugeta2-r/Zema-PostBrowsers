# Phase 1 · Record 07 — Research and Build Process Gap Audit

| Field | Detail |
|---|---|
| **Document** | `research/phase-01-07-process-gap-audit.md` |
| **Version** | 1.1 |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Complete for this audit pass. It records a **defect inventory and its repair**, not a conformance result |
| **Evidence label** | **E** for repository observations (each reproducible by a named command) · **P** for the proposed process rules below · **H** for the claims about what the gap will cost later |
| **Method** | Full read of all 52 Markdown files and 8 Python files; mechanical re-derivation of every published count; mutation testing of the repaired checks; comparison against published conformance-suite and repository-hygiene practice |
| **Author** | ZEMA research agent (Arena AI Agent Mode) on behalf of Better-back |

> **Bottom line.** Phase 1 had an unusually strict *evidence* discipline (a
> claim with no row does not exist, labels, source grades, retraction rules) and
> almost no *structural* discipline. It was rigorous about whether a sentence
> was true and careless about whether two documents said the same thing, whether
> a number matched its own table, or whether a rule could be tested at all. Three
> invariants had genuinely broken, eleven status statements were false, and the
> plan could not answer the one question a conformance plan exists to answer:
> *where is rule X verified?* This record documents each finding, the repair, and
> the mechanical check that now prevents recurrence.

---

## 1. Why this audit exists

The project's own method is *Research → Decide → Build → Measure → Gate*, and
its own rule is *"a claim with no row does not exist."* Both are about content.
Neither says anything about **structure**: how many copies of a fact may exist,
what happens when a status becomes stale, or how a rule is linked to a test.

The repository went through six rapid iterations on 2026-11-03 (draft v0.2 →
v0.2.4, decisions 0008 → 0016, evidence rows #074 → #111, five tracker entries
on one day). Every iteration appends. Nothing merges. The failure mode of
append-only documentation is not lying — every individual statement below was
true when written. The failure mode is **simultaneous truth**: statements that
were true at 09:00 and false at 14:00, both present, both readable, with nothing
saying which one governs.

That is a process gap, and it is the specific gap this repository had.

## 2. What was actually measured

All figures re-derived mechanically on 2026-11-03, not quoted from the
documents:

| Quantity | Measured | Command |
|---|---:|---|
| Markdown files | 52 at audit start (55 after this record and two new indexes) | `git ls-tree -r HEAD --name-only \| grep -c '\.md$'` |
| Python files | 8 at audit start (10 after the new test module) | `git ls-tree -r HEAD --name-only \| grep -c '\.py$'` |
| Normative rule IDs | 106 (34 L + 30 T + 36 E + 6 S) | `python3 tools/audit_phase01.py --check` |
| Rules traceable to a verification method | 0 → **106** (after repair) | same |
| Rules attributable to a conformance area | 92 → **106** (after repair) | same |
| Conformance fixtures written | **0** | `find . -path '*conformance*'` |
| Evidence register rows | 111 at audit start, E 55 / P 26 / H 30 (114 after this record's own rows #112–#114) | same |
| Ambiguities | 47 (42 resolved-proposed, 5 deferred, 0 open) | same |
| Diagnostics registry | 53 codes, 52 active + 1 historical | same |
| Broken relative links | 0 | same |
| Undefined rule/ambiguity references | 0 | same |
| Duplicated result artifacts | 1 | same |
| Split Markdown tables | 4 | `tests/test_document_invariants.py` |
| Rule sets tabulated in two documents | 2 → **0** (after §3.6) | `tools/audit_phase01.py` `duplicated_fact_check()` |
| False or stale status statements | 11 | manual reading, §3.3 |
| Typed prose numbers that disagree with the artifact | 2 ("580 words", "307 fixtures") | `--verify` |

The mechanical layer was in good shape: links, grammar closure, cross-references,
and the manifest all passed **before** this audit. The failures were one level
up — in *joining* the mechanical layer to the prose layer.

## 3. Findings

Severity: **S1** breaks or defeats a gate obligation · **S2** misleads a reader
or a future agent · **S3** untidy but harmless.

### 3.1 The primary gap: rules were never linked to tests (S1)

The specification gives every normative statement a permanent ID (`L-nn`,
`T-nn`, `E-nn`, `S-n`) and says *"conformance tests, diagnostics, and the
ambiguity register can cite them"* (`docs/plain/README.md` §2). The
[conformance plan](../docs/plain/05-conformance-plan.md) allocated a **budget**
of fixtures to **areas**, naming rule *ranges* per area.

No artifact joined the two. The consequences, found by parsing the plan's own
area table:

**14 of 106 rules were named by no area** — `L-05`, `L-06`, `L-07` (all of
comments and doc comments), `L-28` (no user-defined operators), `L-29` (`.`
is field access only), `T-01`…`T-05` (`let`/`mut`/block-locality/no-indexing/
`Bool`), `T-28` (shadowing), `E-13` (short-circuit logic), `E-34` (cost of
checked arithmetic), `E-36` (both profiles agree).

Why this is an S1 and not an omission: **the plan's success criterion is
per-area**, and every area could hit its number without those rules being
touched. `L-05…L-07` is the whole comment subsystem; `T-01…T-05` is the whole
binding model; `E-36` is the *entire justification* for having two execution
profiles. A runner that reported area coverage would have reported green.

The deeper problem is the shape of the artifact. A budget answers *"how much
testing will there be?"*. A gate needs *"which rule is proved, and by what?"*
Those are different documents, and the second one did not exist.

**External check.** This is not a ZEMA-specific worry; it is the standard
requirement-traceability problem. Test262, the closest analogue in the
repository's own Appendix A, attaches per-test frontmatter with a required
`features` key drawn from a controlled `features.txt`, plus a specification
reference ID, precisely so a consumer can filter tests by feature and detect
untagged work ([Test262 authoring guidelines][T1], [technical rationale][T2]).
Safety-critical practice is stricter still: DO-178C and its peers require
**bidirectional** traceability — every requirement to at least one test, and
every test back to a requirement — because a one-directional trace hides
orphan tests and uncovered requirements alike ([DO-178C traceability][T3],
[traceability overview][T4]). ZEMA's own Master Prompt asks for "a conformance
suite with passing results" without specifying the trace, which is why the gap
went unnoticed for six iterations.

**Repair.** New [`docs/plain/07-traceability.md`](../docs/plain/07-traceability.md):
all 106 rule IDs, each with a verification method (`FX`, `RT`, `DZ`, `EM`, `AX`,
`SR`, `PT`, `NV`), the conformance area that owns its fixtures, and the specific
Gate 1 target. It also states plainly that **106/106 allocated ≠ 0/106
verified**, and names the two rules Gate 1 *cannot* verify (`E-31`'s
task-survival clause, `E-34`'s cost claim) with the phase and gate that own them.
The conformance plan gained four areas and a table of deliberate exclusions, and
the budget moved **307 → 341** as a *consequence* of the repair, not as a goal.

### 3.2 Three invariants had actually broken (S1/S2)

**(a) Duplicated result artifact.** The normalization result lived in two files
differing only by a timestamp:

```
research/data/phase-01-normalization-report.json         2026-11-03T18:47:39Z
research/experiments/EN-unicode17-normalization/…json     2026-11-03T18:46:52Z
```

Both carried the same 20,034 rows and 200,340 assertions. Evidence #106 cites
the experiment copy; the tool wrote the `research/data` copy. A future rerun
would update one and not the other, and a reader would have two "current"
numbers. The repository's own rule — *"One canonical copy. Copies drift; links
do not"* (`docs/zema-master-prompt/README.md`) — was already in force and was
already broken. **Repaired:** the experiment record owns the only copy;
`tools/check_unicode17_normalization.py` now writes there.

**(b) Four Markdown tables split by a blank line.** In
`docs/evidence-register.md` (between rows 086/087, 089/090, 090/091, 094/095)
and `docs/plain/03-ambiguities.md` (between A-26/A-27). A split table renders as
two tables; worse, a parser silently drops the detached rows. The evidence
register passed its count check only because the row-counting regex is
line-based and does not care about table boundaries — the check was green while
the artifact was malformed. **Repaired:** rows rejoined.

**(c) A duplicated section number.** `docs/gates/gate-00.md` had both
`## 8. Sign-off` and `## 8. Dated post-gate note`. Every "§8" in the file was
ambiguous, and two other documents cited "§9" for the owner responses, which did
not exist. **Repaired:** sections renumbered 8/9/10, all five inbound references
updated.

### 3.3 Eleven statements that had become false (S2)

C1 and C5 were resolved on 2026-11-03 (§10 of the Gate 0 review). Nine documents
still asserted that build was blocked. This is the most damaging class of defect
in the repository, because the project's method *is* the attribution of
authorization — an agent reading `docs/plain/README.md` would have concluded it
was unauthorized to write code, while `PHASE-TRACKER.md` said the opposite.

| Location | Was | Now |
|---|---|---|
| `docs/plain/README.md` callout | "build tasks are blocked on C1/C5 … once C1/C5 clear" | resolved; C2 + A-* ratifications are what remain |
| `docs/plain/05-conformance-plan.md` §4 | "once C1/C5 clear" | "C1/C5 cleared 2026-11-03" |
| `docs/decisions/0008` status | "owner sign-off still pending (C1/C5)" | resolved, decisions still unratified |
| `docs/decisions/0010` consequences | "build remains blocked by C1/C5" | dated correction note |
| `docs/decisions/0011` consequences | "C1/C5 still block build" | dated correction note |
| `docs/decisions/0012` consequences + note | "C1/C5 still block build work" | dated correction note |
| `docs/gates/gate-00.md` §9 note | "build tasks remain blocked on C1/C5" | corrected in place, with the correction visible |
| `research/phase-01-01` status | "build half blocked on Gate 0 conditions C1/C5" | resolved |
| `research/phase-01-03` status | "implementation remains blocked by C1/C5" | resolved |
| `research/phase-01-05` status + readiness table | "C1/C5 block build", "C1 Open" | resolved |
| `docs/decisions/0002` status | "requires owner confirmation at Gate 0 (condition C1)" | it is **C3**, not C1 — a wrong condition ID |

Two rules were followed in the repair that matter more than the edits: **history
was not rewritten** (decision records keep their original text with a dated
correction beneath it, because a decision record is testimony about what was
decided when), and **no correction was silently absorbed** (each is visible as a
named paragraph so a reader can see the prior claim).

### 3.4 Structural untidiness in the normative documents (S3)

- `docs/plain/01-types.md` presented rules as `T-01, T-02, T-28, T-03, T-29,
  T-30, T-04, T-05, …`. Rule IDs are permanent and must never be renumbered —
  a good rule — but the file had no note explaining the apparent disorder, so a
  reader cannot tell a permanent-ID artefact from a missed edit. **Repaired:**
  `T-01…T-03` restored to order, `T-28` kept beside the binding rules, `T-29`
  moved to top-level constants, `T-30` given its own §8 "Entry point", and an
  explicit note added that IDs are not renumbered. This is what the "one
  notation per concept" doctrine should look like for document structure too.
- `research/README.md` ended in a heading-less list of decisions and a stray
  blank line, so the folder's index stopped being an index. **Repaired:** a
  §7 decisions table and a §8 folder-status section.
- `docs/plain/README.md` §2 pointed `S-nn` at "§9"; sugar is §8 and §9 is
  diagnostics. **Repaired.**
- `docs/plain/01-types.md` T-20 attached `PL0114` to a reference to `T-17`,
  which does not own that code (S-4 and T-20 do). **Repaired.**
- `docs/zema-master-prompt/PHASE-01-EXECUTION-PROMPT.md` sent the reader to
  "§10 fallback" (the file has no §10) and to an "implementation log (§8)" that
  does not exist anywhere in the repository. **Repaired** to point at WP-11 and
  at real recording locations.
- Decision records described themselves as *"Accepted"* for agent-authored
  choices while the readiness packet kept the same items open for the owner.
  The status vocabulary was doing two different jobs — *was this written as
  decided?* and *has the owner ratified it?* — inside one cell. **Partially
  repaired:** every decision record's status line now names both, e.g. "Proposed
  — agent decision recorded; owner ratification pending". A full status-vocabulary
  fix is a process decision and is proposed at §6 rather than performed.

### 3.5 What was checked and found genuinely sound

Reporting only defects would misrepresent the repository. These passed and are
worth not "improving":

- **Link integrity** — 0 broken relative links across 52 files with deep
  relative paths (`../../research/…`).
- **Cross-reference integrity** — every one of 173 defined IDs resolves; no
  dangling rule, ambiguity, or deferral reference.
- **Grammar closure** — 56 productions, no undefined non-terminals.
- **Count honesty** — the evidence summary matched its own rows exactly
  (111 / 55 / 26 / 30) before this audit; the audit tool's drift guard was
  already catching exactly the right thing.
- **Regenerable, dogfooded evidence** — the normalization experiment reproduced
  from a clean clone (`tools/fetch_unicode17.py` → all 16 inputs verified;
  `tools/check_unicode17_normalization.py` → 20,034 rows, 200,340 assertions,
  0 failures), and the six property tests pass once the cache exists. This audit
  re-ran all of it: **the project's one executable claim is real.**
- **Honest scope labelling** — every Phase 1 artifact says in terms that no
  executable core and no gate attempt exist. That discipline is the reason this
  audit could be done mechanically at all.

### 3.6 Second pass: the audit's own repair reproduced the defect

The first pass added four tables. One of them — the list of rules Gate 1 cannot
verify — was written into **both** `05-conformance-plan.md` §5 and
`07-traceability.md` §4, with the row set differing by one rule (`L-33`). That
is the exact defect §3.1 describes, introduced by the document that describes
it, within the same commit.

It was found by re-running the duplication scan against the *new* files, not by
review. Two consequences were recorded rather than quietly fixed:

1. **The first duplicate-detection check was too weak.** It compared rule *sets*
   for exact equality, so a three-row partial copy inside a larger table did not
   trip it. Mutation-testing the check — reintroducing the duplicate and
   observing it pass — exposed that. The check now measures *overlap* between
   per-file rule sets (≥3 shared rules and ≥60 % of the smaller set), which is
   the actual drift mode. `test_no_rule_set_is_tabulated_in_two_documents`
   covers it.
2. **The fact now has one owner.** `07-traceability.md` §4 owns the exclusion
   table; the conformance plan links to that anchor and states the rule without
   restating the table. `test_gate_one_exclusions_have_exactly_one_owner`
   asserts the link exists and the copy does not.

This is worth stating plainly in the record: the failure mode of append-only
documentation is not limited to the original authors. **An audit that adds
documents without the owner rule adds copies too.** That is the argument for
PR-04 being mechanical rather than aspirational.

### 3.7 Defects in the audit's own published numbers

Three figures in v1.0 of this record were wrong, and the repair was the same
class of error it was documenting:

| Claim in v1.0 | Measured | Cause |
|---|---|---|
| "52 Markdown files", "8 Python files" | correct **at audit start**; 55/10 after | the record did not date its snapshot |
| "The unexamined document had an underivable claim" — not stated, but true | `problem-statement.md` claimed "about 580 words of prose"; measured 519 prose / 866 total | a typed number, never computed |
| the exclusion set contained `L-33` in one file and not the other | — | §3.6 |

The remedy is now a tool mode rather than a resolution to be careful: 
`python3 tools/audit_phase01.py --verify` prints the quantities prose is allowed
to quote (`markdown_files`, `python_files`, `normative_rules_L_T_E`,
`sugar_ids`, `ambiguities`, `deferrals`, `evidence_rows`, `decision_records`,
`plain_documents`, `problem_statement_prose_words`,
`problem_statement_total_words`, `conformance_fixtures_written`). That is PR-01
in executable form.

### 3.8 Two repairs completed that the first pass only started

- **PR-06 (two-field decision status) was proposed and then not applied.** All
  16 decision records now carry an `Owner ratification` field beside `Status`,
  and `docs/decisions/README.md` mirrors it. Before this, three records said
  "Accepted" while the readiness packet listed the same items as open for the
  owner — the same word doing two jobs.
- **Document-count drift.** The execution prompt told the executor to read "all
  seven documents" in `docs/plain/`, which has held nine files (eight numbered
  plus the index) since the traceability matrix was added. Corrected to "all
  eight documents", with doc 7 identified as the work list.

## 4. The root cause

One sentence: **the project had an evidence register but no artifact register.**

`docs/evidence-register.md` governs *claims*: every claim needs a row, a label,
a source grade, a status, and retraction is permanent. Nothing governs
*artifacts*: how many copies of a measurement may exist, who owns a status line,
which document is authoritative for a number, or when a stale statement must be
corrected. So:

| Because there was no… | …this happened |
|---|---|
| canonical-location rule enforced by a tool | a result file stored twice, differing by a timestamp |
| single owner for a status fact | eleven documents restating an authorization state, all drifting separately |
| rule-level trace join | 14 rules with no area, invisible behind an area-level budget |
| table/renderer check | 4 split tables and a duplicate section number |
| distinction between "decided" and "ratified" in a status vocabulary | decisions reading "Accepted" while the readiness packet kept them open |

This is the ordinary documentation-drift problem, and the standard remedy is
the ordinary one: **one authoritative source per fact, references instead of
copies, and an automated check that fails when they diverge** ([SSOT practice][T5],
[drift and staleness][T6]). Mature compilers do this with a dedicated
repository-hygiene tool — Rust's `tidy` fails CI on style, licensing, error-code
documentation, and test-directory consistency, exactly the class of check this
audit added by hand ([tidy][T7]). ZEMA's `tools/audit_phase01.py` already had
the right shape; it was simply checking only the claims layer.

## 5. The repair, and proof that it is not decorative

### 5.1 New and changed files

| File | Change |
|---|---|
| `docs/plain/07-traceability.md` | **New.** 106 rule IDs → method → area → target; the NV rules and their owners; the allocation-vs-coverage ledger |
| `docs/plain/05-conformance-plan.md` | +4 areas (comments, bindings, logic, and `L-28`/`L-29`/`E-36` folded into existing rows); §5 exclusions table; budget 307 → 341; traceability pointer |
| `docs/plain/01-types.md` | rule ordering, `T-30` §8, `PL0114` owner fixed |
| `docs/plain/README.md` | stale blockers corrected; `S-nn` §9→§8; document map gains doc 7; decisions 0013–0016 listed |
| `docs/evidence-register.md`, `docs/plain/03-ambiguities.md` | split tables rejoined |
| `docs/gates/gate-00.md` | duplicate `## 8` renumbered 8/9/10; five inbound refs updated; stale sentence corrected visibly |
| `docs/gates/gate-01-readiness.md` | §10 refs; traceability requirement in the evidence checklist |
| `docs/zema-master-prompt/PHASE-TRACKER.md` | status row; dated change-log row for this pass |
| `docs/zema-master-prompt/PHASE-01-EXECUTION-PROMPT.md` | dead `§10`/implementation-log pointers; 341 budget; traceability in the recording map |
| `research/README.md` | §7 decisions, §8 status, audit-tool description |
| `README.md` | 341 budget, matrix in the artifact table, "zero of 341 written" |
| decisions 0002/0006/0007/0008/0010/0011/0012 | status lines and dated corrections |
| `tools/audit_phase01.py` | 3 new checks: `traceability_matrix`, `conformance_area_coverage`, `duplicate_artifact_check`; fixture total now read from the plan and compared to the summed areas |
| `tools/check_unicode17_normalization.py` | writes the canonical experiment report |
| `research/data/phase-01-normalization-report.json` | **deleted** (duplicate) |
| `tests/test_document_invariants.py` | **New.** 11 tests: audit green, rule methods, rule areas, no duplicate results, no rule set tabulated twice, exclusion table has one owner, declared-vs-summed fixture total, evidence summary match, no split table, unique numbered headings, gate-00 internal refs resolve |
| `docs/decisions/README.md` + all 16 decision records | Two-field status (`Status` + `Owner ratification`), mirrored in one index (PR-06) |
| `docs/problem-statement.md` | Typed word count replaced by the measured one (519 prose / 866 total) |
| `tools/audit_phase01.py` `--verify` | Prints the quantities prose may quote (PR-01 in executable form) |
| `tools/audit_phase01.py` `duplicated_fact_check` | Overlap-based, not equality-based; §3.6 explains why the first version failed |

### 5.2 The checks were mutation-tested

A green check that cannot fail is decoration. Each new check was deliberately
broken and observed to fail:

| Mutation | Result |
|---|---|
| Delete the `E-34` row from the traceability matrix | `missing: ['E-34']` → 2 tests fail |
| Remove `L-05` from the comments area row | `unattributed: ['L-05']` → 2 tests fail |
| Insert a blank line inside the ambiguity table | `docs/plain/03-ambiguities.md:54` → test fails |
| Restore the deleted duplicate report | `duplicates: […]` → 2 tests fail (observed on the revert) |
| Partially copy the exclusion table into the conformance plan | `duplicated_facts` clash on `['E-12','E-31','E-34']` → 2 tests fail (**only after the check was rewritten**; the first version passed this mutation, which is how the weakness was found) |
| Add a `Status`-only decision record without `Owner ratification` | not yet mechanized — recorded as an open gap in §9 |

So the repair is enforced, not merely recorded, for the four defect classes this
audit found.

### 5.3 What the repair deliberately did **not** do

- **It did not write a fixture.** Every rule is *allocated*, none is *verified*.
  Writing 341 fixtures is the Phase 1 build, and pretending a matrix is progress
  would repeat the exact error this audit is about.
- **It did not renumber a rule ID.** `T-28` still sits between `T-03` and `T-04`,
  with a note instead of a renumber. IDs are cited by decisions, evidence rows,
  and the ambiguity register.
- **It did not delete an evidence row, a decision, an experiment, or a change
  log.** Only one file was deleted, and it was a byte-identical duplicate with a
  different timestamp.
- **It did not change any normative requirement.** No rule text changed meaning;
  §3.2/§3.4 are ordering, reference, and rendering repairs.
- **It did not resolve an owner action.** C2, C3, C4, and the seven A-*
  ratifications are untouched and still block a Gate 1 attempt.

## 6. Proposed process rules (P)

These are the durable fix; they need owner acceptance like any other proposal.

| ID | Rule | Mechanizes |
|---|---|---|
| **PR-01** | Every number published in prose is computed by `tools/audit_phase01.py` from the artifact that owns it. Prose may restate a computed number; it may not originate one. `--verify` prints the allowed set; `--check` guards the ones with a mechanical owner | "580 words", "307 fixtures", and any future count drift |
| **PR-02** | Every measurement has exactly one canonical file. A second copy is a defect, not a backup. Result files are named for their experiment and only the experiment owns them | the duplicated normalization result |
| **PR-03** | Every rule ID appears in `07-traceability.md`, and a fixture's commit updates its row. "Allocated" and "verified" are distinct states that never collapse | 14 rules with no area |
| **PR-04** | A status fact (condition resolved, gate result, decision ratified) has exactly one owning document. Others **link** to it and never restate it | 11 diverged statements |
| **PR-05** | A superseded statement is corrected in place with a visible dated note; a decision record keeps its original text. Never silently edit, never leave a false sentence standing | the C1/C5 corrections |
| **PR-06** | Decision status uses two fields, not one: **Agent decision** (none / Proposed / Accepted) and **Owner ratification** (pending / ratified / revised / deferred). Applied to all 16 records and the index | "Accepted" vs "open" confusion |
| **PR-07** | Markdown is checked as a structure, not only as prose: no split tables, no duplicate numbered headings, and resolvable internal `§` references | 4 split tables, duplicate §8 |
| **PR-08** | Every check added for a defect is mutation-tested — the defect is reintroduced in a scratch copy and the check must fail — and the mutation is recorded | checks that cannot fail |

## 7. What this gap will cost if it is not held

Hypotheses, labeled as such, and each falsifiable at the gate named:

| # | Claim | Label | Test |
|---|---|---|---|
| 1 | Without PR-03, the Gate 1 review will be conducted against area counts and will pass with rules unexercised | H | At Gate 1, diff the traced rule set against the fixture set; any untraced fixture or unfixtured rule falsifies the claim that the matrix is being used |
| 2 | Without PR-04, at least one gate document will state a stale result at the moment the gate is recorded | H | At Gate 1, grep every document for the gate result string; more than one non-linking restatement falsifies |
| 3 | The class of defect found here (SSOT, stale status, missing trace) will recur in Phases 2–14 unless the checks are extended per phase, because each phase adds documents of the same shape | H | Count `--check` problems introduced per phase; a phase that introduces zero structural problems falsifies |

If hypothesis 1 holds, the consequence is not a bookkeeping error: Gate 1 would
certify a language core whose comment syntax, binding rules, and dual-profile
equivalence were never executed. That is the specific way this project could pass
its own gate and still be wrong.

## 8. Where the project actually stands (unchanged by this audit)

- **Phase 0** — passed with conditions C1–C5; **C1 and C5 resolved 2026-11-03**;
  **C2, C3, C4 open**.
- **Phase 1** — draft v0.2.4. 106 rules allocated, **0 fixtures, 0 % verified**.
  Unicode acquisition and NFC/NFD normalization are the only executable work and
  they pass their pinned corpora. No lexer, parser, type checker, evaluator, or
  runner exists.
- **Gate 1** — **not attempted**, and cannot be attempted until C2 is recorded,
  the seven A-* proposals are ratified or revised, and 341 fixtures exist and
  pass in both profiles under an independent reviewer.

## 8a. Open gaps this pass did **not** close

Stated so the next reader does not assume the repair is total.

| # | Gap | Why it was left | Who should close it |
|---|---|---|---|
| 1 | A decision record without an `Owner ratification` field is not rejected | The field is a document convention, not yet a schema | Add a check to `audit_phase01.py` when decision records stabilize |
| 2 | `docs/evidence-register.md` status cells are free prose ("Confirmed as…", "Proposed; owner…"). No controlled vocabulary is enforced | A vocabulary is a project decision; PR-06 currently covers decisions only | Owner decision |
| 3 | Prose numbers outside the `--verify` list are still unchecked (e.g. "56 productions" is checked; "29 findings" is not) | A general scraper produces false positives; each addition should be justified by a defect | Extend `--verify` per confirmed drift |
| 4 | The 11 stale-status findings were found by reading, not by a check | Detecting "this sentence contradicts that file" needs a claim-level link, which is a bigger design than this pass | Consider a status-owner field in the tracker |
| 5 | Phase 2–14 records do not exist, so none of these checks has been exercised past Phase 1 | Out of scope by the directory guide's rule 4 | Each phase, before its gate |

## 9. Sources

| # | Source | Grade |
|---|---|---|
| T1 | TC39 Test262, *Authoring guidelines* (required `features` frontmatter, specification reference IDs) — <https://github.com/tc39/test262>, retrieved 2026-11-03 | A (project documentation) |
| T2 | TC39 Test262, *Technical Rationale Report* (why per-test metadata exists) — <https://github.com/tc39/test262/wiki>, retrieved 2026-11-03 | A |
| T3 | DO-178C traceability requirements (§5.2, §6.3, §11.9; bidirectional HLR→LLR→test) — as summarized in requirements-traceability guidance, retrieved 2026-11-03 | B (secondary summary of a standard; the standard text itself was not read) |
| T4 | Requirements traceability matrix: forward, backward, and bidirectional trace; orphan requirements and orphan tests — <https://www.autemos.com/en/blogs/traceability-matrix>, retrieved 2026-11-03 | C (practitioner article; used for orientation only) |
| T5 | Single-source-of-truth practice: reference-based reuse vs copy-based reuse, version drift — retrieved 2026-11-03 | C |
| T6 | Documentation drift and staleness in software projects — retrieved 2026-11-03 | C |
| T7 | Rust `tidy`: repository-hygiene checks enforced in CI (style, licence, error-code documentation, test-directory consistency) — <https://doc.rust-lang.org/nightly/nightly-rustc/tidy/>, retrieved 2026-11-03 | A (project documentation) |
| — | Repository observations §2, §3, §5: `tools/audit_phase01.py --check`, `python3 -m unittest discover -s tests -v`, `git log`, and direct reading of all 52 Markdown files | A (project primary) |

**Grade note.** T4–T6 are grade C and are used only to confirm that these defect
classes are conventional and have conventional remedies; no claim in this record
depends on them. T1, T2, and T7 are project documentation for the practice being
cited, not evidence that ZEMA implements it. T3 is a secondary summary: the
DO-178C text itself was not consulted, so the traceability claim is stated as
practice-level, not clause-level.

## 10. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 1.0 | Audit created. Records the rule→fixture traceability gap (14 of 106 rules with no conformance area), three broken invariants (duplicated result, 4 split tables, duplicate §8), 11 stale status statements, 6 structural defects, the root cause, the repair, mutation-test evidence, and 8 proposed process rules. |
| 2026-11-03 | 1.1 | Second pass. §3.6 records that this audit's own repair duplicated the exclusion table and that the first duplicate-detection check was too weak to catch it — found by mutation-testing the check, not by review. §3.7 corrects three typed numbers in v1.0 (including the problem statement's "580 words" → 519 measured) and adds `--verify`. §3.8 completes PR-06 across all 16 decision records and fixes the "seven documents" count. §8a lists five gaps deliberately left open. Duplication check rewritten from set-equality to overlap. |
