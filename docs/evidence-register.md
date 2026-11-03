# ZEMA Evidence Register

| Field | Detail |
|---|---|
| **Document** | The running register of every claim the project makes |
| **Version** | 1.1 (Phase 1 audit) |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 0 → Gate 0 (deliverable: "Evidence register, populated with all claims made so far") |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Active — reviewed in full at Gate 12 (Evidence Gate) |
| **Template** | [`zema-master-prompt/templates/evidence-register.md`](./zema-master-prompt/templates/evidence-register.md) |

> **The rule.** A claim with no row does not exist; a row with no
> evidence is a **Hypothesis**. Retracted claims stay in this file
> forever — deleting a row is falsifying the record.

**Labels:** **E** Established (cited external source, grade A/B) ·
**P** Proposed (decided, not yet implemented/verified) · **H** Hypothesis
(needs measurement or proof). Source grades A/B/C are defined in
[`../research/README.md` §3](../research/README.md#3-source-grades-annotation-not-an-extra-label)
and [`decisions/0001-source-grading.md`](./decisions/0001-source-grading.md).

**Status values:** `Open` · `Confirmed` (link the data) · `Retracted`
(link the data and a one-line reason) · `Superseded by #NNN` · `Blocked`
(cannot be tested yet — say why).

---

## A. Founding and headline claims

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 001 | "ZEMA is the world's first post-browser platform." | H → **retracted** | No source can establish a universal negative; prior art PA-1…PA-7 exists. See [`../research/phase-00-04-prior-art.md`](../research/phase-00-04-prior-art.md) §3 (A) | 0 | 2026-11-02 (claim dated 2026-11-01) | **Retracted at Gate 0.** Reason: other post-browser application platforms exist; "first" is unverifiable by survey and unusable in evidence terms. Use #048 instead |
| 002 | "An integrated language + runtime + state model + UI pipeline can deliver a measurably better combination of developer effort, responsiveness, resource use, security, accessibility, and distribution than comparable web and native alternatives." | H | Experiments E1–E5; Phase 12 equivalent-workload baselines | 0 → 12 | 2026-11-02 | Open — the project's central hypothesis |
| 003 | "Plain is 100× faster." (original draft headline) | H | No metric, baseline, or workload is named. Gate 12 must restate per metric or retract | 12 | 2026-11-02 | Open — **unfalsifiable as written**; must be restated per-metric or retracted |
| 004 | "A reactive update has a fixed per-signal cost." | H | Experiment E1 | 2 | 2026-11-02 | Open — expected to fail; retained to be tested, not assumed |
| 005 | "The cost of a reactive update is proportional to the affected work; there is no blanket O(1) promise." | P | E1; Master Prompt Phase 2 | 2 → 12 | 2026-11-02 | Open — current design position, not a measured result |
| 006 | "ZEMA saves battery versus web and native equivalents." | H | Phase 12 energy measurement (no method yet) | 12 | 2026-11-02 | Open |
| 007 | "A 70/25/5 allocation split (of cost/effort) holds." | H | No source; no definition of the three buckets in this repository | 12 | 2026-11-02 | Open — definition itself is unrecovered (book missing; see §F) |
| 008 | "Million-item lists render at 120 fps." | H | Experiment in Phase 6/12 with a stated item and frame budget | 6, 12 | 2026-11-02 | Open |
| 009 | "Removing the DOM layer yields measurable responsiveness gains." | H | E1, plus pipeline-stage measurement in Phase 6 | 2, 6 | 2026-11-02 | Open |
| 010 | "Compile-time-wired reactive dependencies reduce update cost versus runtime dependency tracking." | H | E1 | 2 | 2026-11-02 | Open |
| 011 | "A retained scene graph updated without diffing reduces per-update work." | H | Phase 6 per-stage measurement | 6 | 2026-11-02 | Open |
| 012 | "Small app packages amortizing a shared runtime reduce install/update size versus apps that bundle a runtime." | H | Phase 11/12 measurement | 11, 12 | 2026-11-02 | Open |

## B. Platform and market facts (Phase 0 research)

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 013 | "The browser is also a distribution and security platform, not only a renderer." | E | RFC 6454 (origin model) [A]; Chromium *Release Cycle* (security refreshes) [A] | 0 | 2026-11-02 | Confirmed — see [`../research/phase-00-02-browser-services-catalog.md`](../research/phase-00-02-browser-services-catalog.md) |
| 014 | "Chrome accounts for roughly two-thirds of global browser usage; Safari for roughly one-sixth; the rest is split among Edge, Firefox, and others." | E | StatCounter desktop series [A]; aggregator summaries [C] | 0 | 2026-11-02 | Open — refresh before any external use (Gate 12) |
| 015 | "About 6 billion people — roughly 74% of the world's population — used the internet in 2025; 2.2 billion remained offline." | E | ITU *Facts and Figures 2025* [A] | 0 | 2026-11-02 | Confirmed (as of the 2025 estimate) |
| 016 | "The median desktop page weighed 2,652 KB in October 2024 (mobile: 2,311 KB)." | E | HTTP Archive, Web Almanac 2024, Page Weight [A] | 0 | 2026-11-02 | Confirmed (for that measurement window) |
| 017 | "The median page ships 613 KB of JavaScript on desktop and 558 KB on mobile, from a median of 24 and 22 requests respectively." | E | HTTP Archive, Web Almanac 2024, JavaScript [A] | 0 | 2026-11-02 | Confirmed (for that window) |
| 018 | "Only about 56% of tracked origins passed all three Core Web Vitals in May 2026 field data." | E | Chrome UX Report release notes [A] | 0 | 2026-11-02 | Confirmed (52–60% across 2025–2026 releases) |
| 019 | "Median page weight grew from about 1.2 MB in 2017 to over 2.3 MB in 2024." | H | Secondary summary [C] only | 0 | 2026-11-02 | Open — needs an A-grade recheck before use (Gate 12) |
| 020 | "Electron bundles Chromium and Node.js into every app." | E | Electron *Security* docs [A] | 0 | 2026-11-02 | Confirmed |
| 021 | "Tauri uses the operating system's webview instead of bundling a browser engine." | E | Tauri v2 documentation [A] | 0 | 2026-11-02 | Confirmed |
| 022 | "Flutter supports desktop targets (Windows, macOS, Linux) on its stable channel." | E | Flutter *Desktop support* + *FAQ* [A] | 0 | 2026-11-02 | Confirmed |
| 023 | "Typical Electron apps are 100 MB+ and hundreds of MB of RAM, while typical Tauri apps are single-digit MB and far lighter." | H | Vendor/comparison blogs [C] | 0 | 2026-11-02 | Open — **must not** be used in any external comparison until measured in Phase 12 |
| 024 | "Android policy forbids downloading executable code outside Play, but permits interpreted code loaded at runtime (for example JavaScript in a WebView)." | E | Google Play *Device and Network Abuse* [A] | 0 | 2026-11-02 | Confirmed |
| 025 | "Apple's guideline 4.7 permits only HTML5/JavaScript mini apps as non-embedded software, and forbids exposing native platform APIs without Apple's permission." | E | Apple Developer News (2024 update) [A]; guideline text [B] | 0 | 2026-11-02 | Confirmed |
| 026 | "On iOS and iPadOS, Web Push is available to Home Screen web apps (from 16.4), not to ordinary browser tabs." | E | WebKit blog, *Web Push for Web Apps on iOS and iPadOS* [A] | 0 | 2026-11-02 | Confirmed |
| 027 | "Outside the EU, iOS browsers must use WebKit; from iOS 17.4 the EU permits alternative engines, and vendors have not widely shipped them." | E | MacStories coverage of iOS 17.4 [B] | 0 | 2026-11-02 | Confirmed (EU-only, with adoption caveat) |
| 028 | "WebAssembly is supported by all modern browsers." | E | CanIUse-derived summary [C] — upgrade needed | 0 | 2026-11-02 | Open — A-grade check (MDN/CanIUse) required in Phase 3 |
| 029 | "Wasmtime provides sandboxed execution with capability-based WASI filesystem access." | E | Wasmtime *Security* docs [A] | 0 | 2026-11-02 | Confirmed |
| 030 | "SQLite is the most widely deployed database engine and provides ACID transactions." | E | sqlite.org, *About SQLite* [A] | 0 | 2026-11-02 | Confirmed |
| 031 | "TUF specifies defenses against rollback, freeze, mix-and-match, and key-compromise attacks." | E | theupdateframework.io, *Security* [A]; TUF specification [A] | 0 | 2026-11-02 | Confirmed |
| 032 | "WCAG 2.2 became a W3C Recommendation on 5 October 2023." | E | W3C WAI, *What's New in WCAG 2.2* [A] | 0 | 2026-11-02 | Confirmed |
| 033 | "Windows exposes UI Automation as its accessibility framework; Linux desktops use AT-SPI." | E | Microsoft Learn, *UI Automation Overview* [A]; GNOME Wiki AT-SPI guide [B] | 0 | 2026-11-02 | Confirmed |
| 034 | "Unicode 16.0 encodes 154,998 characters (September 2024)." | E | Unicode Consortium release as reported [B] | 0 | 2026-11-02 | Confirmed (recheck current version in Phase 7) |
| 035 | "HarfBuzz is a widely deployed text-shaping engine (used in Chrome, Firefox, Android, GNOME, LibreOffice, and others)." | E | HarfBuzz repository [A] | 0 | 2026-11-02 | Confirmed |
| 036 | "Browsers ship a new milestone about every two weeks and refresh the stable channel weekly with security fixes." | E | Chromium *Release Cycle* [A] | 0 | 2026-11-02 | Confirmed — note: Chrome for Developers describes a monthly stable cadence; both are cited and the discrepancy is recorded |
| 037 | "A cross-browser conformance suite (web-platform-tests) exists for the web platform." | E | web-platform-tests project [A] | 0 | 2026-11-02 | Confirmed — ZEMA has no equivalent |
| 038 | "Landlock lets unprivileged Linux processes restrict their own ambient rights, stackable with seccomp-bpf." | E | Linux kernel documentation [A] | 0 | 2026-11-02 | Confirmed; feeds decision 0002 |

## C. Project decisions and rules (Proposed)

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 039 | "ZEMA targets interactive, data-driven service applications and explicitly not general document browsing or arbitrary HTML rendering." | P | [`problem-statement.md`](./problem-statement.md) §3–§4 | 0 | 2026-11-02 | Open — frozen at Gate 0, pending owner sign-off (C1) |
| 040 | "The first release is one workload (task list), one desktop OS, local data + HTTP." | P | Master Prompt Phase 14; [`problem-statement.md`](./problem-statement.md) §4 | 0 → 14 | 2026-11-02 | Open |
| 041 | "Accessibility gaps block release; no exceptions." | P | Master Prompt Gate 8; Core Concerns Concern 11 | 8 | 2026-11-02 | Open — project policy, not a finding |
| 042 | "No composite scores; no unverified numbers." | P | Master Prompt Gate 12 | 12 | 2026-11-02 | Open — policy |
| 043 | "Effects in type signatures provide auditability; only host-issued capability handles provide authority." | P | Master Prompt Phase 5; catalog BSC-08 | 5 | 2026-11-02 | Open |
| 044 | "The rendering, text, database, and runtime layers are reused from maintained projects rather than invented." | P | Master Prompt Phase 6/7/9/14; catalog BSC-09/16/17 | 3–9 | 2026-11-02 | Open |
| 045 | "The capability broker can mediate every sensitive call on the task-list app without breaking the frame budget." | H | Phase 5 audit + Phase 12 measurement | 5, 12 | 2026-11-02 | Open |
| 046 | "Accessibility can be fed from the same semantic tree that drives rendering, so the two cannot drift." | P | Master Prompt Phase 6/8; catalog BSC-16 | 6, 8 | 2026-11-02 | Open — architectural intent, unverified until Phase 8 |
| 047 | "The ZEMA capability model gives users stronger privacy properties than browser tracking prevention." | H | Phase 12 measurement / threat-model review | 12 | 2026-11-02 | Open |
| 048 | "ZEMA is a capability-secured application runtime with one co-designed language, no DOM, and accessibility as a release criterion, aimed at interactive data-driven service applications." | P | Replaces #001; [`../research/phase-00-04-prior-art.md`](../research/phase-00-04-prior-art.md) §3 | 0 | 2026-11-02 | Open |

## D. Language and implementation claims (Hypotheses for later phases)

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 049 | "A safe, executable core of Plain can be specified and implemented within Phase 1's budget." | H | Phase 1 conformance suite | 1 | 2026-11-02 | Open |
| 050 | "Plain's syntax can be frozen at Gate 1 without feature creep." | H | Gate 1 review | 1 | 2026-11-02 | Open |
| 051 | "A small checked interpreter is an adequate provisional runtime for the task-list app." | H | Phase 3 decision record (Decision A) + isolation tests | 3 | 2026-11-02 | Open |
| 052 | "Structured concurrency with cooperative cancellation is sufficient for the target app class." | H | E2 | 4 | 2026-11-02 | Open |
| 053 | "SQLite-backed local storage survives crash recovery with zero loss within stated WAL guarantees." | H | E5 | 9 | 2026-11-02 | Open |
| 054 | "Content hashes support caching but do not prove semantic or version compatibility." | E | Core Concerns Concern 15 (project record); not independently sourced here | 11 | 2026-11-02 | Open — verify against a primary source (TUF/OCI) in Phase 11 |
| 055 | "An honest distribution model can combine URL-like low friction with signed-package security." | H | Decision D (Phase 11) | 11 | 2026-11-02 | Open |

## E. Prior art and relationship claims

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 056 | "Other post-browser application platforms already exist and ship (Electron, Tauri, Flutter, React Native, PWAs)." | E | Electron docs [A]; Tauri docs [A]; Flutter docs [A]; WebKit blog [A] | 0 | 2026-11-02 | Confirmed |
| 057 | "No existing system reviewed combines one co-designed language, a capability-only authority model, no DOM, and accessibility release-gating." | H | Orientation-depth survey only; Phase 1 deep review | 0 → 1 | 2026-11-02 | **Retracted 2026-11-03** — universal negative not supportable; replaced by bounded #074 and record 04 |
| 058 | "The owner's `PlainP` repository is an adjacent, separate platform, not the ZEMA research book." | E | Repository inspection via GitHub API [A] | 0 | 2026-11-02 | Confirmed |
| 059 | "ZEMA's relationship to `PlainP` (superseded, donor, or eventual home) is an open owner decision." | P | [`../research/phase-00-04-prior-art.md`](../research/phase-00-04-prior-art.md) §5, OQ-1 | 0 → 1 | 2026-11-02 | Open |

## F. Unrecovered / blocked claims

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 060 | "The research book (Chapters 1–13) exists and defines §12.1's ambiguity list, Ch. 6's benchmark protocol, and Ch. 7's R1–R29." | H | Not found in this repository or the owner's 10 public repositories; see [`../research/phase-00-05-book-import-audit.md`](../research/phase-00-05-book-import-audit.md) | 0 | 2026-11-02 | **Open — Blocked.** Owner must supply the book or authorize retiring the cross-references by Gate 1 (condition C2) |
| 061 | "Experiment E3 exists and belongs to the Ch. 9 performance cluster (H1–H3)." | H | Attested only by `00-Core-Concerns.md` Concern 3, itself a synthesis | 12 | 2026-11-02 | **Blocked** — its *definition* is unrecoverable; it must not be invented or renumbered |
| 062 | "Decision C exists." | H | No source names it; only A, B, and D are cited anywhere in this repository | — | 2026-11-02 | **Retracted as unattested** — reopen only if the book attests it |
| 063 | "The 70/25/5 split refers to a defined allocation of some resource." | H | No definition found | 12 | 2026-11-02 | **Blocked** — definition unrecovered (see #007) |

## G. Phase 1 language claims (all **Proposed** unless stated)

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 064 | "A language with no exception primitives and no null, carrying failure and absence in its types, can ship production applications." | E | Elm homepage “No Runtime Exceptions” and ports/guide [A] | 1 | 2026-11-02 | Confirmed **for Elm**; not evidence about Plain |
| 065 | "Kotlin's `when` has statement and expression forms, so whether a missing case is an error depends on form and version." | H | Kotlin docs for the expression form [A]; statement-form gap reported by a C-grade source [C] | 1 | 2026-11-02 | **Superseded 2026-11-03 by #078** — Kotlin 1.7 closes the enum/sealed/Boolean statement gap |
| 066 | "Plain's core can be specified completely in four documents, yielding 26 derived ambiguities and 18 recorded deferrals." | E | This repository: [`./plain/`](./plain/) | 1 | 2026-11-02 | **Superseded 2026-11-03 by #082** — “completely” was false; v0.2 has 43 ambiguities, 20 deferrals, and open items |
| 067 | "Requiring NFC for identifiers prevents visually identical, byte-different names from aliasing." | P | Unicode normalization + UAX #31/UTS #39/UTS #55 (rule L-04) | 1 | 2026-11-02 | Open — identifiers only; text literals are not normalized (A-28); NFC does not stop all confusables |
| 068 | "Same-scope UTS #39 skeleton collision detection catches homoglyph identifier spoofing in code review." | P | UTS #39/UTS #55 (rule L-10); canonical skeleton is a versioned sequence-aware mitigation | 1 | 2026-11-02 | Superseded by #099 — LTR-only comparison is too narrow for the proposed code-identifier policy; retained as historical claim |
| 069 | "Checking integer arithmetic in every build profile eliminates build-mode-dependent program behavior." | P | Decision 0006, rules E-05/E-36 | 1 | 2026-11-02 | Open — conformance fixture required (both profiles) |
| 070 | "Checked arithmetic costs measurable performance in hot loops." | H | E1/E2 (Phase 2, Phase 4) | 1 | 2026-11-02 | Open — must be measured, and must not be traded for a silent semantic switch |
| 071 | "Capturing immutable bindings by value and rejecting `mut` capture prevents late-binding closure bugs by construction." | P | Rule E-17 | 1 | 2026-11-02 | Open |
| 072 | "Expression-only exhaustive matching prevents missing-case runtime bugs." | P | Rule E-23 (sealed unions, T-10) | 1 | 2026-11-02 | Open — conformance fixture required |
| 073 | "IEEE 754 binary64 cannot supply a reflexive equality (NaN ≠ NaN, ±0), so `Float` must not be an `Eq` type." | E | IEEE 754 binary64 semantics as specified in rule E-08; IEEE 754-2019 [A] | 1 | 2026-11-02 | **Retracted as overclaim 2026-11-03** — IEEE fact retained in #079; Plain’s design choice is #080 |

## H. Phase 1 audit and primary-source corrections (2026-11-03)

| # | Claim (exact wording) | Label | Source / experiment | Phase | Date added | Status |
|---|---|---|---|---|---|---|
| 074 | "The reviewed prior art already demonstrates language/UI integration, capability discipline, typed full-stack app seams, default-deny permissions, typed effects/content addressing, and derived accessibility semantics in separate systems and partial combinations; no reviewed source establishes ZEMA's measured superiority." | E | Research record 04: Newspeak/Hopscotch, Monte, Unison, Lamdera, Dark, Flutter, PlainP | 1 | 2026-11-03 | Confirmed as a bounded prior-art observation |
| 075 | "The 2025 Newspeak tutorial states that the current prototype provides no security guarantees and that types are annotations rather than enforced checks." | E | Newspeak 2025 tutorial §§1.5/2, pinned URL | 1 | 2026-11-03 | Confirmed |
| 076 | "In the inspected PlainP commit, authority is enforced through parsed `needs` declarations plus checker/runtime host checks, not through opaque non-forgeable host-issued capability handles." | E | PlainP `ast_nodes.py`, `checker.py`, `runtime.py` at `af5ad2e…`; record 04 PP-03/PP-04 | 1 | 2026-11-03 | Confirmed **bounded to inspected code** |
| 077 | "The inspected PlainP accessibility module derives role/label metadata from scene nodes; the inspected artifacts do not establish an OS assistive-technology bridge or AT-user release evidence." | E | PlainP `a11y.py` and docs; record 04 PP-06 | 1 | 2026-11-03 | Confirmed **bounded**; not a claim about every possible file |
| 078 | "Kotlin 1.7 made non-exhaustive `when` statements over enum, sealed, and Boolean subjects an error." | E | JetBrains Kotlin 1.7 compatibility guide, pinned commit | 1 | 2026-11-03 | Confirmed; supersedes #065 |
| 079 | "IEEE 754 binary64 equality is not reflexive for NaN and conflates -0.0 with +0.0." | E | IEEE 754-2019 semantics; Plain rule E-08 | 1 | 2026-11-03 | Confirmed (standard fact only) |
| 080 | "Plain excludes `Float` from structural `Eq` and defers Map/Set until key laws are resolved." | P | Rules E-08, T-26, D-19, A-38 | 1 | 2026-11-03 | Superseded by decision 0009: Eq/Ord laws proposed; Map/Set remain deferred |
| 081 | "UTS #55 recommends normalized identifiers for case-sensitive languages but says programming languages should not silently normalize string-literal contents." | E | UTS #55 revision 5 §3.1.1 | 1 | 2026-11-03 | Confirmed; adopted in L-04/A-28 |
| 082 | "Plain v0.1 contained 98 rules, 26 ambiguities, 18 deferrals, a 275-fixture planning sum mislabeled ≈285, grammar/prose contradictions, and no small-step semantics; v0.2 records 100 rules, 43 ambiguities, 20 deferrals, and 3 open pre-Gate-1 questions at that audit snapshot." | E | Repository audit record 05 and docs/plain v0.2 | 1 | 2026-11-03 | Confirmed as repository observation; not a quality claim |
| 083 | "The v0.2 operational-semantics document is a non-normative research draft, not an implementation, conformance result, or proof." | E | docs/plain/06-operational-semantics.md | 1 | 2026-11-03 | Confirmed |
| 084 | "The hermetic Plain core is deterministic and well-typed programs either produce a value or a defined fault." | H | Operational-semantics conjectures H-OS-1/H-OS-2; no proof or run yet | 1 | 2026-11-03 | Open — requires proof/review and conformance |
| 085 | "Lamdera's official fit page documents SaaS lock-in, no external database, vertical scaling limits, and restricted backend JavaScript." | E | Lamdera *Is it for me?* official page | 1 | 2026-11-03 | Confirmed as vendor-documented limits |
| 086 | "PlainP's GitHub Actions CI run at commit `af5ad2e…` completed successfully." | E | Actions run 41319261463 | 1 | 2026-11-03 | Confirmed raw CI observation; not a local rerun or benchmark |

---

| 087 | "Plain’s initial source/identifier profile pins Unicode 17.0.0, UAX #31 rev43, UAX #15 rev57, UAX #9 rev51, UTS #39 rev32, and UTS #55 rev5; data upgrades require a reviewed diff and conformance rerun." | P | Decisions 0009/0011; research records 03/05 and pinned source manifest | 1 | 2026-11-03 | Proposed language policy; owner/reviewer ratification pending |
| 088 | "In Plain, Eq is derived/sealed; Ord requires Eq and equality-consistent total-order laws; Float is neither Eq nor Ord; ordered collection keys will require Ord." | P | Decision 0009; T-26; E-08/E-09; D-19 | 1 | 2026-11-03 | Proposed language policy; laws are not statically proven |
| 089 | "Gate 1 is proposed to evaluate only the hermetic Plain core; success does not waive or establish later platform obligations." | P | Decision 0010; Master Prompt Phase 1; docs/plain/05-conformance-plan.md §5 | 1 | 2026-11-03 | Proposed gate boundary; owner/reviewer ratification pending |

| 090 | "Featherweight Java is presented as a small calculus that omits many full-Java features to make rigorous type-safety arguments easier." | E | ACM publisher abstract for Igarashi, Pierce & Wadler, OOPSLA 1999, DOI 10.1145/320384.320395; record 05 [S1], grade B | 1 | 2026-11-03 | Confirmed as a statement of the paper’s abstract; not evidence for Plain’s feature scope or safety argument |

| 091 | "UTS #55 revision 5 defines identifier chunks through explicit Camel, HAT, and punctuation boundaries, and requires diagnosis of chunks meeting its mixed-script confusability test (C4)." | E | Unicode UTS #55 rev5 §§5.1.2.1–5.1.2.2 and C4, fetched 2026-11-03; grade A | 1 | 2026-11-03 | Confirmed as standard requirements; severity and Plain adoption remain separate design choices |
| 092 | "UTS #55 revision 5 recommends warning mechanisms for identifiers outside UTS #39's General Security Profile and recommends contextual treatment of ZWNJ/ZWJ." | E | Unicode UTS #55 rev5 §5.1.3 and UTS #39 rev32 §3.1.1, fetched 2026-11-03; grade A | 1 | 2026-11-03 | Confirmed as recommendation, not a claim that Plain already implements it |
| 093 | "Plain proposes UTS #55 C4-based chunk warnings (`PL1101`), interpreted with UTS #39 all-direction identifier confusability, plus an independent out-of-profile warning (`PL1104`)." | P | Decisions 0011/0012; proposed L-10/L-11; UTS #55 rev5 §§5.1.1–5.1.3 and UTS #39 rev32 §4 | 1 | 2026-11-03 | Proposed policy extension; owner/reviewer ratification and implementation/conformance remain pending |
| 094 | "Sixteen Unicode 17.0.0 UCD/security data and conformance files are pinned by immutable repository commit, Git blob IDs, byte lengths, and SHA-256 in the Phase 1 source manifest." | E | `research/data/phase-01-source-manifest.json`; Unicode Consortium's `unicode-org/unicodetools` repository, commit `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c`; source grade A for Unicode data, reproducible repository hash observation | 1 | 2026-11-03 | Confirmed; all 16 blob objects independently re-fetched and matched bytes, SHA-256, and Git blob ID. No file bytes vendored and no conformance suite run |

| 095 | "UAX #15 revision 57 and UAX #9 revision 51 correspond to Unicode 17.0.0; UAX #9 revision 52 corresponds to Unicode 18.0.0 and is excluded." | E | Unicode UAX #15 rev57 and UAX #9 rev51/rev52 version headers, retrieved 2026-11-03; grade A | 1 | 2026-11-03 | Confirmed; selected annexes align with the Unicode 17.0.0 data lock; rev52 excluded |
| 096 | "Plain’s bidi skeleton baseline should use UAX #9 revision 51 so the algorithm revision aligns with the pinned Unicode 17.0.0 UCD/security data." | P | Decision 0011; UTS #39 rev32 skeleton definition; UAX #9 rev51; source manifest | 1 | 2026-11-03 | Proposed, not implemented or conformance-tested |
| 097 | "UTS #39 rev32 §4 says to use LTR, RTL, and FS confusability for programming-language identifiers when single-script or single-directionality restrictions are inappropriate." | E | Unicode UTS #39 rev32 §4, definition of `bidiSkeleton(d, X)` and programming-language identifier guidance; retrieved 2026-11-03; grade A | 1 | 2026-11-03 | Confirmed as standards guidance, not proof of Plain implementation |
| 098 | "UTS #39 rev32 §3.1.1.1(B) permits ZWJ after Letter + Mn* + Virama + Mn-with-nonzero-CCC* only when the next character is not `Indic_Syllabic_Category=Vowel_Dependent`; A1/A2/B also impose single-script and NFC conditions." | E | Unicode UTS #39 rev32 §3.1.1.1(A1/A2/B); Unicode 17.0.0 `IndicSyllabicCategory.txt`; retrieved 2026-11-03; grade A | 1 | 2026-11-03 | Confirmed; missing from the original 15-file lock, added and pinned as file 16 |
| 099 | "Plain should treat identifiers as confusable if any LTR, RTL, or FS `bidiSkeleton` matches, and apply that relation to `PL0105` and the UTS #55 C4-based `PL1101` check." | P | Decision 0012; proposed L-10/L-11; UTS #39 rev32 §4; UTS #55 rev5 §§5.1.1–5.1.2.2; grade A for source guidance, Proposed for Plain policy | 1 | 2026-11-03 | Proposed policy extension; ratification, fixture verification, and implementation remain pending |
| 100 | "UTS #55 rev5 §5.1.3 recommends that an out-of-profile diagnostic be independently suppressible from confusable detection." | E | Unicode UTS #55 rev5 §5.1.3, retrieved 2026-11-03; grade A | 1 | 2026-11-03 | Confirmed recommendation; Plain proposes an independently suppressible `PL1104`, but the configuration mechanism is deferred and owner/reviewer ratification remains pending |

## Register summary (2026-11-03)

| Count | Value |
|---|---|
| Total rows | 100 (63 at Gate 0 + 10 Phase 1 draft + 27 Phase 1 audit/decision) |
| Established (E) | 49 |
| Proposed (P) | 22 |
| Hypothesis (H) | 29 |
| Retracted | 4 — #001, #057, #062, #073 |
| Superseded | 4 — #065, #066, #068, #080 |
| Blocked | 3 — #060, #061, #063 |
| Open headline claims that may **not** ship (Gate 12 rule) | #002, #003, #006, #007, #008, #023, #070 |

## Rules (copied from the template — do not weaken)

- Retracted claims stay in the register forever.
- When a Hypothesis is tested, update the **label and the status in the
  same commit** as the experiment record.
- Review the full register at **Gate 12 (Evidence Gate)**. No `Open`
  headline claim may ship.
- A claim with no row does not exist. Adding a headline claim to any
  document without adding its row here is itself a defect.

## Change log

| Date | Change |
|---|---|
| 2026-11-02 | Register created at Gate 0 with 63 rows covering every claim in the founding documents, the Phase 0 research records, and the planned decisions. #001 retracted; #062 closed as unattested; #060/#061/#063 blocked pending the research book. |
| 2026-11-02 | Phase 1 added rows #064–#073 for the language specification's claims (no-null/no-exceptions posture, identifier normalization and confusables, checked arithmetic, capture rule, exhaustiveness, `Float`/`Eq`, and the specification-completeness observation). #065 and #070 flagged as unverified. |
| 2026-11-03 | Phase 1 audit added #074–#086; retracted #057 universal negative and #073 overclaim; superseded #065/#066; corrected Elm/Kotlin/Unicode sources; summary recomputed. |
| 2026-11-03 | Independent Unicode profile audit added #097–#099; #068 is retained but superseded by #099; all 16 Unicode 17.0.0 data/test blob identities independently verified. |
