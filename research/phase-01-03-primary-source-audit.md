# Phase 1 · Record 03 — Primary-Source Audit and Specification Corrections

| Field | Detail |
|---|---|
| **Document** | `research/phase-01-03-primary-source-audit.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) |
| **Status** | Complete for this research pass. (C1/C5 were resolved on 2026-11-03; implementation is authorized. C2 and the A-* ratifications still block Gate 1.) |
| **Evidence label** | Mixed — each finding carries a label; source grades follow [decision 0001](../docs/decisions/0001-source-grading.md) |
| **Source manifest** | [`data/phase-01-source-manifest.json`](./data/phase-01-source-manifest.json) |

> **Scope.** This record re-checks the language prior-art claims in
> [`phase-01-01-language-prior-art.md`](./phase-01-01-language-prior-art.md)
> against primary sources, then compares those sources with Plain draft
> v0.1. It does **not** implement Plain, write conformance fixtures, or
> sign any Gate 0 condition. GitHub sources are pinned to commit SHAs in
> the manifest; live web sources are identified by URL, version, and
> retrieval date.

---

## 1. Findings that change the record

| ID | Finding | Label | Source | Consequence for Plain |
|---|---|---|---|---|
| PS-01 | Kotlin 1.7 made non-exhaustive `when` **statements** over enum, sealed, and Boolean subjects an error. The old “statement-form gap” is not a current Kotlin defect for those subjects. | E | [S1], [S2] | Correct register #065. Keep Plain’s expression-only `when` as a simplicity choice, not as a fix for a current Kotlin sealed-union hole. |
| PS-02 | Swift’s official book says every `switch` statement must be exhaustive and documents associated values. The prior C-grade Swift citation is replaceable. | E | [S3], [S4] | Replace the secondary Swift source. Do not claim Swift lacks exhaustive statement matching. |
| PS-03 | Rust’s current reference ties overflow checks to `debug-assertions`/`overflow-checks`, and separately says `MIN / -1` and `MIN % -1` checks occur even when overflow checks are disabled. | E | [S5] | Plain’s checked-in-all-profiles rule remains a real difference, but the comparison must be precise about Rust’s division edge case and flags. |
| PS-04 | Elm ports are typed in Elm as `Cmd msg` / `Sub msg` boundaries. The JavaScript implementation outside Elm is not checked by Elm’s type system. Calling the port itself “untyped” is inaccurate. | E | [S6], [S7] | Correct prior-art row L1. Plain’s capability-handle boundary is still different, but the difference is authority mediation, not “Elm has no typed boundary.” |
| PS-05 | Elm’s “No Runtime Exceptions” wording appears on the official homepage, not in the syntax reference cited by v0.1. | E | [S8] | Cite the homepage for that claim and the syntax/guide for syntax and ports. Do not generalize the slogan into a proof about every host interaction. |
| PS-06 | Unison abilities are algebraic-effect handlers: they interpret effect requests and resume computations. They are not, by themselves, host-issued object capabilities. | E | [S9], [S10] | Correct D-01’s rationale. Handlers and capabilities are orthogonal; deferring handlers is a scope/complexity decision, not a claim that handlers forge authority. |
| PS-07 | UAX #31 conformance requires identifying the specification version. Default identifiers are defined by D1/R1; adding `_` to Start is a declared profile, not unmodified R1-1. | E | [S11] | Plain must pin a Unicode version and declare its identifier profile before Gate 1. |
| PS-08 | UTS #55 recommends equivalent normalized identifiers for case-sensitive languages, but explicitly says programming languages should **not** silently normalize string-literal contents. | E | [S12] | Split L-04: NFC for identifiers; preserve text-literal data. Non-NFC text may be highlighted by tooling, not silently rewritten. |
| PS-09 | UTS #55 warns against making semantics depend solely on case because many scripts are unicameral. | E | [S12] | L-12’s case-based naming cannot remain a hard parse error for Ethiopic, Arabic, Hebrew, CJK, and other unicameral identifiers. Use declaration context for roles and diagnostics for style. |
| PS-10 | UTS #55 says the confusable skeleton operation is not a code-point-by-code-point mapping and recommends chunk-based mixed-script detection rather than blanket whole-identifier mixed-script warnings. | E | [S12], [S13] | Correct the prior research note and L-10/L-11. Treat skeleton as a versioned black box; compare visible names, including reserved words where relevant. |
| PS-11 | UAX #15 normalization is not closed under concatenation. | E | [S14] | Even if source literals are NFC, `Text.concat` can produce non-NFC text. A runtime “all Text is NFC” invariant would require re-normalizing every concatenation and changing user data; do not adopt it silently. |
| PS-12 | WebAssembly’s specification presents execution as an abstract machine with prose and formal reduction rules; a well-typed program terminates in values or a trap/exception. | E | [S15] | Use the same dual prose/reduction style for Plain’s core semantics. This is a specification method, not a runtime choice or a Wasm performance claim. |

## 2. Corrections applied to the prior-art record

The following are editorial/evidence corrections, not new language
features:

1. **Kotlin:** the sealed/enum/Boolean statement-form gap is historical.
   Current Kotlin still distinguishes statements from expressions for
   other subject types, but that is not the claimed sealed-union hole.
2. **Swift:** primary book sources replace the SEO/secondary citation.
3. **Rust:** cite the current reference, not only RFC 560 and a 2016 blog.
4. **Elm:** separate the homepage slogan, the syntax reference, and the
   typed port boundary.
5. **Unison:** remove “dependency conflicts structurally impossible” as
   an overclaim. Content addressing removes some name/order conflicts;
   it does not prove semantic compatibility.
6. **Unicode:** replace “skeleton maps characters, not sequences” with
   the UTS #55 warning that skeletons can change length and must be
   treated as a black box.

## 3. Unicode source-code handling: proposed Plain profile

**Status: Proposed; version pin is open (A-27).**

The research supports this profile for the next draft:

- **Identifiers:** NFC; case-sensitive; UAX #31 D1 with XID_Start /
  XID_Continue, plus `_` in Start, declared as a profile. Pin the Unicode
  version and the UTS #39 data version together.
- **Text literals:** valid UTF-8 scalar values; no silent normalization.
  Escapes must reject surrogate code points and values above U+10FFFF.
- **Roles:** declaration context distinguishes types, values, fields,
  and constructors. Case conventions are diagnostics, not the mechanism
  that makes a name parseable.
- **Confusables:** compare UTS #39 skeletons of distinct visible names;
  do not implement skeleton as a per-character fold. Include reserved
  words and prelude names in the relevant-name set when feasible.
- **Mixed script:** use UTS #55 identifier chunks, not a blanket
  “contains Latin plus Cyrillic/Greek” warning.
- **Source display:** diagnostics and plain-text diffs must not let bidi
  controls reorder executable source misleadingly. At minimum, escape or
  visibly mark directional controls in diagnostic output; full editor
  display rules belong to Phase 13 tooling.

This profile deliberately does **not** claim to prevent all spoofing.
UTS #39 and UTS #55 describe mitigations, not a guarantee.

## 4. What this audit does not establish

- It does not establish that Plain is easier, faster, safer, or more
  accessible than any baseline. Those remain Phase 12/13 questions.
- It does not prove type soundness, memory safety, or capability
  security. The operational-semantics draft states conjectures and
  obligations, not theorems.
- It does not choose a Unicode version. The latest UAX #31/UTS #39 pages
  fetched during this pass advertise Unicode 18.0.0; the pinned research
  citations use Unicode 17.0.0 revisions to avoid a moving target. Plain
  must choose and test one before freeze.
- It does not import or adopt third-party code. License condition C4
  remains open.

## 5. Sources

| # | Source | Grade | Manifest ID / retrieval |
|---|---|---|---|
| S1 | JetBrains, *Compatibility guide for Kotlin 1.7.0*, “Make when statements with enum, sealed, and Boolean subjects exhaustive by default” | A | `kotlin-17-compat`, pinned commit |
| S2 | JetBrains, *Conditions and loops* (`control-flow.md`) | A | `kotlin-control-flow`, pinned commit |
| S3 | Swift.org, *The Swift Programming Language: Enumerations* | A | `swift-enums`, pinned commit |
| S4 | Swift.org, *The Swift Programming Language: Control Flow* | A | `swift-control-flow`, pinned commit |
| S5 | Rust Project, *The Rust Reference: Operator expressions — Overflow* | A | `rust-operators`, pinned commit |
| S6 | Elm, *An Introduction to Elm: Ports* | A | `elm-ports`, 2026-11-03 |
| S7 | Elm, *Syntax* | A | `elm-syntax`, 2026-11-03 |
| S8 | Elm homepage, “No Runtime Exceptions” | A (official claim, not independent measurement) | `elm-home`, 2026-11-03 |
| S9 | Unison, *Introduction to Abilities* | A | `unison-abilities`, 2026-11-03 |
| S10 | Unison repository README | A | `unison-readme`, pinned commit |
| S11 | Unicode, UAX #31 revision 43 (Unicode 17.0.0), C1/D1/R1 | A | `uax31-43` |
| S12 | Unicode, UTS #55 revision 5, §§3.1–3.2, 5.1 | A | `uts55-5` |
| S13 | Unicode, UTS #39 revision 32 (Unicode 17.0.0), §§3.1, 4, 5 | A | `uts39-32` |
| S14 | Unicode, UAX #15 revision 57 (Unicode 17.0.0), §1.4 | A | `uax15-57` |
| S15 | WebAssembly 3.0 specification, *Execution Conventions* | A | `wasm-exec-conventions`, 2026-11-03 |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 1.0 | Primary-source audit created; 12 findings, prior-art corrections, proposed Unicode profile, explicit non-findings. |
