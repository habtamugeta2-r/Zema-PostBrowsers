# Phase 0 · Record 03 — The Coordination Cost of Today's Fragmented Stack

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-00-03-coordination-cost.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → Gate 0 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for Gate 0 |
| **Evidence label** | Mixed; the central claim is a **Hypothesis** and is labeled as such throughout |

> **Bottom line up front.** The *existence* of a many-layer stack is
> **Established**. Whether that stack costs more than a unified
> alternative, for ZEMA's target app class, is a **Hypothesis** that only
> Phase 12/13 can settle. This record separates the two on purpose,
> because a founding document that conflates them has already lost the
> evidence argument.

---

## 1. What "the stack" means here

One production web app today typically carries, at minimum, these
independently-versioned layers:

| # | Layer | Typical artifacts |
|---|---|---|
| 1 | Structure | HTML templates / component markup |
| 2 | Style | CSS, preprocessor, utility framework, design tokens |
| 3 | Client logic | JavaScript/TypeScript, framework, state library, router |
| 4 | Build | bundler, transpiler, minifier, dev server |
| 5 | Dependencies | package manager, lockfile, supply-chain policy |
| 6 | Schema/contract | OpenAPI/GraphQL/protobuf/validation schemas |
| 7 | Server | application server, API handlers, job runner |
| 8 | Data | database, migrations, query layer |
| 9 | Deploy/config | containers, IaC, environment configuration, CDN rules |
| 10 | Cross-cutting | auth, accessibility, i18n, telemetry, error handling |

Ten layers, each with its own release cadence and its own failure modes.
*Label: E (layers exist) / P (that "ten" is the right decomposition).*

## 2. What is actually measured

These are other people's measurements, quoted as published. They are
**not** ZEMA measurements and they do not, by themselves, prove anything
about ZEMA.

| ID | Measurement | Value (as published) | What it establishes | Label | Src |
|---|---|---|---|---|---|
| CC-1 | Median page weight, desktop / mobile, October 2024 | **2,652 KB / 2,311 KB** | Shipped payloads are large and grew since 2022 (2,312 / 2,037 KB) | E | [S1] |
| CC-2 | Median JavaScript bytes per page, 2024 | **613 KB desktop / 558 KB mobile**; 2022: 509 / 461 KB | Client-side logic, not content, is a major and growing share of payload | E | [S1] |
| CC-3 | Median JavaScript requests per page, 2024 | **24 desktop / 22 mobile** (90th percentile: 68 mobile) | Even a simple page is assembled from many independently-fetched programs | E | [S1] |
| CC-4 | Composition of median desktop page | HTML 18 KB · CSS 78 KB · fonts 131 KB · **JS 613 KB** · images 1,054 KB | Images are the largest single component; JS is second — "the stack is heavy" is not only about framework bytes | E | [S1] |
| CC-5 | Origins passing all three Core Web Vitals | **55.9%** (May 2026), 54.4% (Dec 2025), 59.5% (Sept 2026) | Roughly **four origins in ten** fail responsiveness/loading/stability thresholds in field data — on the *modern* web | E | [S2] |
| CC-6 | Median page weight trend 2017 → 2024 | ≈1.2 MB → >2.3 MB | Direction of travel is heavier, not lighter | Established **only as C-grade** — needs an A-grade recheck at Gate 12 | [S3] |
| CC-7 | Bundle/memory cost of shipping a browser per app (Electron vs Tauri) | Electron typically 100 MB+ and hundreds of MB RAM; Tauri typically single-digit to low-double-digit MB and far less RAM | The per-app browser tax is real in direction | **H** — numbers come from C-grade vendor/comparison blogs and must be measured in Phase 12 | [S4] |

**Reading CC-1…CC-5 honestly:** they show that the *modern* web
frequently misses its own performance targets and that payloads have
grown. They do **not** show that the cause is the layer count, nor that
a unified language would fix it — a badly-written ZEMA app can be just
as slow. *Label: P.*

## 3. The coordination costs that are not bytes

The Master Prompt names the real problem as *coordination*: markup, style,
client code, server code, schema, query, build, and deploy must agree on
one behavior. The measurable proxies for coordination are weaker than
the byte measurements, and this record is explicit about that:

| ID | Coordination cost | How it shows up | Evidence status | Label |
|---|---|---|---|---|
| CC-8 | **Duplicate description of the same data** — a record must be described in the DB schema, the API schema, the client type, and the form validation | Drift causes runtime bugs that no single compiler catches | Structural argument; no dataset yet | H |
| CC-9 | **Contract negotiation between client and server** — versioning, backward compatibility, error shapes | Release coupling: two deployables must ship in compatible pairs | Structural argument | H |
| CC-10 | **Build and dependency surface** — supply chain, lockfiles, "works on my machine" | Median 22–24 JS requests [CC-3] is a *symptom* of assembled programs | Directional only | H |
| CC-11 | **Accessibility implemented twice** — once visually, once in ARIA/host APIs | Duplicate semantic trees drift; WCAG conformance is asserted, not tested | Structural argument; Core Concerns Concern 11 | P |
| CC-12 | **Tooling sprawl** — each layer has its own debugger, config, and upgrade treadmill | Developer time, not runtime bytes | Phase 13 task-log study is the only honest test | H |

