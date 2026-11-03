# Decision Record 0008 — Continue Phase 1 as research/specification work; adopt draft v0.2 corrections; keep Gate 1 closed

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — research method accepted by the agent. (C1/C5 were resolved on 2026-11-03, after this record was written; the decisions below still await ratification.) |
| **Evidence label** | **Proposed** for design corrections; **Established** for cited primary-source facts |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); owner decisions reserved |
| **Implements** | Research records 03–05; Plain draft v0.2 |

## Context

The user asked to “research in depth and continue your job.” The
repository’s active work is Phase 1, but Gate 0 conditions C1 and C5
still block Phase 1 build tasks, and C2 is due before Gate 1. The prior
research pass had useful language comparisons, but it also contained
outdated or overbroad claims and a draft specification that was not
implementation-ready.

The audit found:

- close prior-art overlap, especially Newspeak/Hopscotch and Lamdera;
- outdated Kotlin/Swift/Rust/Elm/Unicode citations;
- grammar/prose contradictions and missing productions;
- Unicode policies that would silently rewrite text data or exclude
  unicameral scripts;
- no small-step operational semantics;
- conformance targets that mixed Gate 1 core behavior with later-phase
  platform obligations.

## Options considered

### Option A — Start implementing the interpreter now

- **Rejected.** C1/C5 are unsigned. Starting build work would violate the
  gate discipline the project exists to enforce.

### Option B — Deepen research, correct the record, and repair the draft

- **Chosen.** This advances the “research” and “decide” halves of Phase 1
  without pretending the “build” or “gate” halves are complete.

### Option C — Stop until the owner supplies every missing artifact

- **Rejected.** Useful read-only research and specification repair can
  proceed now. Waiting would leave known false claims and contradictions
  in the record.

## Decision

1. **Keep the build gate closed.** No interpreter, compiler, conformance
   fixture, or Gate 1 attempt is produced by this pass.
2. **Adopt Plain draft v0.2 corrections** as proposed specification text:
   - identifiers are NFC; text literals are not silently normalized;
   - name roles are contextual, and case conventions do not exclude
     unicameral scripts;
   - grammar matches constructors, type parameters, bounds, record
     update, lambda annotations, and generic interface heads;
   - top-level user `let` is constant-only; local bindings are
     monomorphic;
   - `?` targets the nearest function and is forbidden in `defer`;
   - `defer` is block-local LIFO, with function early-return unwind;
   - pattern matching is partial and coverage-aware;
   - fault rollback is task-local, not external-effect rollback;
   - core determinism uses fuel/step quotas, not wall-clock semantics.
3. **Defer Map/Set/Hash (D-19) and core Unicode segmentation APIs
   (D-20)** rather than ship contradictory or phase-misplaced rules.
4. **Retire the universal-negative prior-art claim** (#057) and replace
   it with bounded observations (#074–#086). Do not claim ZEMA is novel
   because no reviewed system matches an ever-growing adjective list.
5. **Add a non-normative small-step semantics draft** and mark its
   determinism/soundness statements as conjectures, not theorems.
6. **Do not adopt PlainP code.** The PlainP audit is read-only. Any donor
   decision requires C4, C5, provenance, and semantic mapping.

## Open items as recorded on 2026-11-03 (subsequently addressed by proposed decisions 0009/0010)

| Item | Question | Owner |
|---|---|---|
| C1 | Approve the frozen problem statement/app class/non-goals | Project owner |
| C5 | Rule PlainP superseded / donor / eventual home | Project owner |
| C2 | Import the research book or authorize retiring its cross-references | Project owner |
| A-27 | Pin Unicode/UTS #39 data version and identifier profile | Language spec owner |
| A-38 | Resolve Eq/Ord laws and collection key constraints | Language spec owner |
| A-42 | Ratify Gate 1 core scope versus later platform obligations | Gate 1 reviewer / owner |

## Consequences

- The project record is more honest: prior art is closer than v0.1
  implied, and Plain’s remaining holes are explicit. Decisions 0009/0010
  subsequently propose resolutions for A-27, A-38, and A-42; those
  proposals do not substitute for owner/reviewer ratification.
- Draft v0.2 is closer to implementable, but it is still not frozen.
- At the time this record was written, Gate 1 was also blocked by the
  then-open spec questions. Decisions 0009/0010 now propose resolutions;
  owner/reviewer ratification and C2 remain prerequisites. That is a
  correct state, not a failure to “continue.”
- The next authorized build increment, once C1/C5 clear, is small:
  lexer/layout fixtures first, then parser, checker, evaluator. No large
  interpreter should be written before the open scope questions are
  settled.

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Decision recorded after primary-source audit, integrated-systems review, PlainP read-only audit, and specification repair. |
