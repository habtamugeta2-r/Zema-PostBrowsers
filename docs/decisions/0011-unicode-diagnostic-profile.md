# Decision Record 0011 — Specify UTS #55 chunk diagnostics and lock their Unicode data inputs

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — implementation profile drafted from primary standards; owner/reviewer ratification reserved |
| **Evidence label** | **Established** for Unicode standard clauses and retrieved file bytes; **Proposed** for Plain’s diagnostic policy |
| **Source grade** | A — Unicode Consortium standards and Unicode 17.0.0 data; repository source manifest pins exact mirror bytes |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); Gate 1 reviewer/owner may ratify or revise |
| **Resolves** | A-44; refines A-27 and rules L-08…L-11 |
| **Does not resolve** | C1, C2, C5, or A-42 |

## Context and audit finding

The prior Plain draft said to warn when “UTS #55-style identifier chunks
mix scripts in a suspicious way,” but did not define chunk boundaries,
the test for a confusing chunk, or which identifier-profile data it used.
The external standard has an explicit, implementable scheme: UTS #55
revision 5 §5.1.2.1 defines Camel/HAT/snake boundaries, and §5.1.2.2
requires diagnosis of a chunk meeting a two-part confusingness test
(UTS55-C4). Section 5.1.3 separately recommends a warning mechanism for
identifiers outside the General Security Profile.

The source audit also found two reproducibility gaps. First, naming Unicode
17.0.0 and UTS #39 revision 32 alone identifies the release but did not list
or hash the UCD/security files needed for normalization, XID properties,
confusability, resolved scripts, joining contexts, and bidi skeletons.
Second, the unversioned UAX #9 link initially considered resolves to
revision 52 / Unicode 18.0.0, not the chosen Unicode 17.0.0 baseline; the
matching version is UAX #9 revision 51. The revision is now pinned explicitly.
The source manifest now records those inputs by immutable GitHub commit,
Git blob ID, byte length, and SHA-256; it does not vendor the data.

## Decision 1 — Exact mixed-script chunk diagnostic

Plain adopts the following **proposed profile** from UTS #55 rev5 §§5.1.2
and UTS #39 rev32:

1. **Chunk boundaries.** Use the UTS #55 §5.1.2.1 rules, not an
   implementation-defined heuristic:
   - treat a letter followed by `Mn` or `Me` characters as that letter
     for boundary detection;
   - **Camel boundary:** after `Ll` or a non-Greek `Lt`, with following
     `Mn`/`Me` marks, before `Lu` or `Lt`;
   - **HAT boundary:** before `Lu`/`Lt` followed by `Mn`/`Me` marks and
     then `Ll`, or before a non-Greek `Lt`;
   - **snake boundary:** on both sides of a `P` character except `Po`;
   - there are no other chunk boundaries.
2. For each chunk `X`, call it **confusing** iff both hold:
   - `X` has a UTS #39 revision 32 restriction level greater than
     **Highly Restrictive**; and
   - there exists a string `Y` such that (a) `Y` is confusable with `X`
     under UTS #39 revision 32; (b) `Y`’s resolved script set is neither
     empty nor `ALL`; (c) that resolved script set is a subset of the
     union of `Script_Extensions` for characters in `X`; and (d) `Y` is
     in the UTS #39 revision 32 General Security Profile for Identifiers.
3. Emit **`PL1101` warning** on every confusing identifier chunk. A chunk
   with restriction level above Highly Restrictive but no `Y` satisfying
   the second test is visibly mixed-script, not confusing; Plain does not
   emit `PL1101` for it. This follows UTS #55’s distinction that visibly
   mixed-script chunks are not themselves confusing. A warning is the
   Plain severity choice; the standard requires diagnosis, not a
   particular severity.
4. Use UTS #55’s defined identifier-atom boundaries. Do not split an
   identifier into single characters for display or diagnostics.

## Decision 2 — Out-of-profile warning

Emit **`PL1104` warning** when an identifier token is outside the UTS #39
revision 32 General Security Profile for Identifiers, using the UTS #55
§5.1.3 source-code modification: permit U+200C ZERO WIDTH NON-JOINER and
U+200D ZERO WIDTH JOINER only when they satisfy the UTS #39 §3.1.1
contextual joining-control rules. This warning does not reject the
identifier; it is independent of `PL1101` and `PL0105`.

## Reference cases for future fixtures — planned, not executed

The first cases below are examples explicitly classified by UTS #55 rev5
§5.1.2.2 (**Established, grade A**). The expected diagnostic column is
Plain’s proposed behavior (**Proposed, grade A**), not a test result.

| Input | UTS #55 classification | Proposed Plain outcome |
|---|---|---|
| `Строкa` | Confusing; confusable with all-Cyrillic `Строка` | `PL1101` warning |
| `Δt` | Visibly mixed-script, not confusing | No `PL1101` |
| `ΜΙΚΡA` | Confusing; confusable with all-Greek and all-Latin forms | `PL1101` warning |
| `HTTPसर्वर` | Visibly mixed-script, not confusing | No `PL1101` |
| `microᖯ` | Confusing; confusable with all-Latin `microb` | `PL1101` warning |
| `HTTPЗапрос` | Chunk boundaries separate ASCII `HTTP` and single-script Cyrillic `Запрос`; both are at or below Highly Restrictive | No `PL1101` |
| `به‌روز` | UTS #55 §5.1.3 says not to warn for this valid Persian ZWNJ spelling | No `PL1104` |

