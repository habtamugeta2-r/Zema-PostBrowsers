# Decision Record 0009 — Pin Unicode 17.0.0 for the initial Plain profile; make `Ord` require `Eq`; keep Map/Set deferred

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — specification decision by the agent; owner ratification reserved at Gate 1 |
| **Owner ratification** | **pending — A-27/A-38** — see [`README.md`](./README.md) for the status vocabulary |
| **Evidence label** | **Proposed** for the pin/laws; **Established** for cited Unicode facts |
| **Source grade** | A — Unicode primary specifications for version/profile facts; project-primary Plain rules and source-audit records for design context |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); Gate 1 reviewer/owner may ratify or overrule |
| **Resolves** | A-27 and A-38 in the derived ambiguity register |
| **Does not resolve** | C1, C2, C5, or A-42 |

## Context

Draft v0.2 left two technical questions open before Gate 1:

- **A-27:** which Unicode/UTS #39 data version and identifier profile does
  Plain pin?
- **A-38:** what are the `Eq`/`Ord` laws, and how can `Float.compare`
  coexist with `Float` not being `Eq`?

Both can be answered as specification decisions without starting build
work. Neither answer signs an owner gate condition.

## Decision 1 — Initial Unicode pin

Plain’s initial identifier/source profile pins:

- **Unicode 17.0.0** property data;
- **UAX #31 revision 43** for identifier syntax and conformance clauses;
- **UAX #15 revision 57** for normalization;
- **UAX #9 revision 51** for bidirectional processing used by UTS #39 skeletons;
- **UTS #39 revision 32** for skeleton/confusable data and mechanisms;
- **UTS #55 revision 5** for programming-language source-handling guidance.

The identifier profile remains the declared R1-2 profile:
`(_ | XID_Start) XID_Continue*`, NFC identifiers, preserved text-literal
data, and contextual name roles. Mixed-script/confusability diagnostics
are refined by decision 0011 to the UTS #55 revision 5 chunk algorithm.

### Why not “latest” automatically?

The audit used Unicode 17-era primary documents. Current Unicode pages
advertise newer revisions, but “latest” is a moving target. A language
identifier policy needs reproducible diagnostics and a controlled upgrade
path. Unicode 17.0.0 is the audited baseline for this draft.

### Upgrade policy

A Unicode data upgrade requires:

1. a dated decision record;
2. a diff of XID_Start/XID_Continue, normalization, bidi, skeleton, script, security-profile, and joining-context data;
3. regenerated normalization, bidi, confusable, and mixed-script fixtures;
4. a conformance rerun in both profiles;
5. an explicit statement of whether existing identifiers change meaning.

No silent data bump is allowed.

## Decision 2 — `Eq` and `Ord` laws

1. `Eq` is a **derived, sealed** capability in the Gate 1 core. A type is
   `Eq` only when all components are equality-capable. User `impl Eq` is
   rejected (`PL0231`). This prevents bypassing the `Float`/function
   exclusion by writing a custom equality instance.
2. `Ord` **requires `Eq`**. An `Ord` implementation must be a total order
   consistent with equality:
   - reflexivity: `compare(a,a) == Equal`;
   - totality: exactly one of `Less`, `Equal`, `Greater` for every pair;
   - antisymmetry: `compare(a,b)` and `compare(b,a)` are opposites;
   - transitivity;
   - equality consistency: `compare(a,b) == Equal` iff `a == b`.
3. `Float` is **not `Eq`** and therefore **not `Ord`**. `Float.compare`
   remains an explicit Plain-specified ordering for callers that choose
   it, but it does not make `Float` a generic `Ord` type and is not IEEE
   754 `totalOrder`.
4. `Map`/`Set`/`Hash` remain deferred (D-19). When admitted, ordered
   collection keys/elements require `Ord`; hash collections will require
   `Eq` plus a future `Hash` law set.

The compiler can check the `Eq` prerequisite for `Ord`; it cannot prove
the order laws for user code. Those laws are review/conformance
obligations, not a claimed static guarantee.

## Options considered

### A-27 options

- **Pin the audited Unicode 17.0.0 baseline** — chosen.
- **Track latest Unicode automatically** — rejected: nondeterministic
  diagnostics and silent identifier changes.
- **ASCII-only identifiers** — rejected: contradicts the target app class
  and internationalization concern.

### A-38 options

- **`Ord` requires `Eq`; Float is neither** — chosen.
- **Allow `Ord` without `Eq`** — rejected: generic sorted collections and
  equality-consistent ordering become incoherent.
- **Make Float `Eq` using a total equality** — rejected for v0.2: it would
  silently conflate IEEE equality expectations with a language-defined
  equivalence and needs a separate design/measurement pass.

## Consequences

- A-27 and A-38 move from Open to Resolved (proposed) in the ambiguity
  register. A-42 remains open because it changes Gate 1 scope
  interpretation and needs owner/reviewer ratification.
- The diagnostic registry gains `PL0231` for user `impl Eq`.
- Map/Set remain unavailable in Gate 1; this is a scope decision, not a
  claim that the key-law problem is solved for all future collections.
- No interpreter, fixture, or gate result is produced by this decision.

## Sources

- [Unicode source audit, record 03](../../research/phase-01-03-primary-source-audit.md) — primary-source version checks and handling guidance (A).
- [Specification audit, record 05](../../research/phase-01-05-specification-audit.md) — Plain draft findings and proposed closure criteria (A, repository primary record).
- [Pinned source manifest](../../research/data/phase-01-source-manifest.json) — exact retrieved source versions, URLs, and hashes.
- [Unicode rules L-04/L-08](../plain/00-lexical-and-layout.md) and [T-26](../plain/01-types.md) — the normative proposals this record resolves.

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Proposed Unicode 17.0.0 pin and Eq/Ord law set; resolves A-27/A-38 as specification proposals. |
