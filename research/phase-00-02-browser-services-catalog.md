# Phase 0 · Record 02 — The Browser-Services Catalog

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-00-02-browser-services-catalog.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → Gate 0 (deliverable: "Browser-services catalog with rebuild / interoperate / give-up decisions") |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for Gate 0 |
| **Evidence label** | Mixed — labeled per row/cell |
| **Ratified by** | [`../docs/decisions/0003-browser-service-strategy.md`](../docs/decisions/0003-browser-service-strategy.md) |

> **The rule this record follows.** Master Prompt Phase 0 forbids
> pretending the browser is only a renderer. Every service below is
> either **rebuilt**, **interoperated with**, or **explicitly given up**,
> and every give-up states its cost in the same row. A silent omission
> would be a false claim.

---

## 1. How to read the classification

| Class | Meaning | What it obligates ZEMA to own |
|---|---|---|
| **Rebuild** | ZEMA ships its own mechanism. | Design, implementation, **security review**, and a maintenance cadence. |
| **Interoperate** | ZEMA uses an existing standard or OS mechanism through the capability broker. | Conformance to someone else's spec, plus bounded parsing of whatever that mechanism hands over. |
| **Give up** | ZEMA provides no equivalent, and says so to users and reviewers. | Nothing technical — but the loss must be documented, measured where possible, and recorded as an accepted cost. |