These are named as future fixture candidates only. No fixture files have
been written, and the outcomes have not been run against an implementation.
The listed C4 classifications are UTS #55 baseline examples, while the
last two are scope examples. Decision 0012 proposes a broader all-direction
relation for Plain; the published baseline remains established evidence,
but each proposed Plain outcome must be recomputed before becoming a fixture
expectation.

## Decision 3 — Exact confusable operation and data lock

- **Historical proposal, superseded in part by decision 0012:** this
  decision initially specified that `PL0105` compare the UTS #39 revision
  32 `skeleton(X)` operation (defined via `bidiSkeleton(LTR, X)`). The
  independent audit found LTR-only comparison too narrow for code
  identifiers. Decision [0012](0012-directional-confusability-and-ucd-completeness.md)
  proposes LTR/RTL/FS comparisons for `PL0105` and the C4-based `PL1101`
  relation. Skeleton output remains internal comparison data only and
  must never be displayed or silently stored as normalized source text.
- The Unicode data release is **17.0.0**. The algorithmic baseline is
  UAX #15 revision 57, UAX #9 revision 51, UAX #31 revision 43, UTS #39
  revision 32, and UTS #55 revision 5. (UAX #9 revision 52 is Unicode
  18.0.0 and is intentionally not the selected baseline.) The manifest
  pins the exact SHA-256 and upstream Git blob for the required UCD/security
  source files at `unicode-org/unicodetools` commit
  `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c`. It includes UAX #15
  `NormalizationTest.txt` and UAX #9 bidi conformance data as future
  test inputs, not completed test runs.
- The data files remain external inputs; none are copied into the
  repository. The original 15 byte lengths and SHA-256 values were
  independently rechecked against immutable GitHub blobs. A later audit
  found the missing `IndicSyllabicCategory.txt` input for UTS #39 rev32
  §3.1.1.1(B); decision 0012 adds it, and all 16 byte lengths, Git blob
  IDs, and SHA-256 values were rechecked against pinned GitHub objects.
  Before implementation, the developer must still verify the exact bytes
  fetched for use and preserve Unicode license/attribution. A Unicode
  update still requires the decision, data diff, fixture regeneration,
  and dual-profile rerun required by decision 0009.

## Options considered

- **Use UTS #55 rev5 §§5.1.2–5.1.3 and UTS #39 rev32 exactly, with
  versioned data and a separate warning severity** — chosen.
- **Warn on any Latin-plus-Cyrillic/Greek identifier** — rejected; it
  misses the standard’s confusable-chunk distinction and creates
  false positives for legitimate technical vocabulary.
- **Invent a simpler script-mixing heuristic** — rejected; it would not
  meet UTS55-C4 while claiming this source-handling profile.
- **Treat UTS #39 skeletons as display normalization** — rejected;
  UTS #39 states skeletons are internal confusability artifacts, not
  suitable for display or identifier normalization.

## Consequences

- A-44 moves to **Resolved (proposed)**. L-11 is now algorithmic rather
  than heuristic; the diagnostic registry has 53 codes including one
  historical code, so 52 active-code diagnostic fixtures are required.
  The diagnostics allocation rises from 20 to 52, taking the planning
  total from 275 to 307 fixtures; this remains a target, not coverage.
  The registry also adds `PL1104`.
- The hashed Unicode data manifest is reproducible by immutable commit
  and can be independently checked. Hashing data is not an implementation
  or conformance run.
- No Unicode data, third-party code, interpreter, fixture, or gate result
  is adopted or produced by this decision. *(Correction, same day: C1 and C5 were
  resolved after this text was written — build is authorized. C2 and A-*
  ratification still gate a Gate 1 attempt.)*

## Sources

- [UTS #55 revision 5, §§5.1.1–5.1.3 and C4](https://www.unicode.org/reports/tr55/tr55-5.html) — chunk boundaries, chunk-confusability criteria, and out-of-profile warning guidance (A).
- [UTS #39 revision 32, §§3.1, 3.1.1, 4, 5, 7](https://www.unicode.org/reports/tr39/tr39-32.html) — security profile, joining contexts, skeletons, script resolution, and data files (A).
- [UAX #31 revision 43, §§1.4, 2, 5](https://www.unicode.org/reports/tr31/tr31-43.html) — version and profile conformance, XID properties (A).
- [UAX #15 revision 57](https://www.unicode.org/reports/tr15/tr15-57.html) and [UAX #9 revision 51](https://www.unicode.org/reports/tr9/tr9-51.html) — Unicode 17.0.0 normalization and bidi algorithms (A).
- [`phase-01-source-manifest.json`](../../research/data/phase-01-source-manifest.json) — the initial 15-file lock from this decision, now completed to 16 Unicode 17.0.0 data/test files by decision 0012.

## Change log

| Date | Change |
|---|---|
| 2026-11-03 | Proposed exact UTS #55 chunk diagnostics, GSP warning, UTS #39 skeleton semantics, and the initial 15-file hash lock; decision 0012 later supersedes/refines the directional relation and adds the 16th input. |

## Dated note (2026-11-03, after this record)

The Consequences text above describes the state when this decision was written.
C1 and C5 were resolved later the same day, so build is authorized; this
decision still awaits ratification, and the diagnostic fixture floor recorded
here (52 active codes) is now carried in
[`../../docs/plain/07-traceability.md`](../../docs/plain/07-traceability.md) and
[`05-conformance-plan.md`](../../docs/plain/05-conformance-plan.md).
