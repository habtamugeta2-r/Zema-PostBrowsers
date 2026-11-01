# Evidence Register — TEMPLATE

> **How to use:** Copy this file to `docs/evidence-register.md` when
> Phase 0 begins. Add one row for *every* claim the project makes —
> in documents, talks, README files, and marketing copy alike.
> A claim with no row does not exist; a row with no evidence is a
> **Hypothesis**.

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 001 | _Example: "ZEMA is the world's first post-browser platform."_ | Hypothesis | Pending Phase 0 prior-art review | 0 | YYYY-MM-DD | Open |
| 002 | _Example: "A reactive update costs in proportion to affected work."_ | Hypothesis | Experiment E1 | 2 | YYYY-MM-DD | Open |

## Labels

| Label | Meaning |
|---|---|
| **Established** | Backed by a cited external source. Put the citation in *Source / experiment*. |
| **Proposed** | A design decision that has been made but not yet implemented or verified. Link the decision record. |
| **Hypothesis** | Needs a measurement or a formal proof before it can be trusted. Link the experiment that will test it. |

## Status values

`Open` · `Confirmed` (with link to data) · `Retracted` (with link to
data and a one-line reason) · `Superseded by #NNN`

## Rules

- Retracted claims stay in the register forever. Deleting a row is
  falsifying the record.
- When a Hypothesis is tested, update the label **and** the status in
  the same commit as the experiment record.
- Review the full register at Gate 12 (Evidence Gate). No `Open`
  headline claim may ship.
