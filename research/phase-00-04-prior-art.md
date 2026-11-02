# Phase 0 · Record 04 — Prior Art: Who Has Already Left the Browser

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-00-04-prior-art.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → Gate 0 (deliverable: catalog + evidence register; resolves the "world's first" claim) |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for Gate 0 — orientation depth only; Phase 1 must go deeper |
| **Evidence label** | Mixed; every row labeled |

> **Why this record is uncomfortable on purpose.** The Master Prompt's
> title note already downgraded "the world's first post-browser platform"
> to a Hypothesis and made Phase 0 responsible for confirming or
> retracting it. This record documents what already exists, and then
> recommends the retraction.

---

## 1. The candidates

| # | Project | What it replaces | Runtime model | Security model | Accessibility route | Label | Src |
|---|---|---|---|---|---|---|---|
| PA-1 | **Electron** | Desktop app chrome + web stack | Bundles Chromium **and** Node.js in every app; each app carries its own engine and patch cadence | Chromium sandbox + context isolation + its own permission handler; the app's own Node integration is the classic foot-gun, and Electron's own docs warn about it | Chromium's accessibility tree, exposed to OS APIs | E | [S1] |
| PA-2 | **Tauri** | Desktop app chrome, web UI, native core | Uses the **OS-provided webview** instead of bundling a browser; Rust core | Webview sandbox + capability/allowlist configuration for native commands | Whatever the host webview exposes | E (architecture) / H (size figures) | [S2] |
| PA-3 | **Flutter** | Mobile + desktop UI framework | One codebase, natively compiled, own widget/rendering layer; desktop support on stable for Windows/macOS/Linux | Framework-level; platform sandbox applies | Semantics tree bridged to each platform's accessibility API | E | [S3] |
| PA-4 | **React Native (and Windows/macOS ports)** | Mobile app UI, extended to desktop | JavaScript UI over native widgets | Platform sandbox | Native accessibility props | H (not audited this phase) | [S4] |
| PA-5 | **Progressive Web Apps** | Install-and-run from the web | Browser engine + service worker + manifest | Browser origin sandbox, CSP, permission prompts | Browser accessibility tree | E | [S5], [S6] |
| PA-6 | **Browser-hosted Wasm apps** (e.g. design tools) | Heavy client logic inside the browser | Wasm module in the browser sandbox | Browser sandbox + CSP; no ambient authority beyond web APIs | Browser tree (canvas-based apps must build their own) | H (widely reported; Phase 1 to cite specifics) | [S5] |
| PA-7 | **ChromeOS / kiosk shells** | Whole-OS app delivery around a browser | Browser *is* the app platform | Origin model | Browser tree | P | [S7] |
| PA-8 | **Adjacent owner work: `PlainP` (PLAIN / PL)** | Tries to replace HTML+CSS+JS with one indented language and a scene graph; Python spec-oracle + Rust engine in progress | Own parser/checker/renderer prototype (SVG output), own CLI | Capability checks in checker; preview server hardening recorded in its backlog | Derived accessibility checks in its backlog | E (repository exists and is described; **not audited**) | [S8] |

## 2. What each one teaches (and what none of them does)

| # | Lesson taken | Consequence for ZEMA |
|---|---|---|
| PA-1 | Bundling a browser per app is the most successful way to *avoid* the browser — 100 MB-class installs are apparently acceptable for many users | ZEMA cannot argue on size alone; it must argue per-metric and include install friction |
| PA-2 | Reusing the OS webview cuts the bundle but re-inherits the host engine's semantics and per-OS inconsistency | Reuse-first applies to rendering *and* to text/accessibility; "no DOM" is a design choice ZEMA must pay for |
| PA-3 | One codebase + native compilation + own rendering is a shipping, mainstream answer to "the stack is fragmented" | A "unified language" is not novel by itself; the novelty claim must be narrowed |
| PA-4 | The JS-to-native bridge pattern dominates mobile; desktop is a secondary target | Mobile is out of scope for the first release (one OS rule) |
| PA-5 | The browser can already be installed-to and run offline; iOS limits (WebKit-only outside the EU; push only after home-screen install since 16.4) show the *distribution* wall, not a rendering wall | Distribution is the hardest thing to beat — consistent with BSC-02 |
| PA-6 | The browser's sandbox is a *feature* that heavy apps happily accept | ZEMA's security story must be at least as strong as the browser's, or users will prefer the browser |
| PA-7 | Owning the OS-plus-browser is one path to post-browser; ZEMA deliberately does not take it | Scope boundary: ZEMA is an app runtime, not an OS |
| PA-8 | The same author already started a *different* unified platform with a running prototype | ZEMA must state its relationship to `PlainP` explicitly (see §5) rather than pretend it does not exist |

## 3. The headline-claim audit

Claim under test, verbatim from the Master Prompt's evidence note:

> *"ZEMA is the world's first post-browser platform."*

| Test | Result | Label |
|---|---|---|
| Do other systems replace the browser as an application-delivery target? | **Yes** — PA-1…PA-7 are shipping systems that run applications outside a browser tab (or deliberately replace the document model) | E |
| Does any of them combine one co-designed language + capability host + no DOM + compile-time reactive wiring + accessibility-release-gating? | **Not in the sources reviewed** — but this survey is orientation-depth, not exhaustive | H |
| Can "first" be established from a 7-item survey? | **No.** A universal negative across the entire industry cannot be established by this method | P |

**Recommendation, recorded for the gate:** **retract** the phrase "the
world's first post-browser platform" from all project material, and
replace it with a claim that can be tested:

