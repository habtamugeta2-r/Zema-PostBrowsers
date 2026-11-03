# Decision Records

Every build / reuse / invent choice is recorded here as a numbered decision
record, copied from [`../zema-master-prompt/templates/decision-record.md`](../zema-master-prompt/templates/decision-record.md).
The rule is from the master prompt: *a decision that is not recorded did not
happen, and a decision record that is edited to look better is falsified.*

**Status vocabulary.** A decision has **two** independent states. Read both
before treating anything here as settled:

| Field | Values | Meaning |
|---|---|---|
| **Agent decision** | none · Proposed · Accepted | Whether the agent recorded a choice, and whether it was the agent's to make |
| **Owner ratification** | pending · ratified · revised · deferred | Whether Better-back accepted, changed, or deferred it |

A record whose status line says "Proposed" is **not** authorization. Open owner
actions are tracked in [`../gates/gate-01-readiness.md`](../gates/gate-01-readiness.md).

## Index

| # | Title | Agent decision | Owner ratification |
|---|---|---|---|
| [0001](./0001-source-grading.md) | Source grading (A/B/C) | Accepted | not applicable |
| [0002](./0002-target-os-linux.md) | Target OS = Linux (Ubuntu 24.04 LTS) | Proposed | **pending** (C3) |
| [0003](./0003-browser-service-strategy.md) | Browser-service strategy | Accepted | not required |
| [0004](./0004-research-book-missing.md) | Research book missing / E3 / Decision C | Accepted | not required now |
| [0005](./0005-language-surface-doctrine.md) | Language surface doctrine | Proposed | pending |
| [0006](./0006-type-and-evaluation-core.md) | Type and evaluation core | Proposed | pending |
| [0007](./0007-deferred-features.md) | Deferred-features register (20) | Proposed | pending |
| [0008](./0008-phase-01-research-and-draft-v02.md) | Continue Phase 1 as research; adopt v0.2 corrections | Proposed | pending |
| [0009](./0009-unicode-pin-and-eq-ord-laws.md) | Unicode pin (A-27) and `Eq`/`Ord` laws (A-38) | Proposed | **pending — A-27/A-38** |
| [0010](./0010-gate-1-core-scope.md) | Gate 1 core scope (A-42) | Proposed | **pending — A-42** |
| [0011](./0011-unicode-diagnostic-profile.md) | Unicode diagnostic profile (A-44) | Proposed | **pending — A-44** |
| [0012](./0012-directional-confusability-and-ucd-completeness.md) | Direction-aware confusability; 16-file input lock (A-45/A-46/A-47) | Proposed | **pending — A-45/A-46/A-47** |
| [0013](./0013-phase-1-reference-interpreter.md) | Python reference interpreter | Proposed | pending |
| [0014](./0014-unicode-data-pipeline.md) | Manifest-verified Unicode pipeline | Proposed | pending |
| [0015](./0015-conformance-runner-and-profiles.md) | Conformance runner, checked/optimized profiles | Proposed | pending |
| [0016](./0016-script-value-alias-input.md) | Script value-alias input (A-46 amendment) | Proposed | **pending** — blocks security calcs |

## Rules

1. Numbering is permanent. A superseded decision is kept and superseded *by* a
   later record; it is never deleted or renumbered.
2. A decision record's **Consequences** section describes the state when it was
   written. Later changes are added as a **dated note**; the original text stays
   (see [0010](./0010-gate-1-core-scope.md) and [0011](./0011-unicode-diagnostic-profile.md)).
3. A decision record may cite a rule ID; it may not redefine one. Rule text lives
   in [`../plain/`](../plain/README.md).
4. Nothing here is authorization by itself. Authorization is a gate result or a
   recorded owner response.
