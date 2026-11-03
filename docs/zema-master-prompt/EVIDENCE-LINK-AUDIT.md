# EVIDENCE-LINK-AUDIT — can a reader actually reach the cited source?

| Field | Detail |
|---|---|
| **Document** | Evidence-link audit: whether each register row can be traced to the document it cites |
| **Version** | 1.0.1 |
| **Date** | 2026-11-04 |
| **Status** | Active. Produced by backlog item **B4** |
| **Machine check** | `evidence_link_check()` — counts linked vs unlinked rows; the count is reported by `--check`. Not a gate, because the defect is historical and repairing 106 rows is a mechanical pass that needs a decision first (§5) |
| **Scope** | All 135 register rows; a 13-row sample re-read in full |

> **The question B4 asks.** "Verify that an `E` row's cited source actually says
> what the row claims." That requires reaching the source. The audit found that
> for most rows **you cannot**: the row names a document and gives no route to
> it. The claim may be perfectly true — but a reader has no way to check, and an
> unverifiable Established claim is a Hypothesis wearing the wrong label.

---

## 1. The first hop of the evidence chain is broken

The project's citation convention (`research/README.md` §4) is: a research
record numbers its sources `[S1]`, `[S2]`, … in a **Sources** table with title,
URL, publisher, grade and retrieval date; a claim carries the number inline.

The register does not use that convention. Measured:

| | Rows |
|---|---:|
| Total register rows | 135 |
| Labelled rows (`E`/`P`/`H`) | 134 |
| Cite an http(s) URL | **0** |
| Cite an `[S##]` pointer that a research record defines | **1** |
| Cite a repository path that exists | **31** |
| **Cite a title with no route to it** | **42** |
| **Unlinked per the check, including rows whose source is a Phase or book reference** | **101** |

So 42 `E`/`P`/`H` rows name a document — "Chromium *Release Cycle* [A]", "Tauri v2
documentation [A]", "HarfBuzz repository [A]" — and give no way to find it. The
URLs **do exist**: they are in the research records' Sources tables, which is
where the evidence chain actually starts.

**One missing link would reconnect 18 of the 42.** Matching the register's titles
against the 98 `[S##]` entries indexed across the research records gives, for
example:

| Register row | Research source that holds the URL |
|---|---|
| 014 StatCounter series | `phase-00-02` S2 |
| 016 HTTP Archive, Web Almanac | `phase-00-03` S1 |
| 020 Electron *Security* docs | `phase-00-04` S1 |
| 022 Flutter desktop support | `phase-00-01` S8 |
| 033 UI Automation / AT-SPI | `phase-00-02` S11 |
| 037 web-platform-tests | `phase-00-02` S15 |
| 064 Elm "No Runtime Exceptions" | `phase-01-01` S10 |
| 085 Lamdera *Is it for me?* | `phase-01-04` S6 |

The remaining 24 need a real URL attached, most of them Unicode and IEEE
specifications cited as prose ("UTS #55 rev5 §5.1.3, grade A") with no pinned
link and no retrieval anchor beyond a date.

## 2. The sample re-read (13 rows)

Rows were re-read against the best available source. Three states: **verified**
(the cited document contains the claim), **correct** (the claim is right but the
citation is not the route to it), **stale** (the row's own numbers have since
changed).

