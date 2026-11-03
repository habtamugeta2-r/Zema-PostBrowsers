# Decision Record 0012 — Direction-aware identifier confusability and complete Unicode input lock

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — independently checked against pinned primary sources; owner/reviewer ratification reserved |
| **Owner ratification** | **pending — A-45/A-46/A-47** — see [`README.md`](./README.md) for the status vocabulary |
| **Evidence label** | **Established** for cited Unicode clauses and repository/hash observations; **Proposed** for Plain policy |
| **Source grade** | A — Unicode Consortium standards and Unicode 17.0.0 data |
| **Resolves** | A-45, A-46, and A-47 as proposals; refines A-44, decision 0011, and L-08/L-10/L-11 |
| **Does not resolve** | C1, C2, C5, A-42, or owner ratification of A-27/A-38/A-44/A-45/A-46/A-47 |

## 1. Questions audited

1. What exact chunk boundaries does UTS #55 rev5 §5.1.2.1 define, including marks and Greek titlecase?
2. What are the complete conditions for a confusing chunk in UTS #55 rev5 §5.1.2.2 (C4), and which source examples are confusing versus visibly mixed-script?
3. What does UTS #55 rev5 §5.1.1 recommend for LTR/RTL source order, and what direction-sensitive identifier example does it give?
4. What does UTS #39 rev32 §4 define as `skeleton` and `bidiSkeleton`, and what direction set does it recommend for programming-language identifiers?
5. What are the UTS #39 rev32 General Security Profile character rules and its exceptions for join controls?
6. What are UTS #39 rev32 §3.1.1.1 contexts A1, A2, and B, including their global script and normalization conditions?
7. Do UAX #15 rev57 and UAX #9 rev51 correspond to Unicode 17.0.0, and what version is UAX #9 rev52?
8. Which pinned input file supports each declared runtime property/algorithm and each conformance test, and is any required source absent?
9. Do all pinned Unicode 17.0.0 manifest file identities match the immutable upstream blob objects?
10. Does UTS #55 recommend independently suppressing the out-of-profile warning, and does Plain specify that behavior?

## 2. Source findings (Established)

### 2.1 UTS #55 chunk boundaries and C4

UTS #55 rev5 §5.1.2.1 says to treat a letter followed by nonspacing or enclosing marks as that letter for boundary detection. Its boundary rules are:

- CamelBoundary: after `Ll` or a non-Greek `Lt`, with zero or more `Mn`/`Me`, before `Lu` or `Lt`.
- HATBoundary: before `Lu`/`Lt` plus optional `Mn`/`Me` then `Ll`, or before a non-Greek `Lt`.
- snake boundary: on both sides of punctuation excluding `Po`.
- No other word boundaries exist.

