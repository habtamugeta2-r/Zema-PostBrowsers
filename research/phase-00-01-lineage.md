# Phase 0 · Record 01 — Historical Lineage: From Hypertext to an Accidental Application Platform

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-00-01-lineage.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 → Gate 0 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for Gate 0 |
| **Evidence label** | Mixed — each row is labeled individually; see the legend below |

**Legend:** every row carries its label — **E** Established, **P**
Proposed, **H** Hypothesis — and a source number in brackets. Grades
(A/B/C) follow [`README.md` §3](./README.md#3-source-grades-annotation-not-an-extra-label).

---

## 1. Why this record exists

The Master Prompt's Phase 0 puts the lineage first for a reason: ZEMA is
allowed to replace *some* of the browser, and the only way to know which
parts is to know what each historical layer was actually solving. This
record is deliberately short on dates and long on **inherited
obligations** — the things that still have to be paid for after the
browser is gone.

## 2. Timeline and inherited obligations

| # | Era | What it introduced | What it got right | The obligation it hands ZEMA | Label | Source |
|---|---|---|---|---|---|---|
| L1 | 1945 — Bush's *memex* | Associative trails through a personal store of documents | Framed information retrieval as a *device*, not a filing cabinet; explicitly linked records by association rather than hierarchy | Any replacement must still answer "how do I get back to what I was looking at?" — history and linking are not optional features | E | [S1] |
| L2 | 1989 — Berners-Lee, *Information Management: A Proposal* | Distributed hypertext over existing networks; links between nodes; non-centralised growth | Solved "the information was not naturally organised into a tree" with a link, and did so without central control | Addressing, linking, and decentralized joining of independent systems are the *original* requirements, not web-era add-ons | E | [S2] |
| L3 | 1993–2000s — Mosaic, Netscape, Internet Explorer | Document browser model: URLs, back/forward, view-source, rendering of arbitrary HTML | Made the network legible to non-programmers; created the installed base | A document-oriented navigation model is what users will *expect*; ZEMA must decide which parts of it to refuse | P | [S3] |
| L4 | 1999–2015 — DHTML → Ajax → SPAs | Script-driven UI inside the document model; the page becomes an app | Proved interactive apps can ship over the network without installs | The browser became an application platform *without being designed as one* — which is precisely the mismatch ZEMA targets | P | [S3] |
| L5 | 2010s — Wasm, WebGPU, HTTP/3, PWAs, CSP | Native-grade code, GPU access, modern transport, installability, policy | Closed many of the gaps that a post-browser pitch would otherwise claim | The honest baseline is the **modern** web, not a caricature; most 2010s complaints have partial answers inside the browser | E | [S4], [S5] |
| L6 | 2015–present — Electron, Tauri, Flutter, React Native | Desktop/mobile app shells over web or custom rendering | Shipped millions of real apps; established the demand for one codebase | "One language, one runtime" is already a shipping product category, so novelty is not the argument — measured cost is | E | [S6], [S7], [S8] |
| L7 | 2017–present — sandboxed OS/Wasm runtimes (Wasmtime, seccomp/Landlock, CHERI research) | Untrusted code execution as an engineering discipline | Proved that containment is a *host* property, with quotas and explicit imports | ZEMA must reuse these mechanisms, not reinvent them; a new verifier is new attack surface | E | [S9] |

**What the timeline does *not* support.** Nothing in L1–L7 establishes
that an integrated language is faster, smaller, or easier. Those remain
**Hypotheses** (E1–E5, Phase 12).

## 3. The one structural finding of this record

> **The browser accumulated three different products in one binary: a
> document reader, a security and distribution platform, and an
> application runtime.** Every "post-browser" proposal to date has
> replaced the third while inheriting the first two — usually by shipping
> a browser (Electron) or borrowing the OS webview (Tauri). [S6][S7]

That reading is the load-bearing observation behind the Phase 0
catalog: ZEMA cannot simply say "the browser was for documents"; it has
to say, service by service, what it replaces and what it drops. See
[`phase-00-02-browser-services-catalog.md`](./phase-00-02-browser-services-catalog.md).

**Label: P (Proposed interpretation).** It is an interpretive synthesis
of cited facts, not a measured result.

## 4. Consequences recorded for later phases

1. **History and deep links are obligations, not features** (L1, L2) —
   they enter the UI/navigation design in Phase 6, not as a nice-to-have.
   *Label: P.*
2. **The baseline must stay modern** (L5) — Phase 12 baselines are
   web/PWA **and** native/Flutter builds on current runtimes; a baseline
   built on an obsolete stack would be a rigged comparison. *Label: P.*
3. **Novelty must not be claimed from the lineage** (L6) — the catalog
   records what already exists so that Phase 12 compares, not boasts.
   *Label: P.*
4. **Containment comes from the host** (L7) — feeds directly into Phase 3
   (interpreter/Wasm decision, Decision A) and Phase 5. *Label: P.*

## 5. Sources

| # | Source | Grade | Retrieved |
|---|---|---|---|
| S1 | Vannevar Bush, *As We May Think*, Atlantic Monthly, July 1945 — excerpt and bibliographic record: <https://www.livinginternet.com/i/ii_bush.htm> (also indexed at ACM DL: <https://dl.acm.org/doi/pdf/10.5555/636669.636692>) | B | 2026-11-02 |
| S2 | Tim Berners-Lee, *Information Management: A Proposal*, CERN, March 1989 — W3C historical archive: <https://www.w3.org/History/1989/proposal-msw.html> | A | 2026-11-02 |
| S3 | Master Prompt v1.1, Phase 0 "Historical lineage" and Phase 1–14 lineages (project record): [`../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md`](../docs/zema-master-prompt/ZEMA-Master-Research-and-Build-Prompt.md) | A (project record) | 2026-11-02 |
| S4 | MDN/CanIUse-derived summary of WebAssembly browser support, incl. all modern engines shipping in 2017 — <https://www.testmuai.com/learning-hub/webassembly-compatible-browsers/> | C (orientation only; A-grade check: CanIUse/MDN at Phase 3) | 2026-11-02 |
| S5 | Chromium, *Chrome Release Cycle* (two-week milestones, weekly security refreshes) — <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_cycle.md>; Chrome for Developers, *Chrome release channels* (auto-update on stable) — <https://developer.chrome.com/docs/automation-and-testing/release-channels> | A | 2026-11-02 |
| S6 | Electron documentation, *Security* (bundled Chromium/Node, sandboxing, context isolation) — <https://www.electronjs.org/docs/latest/tutorial/security> | A | 2026-11-02 |
| S7 | Tauri project documentation and comparison material (OS webview instead of bundled Chromium) — <https://v2.tauri.app/> ; size/memory figures cited only as Hypothesis in [`phase-00-04-prior-art.md`](./phase-00-04-prior-art.md) | C (figures) / A (architecture) | 2026-11-02 |
| S8 | Flutter, *Desktop support for Flutter* (stable Windows/macOS/Linux) — <https://docs.flutter.dev/platform-integration/desktop> | A | 2026-11-02 |
| S9 | Wasmtime, *Security* documentation (linear-memory sandboxing, capability-based WASI filesystem access) — <https://docs.wasmtime.dev/security.html> | A | 2026-11-02 |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created at Phase 0 with seven lineage rows, the structural finding, and four consequences for later phases. |
