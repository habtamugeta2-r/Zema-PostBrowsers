# ZEMA Vertical Trace — Concerns → Phases → Gates → Evidence

| Field | Detail |
|---|---|
| **Document** | The vertical trace: the only artifact that joins the three document layers |
| **Version** | 0.1.0 (draft) |
| **Date** | 2026-11-03 |
| **Phase / gate** | Spans Phase 0 → Phase 14. Every gate review is an input |
| **Status** | **Proposal + measurement.** The measured gaps below are Established; every proposed requirement is Proposed |
| **Evidence label** | **E** for the measured gaps; **P** for the conformance obligations proposed here |
| **Owner ratification** | **pending** — §4 proposes three new gate-review fields; adopting them is an owner decision |
| **Machine check** | `python3 tools/audit_phase01.py --check` now verifies that every concern has a row here, that every phase has a gate, and that a concern claimed *traced* really has an evidence row |

> **Why this exists.** The project holds its obligations in three separate
> places that never touch each other:
>
> | Layer | Artifact | What it holds | Measured |
> |---|---|---|---|
> | **Why** | [`00-Core-Concerns.md`](./00-Core-Concerns.md) | 19 concerns | 719 lines, ~4,500 words |
> | **What / when** | [Master Prompt](./ZEMA-Master-Research-and-Build-Prompt.md) | 15 phases, **50 gate exit criteria**, 66 research + 62 build tasks | 1,267 lines, ~6,700 words |
> | **Proof** | [`../evidence-register.md`](../evidence-register.md) | 123 evidence rows | 123 rows |
>
> **Nothing joins them.** The measurement that produced this document:
>
> - **3 of 19 concerns have any evidence row.** Concerns 1, 2, 4–10, 12–14,
>   16–19 have none — including Concerns 16, 17 and 18, which are the
>   *rules about how the project is run* and therefore the ones that must be
>   demonstrably in force.
> - **No gate document mentions a concern.** `docs/gates/gate-00.md` and
>   `gate-01-readiness.md` contain zero occurrences of "Concern".
> - **The Master Prompt never mentions "Concern".** The Concern → Phase map is
>   asserted only from the Concerns document's side, so it cannot be wrong
>   *visibly* — nothing on the phase side disagrees with it.
> - **Gate 1's own exit criteria appear nowhere.** The readiness packet re-derives
>   its own 9-item list and never restates the Master Prompt's 3 criteria.
>
> This is the same defect as the diagnostic gap, one level up. There, the
> specification named its rules but not its failure modes. Here, the project
> names its reasons, its schedule, and its evidence — and not the **edges
> between them**. Each layer is internally coherent. The chain is not
> connected, and a chain is only as strong as its joints.

---

## 1. The three layers and their actual coupling

| Coupling required | Where it should be asserted | What actually exists |
|---|---|---|
| Concern → Phase (which phase advances which concern) | Master Prompt phase headers | **Nothing.** 0 occurrences of "Concern" in 1,267 lines |
| Phase → Gate (which criterion proves which phase) | Gate sections in the Master Prompt | Exists — 50 criteria across 15 gates, in one direction only |
| Gate → Evidence (which rows discharge which criterion) | Gate review records | **Nothing.** No gate document names an evidence row |
| Concern → Evidence (is this concern still unproven?) | Evidence register | **3 of 19** concerns referenced |

Every arrow that points *downward from rationale to proof* is missing. The one
arrow that exists points sideways within a single document.

## 2. The measured trace

This table is generated from the Master Prompt, not typed. `traced` means "at
least one evidence row cites this concern".

| # | Concern | Phase(s) per Appendix A | Gate criteria in that phase | Traced? |
|---|---|---|---|---|
| 1 | Post-browser platform | 0, 11, 14 | 3 + 3 + 6 | **no** |
| 2 | One unified language | 1, 13 | 3 + 3 | **no** |
| 3 | Performance | 12 (+2,4,6) | 3 | yes |
| 4 | Language semantics | 1 | 3 | **no** |
| 5 | Reactive correctness | 2 | 3 | **no** |
| 6 | Execution & isolation | 3 | 3 | **no** |
| 7 | Memory & concurrency | 4 | 3 | **no** |
| 8 | Capability security | 5 (stub in 3) | 3 | **no** |
| 9 | UI / rendering | 6 | 3 | **no** |
| 10 | Text & i18n | 7 | 4 | **no** |
| 11 | Accessibility | 8 | 4 | yes |
| 12 | Data & replication | 9 | 3 | **no** |
| 13 | Networking | 10 | 3 | **no** |
| 14 | Delivery & adoption | 11 | 3 | **no** |
| 15 | Developer experience | 13 | 3 | yes |
| 16 | **Evidence discipline** | 12, every phase | 3 | **no** |
| 17 | **Stage gates** | every gate, 14 | — | **no** |
| 18 | **Named risks** | 14 | 6 | **no** |
| 19 | **Scope discipline** | 14, every phase | 6 | **no** |

**Coverage: 3 / 19.** The three that are traced are the ones with an obvious
metric (Concern 3 performance, 11 accessibility, 15 developer experience). The
four concerns in bold are the project's own governance rules; none is traced.

## 3. Three specific defects this measurement exposes

