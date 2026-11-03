# Phase 1 · Record 04 — Integrated Systems, Capability Prior Art, and `PlainP`

| Field | Detail |
|---|---|
| **Document** | `research/phase-01-04-integrated-systems-and-plainp.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1; answers Phase 0 hand-off Q1 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) |
| **Status** | Deep prior-art pass complete; no benchmark and no adoption decision |
| **Evidence label** | Mixed — per row; grades per [decision 0001](../docs/decisions/0001-source-grading.md) |
| **Source manifest** | [`data/phase-01-source-manifest.json`](./data/phase-01-source-manifest.json) |

> **Question.** Phase 0 asked which existing system is closest to ZEMA’s
> suspected intersection: one co-designed language, capability-mediated
> authority, no DOM, reactive state, and accessibility release-gating.
> This record answers with documented overlap, not with a universal
> negative. **No reviewed source establishes ZEMA’s measured superiority.**

---

## 1. Comparison matrix

“Not established” means the inspected sources do not establish the
property for that system. It does not mean the property is impossible or
that no other source could establish it.

| System | Integrated surface | Authority model | UI / DOM position | Accessibility evidence | Maturity / limit shown by sources | Label |
|---|---|---|---|---|---|---|
| **Newspeak + Hopscotch** | One message-based language with modules, live IDE, and Hopscotch reactive GUI fragments/presenters | Object-capability discipline: no static state; platform objects and aliens mediate access | Current implementation runs in the browser/Wasm and can be served as a PWA; Hopscotch has an HTML5 backend | GUI framework documented; inspected HTML backend has some `tabIndex` handling, but no AT-user release evidence in the reviewed sources | 2025 tutorial explicitly says the prototype provides **no security guarantees** and types are annotations, not enforced checks | E for documented architecture; H for any security/accessibility guarantee |
| **Monte** | Dynamic expression language with object message passing, auditors, and module imports | Object-capability discipline; `safeScope` excludes powerful objects; `DeepFrozen` auditors for exports | Web-server tutorial, not a co-designed client UI/layout language | Not established | Tutorial explicitly notes capability discipline does not address denial of service; vats need computation limits | E |
| **Unison** | Statically typed functional language, content-addressed code, effect abilities, cloud/distributed tooling | Abilities are algebraic effects with handlers; not equivalent to opaque host capabilities | No co-designed UI/layout surface established | Not established | Content addressing removes some name/order conflicts; it does not prove semantic compatibility | E |
| **Lamdera / Elm** | Elm frontend and backend, typed wire, persistence, migrations, deployment tooling | Platform/service boundary; backend JavaScript/ports restricted; not shown as capability-only authority | Browser target; Elm UI uses HTML/virtual DOM | Inherits Elm/browser accessibility route; no AT-release gate established | Official fit page states SaaS lock-in, no external database, vertical scaling limits | E |
| **Darklang** | Combined language, editor, and infrastructure for backends/CLIs | Current README says fresh install cannot touch files/network/processes/env until allowed | Not a client UI platform in the inspected README | Not established | README says dark-next is not production-ready; Classic is separate | E |
| **Skip** | Reactive backend services; TypeScript interfaces; Skiplang runtime; SKDB | Not established as capability-only | Backend/service focus, not one client UI language | Not established | Provides native and Wasm runtimes; Wasm runtime limited to 32-bit address space | E |
| **Flutter** | Dart application/UI framework with semantics tree and accessibility testing tooling | Platform sandbox/framework; capability-only authority not established | Native rendering on desktop/mobile; web target uses browser semantics/ARIA route | Official accessibility-testing docs describe semantics inspection and guideline checks | Shipping baseline, not evidence of ZEMA’s performance or accessibility | E |
| **Modern PWA/browser** | HTML/CSS/JS/Wasm plus browser services | Origin sandbox, permissions, CSP; not one language | Browser DOM by definition | Browser accessibility tree | Phase 0 already records distribution/security advantages; remains mandatory baseline | E (Phase 0 record) |
| **PlainP (owner work)** | Node-line PL prototype: parser/checker/runtime/SVG/derived a11y; separate function-based proposal | `needs` declarations + checker/runtime host checks; not opaque host-issued handles | SVG + local web preview, not production GPU/native window | Derived role/label tree; no OS bridge or AT-user evidence established | Python oracle runs; Rust port is parser/checker stage; CI success at pinned commit | E for inspected code/CI; H for production claims |

## 2. What the matrix changes

### 2.1 Newspeak is the closest architectural counterexample to “new intersection”

Newspeak/Hopscotch already combines a capability-disciplined language,
module platform objects, a reactive GUI framework, live tooling, and
browser/PWA deployment [S1], [S2]. It differs from Plain in important
ways: its current type annotations are not enforced, its prototype
explicitly disclaims security guarantees, and its reviewed UI backend is
HTML-based [S1]. Those differences are real, but they do not support a
claim that language + capability discipline + reactive UI is unoccupied.

**Consequence:** retire the universal-negative framing of evidence row
#057. Replace it with the bounded, checkable observation in #074: the
reviewed prior art already demonstrates these properties separately and
in partial combinations. Do not move the goalposts by adding more
adjectives until no prior art can match.

### 2.2 Capability discipline is not a resource-quota story

Monte’s tutorial is explicit: object-capability discipline restricts
authority, but it does not by itself address denial of service; vats need
a finite computation limit [S3]. Newspeak’s tutorial likewise separates
the capability foundation from the missing work of secure APIs, audits,
and binary formats [S1].

**Consequence:** Phase 3/5 must keep quotas, termination, parsing bounds,
and maintenance capacity as separate obligations. A capability type or
handle is not a sandbox proof.

### 2.3 Effect handlers and capabilities are orthogonal

Unison abilities let handlers interpret effect requests and resume the
computation [S4]. That does not mean a handler can mint host authority.
A host can still require an opaque capability before performing the
underlying operation.

**Consequence:** D-01 should be deferred for scope, inference, runtime,
and diagnostic complexity — not because handlers inherently “re-implement
a revoked capability.” The corrected rationale is recorded in the draft
spec and decision 0008.

### 2.4 Lamdera is the closest full-stack seam-removal baseline

Lamdera’s official material describes one Elm codebase for frontend and
backend, with hosting, deployments, migrations, networking, and
persistence handled by the platform [S5], [S6]. It also states the costs:
SaaS lock-in, no external database, vertical scaling, and restricted
backend JavaScript [S6].

**Consequence:** Phase 13 cannot compare Plain only against a fragmented
HTML/CSS/JS caricature. A feature-complete task app should include a
Lamdera/Elm-style integrated baseline where feasible, alongside the
required web/PWA and native/Flutter baselines. This is a recommendation,
not a new Gate 12 obligation imposed by this record.

## 3. Read-only `PlainP` audit

### 3.1 What was inspected

- Repository: `habtamugeta2-r/PlainP`
- Pinned commit: `af5ad2e7ff4fcba00a295dbbeb4c89125b598`
- License metadata: Apache-2.0 (metadata only; ZEMA license C4 is still open)
- CI: GitHub Actions run `41319261463`, conclusion `success` at that commit [S7].

Inspected files include README, docs 03/06/08, Python runtime/checker/
expression evaluator/AST/a11y/server, Stage-1 tests, and CI config. The
full byte hashes are in the source manifest. **No code was copied into
ZEMA, no PlainP test was run locally, and no PlainP benchmark is adopted.**

### 3.2 Established observations

| ID | Observation | Label | Evidence |
|---|---|---|---|
| PP-01 | The running prototype is the node-line PL language. The function-based Plain document is explicitly a proposal, not the syntax accepted by the current prototype. | E | README and doc 08 [S8] |
| PP-02 | Python is the spec-oracle; Rust production port has tokens/parser/checker slices, with runtime/scene/layout/paint listed as next/planned. | E | doc 06 §8 [S9] |
| PP-03 | Capabilities are represented as parsed `needs` declarations on the program AST. The checker validates literal network/storage use; runtime checks storage permission and network host/redirect targets. | E | `ast_nodes.py`, `checker.py`, `runtime.py` [S10] |
| PP-04 | The inspected authority mechanism is policy attached to the program, not an opaque, non-forgeable, host-issued handle with attenuation/revocation. | E (bounded to inspected code) | `Program.has_capability`, `Program.allows_network_url`, `_storage_allowed`, `_http_request` [S10] |
| PP-05 | Network code checks initial and redirect hosts, uses a 10-second timeout, retries safe GET/HEAD but not POST, and reads the response with `resp.read()` without an explicit response-size cap in the inspected function. | E | `runtime.py` [S10] |
| PP-06 | Accessibility is derived from scene nodes into role/label dictionaries, with button activatable/min-target metadata. The inspected module does not expose AT-SPI or prove keyboard/focus/IME/screen-reader behavior. | E (bounded) | `a11y.py` [S11] |
| PP-07 | The preview server documents POST mutation endpoints, session cookies, CSRF checks, origin checks, and a 64 KiB request-body cap; it is described as a local/sandbox developer preview, not a multi-tenant production host. | E | doc 06 §2 [S9] |
| PP-08 | Reactivity recomputes derivations on read; paint is SVG; text metrics are approximate. These are recorded prototype divergences, not the production Clear design. | E | doc 06 §6 [S9] |
| PP-09 | CI configuration runs Python tests, corpus check, formatter check, validate harness, Rust tests, and Rust corpus check; the pinned commit’s Actions run reports success. | E | CI file and Actions run [S7], [S12] |

### 3.3 What the audit does not establish

- It does not establish that PlainP is secure, production-ready,
  accessible to AT users, or faster than any baseline.
- It does not establish that no other file contains an OS accessibility
  bridge; it says the inspected artifacts do not prove one.
- It does not resolve C5. Supersede / donor / eventual home remains an
  owner decision.
- It does not satisfy C4. Apache-2.0 metadata on PlainP does not choose a
  license for ZEMA or authorize copying into an unlicensed project.

### 3.4 Donor candidates, if the owner chooses “donor”

These are **candidates for later review**, not adopted components:

1. The example corpus and diagnostic wording discipline.
2. The idea of deriving an accessibility view from the same scene tree.
3. The Python-oracle / Rust-port parity test pattern.
4. Preview-server request-hardening checks as a developer-tool baseline.

The Rust parser/checker is not a drop-in Plain core: PlainP’s current
node-line syntax and ZEMA’s expression/core-language draft differ. Any
donation needs C4, C5, a license/provenance record, and a mapping from
PlainP semantics to Plain rules before code is reused.

## 4. Recommendation to Gate 1

1. **Do not claim novelty by universal negative.** Keep #048 as the
   descriptive project claim; retire #057’s “no existing system” framing.
2. **Keep the stop condition alive.** The existence of close prior art
   raises the burden for Phase 12/13; it does not by itself prove an
   existing solution is better for the frozen task-list workload.
3. **Do not merge PlainP wholesale.** If C5 chooses donor, select small
   components after C4 and semantic mapping. If C5 chooses eventual home,
   record the repository move and spec reconciliation explicitly.
4. **Keep accessibility and security claims bounded.** Derived trees and
   capability declarations are useful prototypes, not release evidence.

## 5. Sources

| # | Source | Grade | Manifest / locator |
|---|---|---|---|
| S1 | Newspeak team, *The Newspeak Programming System*, 2025-07-11, §§1.5, 2, 4–6.2 | A | `newspeak-tutorial-2025` |
| S2 | Newspeak repository README and `HopscotchForHTML5.ns` | A | `newspeak-readme`, `newspeak-html-ui`, pinned commit |
| S3 | Monte, *A Taste of Monte: Hello Web* | A | `monte-taste`, pinned commit |
| S4 | Unison, *Introduction to Abilities* | A | `unison-abilities` |
| S5 | Lamdera compiler README | A | `lamdera-readme`, pinned commit |
| S6 | Lamdera, *Is it for me?* | A (official scope/limits) | `lamdera-fit` |
| S7 | GitHub Actions run for PlainP commit `af5ad2e…` | A (raw observation) | <https://github.com/habtamugeta2-r/PlainP/actions/runs/41319261463> |
| S8 | PlainP README and doc 08 | A (project record) | `plainp-readme`, `plainp-unified` |
| S9 | PlainP doc 06, Stage 1–3 prototype | A (project record) | `plainp-prototype` |
| S10 | PlainP `ast_nodes.py`, `checker.py`, `runtime.py`, `expr.py` | A (source inspection) | manifest entries, pinned commit |
| S11 | PlainP `a11y.py` | A (source inspection) | `plainp-a11y` |
| S12 | PlainP `.github/workflows/ci.yml` | A | `plainp-ci` |
| S13 | Darklang README | A | `dark-readme`, pinned commit |
| S14 | Skip README | A | `skip-readme`, pinned commit |
| S15 | Flutter, *Accessibility testing* | A | `flutter-a11y-testing` |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 1.0 | Deep prior-art matrix, Newspeak/Monte/Unison/Lamdera corrections, read-only PlainP audit, bounded recommendations. |