Labels: **E** Established · **P** Proposed · **H** Hypothesis. Grades
(A/B/C) per [`README.md` §3](./README.md#3-source-grades-annotation-not-an-extra-label).
IDs `BSC-nn` are permanent row IDs; cite them as "BSC-04".

---

## 2. Group A — Distribution, identity, and reach

| ID | Service the browser provides | Class | What ZEMA does instead | Cost / accepted loss | Label | Src |
|---|---|---|---|---|---|---|
| BSC-01 | **Addressing and linking**: a URL identifies any resource; links are one-directional and unowned; back/forward history is universal. | **Interoperate (narrow) + Give up (broad)** | Interoperate: ZEMA consumes `https://` URLs for app discovery and for `zemalink:`-style deep links into *declared* app routes. Give up: universal addressability of arbitrary content and in-document anchors. | No linkable deep structure *inside* arbitrary app state; app authors must declare routes; no "view source" of a remote artifact. Back/forward semantics must be rebuilt per app shell (Phase 6). | E (browser offers it) / P (ZEMA's replacement) | [S1] |
| BSC-02 | **Zero-install distribution**: 6 billion people can open anything by receiving a link; no installer, no store, no admin rights. | **Give up** | A signed package plus a runtime the user installs once (Phase 11). | **This is the single largest accepted cost in the project.** Every comparison at Gate 11/12 must include install friction, and "adoption friction too high" is a named stopping condition. Mitigation path: browser-hosted Wasm pivot. | E (reach) / P (cost) | [S2] |
| BSC-03 | **Automatic security updates**: browsers ship a new milestone every two weeks and weekly security refreshes, silently. | **Rebuild** | Versioned manifests, signatures, anti-rollback, TUF-style verification, background update, revocation (Phase 11). | ZEMA inherits a *permanent* security-response duty: triage, patch, ship, revoke. If that capacity does not exist, the project's own stopping condition says **stop**. | E (browser cadence) / P (ZEMA duty) | [S3] |
| BSC-04 | **Shared standards and test suites** (WHATWG/W3C specs, and the cross-browser web-platform-tests suite). | **Interoperate (at the edges) + Give up (the model)** | Interoperate only where a standard already exists and is audited (TLS, Unicode, fonts, media containers). Give up the "any document renders the same everywhere" guarantee. | ZEMA's semantics are its own; there is no third-party conformance suite to catch regressions. ZEMA must build its own conformance suite (Phase 1) and its own compatibility discipline. | E (standards and WPT exist) / P (consequence) | [S4], [S15] |
| BSC-05 | **Installed base and network effects**: users already have the runtime; publishers already target it; content is discovered through it. | **Give up** | Nothing replaces network effects in a first release. Distribution is by explicit install, one workload, one OS. | Cold-start adoption. Recorded as a named risk with a pivot condition, not solved by engineering. | E | [S2] |
| BSC-06 | **Search indexing and discoverability**: public pages are crawled, ranked, and surfaced. | **Give up** | No general crawling. Mitigation only: a curated app directory and in-app search built by each app. | Public discovery of ZEMA apps is *pull* (someone tells you the link/package), not *push* (search finds you). Any product that depends on organic search is out of scope. | E | [S5] |
| BSC-07 | **Extension ecosystem**: third parties extend the runtime without forking it. | **Give up** | No extension API, no third-party runtime modifications in the first release. Extensions are an explicit research track (never a prerequisite). | No ad blockers, password managers, or enterprise extensions *of ZEMA's own*; those functions must exist as capabilities or host features instead. | P | [S4] |

## 3. Group B — Security and isolation

| ID | Service the browser provides | Class | What ZEMA does instead | Cost / accepted loss | Label | Src |
|---|---|---|---|---|---|---|
| BSC-08 | **A trust boundary per origin, plus a defense-in-depth policy language**: scheme/host/port triples are the unit of privilege; the same-origin policy governs object access, and Content-Security-Policy lets a document restrict its own loading and execution. | **Rebuild** | A different primitive: opaque, host-issued **capability handles** per resource, checked on every sensitive call, with attenuation and revocation (Phase 5); declared capabilities in Plain's types supply the *auditability* a CSP supplies to a page, and the host supplies the authority. | ZEMA must justify a replacement for the most scrutinized security model on the planet, with no equivalent body of public attack history. There is also no third-party-content injection problem to mitigate — which removes a whole class of CSP use, and removes CSP's *safety net* for mistakes in ZEMA's own policy. The capability model is **Proposed**, not proven, for this app class. | E (origin + CSP) / P (replacement) | [S1], [S18] |
| BSC-09 | **Process isolation and sandboxing**: separate OS processes, site isolation, OS sandboxes. | **Interoperate** | Reuse OS mechanisms (process separation; seccomp-bpf/Landlock on the chosen OS) and, if Wasm is chosen, a maintained engine's sandbox. | Conformance and hardening work stays with the OS/runtime, but ZEMA owns the *policy*: which handles exist, which quotas apply, and how termination works. | E | [S6], [S7] |
| BSC-10 | **TLS trust and the CA root store**: browsers ship and govern trust anchors, verify certificates, and revoke. | **Interoperate** | A reviewed TLS stack (e.g. rustls-class) plus a root-store policy borrowed from an existing program; full certificate verification is mandatory. | Root-store governance and incident response become ZEMA's problem, in a smaller organization. Weak fallback authority: no ability to override a broken CA for users. | E | [S8] |
| BSC-11 | **Permission prompts**: unspoofable, host-drawn consent for camera, mic, file access, notifications. | **Rebuild** | Host-drawn prompts bound to capability issuance, impossible for an app to imitate (Phase 5). | Prompt fatigue is a real usability risk; ZEMA must design attenuation so users are not asked repeatedly. *Hypothesis for later measurement.* | P | [S1] |
| BSC-12 | **Cross-site identity and SSO**: cookies, redirects, embedded login, third-party identity flows. | **Give up (ambient) + Interoperate (explicit)** | Explicit OIDC/OAuth-class flows through the network capability and the OS credential store; no ambient cookie identity across apps. | No "log in once and every site knows you"; embedded third-party login widgets are out of scope; enterprise SSO needs a deliberate design (Phase 10/11). | P | [S9] |
| BSC-13 | **Credential management, autofill, and payments**: password manager, form fill, saved cards, native payment sheets. | **Give up** | Delegate to the OS credential store; no ZEMA-run password manager, no payment instrument handling in v1. | Users lose browser-grade autofill convenience; commerce apps must integrate a payment provider themselves. | P | [S4] |
| BSC-14 | **Privacy controls**: cookie blocking, tracking prevention, fingerprint resistance, incognito. | **Rebuild (by construction) + Give up (some controls)** | Rebuild: no cookies, no cross-origin script, and a capability-gated network surface remove whole tracking classes by design. Give up: per-site privacy toggles and incognito modes as users know them. | Fewer knobs to explain, but also no familiar privacy vocabulary; ZEMA cannot claim privacy *benefits* until measured (Hypothesis). | H | [S6] |
| BSC-15 | **Enterprise management**: proxy configuration, certificate injection, policy control, managed deployment. | **Interoperate (OS settings) + Give up (browser policy engine)** | Follow the OS proxy and trust settings; ship a documented installer and policy file for later enterprise work. | Enterprise deployment is likely blocked in v1; the OS sandbox may conflict with TLS-inspecting proxies. Named risk for Gate 11. | P | [S8] |

## 4. Group C — Accessibility and text

| ID | Service the browser provides | Class | What ZEMA does instead | Cost / accepted loss | Label | Src |
|---|---|---|---|---|---|---|
| BSC-16 | **An accessibility API bridge**: a semantic tree exposed to screen readers, magnifiers, and switch access on each OS. | **Interoperate (mandatory)** | Feed AT-SPI (Linux), UI Automation (Windows), or NSAccessibility from the *same* semantic view tree that drives rendering; expose role, name, state, value, and actions for every control (Phase 8). | ZEMA owns the mapping and every regression in it. Compiler warnings and snapshot tools are aids, not proof; real AT-user testing gates the release. **Accessibility gaps block release — no exceptions.** | E (APIs exist) / P (ZEMA mapping) | [S10], [S11] |
| BSC-17 | **Internationalization services**: bidi, segmentation, line breaking, shaping, font fallback, IME, collation. | **Interoperate** | Reuse HarfBuzz-class shaping, ICU-class data, OS IME, and OS font stacks; select and edit by grapheme cluster (Phase 7). | ZEMA must prove the *integration*, script by script (E4), including Ethiopic, Arabic, Hebrew, Indic, CJK, combining marks, and mixed direction. | E (components exist) / H (integration quality) | [S12], [S13] |

## 5. Group D — Tooling and operations

| ID | Service the browser provides | Class | What ZEMA does instead | Cost / accepted loss | Label | Src |
|---|---|---|---|---|---|---|
| BSC-18 | **Developer tools and automation**: inspector, console, debugger, performance/memory panels, network inspection, remote debugging, automation. | **Rebuild** | A Plain language server, formatter, debugger, and a pipeline-stage profiler; plus a test harness and semantic-tree snapshots (Phases 6, 12, 13). | This is a multi-year product surface that browsers got from a 30-year accumulation. Its absence is a direct developer-experience cost and must be measured honestly (Phase 13), not asserted away. | E (browser surface) / P (ZEMA plan) | [S16] |
| BSC-19 | **OS integration**: clipboard, drag-and-drop, file open/save dialogs, printing/PDF export, notifications, system tray, and OS deep links. | **Interoperate** | Each is a capability granted by the host; on the chosen OS these are portal-mediated (file chooser, print, notification, open-URI) rather than ambient, and all inbound data is parsed with bounds checks (Phase 5, Phase 6). | Every one is a separate native integration on the chosen OS, and a portability cost if the OS changes. Printing is the most likely to be deferred — and must then be recorded as a give-up. | E (portal mechanism) / P (ZEMA plan) | [S17] |
| BSC-20 | **Media playback and DRM**: codecs, hardware decode, and a content-decryption module approved by studios. | **Give up** | No DRM. Media playback, if any, uses OS-provided codecs behind a capability. | Streaming-services apps, DRM video, and protected content are **out of the target class** and must be excluded from baselines and marketing. | P | [S4] |
| BSC-21 | **Crash recovery and error surfaces**: session restore, crash reporting, informative error pages. | **Rebuild** | A supervisor that restarts the UI shell and restores scene + state from the local store; a bounded crash-report pipeline (Phase 9, Phase 11). | ZEMA owns reliability engineering and its own error UX; no browser "Aw, Snap" page to blame, and no automatic crash telemetry unless deliberately built. | P | [S3] |

---

## 6. The three costs that dominate everything else

Recorded here so no later phase can pretend they are small.

1. **Install friction (BSC-02) is the existential cost.** The browser's
   real competitor is not Chromium the renderer — it is the fact that a
   link already works. *Label: E for the mechanism, H for ZEMA's ability
   to overcome it.* This is why Phase 11 exists before Phase 14, and why
   "pivot to browser-hosted Wasm" is a pre-agreed response.
2. **Security-update capacity (BSC-03) is a standing obligation.** A
   browser ships weekly security refreshes [S3]; ZEMA must ship them for
   its runtime *and* for every capability broker it writes. The project's
   own stopping condition — "security-maintenance capacity insufficient →
   stop" — is a direct reading of this row. *Label: P.*
3. **Tooling (BSC-18) and accessibility (BSC-16) are not free
   consequences of unification.** Both are named as obligations in Core
   Concerns (Concerns 2, 11, 15) and both must be resourced as products,
   not as side effects. *Label: P.*

## 7. Services deliberately left out of the first release

Not "forgotten" — scheduled as give-ups or research tracks, with the
gate that owns the decision:

| Service | Status | Owner |
|---|---|---|
| Extensions (BSC-07) | Research track only | Phase 14 |
| DRM media (BSC-20) | Permanent give-up | Phase 14 |
| Enterprise policy/proxy depth (BSC-15) | Give-up in v1; revisit if adoption requires it | Gate 11 |
| Payments and password management (BSC-13) | Delegate to OS/provider | Phase 11 |
| Cross-site ambient identity (BSC-12) | Give-up | Phase 10 |
| Search/discovery (BSC-06) | Give-up; directory only | Phase 11 |

## 8. Open questions handed forward

| # | Question | Phase that must answer it | Why it cannot be answered now |
|---|---|---|---|
| Q1 | Can a capability broker mediate every sensitive call on the task-list app without breaking the frame budget? | Phase 5 (audit) + Phase 12 (measurement) | Requires a working broker and a harness; Phase 0 has neither. |
| Q2 | Which single OS first, given accessibility testing and sandboxing? | **Gate 0** → decision 0002 | Needs an owner decision; recorded as Proposed. |
| Q3 | What exactly replaces back/forward history in a multi-view app? | Phase 6 | Depends on the scene graph and navigation model. |
| Q4 | Is a directory enough to make ZEMA apps findable, or does adoption require interop with an existing app store? | Phase 11 | Measurement and market reality, not design. |
| Q5 | Do the capability model's privacy properties actually beat browser tracking prevention? | Phase 12 | **Hypothesis** — must be measured, not asserted. |

## 9. Sources

| # | Source | Grade | Retrieved |
|---|---|---|---|
| S1 | RFC 6454, *The Web Origin Concept* (same-origin policy, protection domains) — <https://www.rfc-editor.org/rfc/rfc6454.txt> | A | 2026-11-02 |
| S2 | ITU, *Facts and Figures 2025* — about 6 billion people online (~74%) in 2025, 2.2 billion offline: <https://www.itu.int/en/mediacentre/Pages/PR-2025-11-17-Facts-and-Figures.aspx>; StatCounter desktop browser share (Chrome ≈65.7% desktop North America; Chrome ≈2/3 globally across aggregator summaries): <https://gs.statcounter.com/browser-market-share/desktop/north-america/2025> | A (ITU, StatCounter) / C (aggregator summaries) | 2026-11-02 |
| S3 | Chromium, *Chrome Release Cycle* (two-week milestones, weekly stable refreshes): <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_cycle.md>; Chrome for Developers, *Chrome release channels* (auto-update by default): <https://developer.chrome.com/docs/automation-and-testing/release-channels> | A | 2026-11-02 |
| S4 | Master Prompt v1.1 (Phases 0–14, scope rules, named risks): [`../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md`](../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md); Core Concerns v1.1: [`../docs/zema-master-prompt/00-Core-Concerns.md`](../docs/zema-master-prompt/00-Core-Concerns.md) | A (project record) | 2026-11-02 |
| S5 | Google Search Central documentation (crawling, indexing, ranking of public pages) — <https://developers.google.com/search/docs> | A | 2026-11-02 |
| S6 | Chromium, *Process Model and Site Isolation*: <https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md>; *Threat Model and Defenses Against Compromised Renderers*: <https://chromium.googlesource.com/chromium/src/+/master/docs/security/compromised-renderers.md> | A | 2026-11-02 |
| S7 | Wasmtime, *Security* (sandboxing, capability-based WASI filesystem access): <https://docs.wasmtime.dev/security.html> | A | 2026-11-02 |
| S8 | Rustls / webpki project documentation for a reviewed TLS implementation (no root-store governance assumed) — <https://github.com/rustls/rustls> | B | 2026-11-02 |
| S9 | OAuth 2.0 / OpenID Connect specifications (explicit delegated identity, no ambient cookie model) — <https://openid.net/connect/> | A | 2026-11-02 |
| S10 | W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, Recommendation 5 October 2023: <https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/>; publication history: <https://www.w3.org/standards/history/WCAG22/> | A | 2026-11-02 |
| S11 | Microsoft Learn, *UI Automation Overview* (Windows accessibility framework): <https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-uiautomationoverview>; GNOME Wiki, AT-SPI/ATK guide (Linux): <https://wiki.gnome.org/Accessibility(2f)Documentation(2f)GNOME2(2f)AtkGuide.html> | A (Microsoft) / B (GNOME) | 2026-11-02 |
| S12 | HarfBuzz text shaping engine (used by Chrome, Firefox, Android, GNOME, LibreOffice, and others): <https://github.com/harfbuzz/harfbuzz> | A | 2026-11-02 |
| S13 | Unicode Consortium, Unicode 16.0 (154,998 encoded characters, September 2024) — reported with the Consortium's release statement: <https://blog.emojipedia.org/whats-new-in-unicode-16-0/> | B | 2026-11-02 |
| S14 | Electron documentation, *Security* (prior art for the runtime's privilege surface): <https://www.electronjs.org/docs/latest/tutorial/security> | A | 2026-11-02 |
| S15 | web-platform-tests, *The web-platform-tests Project* (cross-browser conformance suite for the web platform): <https://github.com/web-platform-tests/wpt> | A | 2026-11-02 |
| S16 | Chrome for Developers, *Chrome DevTools — Overview* (inspector, console, sources/debugger, performance, memory, network, remote debugging): <https://developer.chrome.com/docs/devtools/overview> | A | 2026-11-02 |
| S17 | XDG Desktop Portal (file chooser, print, notification, OpenURI, screenshot, proxy resolver portals; per-file grants instead of ambient access): <https://github.com/flatpak/xdg-desktop-portal> | A | 2026-11-02 |
| S18 | W3C, *Content Security Policy Level 3* (Working Draft) and *Level 2* (Recommendation, 2016): a policy language restricting what a page may fetch or execute — <https://www.w3.org/TR/CSP/all/> | A | 2026-11-02 |

## 10. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: 21 services (BSC-01…BSC-21) classified rebuild / interoperate / give-up with costs; three dominant costs; six scheduled give-ups; five open questions. |