> **Proposed replacement claim (v1.0):** *ZEMA is a capability-secured
> application runtime with one co-designed language, no DOM, and
> accessibility as a release criterion, aimed at interactive
> data-driven service applications.*

Even this narrower claim is **H** until Phase 1's deeper prior-art
review confirms no existing system occupies the same intersection.

## 4. What might genuinely be unoccupied

Recorded as a **Hypothesis**, with the evidence that would settle it:

| # | Suspected gap | Why it might hold | How to test | Label |
|---|---|---|---|---|
| U-1 | **One language that is simultaneously the state model, the layout model, and the logic** — without macros or code generation | PA-1…PA-5 all keep markup/CSS/JS or a widget DSL + host language in separate mental models | Comparative implementation of the task list app in one artifact per stack (Phase 13) | H |
| U-2 | **Compile-time-wired reactive dependencies feeding a retained scene graph directly** (no diff, no virtual DOM) | Mainstream systems largely diff or re-render; incremental approaches exist in research and niche frameworks | E1 raw data + a written comparison to at least two incremental systems (Phase 2/12) | H |
| U-3 | **A capability broker as the only path to authority, with type-level effects for auditability** | Even least-privilege app frameworks expose a broad native command surface (PA-2's allowlists) | Phase 5 attack tests + audit | H |
| U-4 | **Accessibility generated from the same semantic tree, gating the release from day one** | Most frameworks treat a11y as app responsibility; PA-3 bridges a semantics tree but does not gate releases | Phase 8 with real AT users | H |

If Phase 1 finds an existing system that already does U-1…U-4, the
honest outcome under Concern 18 is to say so and stop or narrow the
project — not to move the goalposts.

## 5. Relationship to the owner's adjacent `PlainP` work

An earlier, separate repository by the same owner describes a
"PLAIN" platform with its own language (PL), a rendering engine, a
scene graph, and Python/Rust reference implementations [S8]. Facts
recorded here:

- **E:** the repository exists, is public, and describes a running
  prototype with tests.
- **E:** it is **not** the ZEMA research book: its documents are
  design/architecture docs (00–08), not Chapters 1–13, and it contains
  no E1–E5 experiments or Decisions A–D as referenced by the ZEMA
  documents [S8], [S9].
- **P:** ZEMA does **not** adopt `PlainP`'s code or claims at Gate 0.
  No line of it has been reviewed, and no benchmark from it is used.
- **Open question OQ-1 (owner decision, Gate 0/Gate 1):** is `PlainP`
  (a) prior art to be superseded, (b) a donor for implementation
  components, or (c) the eventual implementation home of ZEMA? Choosing
  (b) or (c) would change Phase 1's starting point, and would need its
  own decision record.

## 6. Open questions handed forward

| # | Question | Phase |
|---|---|---|
| Q1 | Which existing system is closest to U-1…U-4, and what exactly does it lack? | Phase 1 (deep prior-art review) |
| Q2 | What are measured install/update sizes and cold-start times for Electron and Tauri builds of a comparable app? | Phase 12 (replaces all C-grade figures) |
| Q3 | What is the owner's ruling on `PlainP` (OQ-1)? | Gate 0 → Gate 1 |
| Q4 | Do PWAs already satisfy the target app class well enough to make ZEMA unnecessary? | Phase 11/12, with measured friction, not opinion |

## 7. Sources

| # | Source | Grade | Retrieved |
|---|---|---|---|
| S1 | Electron, *Security* (bundled Chromium/Node, context isolation, process sandboxing, permission handler) — <https://www.electronjs.org/docs/latest/tutorial/security> | A | 2026-11-02 |
| S2 | Tauri documentation — <https://v2.tauri.app/> (architecture: OS webview + native core; size/memory figures deliberately **not** cited as fact here) | A (architecture) | 2026-11-02 |
| S3 | Flutter, *Desktop support for Flutter* — <https://docs.flutter.dev/platform-integration/desktop>; *FAQ* (one codebase, native compilation, desktop on stable) — <https://docs.flutter.dev/resources/faq> | A | 2026-11-02 |
| S4 | React Native Windows project documentation — <https://microsoft.github.io/react-native-windows/> (not audited this phase; marked H) | B | 2026-11-02 |
| S5 | WebAssembly support across modern browsers — <https://www.testmuai.com/learning-hub/webassembly-compatible-browsers/> | C (orientation) | 2026-11-02 |
| S6 | MacStories, iOS 17.4 release coverage (third-party engines in the EU only; Home Screen web apps remain WebKit) — <https://www.macstories.net/stories/apple-releases-ios-and-ipados-17-4-with-major-safari-and-app-store-changes-in-the-eu-transcripts-for-podcasts-new-emoji-and-more/>; PWA capability summary on iOS (push since 16.4, home-screen install required) — <https://www.mobiloud.com/blog/progressive-web-apps-ios/> | B / C | 2026-11-02 |
| S7 | Chromium, *Chrome Release Cycle* and *Process Model and Site Isolation* (the browser-as-platform model ChromeOS builds on) — <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_cycle.md>, <https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md> | A | 2026-11-02 |
| S8 | `habtamugeta2-r/PlainP` repository, `README.md` and `docs/README.md` (PLAIN platform, PL language, Clear engine, Python/Rust prototype), inspected via GitHub API — status: described, **not audited** | A (as a repository fact) | 2026-11-02 |
| S9 | This repository's founding documents (research book absent; E1–E5 / Decisions A–D references) — [`../docs/zema-master-prompt/`](../docs/zema-master-prompt/) | A (project record) | 2026-11-02 |

## 8. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: 8 prior-art entries, 4 suspected gaps, headline-claim audit recommending retraction, `PlainP` relationship question OQ-1. |
