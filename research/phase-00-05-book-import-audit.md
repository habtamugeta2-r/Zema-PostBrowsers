# Phase 0 · Record 05 — Research-Book Import Audit (Book Missing — Evidence Recorded)

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-00-05-book-import-audit.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → Gate 0 (task: locate, import, or explicitly mark the research book missing) |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for Gate 0 — outcome is a **negative finding**, recorded in full |
| **Evidence label** | **Established** (observations), with the consequences labeled **Proposed** |
| **Feeds** | [`../docs/decisions/0004-research-book-missing.md`](../docs/decisions/0004-research-book-missing.md) |

> Master Prompt v1.1 says the research book is not in this repository and
> makes locating or importing it an explicit Phase 0 task. This record
> shows the search that was performed, states what is therefore **not**
> recoverable, and refuses to invent the missing pieces.

---

## 1. What was searched (raw method)

Performed on **2026-11-02** from a checkout of this repository, using the
GitHub CLI against the owner's public account:

| Step | Command (abridged) | Result |
|---|---|---|
| 1. Enumerate owner repositories | `gh repo list habtamugeta2-r --limit 100` | **10 public repositories**: `PlainP`, `Zema-PostBrowsers`, `Catalog-Server-Rendered-Product-Store`, `ReleaseKit`, `Plain`, `PlainUI`, `TeamFlow`, `Better-backJS`, `FileVault-Private-Document-Storage`, `SupportDesk` |
| 2. List files of each plausibly relevant repo | `gh api repos/habtamugeta2-r/<repo>/git/trees/HEAD?recursive=1` | No `Chapters 1–13` book; `PlainP` has design docs `00`–`08`; `PlainUI` has specs `00`–`13`; `Plain` contains only a `LICENSE` |
| 3. Full-text search for the book's distinctive markers | GitHub code search: `"Experiment E3"`, `"Decision C"`, `"Chapter 13"` scoped to the owner | **`"Experiment E3"`: 2 hits — both in this repository's own documents.** **`"Chapter 13"`: 0 hits.** `"Decision C"`: no book-level hits |
| 4. Inspect this repository's tree | `git ls-tree -r --name-only HEAD` | 9 files, all founding documents/templates; no book, no experiments, no data |