### 3.1 "Governs every statement" is enforced nowhere

Concern 16 states: *"Three labels govern **every** statement the project
makes."*

Measured, with a broad pattern that counts a bare `E (` or a `**E**` cell:

| Document layer | Documents | With any evidence label |
|---|---:|---:|
| Research records (`research/*.md`) | 13 | 9 |
| Evidence register | 1 | 1 |
| **Normative specification (`docs/plain/`)** | **10** | **0** |
| **Founding documents, Master Prompt, gates, decisions** | **26** | **0** |
| **All markdown, before this document** | **56** | **10** |

The research layer does this well — `phase-00-02`'s catalog carries a label on
all 30 rows. The layer that *defines the language* carries none. Every one of
the 100 normative rules is unlabeled, so a reader cannot tell an Established
rule from a Proposed one, and L-30's own contract does not apply to itself.

> **A correction to this document's first draft.** It claimed 1 of 55 documents
> carried labels, using a pattern that only matched table cells. It also gave
> Core Concerns as 11,000 words when the file is ~4,500. Both were typed from
> impression rather than measured. The real figures are 10 of 56, and the
> research layer's inline `E (…) / P (…)` labels are what the first pattern
> missed. The *conclusion* survives — the spec layer has none —
> but the number was wrong, and a wrong number is how this project's last four
> audits started. The lesson is PR-01 again: the pattern is part of the claim.

### 3.2 The same gate number means two different gates, 365 times

Concern 17 requires: *"When in doubt, write 'Book Gate 2' or 'Prompt Gate 8' —
never a bare 'Gate 2'."*

Measured: **7** uses of "Book Gate", **7** uses of "Prompt Gate", and **365**
bare `Gate N` references in the colliding range 0–5, where the book's six
milestone gates and the prompt's fifteen phase gates overlap. 259 of them are
`Gate 1` alone, which is *both* "a safe executable core" (Book) and "the
unified language" (Prompt).

The irony is that the rule exists, is stated correctly, and is violated by
three orders of magnitude — because it is a prose caution with no check behind
it. That is the same shape as the diagnostic gap: a stated convention that
nothing enforces, decaying silently.

### 3.3 Two of the eight named stopping conditions are unreachable

Concern 18 and Master Prompt Phase 14 define eight named risks with stopping
conditions. Occurrences outside the Master Prompt:

| Risk | Occurrences elsewhere |
|---|---:|
| Adoption or install friction too high | **0** |
| Platform or app-store restrictions apply | **0** |
| Security-maintenance capacity insufficient | 2 |
| Language scope explodes | 2 |
| Offline data loss observed | 2 |
| An existing solution is better | 2 |
| Performance hypotheses fail | 1 |
| Accessibility gaps remain | 1 |

A stopping condition that appears in exactly one file cannot be *checked* at a
gate — nobody reviewing Gate 7 is told to ask "has install friction become too
high yet?". Note the two at **zero**: they are the two conditions under which
the project should *stop*, and they are the two nobody outside the Master
Prompt has ever had to read.

## 4. What this document proposes (P)

Three fields added to the existing gate-review template
([`zema-master-prompt/templates/gate-review.md`](./templates/gate-review.md)),
which already has a "Stopping-condition check" section:

| # | Proposed requirement | Why this one |
|---|---|---|
| **VT-1** | Every gate review **MUST** name the concerns it advances and re-state each one's *current* proof status, copying the evidence row numbers. | This is the only arrow that reaches the top, and it is the arrow that is missing |
| **VT-2** | Every gate review **MUST** restate the Master Prompt's exit criteria **verbatim**, then mark each pass / fail / not-attempted. Re-deriving a local list is forbidden. | Gate 1's readiness packet already drifted into its own 9-item list; the template's "Exit criteria checklist" is free-form |
| **VT-3** | Every stopping condition **MUST** be re-read and answered at **every** gate, not only Phase 14. | Two of eight are named in exactly one file, so no review has ever had to consider them |

All three are cheap: they add fields to a template that already exists, and they
require no new document from any future phase.

## 5. What this pass deliberately does not do

| # | Not done | Why |
|---|---|---|
| 1 | Renaming the 365 bare gate references | Mechanical but large; it needs a decision on whether `Prompt Gate` or `Phase Gate` is the term, and a script that can tell which sense is meant — some are unambiguous from context, some are not |
| 2 | Adding `[E]`/`[P]` labels to 100 normative rules | This is a real specification change touching every rule; it needs owner ratification of the labelling granularity first (per rule? per clause?) |
| 3 | Writing evidence rows for the 16 untraced concerns | Most would be **H** — the concern is a goal, not a claim. Whether a *concern* should have an evidence row at all is a design decision I should not make unilaterally |
| 4 | Modifying the gate-review template | It is a controlled template; §4 proposes the change and waits |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 0.1.0 | Created. Measures the vertical trace: 3/19 concerns traced to evidence, 0 gate documents mentioning a concern, 0 phase documents mentioning a concern, 365 ambiguous bare gate references, 2 of 8 stopping conditions named in only one file. Proposes VT-1…VT-3. Corrects two of its own first-draft figures: label coverage 1/55 → 10/56 (both including this file), and Core Concerns 11,000 → ~4,500 words. |