**Established, grade A:** these are the published rules, not a Plain heuristic. Citation: [UTS #55 rev5 §5.1.2.1](https://www.unicode.org/reports/tr55/tr55-5.html#Identifier-Chunks), retrieved 2026-11-03.

UTS #55 rev5 §5.1.2.2 defines a chunk `X` as confusing only when (1) its UTS #39 restriction level is greater than Highly Restrictive and (2) some `Y` is confusable with `X`, has a resolved-script set neither empty nor `ALL`, that set is a subset of the union of `Script_Extensions` for characters in `X`, and `Y` is in the General Security Profile. If condition (1) holds but no such `Y` exists, the chunk is visibly mixed-script, not confusing. The standard says implementations shall diagnose confusing identifier chunks.

**Established, grade A:** this C4 test does not equate visible script mixing with a warning. Citation: [UTS #55 rev5 §5.1.2.2](https://www.unicode.org/reports/tr55/tr55-5.html#Mixed-Script-Chunks), retrieved 2026-11-03.

### 2.2 UTS #55 direction and profile-warning recommendations

UTS #55 rev5 §5.1.1 recommends using LTR confusability for a source document with LTR atom order and RTL confusability for RTL atom order. Its Rust example names `aא1` / `a1א` as a pair that Rust's described relation fails to diagnose. This recommendation is contextual to document atom order; it is not itself the UTS #39 all-directions recommendation.

UTS #55 rev5 §5.1.3 recommends a warning mechanism for identifiers outside the UTS #39 General Security Profile because confusables data do not cover all Unicode thoroughly. It recommends modifying that profile to allow U+200C/U+200D only under the UTS #39 joining-control restrictions and states that valid Persian `به‌روز` should not warn. It also shows spurious ZWNJs such as those in `V‌ersion` and `به‌رو‌ز` as cases the warning can catch. The section says it should be possible to turn off this diagnostic independently from confusable detection.

**Established, grade A:** citations: [UTS #55 rev5 §§5.1.1 and 5.1.3](https://www.unicode.org/reports/tr55/tr55-5.html#Confusable-Detection), retrieved 2026-11-03.

### 2.3 UTS #39 skeletons and programming identifiers

UTS #39 rev32 §4 defines `internalSkeleton(X)` by NFD, removing Default_Ignorable_Code_Point characters, mapping characters to prototypes from `confusables.txt`, and applying NFD again. It defines `bidiSkeleton(d, X)` for `d ∈ {RTL, LTR, FS}` using UAX #9 reordering through L2, L3 mark movement, L4 mirrored-glyph substitution, then `internalSkeleton`. It defines the compatibility `skeleton(X)` as `bidiSkeleton(LTR, X)`. The same section says LTR, RTL, and FS confusability should be used where single-script or single-directionality constraints are inappropriate, specifically programming-language identifiers. Skeletons are not display strings and are not stable across Unicode versions.

**Established, grade A:** citation: [UTS #39 rev32 §4](https://www.unicode.org/reports/tr39/tr39-32.html#Confusable_Detection), retrieved 2026-11-03.

UTS #39 rev32 §5.1 defines augmented script sets (including specified Hanb/Jpan/Kore additions and Common/Inherited handling) and resolved script sets as intersections of those augmented sets. §5.2 defines restriction levels, requiring an identifier profile for levels 1–5 and using resolved script sets/script coverage.

**Established, grade A:** citations: [UTS #39 rev32 §§5.1–5.2](https://www.unicode.org/reports/tr39/tr39-32.html#Mixed_Script_Detection), retrieved 2026-11-03.

### 2.4 General Security Profile and joining contexts

UTS #39 rev32 §3.1 says the General Security Profile disallows `Identifier_Status=Restricted` unless the implementation documents an addition; the profile filters the identifier syntax and may define exceptions. Join controls are classified as Default_Ignorable/Restricted in the profile data; implementations retaining them must declare a profile modification and enforce joining contexts. UTS #55 rev5 §5.1.3 independently recommends contextual exceptions for U+200C/U+200D.

UTS #39 rev32 §3.1.1.1 states a global script restriction and NFC condition for each of A1, A2, and B: the relevant sequence must consist of one script after ignoring Common and Inherited characters, and be NFC (or first transformed to NFC for a test where input is not required to be NFC).

- **A1, ZWNJ:** `LJ/DJ`, then zero or more `T`, ZWNJ, zero or more `T`, then `RJ/DJ`, where the terms are `Joining_Type` values.
- **A2, ZWNJ:** Letter, `Mn*`, Virama (`Canonical_Combining_Class=Virama`), `Mn` with nonzero CCC*, ZWNJ, `Mn` with nonzero CCC*, Letter.
- **B, ZWJ:** Letter, `Mn*`, Virama, `Mn` with nonzero CCC*, ZWJ, **not followed by** a character whose `Indic_Syllabic_Category=Vowel_Dependent`.

**Established, grade A:** citations: [UTS #39 rev32 §§3.1 and 3.1.1.1(A1/A2/B)](https://www.unicode.org/reports/tr39/tr39-32.html#Limited_Contexts_for_Joining_Controls), retrieved 2026-11-03. The exact negative lookahead in B is `(?!$D)`; the rule is not equality with `Vowel_Dependent`.

### 2.5 Version alignment

The version headers of UAX #15 rev57 and UAX #9 rev51 say Unicode 17.0.0. The UAX #9 rev52 version header says Unicode 18.0.0. Therefore the selected rev57/rev51 pair matches the Unicode 17.0.0 data lock, while rev52 is excluded.

**Established, grade A:** [UAX #15 rev57](https://www.unicode.org/reports/tr15/tr15-57.html), [UAX #9 rev51](https://www.unicode.org/reports/tr9/tr9-51.html), and [UAX #9 rev52](https://www.unicode.org/reports/tr9/tr9-52.html), retrieved 2026-11-03.

## 3. Proposed Plain profile

### 3.1 Direction-aware confusable relation

Define `confusable_any_direction(X,Y)` as true iff any of `bidiSkeleton(LTR,·)`, `bidiSkeleton(RTL,·)`, or `bidiSkeleton(FS,·)` returns equal sequences for `X` and `Y`.

For `PL0105`, compare distinct semantic names that are simultaneously visible under L-10’s scope rule. Emit the already proposed Plain **error** if `confusable_any_direction` is true. Skeletons remain internal comparison values, never displayed or substituted for source text.

For `PL1101`, keep every C4 boundary, restriction-level, resolved-script-set, `Script_Extensions`, and General Security Profile condition unchanged, but interpret the C4 phrase “Y is confusable with X” through the same any-direction relation for Plain identifiers.

**Important distinction:** UTS #55 §5.1.1 gives source-document-order LTR/RTL guidance; UTS #39 §4 recommends all three directions for programming-language identifiers when single directionality cannot be assumed. Applying the union of LTR/RTL/FS matches in both Plain checks is a **Proposed Plain policy extension** informed by UTS #39—not a claim that UTS #55 C4 itself explicitly defines that extension. It may change which chunks qualify and must be evaluated before fixture expectations are ratified.

**Proposed, source grade A:** UTS #39 rev32 §4 and UTS #55 rev5 §§5.1.1–5.1.2.2. Owner/reviewer ratification and algorithm conformance remain outstanding.

### 3.2 Join-control warning

Retain `PL1104` as a separate proposed warning. A U+200C/U+200D exception is permitted only when the full UTS #39 §3.1.1.1 context, including the global single-script and NFC conditions, passes. L-04 already requires NFC identifiers; the script restriction still applies. A valid contextual joiner is not warned by `PL1104`; an invalid joiner is. This does not make join controls exceptions to L-08's identifier syntax.

**Proposed, source grade A:** UTS #39 rev32 §§3.1/3.1.1.1 and UTS #55 rev5 §5.1.3. No algorithm has been run.

### 3.3 Independent suppression of the profile warning

**Established, grade A:** UTS #55 rev5 §5.1.3 says it should be possible to turn off the out-of-profile diagnostic independently from confusable detection. Plain already assigns a separate code, `PL1104`, but the suppression behavior was not previously specified.

**Proposed Plain policy:** keep `PL1104` enabled by default and independently suppressible from `PL0105` and `PL1101`. Defer the configuration mechanism and user-interface details to the tooling/configuration phase; the lexical and profile-warning predicates remain unchanged. This is A-47, a proposed resolution pending owner/reviewer ratification.

## 4. Data dependency and sufficiency audit

The table separates runtime property/algorithm data from conformance corpora. “Required” means the standard operation references the property/mapping; it is not a claim that the project has selected an implementation or that a concrete library has no further generated build inputs.

| Adopted operation | Runtime data needed from pinned Unicode 17.0.0 files | Conformance/test input |
|---|---|---|
| XID_Start/XID_Continue and Default_Ignorable_Code_Point | `DerivedCoreProperties.txt` | — |
| NFC/NFD and UTS #39 canonical-equivalence/profile checks | `UnicodeData.txt`, `DerivedNormalizationProps.txt` | `NormalizationTest.txt` |
| UTS #39 internal skeleton prototype mapping | `confusables.txt`, `DerivedCoreProperties.txt` (default ignorables), normalization data above | — |
| Resolved scripts, Script_Extensions union, C4 restriction level / GSP membership | `Scripts.txt`, `ScriptExtensions.txt`, `IdentifierStatus.txt`, `IdentifierType.txt`, `confusables.txt`, `DerivedCoreProperties.txt` | — |
| UTS #55 chunk category and Greek-titlecase boundary rules | `UnicodeData.txt` (General_Category), `Scripts.txt` (Greek exception) | — |
| Join controls A1/A2/B, including NFC and script restriction | `ArabicShaping.txt` (Joining_Type), `UnicodeData.txt` (General_Category/CCC), `Scripts.txt` (single-script condition), `DerivedNormalizationProps.txt` (normalization), `IndicSyllabicCategory.txt` (B successor restriction) | — |
| UTS #39 bidiSkeleton / UAX #9 reordering and mirroring | `DerivedBidiClass.txt`, `BidiBrackets.txt`, `BidiMirroring.txt`, `UnicodeData.txt` (including mirrored/category data), plus skeleton inputs above | `BidiTest.txt`, `BidiCharacterTest.txt` |

The union of the runtime and test columns is the following **16** pinned files: `ArabicShaping.txt`, `BidiBrackets.txt`, `BidiCharacterTest.txt`, `BidiMirroring.txt`, `BidiTest.txt`, `confusables.txt`, `DerivedBidiClass.txt`, `DerivedCoreProperties.txt`, `DerivedNormalizationProps.txt`, `IdentifierStatus.txt`, `IdentifierType.txt`, `IndicSyllabicCategory.txt`, `NormalizationTest.txt`, `ScriptExtensions.txt`, `Scripts.txt`, and `UnicodeData.txt`.

**Established, grade A / repository observation:** the original manifest held 15 of those files and lacked `IndicSyllabicCategory.txt`. The Unicode 17.0.0 file is at `unicodetools/data/ucd/17.0.0/IndicSyllabicCategory.txt`, pinned commit `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c`, Git blob `43287cca65e978e4ca04a49faa7032dde3ddf250`, 86,695 bytes, SHA-256 `3fc122f4cf58b0c19268d5f810263b04ab4e1e67743386ec0e0ada9c76aec5be`; its header is `IndicSyllabicCategory-17.0.0.txt`.

All 15 previously pinned GitHub blob objects were independently re-fetched and matched manifest byte length, Git blob ID, and SHA-256. The new 16th object was independently fetched and matched all three fields. No bytes were saved into the repository. This verifies identity and the identified dependency mapping; it is not a runtime algorithm, standards conformance run, or proof that an eventual implementation is complete.

## 5. Future example candidates — planned, not executed

| Case | Established source fact | Proposed Plain follow-up |
|---|---|---|
| `aא1` / `a1א` as distinct simultaneously visible names | UTS #55 rev5 §5.1.1 names this direction-sensitive pair in its Rust example | Compare all LTR/RTL/FS skeleton pairs in a future oracle/fixture; do not state which Plain result occurs before those values are established |
| `Строкa`, `Δt`, `μэow`, `ΜΙΚΡA`, `HTTPसर्वर`, `microᖯ` | UTS #55 rev5 §5.1.2.2 publishes baseline C4 classifications | Preserve the standard classification, then evaluate the Plain all-direction extension separately; do not copy baseline results as final Plain outputs |
| `HTTPЗапрос`, `TypeII`, `OCaml`, `LOUD_SNAKE`, `Paral·lel` | UTS #55 rev5 §5.1.2.1 illustrates acronym, case, punctuation, and Other_Punctuation chunk edges | Verify token chunks exactly; their final PL1101 outcomes remain determined by the C4 test |
| Persian `به‌روز`, `V‌ersion`, `به‌رو‌ز` | UTS #55 rev5 §5.1.3 explicitly says the first should not warn and shows spurious ZWNJs in the latter examples | Future PL1104 cases: valid contextual joiner versus out-of-context joiners |
| Sinhala letter + virama + ZWJ + RA + Vowel Sign II; successor changed to an ISC Vowel_Dependent scalar | UTS #39 rev32 §3.1.1.1(B) gives the first contextual example structure and bars a Vowel_Dependent successor | Candidate positive/negative boundary pair; select code points from pinned UCD and verify global single-script/NFC conditions before any fixture is authored |

These are **Hypotheses/proposed test targets**, not expected algorithm outputs. No fixtures, implementation, or conformance run was made.

## 6. Options and consequences

- **Use all three UTS #39 directional skeletons** for Plain identifiers — selected as a proposed policy because UTS #39 §4 expressly recommends this for programming-language identifiers when single-directionality cannot be assumed. This is broader than UTS #55's document-order recommendation; preserve that distinction.
- **Keep only `skeleton(X)` (LTR)** — rejected as the proposed policy because it does not implement UTS #39's all-direction guidance for mixed-direction code identifiers.
- **Vendor `IndicSyllabicCategory.txt` or third-party implementation code** — rejected; the repository pins the identity only. No Unicode data or third-party code is adopted.
- **Make PL1104 separately suppressible** — selected as a proposed behavior, consistent with UTS #55 rev5 §5.1.3; default remains enabled. Configuration syntax and UI remain outside this profile decision and are deferred to the tooling phase.

A-45/A-46/A-47 are **Resolved (proposed)**; L-10/L-11 and the profile input lock are updated accordingly. LTR/RTL/FS example outcomes and every operation remain unimplemented and untested. The conformance planning total remains 307; the existing 14-identifier allocation includes these candidate cases and is a planning budget, not coverage evidence. C1/C5 still block build work and C2 remains due before Gate 1. *(Correction, same day: C1 and C5 were resolved after this text was written — build is authorized. C2 and A-* ratification still gate a Gate 1 attempt.)*

## Sources

- [UTS #55 rev5 §§5.1.1–5.1.3](https://www.unicode.org/reports/tr55/tr55-5.html) — source-order confusability advice, chunk boundaries/C4, GSP warning advice (A).
- [UTS #39 rev32 §§3.1, 3.1.1.1(A1/A2/B), 4, 5.1–5.2](https://www.unicode.org/reports/tr39/tr39-32.html) — profile, join-control contexts, directional skeletons, resolved scripts and restriction levels (A).
- [UAX #31 rev43 §2](https://www.unicode.org/reports/tr31/tr31-43.html) — identifier properties and XID profile basis (A).
- [UAX #15 rev57](https://www.unicode.org/reports/tr15/tr15-57.html), [UAX #9 rev51](https://www.unicode.org/reports/tr9/tr9-51.html), [UAX #9 rev52](https://www.unicode.org/reports/tr9/tr9-52.html) — version alignment/exclusion (A).
- [Unicode 17.0.0 `IndicSyllabicCategory.txt`](https://www.unicode.org/Public/17.0.0/ucd/IndicSyllabicCategory.txt) — context-B data file (A).
- [`phase-01-source-manifest.json`](../../research/data/phase-01-source-manifest.json) — immutable 16-file input lock.

## Post-audit execution note (2026-11-03)

The earlier statements in this record describe the state at the time Decision 0012 was prepared. Later on 2026-11-03, all 16 pinned Unicode files were fetched into an ignored cache and verified against manifest Git blob SHA-1, byte length, and SHA-256. A project-owned `internalSkeleton` implementation (NFD → remove Default_Ignorable_Code_Point → `confusables.txt` map → NFD) computed outputs for the five candidates in [`phase-01-internal-skeleton-examples.json`](../../research/data/phase-01-internal-skeleton-examples.json). These are **internalSkeleton only**, not `skeleton(X)` or LTR/RTL/FS `bidiSkeleton` outputs; no Plain confusability result, chunk/C4 diagnostic, or language fixture is asserted. The full NormalizationTest corpus passed via experiment EN-unicode17-normalization. C1/C5 were subsequently resolved; C2 and A-* ratifications remain outstanding before Gate 1. Rule-level traceability for all 106 rule IDs is now recorded in [`../plain/07-traceability.md`](../plain/07-traceability.md).

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Independent audit distinguishes UTS #55 source-order recommendations from UTS #39 all-direction guidance, proposes the broader Plain relation, clarifies exact joiner context B, and completes the Unicode 17.0.0 data/test input inventory. |
| 2026-11-03 | Added post-audit note: all 16 inputs verified, full normalization corpus passed, and internalSkeleton values computed for five examples. Full bidiSkeleton/C4/Plain behavior remains unimplemented; C1/C5 now resolved, C2/A-* still pending for Gate 1. |
