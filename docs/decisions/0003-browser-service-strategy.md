# Decision Record 0003 — Browser-service strategy: rebuild the runtime, interoperate with the OS, give up the network effects

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 / Gate 0 |
| **Status** | **Accepted** as Phase 0's classification; individual rows remain revisitable at their owning gates |
| **Evidence label** | **Proposed** |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); project owner sign-off at Gate 0 (condition C1) |
| **Ratifies** | [`../../research/phase-00-02-browser-services-catalog.md`](../../research/phase-00-02-browser-services-catalog.md) (BSC-01 … BSC-21) |

## Context

Master Prompt Phase 0 requires every browser service beyond rendering to
be classified **rebuild**, **interoperate**, or **admit giving up**, with
the cost recorded. The catalog does that row by row. This record states
the *rule* behind the rows, so that later phases classify new services
consistently instead of relitigating from scratch — and so that no later
phase can quietly reintroduce a service (an extension API, a plugin
format, an embedded webview) that Phase 0 gave up.

Three constraints force the shape of the rule:

1. **Concern 19 (scope):** one workload, one OS, local data + HTTP first.
2. **Concern 8 (authority):** only host-issued capabilities confer
   authority; types give auditability.
3. **Reality:** the browser's most valuable assets are not code. They are
   network effects — six billion users [S1], universal linkability [S2],
   and an update channel that patches the world weekly [S3].

## Options considered

### Option A — Reuse: build ZEMA as a shell over an existing engine/webview

- What it is: Electron/Tauri-style. Keep HTML/CSS/JS semantics inside, add
  a capability layer on top.
- Security cost: inherits the full web attack surface plus a JS bridge —
  the classic privilege-escalation seam, as Electron's own security guide
  documents [S4].
- Performance cost: inherits the DOM/CSS pipeline that Core Concerns
  Concern 3 identifies as the thing ZEMA is betting against.
- Fit: **rejected** — it makes Phases 1–6 unnecessary and abandons the
  only novel claim (one co-designed language).

### Option B — Invent: reimplement every browser service inside ZEMA

- What it is: own root store, own search index, own extension model, own
  media stack, own protocol.
- Security cost: enormous, unauditable by a small team; new trust anchors
  and new parsers everywhere.
- Performance cost: all maintenance, permanently.
- Fit: **rejected** — violates "reuse before invent" and the stopping
  conditions on security-maintenance capacity.

### Option C — Interoperate where someone else owns the mechanism, rebuild only what carries the bet, give up the network effects openly

- What it is: the catalog's three-way split.
- Security cost: bounded and *reviewable* — each reuse boundary is named.
- Performance cost: concentrated where ZEMA actually competes
  (state → layout → scene), not in TLS or font shaping.
- Fit: **chosen.**

## Decision

**Choose Option C**, applied by the following rule, in order:

1. **Does a standards body or the OS already own a correct mechanism?**
   → **Interoperate** (TLS, accessibility APIs, text shaping, IME, fonts,
   OS sandbox primitives, clipboard/file/print integration).
2. **Is the service part of ZEMA's actual bet — the language, the
   reactive graph, the scene graph, the capability model, the update
   path?** → **Rebuild**, with an explicit security review and owner
   (Phases 1–5, 11).
3. **Is the service valuable mainly because of network effects ZEMA
   cannot create?** → **Give up**, in writing, with the loss stated to
   users (search, zero-install reach, extensions, ambient cross-site
   identity, DRM).

The three dominant costs accepted by this decision, in order of severity:

| Rank | Accepted cost | Catalog ID | Why it dominates |
|---|---|---|---|
| 1 | No zero-install reach | BSC-02 | The browser's real competitor is the working link |
| 2 | A permanent security-update duty | BSC-03 | A runtime that cannot ship weekly fixes must not ship |
| 3 | Tooling and accessibility as products | BSC-18, BSC-16 | Neither is a free consequence of unification |

## Consequences

- **Positive:** later phases inherit a default answer and a written
  rationale; scope disputes become "which class is this?" rather than
  "should we build it?"; the give-up list is public and cannot be
  discovered late by users.
- **Negative / accepted costs:** ZEMA gives up the features users most
  associate with "the web" (search, extensions, instant open, DRM video);
  each is recorded and must be communicated honestly at release.
- **New obligations created:**
  - Every **interoperate** row needs a conformance and bounded-parsing
    test (Phase 5/7).
  - Every **rebuild** row needs an owner, a security review, and a
    maintenance cadence (Phases 3–5, 11).
  - Every **give-up** row needs a user-facing statement and, where
    measurable, a cost measurement (Phases 11/12).
- **What would make us revisit this decision:**
  1. Gate 11 shows install friction is fatal → the pre-agreed pivot is
     browser-hosted Wasm (which re-imports BSC-04/05 in exchange for
     BSC-02).
  2. Phase 5 shows the capability broker cannot match the browser's
     sandbox without reusing more engine code than planned.
  3. Phase 8 shows the accessibility bridge is not achievable on the
     chosen OS → reopen 0002 before reopening this.

## Evidence

- Citations: see the catalog's Sources table (S1–S14) — in particular
  RFC 6454 (origins) [S2 in catalog], Chromium *Release Cycle* [S3],
  ITU 2025 [S2], Electron *Security* [S14], Wasmtime *Security* [S7].
- Experiments: none at Phase 0. BSC-14's privacy claim and BSC-11's
  prompt-fatigue claim are explicit Hypotheses (#047, #045 in the
  register).
- Related records: [`0002-target-os-linux.md`](./0002-target-os-linux.md),
  [`../problem-statement.md`](../problem-statement.md) §4.
