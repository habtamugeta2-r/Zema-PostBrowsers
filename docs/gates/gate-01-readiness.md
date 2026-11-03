# Gate 1 Readiness Packet — Owner/reviewer actions only; no gate attempt

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 preparation |
| **Status** | **Preparation only** — no implementation, fixtures, review result, or gate attempt |
| **Evidence label** | **Proposed** for recommendations; **Established** for recorded conditions and repository state |
| **Source grade** | A — project-primary records: `docs/gates/gate-00.md`, decisions 0004/0008/0009/0010, and the Plain draft |
| **Purpose** | Put owner-controlled blockers and the three proposed scope/spec decisions in one response packet |

> **Do not treat this packet as a gate review or as authorization to build.**
> Gate 0 conditions C1 and C5 still block Phase 1 build; C2 is due before
> a Gate 1 attempt. No Gate 1 criteria have been tested.

## 1. Decisions ready for owner/reviewer response

For each item, select **Ratify**, **Revise**, or **Defer** and record the
name/date. A revision must include replacement wording or a pointer to a
new decision record. Silence is not approval.

| ID | Proposed decision | Consequence if ratified | Response |
|---|---|---|---|
| A-27 / decision 0009 | Pin the initial identifier/source profile to Unicode 17.0.0, UAX #31 rev43, UAX #15 rev57, UAX #9 rev51, UTS #39 rev32, and UTS #55 rev5, with a controlled, non-silent upgrade policy. | The profile is stable for implementation and fixture generation; the evidence/data version remains reportable. | ☐ Ratify ☐ Revise ☐ Defer — name/date: ____________________ |
| A-38 / decision 0009 | `Eq` is derived/sealed; `Ord` requires `Eq` and obeys stated total-order/equality-consistency laws; `Float` is neither; Map/Set/Hash stay deferred. | The Gate 1 type/evaluation profile has no unresolved generic equality/ordering rule. Laws remain review obligations, not a compiler proof. | ☐ Ratify ☐ Revise ☐ Defer — name/date: ____________________ |
| A-42 / decision 0010 | Gate 1 evaluates the hermetic Plain core only; later platform obligations remain binding and unwaived in their own phases. | Any eventual pass can claim only “Plain core passed Gate 1,” not platform security/completeness. | ☐ Ratify ☐ Revise ☐ Defer — name/date: ____________________ |
| A-44 / decision 0011 | Adopt UTS #55 rev5 chunk/C4 diagnostics, the independent UTS #39 General Security Profile warning, and the hashed Unicode 17.0.0 inputs. | PL1101/PL1104 behavior is precise and the profile is reproducible; conformance remains unrun. | ☐ Ratify ☐ Revise ☐ Defer — name/date: ____________________ |

## 2. Owner-controlled Gate 0 conditions

These cannot be completed by the research agent.

| ID | Required action | Recorded state | Owner response / evidence |
|---|---|---|---|
| C1 | Review and sign the frozen problem statement, target app class, and non-goals; record sign-off in `docs/gates/gate-00.md`. | Outstanding; blocks Phase 1 build. | Name/date: ____________________ |
| C5 | Rule whether PlainP is superseded, a donor, or an eventual home; record the decision in the project record. | Outstanding; blocks Phase 1 build. No code has been adopted. | ☐ Superseded ☐ Donor ☐ Eventual home ☐ Other: ______ — name/date: ______ |
| C2 | Import the research book, or explicitly authorize retirement of its chapter cross-references under decision 0004. | Outstanding; due before any Gate 1 attempt. | ☐ Import supplied at: ______ ☐ Authorize retirement ☐ Defer (Gate 1 remains blocked) — name/date: ______ |

C4 (licensing) remains due before public release or third-party code
adoption. It is not silently waived by this packet; no third-party code
has been adopted. C3 remains due before Phase 5.

## 3. What this packet does not authorize

- No interpreter/compiler or conformance fixtures may be started until
  C1 and C5 are resolved.
- No Gate 1 review may be scheduled until C2 and the A-27/A-38/A-42/A-44
  proposals are ratified or revised.
- No Gate 1 result may be recorded until an executable core and the
  checked/optimized conformance suite pass the requirements in
  [`../plain/05-conformance-plan.md`](../plain/05-conformance-plan.md).
- No PlainP code may be copied or adopted without the required licensing,
  provenance, and owner decisions.

## 4. Gate 1 evidence that will be required later

This is a checklist of future evidence, not evidence already produced:

- [ ] C1 and C5 recorded; build authorization is clear.
- [ ] C2 recorded (book imported or chapter references retired).
- [ ] A-27/A-38/A-42/A-44 ratified or replaced by signed decisions.
- [ ] Core interpreter/compiler exists and is scoped to the accepted
  profile.
- [ ] Every in-scope rule has at least one fixture; no uncovered rules.
- [ ] Checked and optimizing profiles agree on all fixtures.
- [ ] Diagnostics fixtures cover every active registered code, including PL1101 and PL1104.
- [ ] Unicode 17.0.0 source files match their recorded SHA-256 values before use.
- [ ] Gate review states the tested scope and explicitly lists later
  platform obligations as untested and still binding.

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Assembled the owner/reviewer action packet after proposed decisions 0009/0010; no sign-off or gate result recorded. |
