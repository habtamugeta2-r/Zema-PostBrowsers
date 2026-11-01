# Improvement Record — ZEMA Master Prompt v1.1

| Field | Detail |
|---|---|
| **Date** | 2026-11-01 |
| **From** | v1.0 — original draft as pasted into the repository session |
| **To** | v1.1 — [`ZEMA-Master-Research-and-Build-Prompt.md`](./ZEMA-Master-Research-and-Build-Prompt.md) |
| **Principle** | Improve clarity, structure, and consistency. **Remove nothing of substance.** Every phase, research task, build task, and exit criterion from v1.0 is present in v1.1. |

This file is the *record* of the improvement pass, kept in the spirit of
the prompt's own instruction: **record everything.**

---

## 1. Structural improvements

| Change | Why |
|---|---|
| Added a document-control table (version, date, status, canonical location) | A 15-phase program needs to know which copy is authoritative. v1.0 had no version or status. |
| Added a full table of contents with anchor links | The document is long; readers could not jump to a phase or gate. |
| Added §3 *Guiding Principles* | v1.0's principles were scattered across phases (e.g., "correct before fast," "reuse before invent"). Collecting them in one place makes conflicts visible and resolvable. No new principle was invented — all seven are quotations or tight paraphrases of v1.0 text. |
| Standardized every phase to the same template: *Purpose → Historical lineage → Research tasks → Build tasks → Reuse vs. invent → Deliverables to record → Gate exit criteria* | In v1.0, Phase 14 used a completely different structure and several phases mixed invention notes into prose. A uniform template makes gate reviews mechanical and auditable. |
| Added a *Deliverables to record* list to every phase | v1.0 said "record everything" but rarely named the artifact. Each phase now states exactly what must exist in the repo before its gate. |
| Added a Mermaid diagram of the five-step loop | The loop is the project's core method; a picture makes the "gate can stop the project" branch unmissable. |
| Added Appendix A (glossary), Appendix B (what to record, and where), Appendix C (version history) | Terms such as "capability broker" and "glitch" were used before being defined, and "record everything" had no file-system home. |

## 2. Correctness and consistency fixes

| # | Issue in v1.0 | Fix in v1.1 |
|---|---|---|
| 1 | **Dual gate numbering.** Phase 8 ended with "Gate 2," Phase 11 with "Gate 3," Phase 12 with "Gate 4," Phase 14 with "Gate 5" — while Phase 2 also had a Gate 2. Phases 3–7, 9, 10, 13 had unnumbered gates. | One gate per phase, numbered to match (Gate 0–Gate 14). The four release-blocking gates keep their special status as *named milestone gates*: Gate 8 Accessibility Release Gate, Gate 11 Delivery Gate, Gate 12 Evidence Gate, Gate 14 Production Gate. A mapping note is included so old references still resolve. |
| 2 | **Broken numbering in the one-sentence summary.** It cited items "(1)", "(2)", "(4–15)", "(16–19)" — 19 items that do not exist in a 15-phase document (a leftover from the research book's chapter numbering). | Rewritten as one sentence citing phase numbers (Phases 1–3, 12, 1–11 & 13, 0/12/14), and the heading corrected to "One-Sentence Summary" (it is, now, one sentence). |
| 3 | **Unverified headline claim.** The title asserted ZEMA is "the world's first post-browser platform," which violates the document's own evidence discipline (Phase 12). | The phrase is retained as an aspiration but explicitly labeled a **Hypothesis** in an evidence note under the title, to be confirmed or retracted by the Phase 0 prior-art review. |
| 4 | **Duplicated capability broker.** Both Phase 3 and Phase 5 said "implement the capability broker," with no stated relationship. | Phase 3 now builds a *provisional broker stub* (so no prototype code path ever bypasses mediation); Phase 5 builds the *full, audited broker* that replaces it. Both phases cross-reference each other. |
| 5 | **Dangling references.** Tasks cited "§12.1 of the research book," "Ch. 6 metrics," "Chapter 7 format," etc., but the book is not in this repository and v1.0 never said so. | The cross-reference section now states plainly that the book is not yet in the repo, and makes locating/importing it (or marking it missing in the evidence register) an explicit Phase 0 responsibility. |
| 6 | **Unstated keyword force.** v1.0 mixed "must," "never," "no exceptions," and soft recommendations with no defined meaning. | Added RFC 2119 conventions (MUST / SHOULD / MAY) and applied MUST sparingly, only where v1.0's intent was clearly absolute (e.g., no raw FFI for guests; accessibility gates block release). |

## 3. Language improvements

- **Tightened the vision section** without changing its argument:
  "bolted an entire application platform onto a document renderer" and
  the Reading Age / Service Age framing are kept verbatim where they
  were already strong; redundant phrasing was trimmed.
- **Parallel structure:** checklist items now consistently begin with a
  verb (*Study…, Research…, Implement…, Build…*), and all exit criteria
  are checkable statements (`- [ ]`) rather than a mix of bullets and
  prose.
- **Spelling and naming normalized** to one convention throughout:
  US English (*color*, not *colour*), and correct product
  capitalization (*Vello/Piet*, *HarfBuzz*, *TechEmpower*,
  *IntelliJ IDEA*, `UITableView`, `RecyclerView`).
- **Dates and attributions regularized** in the historical lineages
  (e.g., "Bush 1945" → "Bush, 1945"); screen-reader chronology in
  Phase 8 put in true date order (JAWS 1995, VoiceOver 2005, NVDA 2006,
  TalkBack 2011).
- **Defined before use:** Wasm, PWA, FRP, IME, CRDT, CSP, and SDF are
  expanded at first mention; remaining specialist terms are in the new
  glossary.
- **Inclusive, precise wording:** e.g., Phase 8 testing now reads
  "including assistive-technology users *as testers*, not only as
  subjects of simulation."

## 4. What was deliberately **not** changed

- **No phase, task, or exit criterion was removed or weakened.** The
  uncompromising lines — *"Accessibility gaps block release. No
  exceptions."*, *"No composite scores. No unverified numbers."*,
  *"An existing solution is better — a valid outcome"* — are preserved
  (now bolded).
- **The scope is untouched:** one workload (task list), one desktop OS,
  local data + HTTP first, all eight named risks and stopping conditions,
  and the full deferred-features list.
- **The experiments keep their original IDs** (E1, E2, E4, E5). The gap
  at E3 is inherited from the research book; renumbering would break
  cross-references, so it is left for Phase 0 to resolve when the book
  is imported.
- **No new technical commitments were added.** Every "new" sentence in
  v1.1 is either navigation, definition, or an explicit statement of
  something v1.0 already implied. Where v1.1 makes an implied point
  explicit (e.g., the Phase 3 broker stub), this record says so.

## 5. Known open items for the next revision

These were noticed during the improvement pass but are **decisions for
the project**, not editorial fixes, so they are recorded here rather
than silently resolved:

1. **The research book is missing from the repo.** Import it or retire
   the chapter cross-references (Phase 0).
2. **Experiment E3 does not exist** in the prompt (E1, E2, E4, E5 only).
   Confirm whether E3 lives in the research book.
3. **"Decision A / B / D"** are referenced for Phases 3, 6, 11 with no
   Decision C. Same question as E3.
4. **The target desktop OS for Phase 14 is unnamed** ("pick one"). The
   choice affects Phases 5, 6, and 8 and should ideally be recorded at
   Gate 0, not at the end.
5. **No license** is stated for the project or this document yet.