| Row | Claim (abridged) | State | Note |
|---|---|---|---|
| 013 | The browser is also a distribution and security platform | correct | RFC 6454 supports the origin half; the *distribution* half is not in that RFC. Two citations merged into one cell |
| 016 | Median desktop page 2,652 KB, October 2024 | **verified** | `phase-00-03` S1 holds the exact figures and the URL |
| 022 | Flutter supports desktop on stable | correct | `phase-00-01` S8 |
| 029 | Wasmtime provides sandboxed capability-based WASI access | correct | `phase-00-01` S9 |
| 033 | Windows UIA; Linux AT-SPI | correct | `phase-00-02` S11 |
| 064 | Elm ships production apps with no exceptions and no null | correct | `phase-01-01` S10 |
| 085 | Lamdera documents SaaS lock-in and no external database | correct | `phase-01-04` S6 |
| 091 | UTS #55 rev5 defines chunks and requires C4 diagnosis | correct | Cited as prose with a date; no pinned URL in the row |
| 106 | 20,034 rows, 200,340 assertions, zero failures | **verified** | `normalization-report.json` confirms all three numbers exactly |
| 111 | Six Unicode property-accessor tests pass | correct | File exists; the raw report exists |
| 114 | Eleven statements across nine documents still asserted C1/C5 blocked build | correct | Table of locations in the audit record |
| **124** | **3 of 19 concerns cited by any evidence row** | **stale** | **Now 5 of 19.** The audit that produced this row added rows #124–#127, which cite Concerns 16 and 17. The claim was true when written and is false now |
| 130 | 8 / 27 / 8 / 7 gate-criteria dispositions | **verified** | `gate_coverage_check()` reproduces exactly |

**Nothing in the sample was substantively wrong.** One row was stale, and one
(013) conflated two citations whose support differs. That is a better result
than the linkage problem predicted — but it is also only 13 of 135 rows, and the
rows easiest to re-read are the ones with repository paths.

## 3. Row 124 is the interesting defect

It is not a typo. It is a **self-invalidating measurement**: the audit pass
that recorded "only 3 of 19 concerns are traced" simultaneously added four
evidence rows that cite three more concerns. The finding was correct on the day
it was written and wrong within the same commit.

This is the first observed case of a claim becoming stale *because of the work
that recorded it* — distinct from the drift §3.1–3.8 of the process audit found,
where copies diverged over time. The remedy is the same as PR-01's: a claim that
can be recomputed must carry the command that recomputes it, so staleness is
detectable rather than discovered by accident.

## 4. What is *not* wrong

Worth stating, because the linkage defect makes the layer look worse than it is:

- **The research layer is properly cited.** 78 URLs across the research records,
  in Sources tables with publisher, grade and retrieval date.
- **The project's own measurements are verifiable and correct.** Row 106's three
  numbers reproduce exactly from the committed report; row 130's four counts
  reproduce from a check. Where the project measured something itself, the
  evidence is solid.
- **The labels are not inflated.** Nothing sampled was a grade-C source
  presented as Established.

The defect is narrow and specific: **the register's citation cell is prose, and
prose is not a link.**

## 5. Proposed remedy (P)

| # | Proposal | Why it is a proposal, not an action |
|---|---|---|
| **EL-1** | Change the register's source-cell convention: a row must cite either a repository path, a URL, or an `[S##]` pointer that a research record defines. Add the check as a gate once the backlog row is repaired | 101 rows would change. That is a large mechanical edit to the project's central evidence artifact and needs the owner to accept the new convention first |
| **EL-2** | Give every register row an `[S##]` back-pointer into the research record that holds the URL, for the 18 rows where one exists | Cheap and mechanical, but it changes what the register *means*, so it waits with EL-1 |
| **EL-3** | A row whose claim can be recomputed states the command in its source cell (as rows 106, 111, 124 and 130 already do) | This is PR-01 applied to evidence: it is what would have caught row 124 |
| **EL-4** | Row 124 is corrected in place with a dated note; the original wording is retained | Correcting a stale row is allowed now; rewriting history is not |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-04 | 1.0.1 | The check's first version counted only backticked paths, not markdown links, so it flagged row 138 — which cites its own audit record as a markdown link. Caught by the ratchet test. Unlinked figure 106 → 101. |
| 2026-11-04 | 1.0.0 | Created by backlog item B4. Measured: 0 of 135 rows cite a URL, 1 cites a defined `[S##]`, 42 cite a title with no route, 101 unlinked overall by the check (which counts a row unlinked when its source names a phase, an experiment, or a book chapter that is not a document in this repository). 13 rows re-read: 3 verified, 9 correct, 1 stale (row 124, self-invalidated by its own audit). Records that the research layer is properly cited and the project's own measurements reproduce exactly. Proposes EL-1…EL-4. |
