# ZEMA — Problem Statement (Frozen at Gate 0)

| Field | Detail |
|---|---|
| **Document** | Problem statement — the one-page definition of the problem ZEMA exists to solve |
| **Version** | 1.0 (frozen) |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → **Gate 0** |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner (Better-back) |
| **Status** | **Frozen at Gate 0**, subject to the recorded conditions in [`gates/gate-00.md`](./gates/gate-00.md). Changes require a new version and a recorded decision |
| **Evidence label** | Mixed — the problem framing is **Proposed**; every supporting measurement is cited and labeled in the Phase 0 research records |
| **Length** | About 520 words of prose, 828 words including the control block and reference tables (measured 2026-11-03 by `python3 tools/audit_phase01.py --verify`, which excludes this row so that editing it cannot move the number it quotes). The Master Prompt's "one page" constraint is applied to the prose; the tables are lookups, not argument |

---

## 1. The problem in one paragraph

The browser was built to **read documents**. It is now the world's default
**application platform**, and the mismatch is paid for by everyone who
ships software: one app is described in markup, styled in CSS, programmed
in JavaScript/TypeScript, modelled in a server language, constrained by a
schema, assembled by a build system, delivered by a deployment
configuration, and made accessible by a second, hand-written semantic
layer. The result is measurable: the median desktop page ships
**2,652 KB** (613 KB of it JavaScript, from ~24 requests) and only about
**56%** of origins pass all three Core Web Vitals in field data. **[E]**
*(Sources: HTTP Archive Web Almanac 2024; Chrome UX Report, May 2026 —
see [`../research/phase-00-03-coordination-cost.md`](../research/phase-00-03-coordination-cost.md).)*
Whether a unified alternative actually removes that cost is a
**Hypothesis**, not a finding.

## 2. What ZEMA is

**ZEMA is a research-and-build project for a post-browser application
platform:** a deliberately constrained, capability-secured client runtime
with one co-designed language (**Plain**) — one typed surface for state,
layout, logic, and accessibility — that replaces the browser *for a
defined class of interactive, data-driven service applications*. **[P]**

It is not a browser, not a framework, not an OS, and not a document
reader.

## 3. The class of applications it targets

An app is in the target class if **all** of the following hold:

1. It is **interactive and data-driven**: lists, forms, tables, filters,
   status transitions, and small frequent state changes.
2. It has **durable user data** that must survive crashes, with a local
   store and an optional server (offline tolerance is desirable, not
   required, in v1).
3. Its **UI is application-shaped**, not document-shaped: no arbitrary
   third-party markup, no in-app browser.
4. It is **delivered to a known audience** — a team, a company, a
   professional community — rather than to anonymous public traffic that
   must be found via search.
5. It is **required to be accessible**, not merely encouraged to be.

**Concrete examples** (first is the reference workload):

| # | App | Why it qualifies |
|---|---|---|
| 1 | **Task list** — add / toggle / filter / restart, local storage, capability broker | The Master Prompt's single reference workload; defines every gate's demo |
| 2 | Team issue tracker | Lists, filters, identity, offline reads |
| 3 | Support-desk console | Queues, assignment, conflict-prone updates |
| 4 | Inventory / stock-taking | Real business invariants (counts, uniqueness) |
| 5 | Appointment scheduling for a clinic | Identity, permissions, local data, accessibility-critical |
| 6 | Expense approval | Multi-step state, authorization, audit trail |

## 4. The class it explicitly does **not** target

| Non-goal | Why |
|---|---|
| General document browsing; rendering arbitrary HTML | The browser wins; replacing it is not the goal |
| A new internet protocol (**PlainProto** is deferred) | HTTPS + existing schema encodings first |
| Full offline collaboration / CRDT sync in v1 | Convergence does not preserve business invariants |
| Every OS, or mobile, in the first release | **One workload, one desktop OS** |
| DRM-protected media, streaming-services apps | Requires a content-decryption path ZEMA will not build |
| An extension ecosystem, public package registry, self-hosting | Research tracks at most; never prerequisites |
| A search engine or content-discovery platform | Network effects ZEMA cannot buy |
| Winning on a composite benchmark score | Per-metric evidence only; composite scores are forbidden |

## 5. What success would mean (all measurable)

ZEMA succeeds only if, on the **same feature-complete task list app**
(same tests, migrations, accessibility, error handling, schema, and
configuration), it can publish raw per-metric data showing a defensible
advantage over **both** a modern web/PWA build and a native/Flutter
build on at least: cold/warm start, interaction-to-present latency,
missed frames at 60/120 Hz, CPU/GPU time, memory, install/update size
(including the shared runtime), network bytes, and energy — **and** pass
digital-accessibility testing with real assistive-technology users — **and**
install, update, and verify signatures end to end. **[P]**

## 6. What failure means (and is allowed)

The project stops, narrows, or pivots — and publishes why — if any of
the following holds **[P]**:

- the security-maintenance capacity needed for a runtime does not exist;
- accessibility parity cannot be reached with real AT users;
- install friction outweighs the measured benefits, with no viable pivot;
- performance hypotheses fail under equivalent-workload measurement;
- **an existing web, PWA, Wasm, or native solution meets the problem
  better.**

That last outcome is a successful result of the research, not a defeat.

## 7. Freeze statement

Frozen at Gate 0 on **2026-11-02**. Frozen means: the target class, the
non-goals, and the success/failure tests do not change silently. Any
change requires a dated revision of this file, a decision record, and a
gate at which it was made.
