# Decision Record 0010 — Define Gate 1 as a hermetic Plain core pass, not a platform-completion claim

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — scope recommendation by the agent; owner/reviewer ratification remains required |
| **Evidence label** | **Proposed** for scope; **Established** for repository phase/gate definitions |
| **Source grade** | Repository primary documents: Master Prompt Phase 1 gate text and derived conformance plan; supporting semantics and prior-art records are not external authority for project scope |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); Gate 1 reviewer/owner may ratify or overrule |
| **Resolves** | A-42 in the derived ambiguity register |
| **Does not resolve** | C1, C2, C5, nor any platform-phase gate |

## Context

The Master Prompt calls Gate 1 for a “safe executable core language” and
passing conformance suite. The conformance plan also allocates later
reactivity, supervision, capability, text-segmentation, and durable-I/O
work to other phases. Without an explicit boundary, a core pass could be
misreported as platform security or completeness, while expanding Gate 1
to include every later subsystem would contradict the phase plan.

## Decision

**Gate 1 evaluates only the hermetic Plain core**: lexer and layout,
grammar, type checking, local evaluation, patterns, closures, `?`,
`defer`, checked arithmetic, deterministic fuel faults, and diagnostics,
with the final operational-semantics document serving as a normative
cross-check after it is separately reviewed and promoted. It requires an
executable implementation and conformance suite for the declared core;
this decision does not itself produce either.

A Gate 1 result must be worded **“Plain core passed Gate 1”** or
**“Plain core did not pass Gate 1.”** It must not say or imply that the
runtime/platform is secure, complete, production-ready, or compliant with
later-phase obligations.

The following remain explicit obligations in their named phases and are
**not waived** by Gate 1:

- reactive transactions and glitch behavior (Phase 2);
- task supervision/isolation and host scheduling (Phases 3–4);
- real capability issuance, revocation, and sandboxing (Phase 5);
- text segmentation and shaping (Phase 7);
- durable I/O, authorization, and external-effect compensation (Phase 9).

Any host capability used in core tests is a deterministic test stub, not
evidence that the real broker satisfies Phase 5. Gate 1's fixture report
must separate core coverage from all platform obligations and explicitly
state the latter are not evaluated.

## Options considered

- **Hermetic core only, later obligations stay binding** — chosen; matches
  the Master Prompt's executable-core criterion and the phase allocation.
- **Require all later platform subsystems at Gate 1** — rejected; would
  collapse separately staged gates and require behavior not specified in
  the Phase 1 core.
- **Treat later obligations as optional or waived after Gate 1** —
  rejected; no evidence or authority supports waiving them.

## Consequences

- A-42 moves to **Resolved (proposed)**. The owner/reviewer must ratify
  or revise this scope before recording Gate 1.
- The conformance plan's core/platform split is the operational checklist
  for this boundary; coverage counts must not merge the two.
- The build remains blocked by C1/C5. C2 remains due before any Gate 1
  attempt. No interpreter, fixture, or gate result is created here.

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Proposed explicit Gate 1 core scope and non-waiver of later platform obligations. |
