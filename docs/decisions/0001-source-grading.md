# Decision Record 0001 — Grade every citation A / B / C, in addition to the three evidence labels

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 / Gate 0 |
| **Status** | **Accepted** (methodological; easily reversible) |
| **Evidence label** | **Proposed** |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); project owner sign-off recorded as condition C1 at Gate 0 |

## Context

The Master Prompt's evidence discipline has three labels — Established,
Proposed, Hypothesis — and one rule: *"Established" means backed by a
cited external source*. Phase 0 immediately hit the limit of that rule:
a vendor comparison blog and a W3C Recommendation are both "cited
external sources," and treating them as equal is exactly how projects
end up shipping marketing numbers as results.

Phase 12 makes the problem urgent: it forbids unverified numbers, but
Phase 0 needs to record facts it cannot yet measure (browser share, page
weight, framework bundle sizes) *and* be honest about how much those
facts can bear.

## Options considered

### Option A — Keep three labels only; judge sources informally

- What it is: current practice; each author decides whether a source is strong enough.
- Security cost: none.
- Performance cost: none.
- Fit for ZEMA: **poor.** It is unreviewable. A reader cannot tell why one row is stronger than another.

### Option B — Add a fourth evidence label ("Well-sourced" / "Weakly sourced")

- What it is: extend the label set.
- Fit: **rejected.** The three labels are fixed by the founding documents and are permanent vocabulary. Adding a fourth invites redefinition of "Established," which is the one thing evidence discipline cannot survive.

### Option C — Keep the three labels and annotate source *strength* beside them

- What it is: **A** primary/official/spec/measurement; **B** independent secondary; **C** tertiary/vendor/marketing. Rule: `Established` requires grade A or B; a C-only citation can only support a `Hypothesis`.
- Security cost: none.
- Performance cost: one extra column of typing.
- Fit: high. It separates *what we claim* (label) from *how well we can support it* (grade), and it gives reviewers a mechanical check.

## Decision

**Choose Option C.** Every citation in `research/` and
`docs/evidence-register.md` carries a grade (A/B/C) beside its evidence
label. The three labels remain the only labels. The operative rule is:

> **Established requires an A- or B-grade source. A C-grade-only
> citation supports a Hypothesis.**

Where only C-grade sources exist, the record names the A-grade check
that will replace them (for example, "measure in E1", "read the WebKit
release notes in Phase 7").

## Consequences

- **Positive:** headline claims can no longer be laundered through a
  vendor blog; reviewers can audit the register by scanning one column;
  weak evidence remains visible instead of being softened in prose.
- **Negative / accepted costs:** more bookkeeping; grades are themselves
  a judgement, and a mis-graded source is a new failure mode. A grade
  never upgrades a claim by itself.
- **New obligations created:** the register's Gate 12 review now checks
  grades as well as statuses; any `Established` row resting on a C-grade
  source is a defect.
- **What would make us revisit this:** if grading becomes ritual (grades
  copied without checking), replace it with a rule that only A/B sources
  may be cited at all — a stricter, simpler discipline.

## Evidence

- Citations: definitions are documented in [`../../research/README.md` §3](../../research/README.md#3-source-grades-annotation-not-an-extra-label); applied throughout [`../../research/phase-00-02-browser-services-catalog.md`](../../research/phase-00-02-browser-services-catalog.md) and the register.
- Experiments: none — this is a recording convention, not a claim about ZEMA.
- Related records: [`0004-research-book-missing.md`](./0004-research-book-missing.md) (the same honesty problem, for missing sources rather than weak ones).