## 4. Steel-manning the incumbent

The catalog and this record are only credible if they state the case
*against* ZEMA in the same voice.

1. **The stack exists because it solved real problems.** Separation of
   presentation, logic, and data let teams work in parallel and let
   organizations replace one layer without the others. Unification
   re-couples what decades of practice deliberately de-coupled.
   *Label: P.*
2. **The web's *outcomes* are extraordinary.** Six billion people online
   [S5], any link opens on any device, and the platform has absorbed
   Wasm, WebGPU, HTTP/3, and PWAs without a flag day [S6]. A replacement
   must beat *that*, not the 2009 web.
3. **Most page weight is content, not framework** — 1,054 KB of images
   versus 613 KB of JavaScript in the median desktop page [CC-4]. A new
   runtime does not shrink a photograph. *Label: E.*
4. **Frameworks are not overhead in the abstract.** They encode
   accessibility fixes, browser quirks, and security patches that a
   small team would otherwise rediscover. Removing them removes that
   accumulated knowledge too. *Label: P.*
5. **Existing "post-browser" tools already give developers one language**
   (Flutter, React Native, Tauri, Electron) and are widely adopted
   [S7]. The marginal gain of one *more* unified language must be shown
   against them, not against hand-written HTML. *Label: E (adoption) / H
   (marginal gain).*

## 5. What would falsify the project's cost story

Stated in advance, per the experiment template's rule:

1. **Falsifier F-1:** A controlled task-log study shows Plain developers
   are **not** faster than web or Flutter developers on the same
   spec-complete task-list app. → The developer-effort half of the bet
   fails (Phase 13).
2. **Falsifier F-2:** Equivalent-workload measurement shows no per-metric
   win on any of startup, interaction-to-present, memory, install size,
   or energy (Phase 12). → The performance half fails; publish and stop
   or simplify.
3. **Falsifier F-3:** Install friction causes abandonment at the rates
   the Gate 11 comparison suggests, with no viable pivot. → Distribution
   half fails; the pre-agreed pivot is browser-hosted Wasm.
4. **Falsifier F-4:** Accessibility parity cannot be reached with real
   assistive-technology users within the Phase 8 budget. → **Release
   blocked**, not "shipped with a plan".

Any of F-1…F-4 is a legitimate, publishable outcome under Concern 18.

## 6. Consequences recorded for later phases

- Phase 12 must define **equivalent workload** as *feature parity on the
  task list app*, including tests, migrations, accessibility, error
  handling, schema, configuration, and runtime code — and must publish
  raw data per metric.
- Phase 12 must **re-measure CC-1…CC-5 at the time of comparison**;
  citing a 2024 Almanac figure in 2027 would be dishonest.
- Phase 13 must use **task logs and maintainability exercises**, never
  line counts.
- No document may cite CC-7 (Electron/Tauri numbers) as a ZEMA result;
  it is prior-art orientation only.

## 7. Sources

| # | Source | Grade | Retrieved |
|---|---|---|---|
| S1 | HTTP Archive, *Web Almanac 2024 — Page Weight* (median 2,652 KB desktop / 2,311 KB mobile; 613 KB / 558 KB JS; 24 / 22 JS requests; composition) — <https://almanac.httparchive.org/en/2024/page-weight>; *JavaScript* chapter — <https://almanac.httparchive.org/en/2024/javascript> | A (primary measurement) | 2026-11-02 |
| S2 | Chrome UX Report, *Release notes* (origins with good Core Web Vitals: 55.9% May 2026, 54.4% Dec 2025, 59.5% Sept 2026) — <https://developer.chrome.com/docs/crux/release-notes/> | A | 2026-11-02 |
| S3 | Secondary summary of HTTP Archive page-weight trend 2017→2024 — <https://www.greadme.com/blog/performance/what-is-total-byte-weight-complete-guide> | C (orientation only) | 2026-11-02 |
| S4 | Vendor/comparison blogs on Electron vs Tauri size and memory — <https://rustify.rs/articles/rust-tauri-vs-electron-2026>, <https://www.buildmvpfast.com/blog/tauri-v2-vs-electron-desktop-apps-2026> | C (must be replaced by Phase 12 measurement) | 2026-11-02 |
| S5 | ITU, *Facts and Figures 2025* — <https://www.itu.int/en/mediacentre/Pages/PR-2025-11-17-Facts-and-Figures.aspx> | A | 2026-11-02 |
| S6 | Chromium, *Chrome Release Cycle* — <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_cycle.md>; WebAssembly browser support summary — <https://www.testmuai.com/learning-hub/webassembly-compatible-browsers/> | A / C | 2026-11-02 |
| S7 | Flutter desktop support (stable, Windows/macOS/Linux) — <https://docs.flutter.dev/platform-integration/desktop>; Electron documentation — <https://www.electronjs.org/docs/latest/tutorial/security> | A | 2026-11-02 |

## 8. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: 12 cost entries (7 measured, 5 structural), steel-manned incumbent case, four falsifiers, four consequences. |