**Conclusion (Established):** the ZEMA research book (Chapters 1–13,
including §12.1's ambiguity catalog, Ch. 6's benchmark protocol, Ch. 7's
R1–R29 references, Ch. 9's experiments/decisions) **is not in this
repository and was not found in any of the owner's 10 public
repositories**. It may exist privately; nothing in this search proves it
does not exist at all.

## 2. What is consequently unavailable

| Missing artifact | What the founding documents assume it contains | Effect now |
|---|---|---|
| **Ch. 1, 11** | Vision, adoption framing, distribution lineage | Master Prompt's own summaries are used; no new claims derived |
| **Ch. 2, 8, 12 §12.1** | Full language design and the catalog of **draft ambiguities to resolve** | Phase 1 must build its own ambiguity list from the normative grammar it drafts, and mark the original list **unrecovered** |
| **Ch. 3, 13.1** | UI/rendering analysis, Decision B | Phase 6 proceeds from the Master Prompt summary only |
| **Ch. 4, §12.3, Decision A** | Memory/concurrency analysis, execution-model decision | Phase 3/4 must re-derive the options; no "as the book says" appeals |
| **Ch. 5** | Security/capability chapter | Phase 5 proceeds from the threat model the team writes |
| **Ch. 6** | Benchmark protocol (cold/warm start, INP, frame budgets, etc.) | Phase 12 uses the protocol **as summarized in Master Prompt v1.1**; the summary is thinner than the chapter and must be recorded as such |
| **Ch. 7, R1–R29** | Evidence register of what would establish each headline claim | Rebuilt independently in [`../docs/evidence-register.md`](../docs/evidence-register.md) — **this repository's register is now canonical** |
| **Ch. 9, Experiment E3** | The third performance experiment (H1–H3 cluster) | **Blocked.** Its definition must not be invented |
| **Ch. 9, Decision C** | An unattested decision (only A, B, D are cited anywhere) | Treated as **nonexistent** until attested |
| **Ch. 10, §13.2–13.5** | Data, networking, and the book's own limitations statement | Phase 9/10 proceed from Master Prompt summaries |

## 3. The three open numbering items, resolved as far as the evidence allows

| Item | Prior status | Finding | Resolution |
|---|---|---|---|
| **E3** | "Blocked — awaiting book" (tracker, 2026-11-01) | Its existence is attested only by `00-Core-Concerns.md` Concern 3, which itself is a synthesis that "adds no new claims" | **Remains blocked.** E3 is *not* renumbered, redefined, or deleted. It never blocks a phase gate; it blocks only a completeness claim about the performance cluster |
| **Decision C** | "Unattested" (IMPROVEMENTS §5 item 3) | No source in this repository or the owner's public repos names a Decision C | **Closed as unattested.** If the book arrives and names one, reopen with a dated note |
| **Target desktop OS** | "Unnamed; ideally recorded at Gate 0" (IMPROVEMENTS §5 item 4) | An owner decision, not a research finding | **Decided (Proposed)** in [`0002-target-os-linux.md`](../docs/decisions/0002-target-os-linux.md) — Linux (Ubuntu 24.04 LTS), pending owner confirmation (C3) |

> Correcting a possible misreading: E3's absence does **not** lower the
> evidence bar. Phase 12 still requires every headline claim to be
> confirmed or retracted with raw data — E1, E2, E4, and E5 plus whatever
> measurement is needed for a claim is enough to satisfy that; E3 was
> only ever a *third* performance experiment in the book's cluster.

## 4. Options considered for the missing book

| Option | What it would take | Cost | Recommendation |
|---|---|---|---|
| **A — Import the book** | Owner supplies the file(s) or a repository/URL; commit under `research/book/` with a version note | Low, if the text exists; copyright/licensing question if it will be public | **Preferred**, and possible at any time |
| **B — Rebuild the missing parts** | Write a new Ch. 6 benchmark protocol and §12.1 ambiguity list from scratch inside this repo | High; risks fabricating "book" content and mis-citing it | Only for the benchmark protocol, and labeled as **this repository's** protocol, never as the book's |
| **C — Retire the cross-references** | Delete or annotate every "Ch. N" pointer; rewrite affected tasks | Medium; must not silently drop the tasks the pointers described | Acceptable fallback at Gate 1 if no book arrives |
| **D — Ignore the gap** | Do nothing | Certain drift and accidental fabrication | **Rejected** |

**Decision taken now:** keep the cross-references as *unresolved
pointers*, keep E3 blocked, and proceed. Deadline for the owner: before
**Gate 1** (options A or C); recorded as condition **C2** in
[`../docs/gates/gate-00.md`](../docs/gates/gate-00.md).

## 5. What the team must not do

1. **Do not invent E3.** No "reconstructed" experiment definition may be
   attributed to the book.
2. **Do not cite a chapter for a claim.** Chapter pointers currently
   establish nothing; they are placeholders (Concern 16: a reference
   establishes background only, never Plain's performance).
3. **Do not silently close the numbering.** If E3 is eventually declared
   retired, that is a recorded decision at a named gate.
4. **Do not treat `PlainP` (PA-8) as the book.** It is a different
   artifact with different documents.

## 6. Sources

| # | Source | Grade | Retrieved |
|---|---|---|---|
| S1 | GitHub CLI output of `gh repo list habtamugeta2-r` (10 public repositories) and per-repo tree listings for `PlainP`, `Plain`, `PlainUI` | A (raw observation; commands reproducible by anyone with access) | 2026-11-02 |
| S2 | GitHub code search results for `"Experiment E3"` (2 hits, both in `docs/zema-master-prompt/`) and `"Chapter 13"` (0 hits) scoped to the owner's account | A (raw observation) | 2026-11-02 |
| S3 | `00-Core-Concerns.md` Appendix A open numbering items and Concern 3 (E1–E3 cluster): [`../docs/zema-master-prompt/00-Core-Concerns.md`](../docs/zema-master-prompt/00-Core-Concerns.md) | A (project record) | 2026-11-02 |
| S4 | `IMPROVEMENTS.md` §5 items 1–4 (book missing, E3, Decision C, target OS): [`../docs/zema-master-prompt/IMPROVEMENTS.md`](../docs/zema-master-prompt/IMPROVEMENTS.md) | A (project record) | 2026-11-02 |
| S5 | `PlainP` repository `README.md` and `docs/README.md` (documents 00–08, not chapters): <https://github.com/habtamugeta2-r/PlainP> | A (as a repository fact) | 2026-11-02 |

## 7. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: reproducible search method, 11 unavailable artifacts, resolution of E3 / Decision C / target-OS items as far as evidence allows, four options with deadline before Gate 1. |
