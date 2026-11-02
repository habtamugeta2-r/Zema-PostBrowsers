# Research Records — Index, Method, and Citation Rules

| Field | Detail |
|---|---|
| **Document** | Research record index (`research/`) |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → Gate 0 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner (Better-back) |
| **Status** | Active — one index for all phases |
| **Evidence label** | This file is method, not claim. Claims live in the records below and in [`../docs/evidence-register.md`](../docs/evidence-register.md). |

This folder holds the **RESEARCH** half of the five-step loop
(Research → Decide → Build → Measure → Gate). Master Prompt
[Appendix B](../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md#appendix-b--what-to-record-and-where)
says research findings go in `research/phase-NN-*.md`. This index makes
that folder navigable and states the rules the records follow.

---

## 1. Records

| Phase | Record | What it answers |
|---|---|---|
| 0 | [`phase-00-01-lineage.md`](./phase-00-01-lineage.md) | How did we get from hypertext to a document browser that accidentally became an application platform — and what did each era get right? |
| 0 | [`phase-00-02-browser-services-catalog.md`](./phase-00-02-browser-services-catalog.md) | What does a browser actually provide beyond rendering, and does ZEMA **rebuild**, **interoperate**, or **admit giving up** on each service? |
| 0 | [`phase-00-03-coordination-cost.md`](./phase-00-03-coordination-cost.md) | How expensive is today's markup + style + code + schema + build + deploy stack, using published measurements rather than adjectives? |
| 0 | [`phase-00-04-prior-art.md`](./phase-00-04-prior-art.md) | Who has tried to leave the browser, what did they ship, and what does their existence do to ZEMA's headline claim? |
| 0 | [`phase-00-05-book-import-audit.md`](./phase-00-05-book-import-audit.md) | Where is the research book (Ch. 1–13)? What happens to experiments E1–E5 and Decisions A/B/D while it is missing? |
| 1 | [`phase-01-01-language-prior-art.md`](./phase-01-01-language-prior-art.md) | What have Elm, Rust, Kotlin, Swift, Unison, and Unicode already settled about "easy" — and what must Plain refuse? |
| 1 | [`phase-01-02-honest-limits.md`](./phase-01-02-honest-limits.md) | Which seams does one language actually remove, and which ten domains stay hard no matter what? |

Phase 1 and later get their own `phase-NN-*.md` records; do not create
them before the phase begins.

## 2. Evidence labels (from Master Prompt §2)

Every claim in every record carries exactly **one** label:

| Label | Meaning |
|---|---|
| **Established** | Backed by a cited external source. |
| **Proposed** | A design decision that has been made but not implemented or verified. |
| **Hypothesis** | Needs a measurement or a formal proof before it can be trusted. |

An unlabeled claim is a Hypothesis by definition. Negative results are
recorded with the same care as positive ones.

## 3. Source grades (annotation, not an extra label)

Evidence discipline is only as good as its sources. Because Phase 12
forbids relying on vendor marketing, every citation also carries a
**grade**:

| Grade | What it is | Examples from Phase 0 |
|---|---|---|
| **A — Primary** | A specification, official documentation, official measurement dataset, court/regulator or platform-policy text, or the project's own recorded documents. | IETF RFC; Chromium/Chrome docs; W3C Recommendation; `sqlite.org`; Microsoft Learn; Apple Developer News; Google Play policy; HTTP Archive / CrUX; ITU; Electron docs; `docs.wasmtime.dev` |
| **B — Independent secondary** | Reputable reporting or an independent technical write-up that is not the vendor's own marketing. | MacStories, The Register, GNOME Wiki, an academic preprint |
| **C — Tertiary / vendor / marketing** | Blog comparisons, statistics aggregators, developer posts, SEO content. Useful for orientation and for finding A-grade sources — **never** sufficient on its own for a headline claim. | vendor comparison blogs, aggregators, `dev.to` posts |

Rules for grades:

1. **Established** requires a **grade A or B** source. A grade-C-only
   citation supports a **Hypothesis**, not an Established claim.
2. Where only grade C exists today, the record says so and names the
   A-grade check to perform (for example: "measure in E1", "read WebKit
   release notes in Phase 7").
3. Grades are recorded *beside* labels and never replace them. The three
   labels remain the only labels.
4. This convention is itself a recorded decision — see
   [`../docs/decisions/0001-source-grading.md`](../docs/decisions/0001-source-grading.md).

## 4. Citation format

- Records number their sources `[S1]`, `[S2]`, … in a **Sources** table
  at the end of the file: title, URL, publisher, grade, date retrieved
  (all Phase 0 sources were retrieved **2026-11-02**).
- A claim in a table carries the source number inline (`[S4]`) and its
  label in its own column. No claim without both.
- Numbers published by someone else are quoted **as published**, with
  their own date and population attached. "56% of origins" is not a
  claim about ZEMA.
- Third-party performance numbers are **never** reused as ZEMA numbers.
  ZEMA numbers come only from `experiments/EN-*/` raw data.

## 5. What Phase 0 did not do

Stated plainly so no reader over-reads this folder:

- **It did not import the research book** (Ch. 1–13). It is not in this
  repository and was not found in the owner's ten public repositories;
  see [`phase-00-05-book-import-audit.md`](./phase-00-05-book-import-audit.md).
  Therefore experiments **E3** and **Decision C** remain undefined.
- **It did not audit the adjacent `PlainP` repository's code.** Its
  existence is recorded as prior art; its claims are not adopted.
- **It ran no benchmark and no build.** Phase 0 has no build task by
  design. Every performance sentence in these records belongs to
  somebody else's measurement, cited as such.
- **It did not test anything with assistive-technology users.** That is
  Phase 8, and nothing in Phase 0 substitutes for it.
- **It did not choose a distribution channel.** That is Phase 11
  (Decision D), and Phase 0 only records the comparison axes.

## 6. Maintenance rules

1. One record per question. When a record is superseded, keep it and add
   a dated note at the top — do not delete.
2. Change the record's own version and add a row to its change log when
   its conclusions change.
3. Any new claim that leaves this folder **must** have a row in
   `docs/evidence-register.md` first.
4. Re-check phase-0 numbers at Gate 12: page-weight and browser-share
   figures age quickly and must be refreshed before any external use.
