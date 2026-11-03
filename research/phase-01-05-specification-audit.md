# Phase 1 · Record 05 — Plain v0.1 Specification Audit

| Field | Detail |
|---|---|
| **Document** | `research/phase-01-05-specification-audit.md` |
| **Version** | 1.3 |
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) |
| **Status** | Audit complete; draft v0.2 corrections applied where mechanical; open items remain before freeze |
| **Evidence label** | E for repository observations; P for proposed resolutions; H where proof/measurement is still required |
| **Method** | Rule-by-rule reading, grammar/prose comparison, count audit, primary-source cross-check, and a non-executable semantics sketch |

> **Bottom line.** Plain v0.1 was a useful draft, but it was not
> implementation-ready. The audit found mechanical contradictions,
> missing grammar productions, Unicode policy problems, and gate-scope
> ambiguity. v0.2 fixed the mechanical issues; v0.2.3 specified the
> initial Unicode security diagnostics and data lock. The v0.2.4 independent
> audit checked direction-sensitive confusability, all join-control clauses,
> version alignment, and the 16-file data/test input inventory. The text remains a proposal. **Gate 1 is
> still not attempted.** C1/C5 still block build tasks; C2 is still due
> before Gate 1.

---

## 1. Count and reference audit

These are repository observations, not quality claims.

| Check | v0.1 result | Action |
|---|---|---|
| Normative rules in docs 00–02 | v0.1: 34 L + 28 T + 36 E = **98**; v0.2 adds T-29/T-30 = **100** | Tracker’s “60 normative rules” corrected; reproducible via `tools/audit_phase01.py` |
| Derived ambiguities | 26 rows: 21 resolved, 5 deferred | v0.2 adds A-27…A-43; v0.2.2/0.2.3 add proposed resolutions and A-44; v0.2.4 adds A-45–A-47; now 47 total (42 proposed-resolved, 5 deferred, 0 open) |
| Deferrals | 18 rows | v0.2 adds D-19/D-20 for Map/Set and Unicode segmentation APIs |
| Evidence register | 96 rows before this audit | Now 100 rows (E49/P22/H29); new rows #097–#100 capture directionality, joining-context and warning-suppression findings/proposals |
| Unicode source lock | 57 total manifest entries, 15 Unicode 17.0.0 data/test files | Now 58 entries, 16 Unicode 17.0.0 files; all 16 pinned blob IDs, byte lengths, and SHA-256 values independently match |
| Conformance target | The v0.2 listed area counts summed to **275**, not “≈285” | Decision 0011 raised the diagnostics floor from 20 to 52 active codes; current plan sums to 307 and remains a planning target, not a coverage proof |
| Relative Markdown links | 0 broken at audit time | Rechecked after edits by `tools/audit_phase01.py --check` |
| Small-step operational semantics | Absent | Non-normative draft added as [`../docs/plain/06-operational-semantics.md`](../docs/plain/06-operational-semantics.md); not a proof or implementation |

## 2. Findings

Severity: **Blocker** = cannot freeze/ implement consistently until
resolved; **Major** = likely wrong behavior or false claim; **Minor** =
editorial/count/reference defect.

| ID | Severity | Finding | Resolution in current draft | Status |
|---|---|---|---|---|
| SA-01 | Minor | Tracker says 60 rules; docs contain 98. | Tracker and README corrected. | Fixed |
| SA-02 | Minor | Conformance area counts sum to 275, not 285. | Historical v0.2 correction retained; decision 0011 reallocates 32 additional diagnostics targets for the 52 active codes, making the current v0.2.3 plan 307. | Fixed and expanded |
| SA-03 | Minor | Cross-references point to wrong rules/ambiguities: L-09→A-14 instead of A-15; grammar notes→E-11/T-20/E-15 instead of E-17/T-21/E-28; A-06/D-16 cite L-22 for the operator table; types open-item A-17 was mislabeled. | References corrected. | Fixed |
| SA-04 | Blocker | Compact grammar cannot express several normative forms: uppercase constructors as expressions; lowercase type parameters in types; inline bounds; optional lambda parameter types; required named-function return types; generic interface heads; record-update sugar. | Grammar rewritten to match prose; name roles are contextual, not case-tokenized. | Fixed in draft; needs parser tests later |
| SA-05 | Major | Recursive-union example `Node(Tree, Tree)` violates T-09’s one-payload rule. | Example changed to `Node({ left: Tree, right: Tree })`. | Fixed |
| SA-06 | Major | E-03 defines pipe evaluation order but also says programs “MUST NOT depend” on it; S-3 uses `Display.display` while E-11 names `Text.from`. | Pipe order is explicit and deterministic; interpolation desugars to `Text.concat` + `Display.display`. | Fixed |
| SA-07 | Major | L-04 requires NFC for text literals. UTS #55 says not to silently normalize string literals; UAX #15 says NFC is not closed under concatenation. | L-04 now applies to identifiers only; text preserves scalar data; escapes reject surrogates/out-of-range. | Fixed |
| SA-08 | Major | L-12 makes UpperCamel/lower_snake a syntax error, excluding unicameral scripts from type/value names. | Roles come from declaration/resolution context; naming conventions become warnings, with script-aware style checks. | Fixed as proposed design |
| SA-09 | Major | Prior note describes skeleton as character-based; L-11 warns on whole-identifier Latin/Cyrillic/Greek mixing. | Skeleton uses UTS #39 rev32; decision 0011 states exact UTS #55 C4 chunk rules and the separating conditions for confusing vs visibly mixed chunks. | Fixed as proposed design; A-44 ratification pending |
| SA-10 | Blocker | Top-level `let` has no initialization order, forward-reference, or cycle rule. | v0.2 restricts user top-level `let` initializers to constant expressions; builtins are separate. | Proposed; A-32 |
| SA-11 | Major | “Local, rank-1” does not say whether local `let`/lambdas generalize. | v0.2 makes local bindings monomorphic; explicit declaration type parameters are the only rank-1 polymorphism entry point. | Proposed; A-33 |
| SA-12 | Blocker | `?` boundary is unclear for lambdas and `defer`; a cleanup could override the enclosing result. | `?` targets the nearest function, including a lambda; `?` is forbidden inside `defer` in v0.2. | Proposed; A-35 |
| SA-13 | Major | `defer` says “enclosing block” but `?` says “that function’s defers”; E-32 implies all app-visible effects roll back. | Block-local LIFO unwind; function early return unwinds active blocks in that function; faults do not guarantee defers; rollback claim limited to local task state. | Proposed; A-36/A-39 |
| SA-14 | Blocker | E-27 calls arm bindings “irrefutable by construction,” but nested literal/variant patterns can fail. Coverage algorithm and binder rules are absent. | Pattern matching is a partial function returning bindings only on success; duplicate binders rejected; coverage rules sketched in semantics draft. | Proposed; A-37 |
| SA-15 | Blocker | `Map` requires only `Ord`, E-09 gives Float a total order, T-26 says Float cannot be a Map key; `Set` is mentioned without a type/API; `Hash` is deferred. | Decision 0009 settles Eq/Ord laws as proposals; Map/Set/Hash APIs and collection behavior remain Phase 9 work (D-19). | Resolved (proposed); API deferred |
| SA-16 | Major | D-01 says effect handlers would let an app re-implement revoked authority. Unison shows handlers interpret effects; host authority is a separate question. | D-01 rationale corrected to scope/complexity; capability rule unchanged. | Fixed |
| SA-17 | Major | Gate 1 plan includes grapheme segmentation, task isolation, host revocation, and I/O fault behavior owned by Phases 3/5/7/9. | Decision 0010 proposes a hermetic-core-only Gate 1 and explicitly preserves later obligations. | Resolved (proposed); ratification pending |
| SA-18 | Major | L-34 requires per-code coverage; the initial 20-fixture diagnostics allocation was below the active registry size. | Audit emits 53 codes (52 active, one historical); the diagnostics target is now 52+ and the total plan is 307. | Fixed in v0.2.3 plan/registry |
| SA-19 | Major | Evidence #057 is a universal negative; #065 relies on an outdated Kotlin gap; #066 calls four documents “complete.” | #057 retired in favor of bounded #074; #065 superseded; #066 superseded by audit observation. | Fixed in register |
| SA-20 | Blocker | No small-step semantics, so “safe executable core” has no independent dynamic specification. | Non-normative core reduction draft added; open holes listed; no soundness/security theorem claimed. | Draft, not gate-ready |
| SA-21 | Major | Source handling does not address bidi controls, unrecognized line terminators, or safe diagnostic quoting. | A-41 records UTS #55 display/diagnostic obligations; L-02/L-30 tightened for LF/CRLF and escaped diagnostic output. | Proposed |
| SA-22 | Major | E-33 says faults are deterministic under quotas, but wall-clock timeouts are scheduling-dependent. | Conformance uses deterministic fuel/step quotas; wall-clock policy is a host concern, not a core semantic input. | Proposed; A-40 |
| SA-23 | Blocker | L-11 said “UTS #55-style chunks” but did not state chunk boundaries, UTS55-C4’s confusing-chunk test, or the required General Security Profile membership test. | Decision 0011 imports UTS #55 rev5 §§5.1.2.1–5.1.2.2 and assigns `PL1101` only to confusing chunks; UTS #39 data are versioned. | Resolved (proposed); A-44 ratification pending |
| SA-24 | Major | No distinct diagnostic warned about identifiers outside UTS #39’s General Security Profile or specified valid ZWNJ/ZWJ contexts. | Decision 0011 proposes independent `PL1104` and UTS #39 rev32 §3.1.1 joiner-context handling; this does not reject identifiers. | Resolved (proposed) |
| SA-25 | Major | The Unicode pin named standards but had no file-level hashes for XID, normalization, script, security, or bidi inputs; unversioned UAX #9 resolves to rev52/Unicode 18.0.0. | Decision 0011 pins UAX #9 rev51/Unicode 17.0.0 and the initial 15 Unicode 17 data/test files. Decision 0012 adds `IndicSyllabicCategory.txt`; all 16 blob IDs, lengths, and SHA-256 values match independently re-fetched pinned GitHub blobs. | Fixed as research manifest; no data vendored |
| SA-26 | Major | The 20+ diagnostics fixture target was incompatible with L-34’s one-active-code/one-fixture minimum once 52 active codes were counted. | Target raised to 52+; total planning sum rises from 275 to 307. Still a target, not coverage or a test run. | Fixed in v0.2.3 plan |
| SA-27 | Major | L-10 compared only canonical LTR `skeleton(X)` even though UTS #39 rev32 §4 recommends LTR, RTL, and FS confusability for programming-language identifiers when direction is not constrained. **Established, grade A.** | Decision 0012 proposes the union of all three `bidiSkeleton` relations for PL0105 and as a deliberate extension to PL1101 C4. UTS #55’s LTR/RTL source-order recommendation is distinguished from this UTS #39 guidance. **Proposed; grade A source guidance; ratification and algorithm check pending.** | Addressed in draft policy; not implemented or tested |
| SA-28 | Major | The original 15-file lock omitted `IndicSyllabicCategory.txt`, required by UTS #39 rev32 §3.1.1.1(B) to test that a ZWJ is not followed by a Vowel_Dependent scalar. **Established, grade A.** | Added Unicode 17.0.0 file 16; documented A1/A2/B and global script/NFC conditions; independently verified all 16 blob IDs, lengths, and SHA-256 values. **Proposed input inventory; grade A.** | Fixed in research manifest; no data vendored or algorithm run |
| SA-29 | Major | UTS #55 rev5 §5.1.3 recommends that the out-of-profile warning be independently suppressible from confusable detection; Plain named `PL1104` separately but did not specify suppression. **Established, grade A.** | Propose `PL1104` enabled by default and independently suppressible from `PL0105`/`PL1101`; defer configuration/UI mechanism to tooling phase. **Proposed; grade A source guidance.** | A-47 added as resolved (proposed); owner/reviewer ratification pending |

## 3. Representative counterexamples

These are **specification probes**, not passing Plain programs.

### 3.1 Constructors and type parameters were not parseable

```plain
fn always_true() -> Bool:
  True

fn identity<a>(value: a) -> a:
  value
```

v0.1’s `primary` had no constructor expression, and `type` had no
lowercase type-parameter production, despite T-05/T-14 requiring both.

### 3.2 Inline bounds and record update were prose-only

```plain
fn show<a: Display>(value: a) -> Text:
  Display.display(value)

let updated = { task with done = True }
```

v0.1’s `type_params` had no bound syntax and `record` had no `with`
production, despite T-15 and S-1.

### 3.3 One-payload recursive union

```plain
-- Invalid under T-09:
type Tree = Leaf | Node(Tree, Tree)

-- Intended form:
type Tree = Leaf | Node({ left: Tree, right: Tree })
```

### 3.4 Pipe order cannot be both defined and forbidden

```plain
read() |> combine(clock())
```

Under S-2 this is `combine(clock(), read())`, so `clock()` is evaluated
before `read()`. That order may be surprising, but it is defined. The
specification should not also claim programs must not depend on it.

### 3.5 `defer` and `?` need a control boundary

```plain
fn example() -> Result<Int, Text>:
  defer:
    cleanup()?
  Ok(1)
```

If `cleanup()` returns `Err`, v0.1 does not say whether the original
`Ok(1)` is replaced, whether remaining defers run, or which function
receives the error. v0.2 forbids `?` inside `defer`.

### 3.6 Pattern bindings are not irrefutable

```plain
when Some(1):
  Some(0): 0
  _: -1
```

The first arm fails; no binding from that arm may leak. E-27’s
“irrefutable by construction” wording was false for nested patterns.

### 3.7 Float ordering and Map keys disagreed

```plain
Map<Float, Int>
```

T-02’s table says Map requires `Ord`; E-09 supplies a Float total order;
T-26 says Float cannot be a Map key. v0.2 defers Map/Set rather than
pretending the constraint is settled.

## 4. Gate 1 readiness after this pass

| Requirement | State |
|---|---|
| Owner sign-off C1 | **Open** — blocks build |
| PlainP relationship C5 | **Open** — blocks build |
| Book import/retirement C2 | **Open** — due before Gate 1 |
| Normative grammar/prose consistency | Improved in draft v0.2; still needs implementation tests |
| Small-step semantics | Non-normative draft exists; open items and proof obligations remain |
| Conformance suite | **Zero fixtures**; plan only |
| Executable core | **None** |
| Gate 1 review | **Not attempted** |

The next engineering step after C1/C5 is not “start writing a large
interpreter.” It is: ratify or revise proposed decisions 0009–0011, freeze the
Gate 1 core subset, verify the manifest-pinned Unicode bytes, then build
lexer/layout → parser → checker → evaluator with fixtures at each step.

## 5. Sources

Repository observations cite the draft files directly. External support
is in [`phase-01-03-primary-source-audit.md`](./phase-01-03-primary-source-audit.md)
and [`phase-01-04-integrated-systems-and-plainp.md`](./phase-01-04-integrated-systems-and-plainp.md).
The reduction style follows WebAssembly’s execution conventions [S15 in
Record 03]. **[Established, grade B]** Featherweight Java’s publisher
abstract says it omits many full-Java features to enable rigorous
type-safety arguments and a compact calculus [S1]. **[Proposed, grade A]
Interpretation:** this is only a bounded methodological precedent for
using a small core; it does not show that any particular Plain feature
can be omitted without changing Plain’s safety argument.

| # | Source | Grade |
|---|---|---|
| S1 | Igarashi, Pierce, Wadler, “Featherweight Java: A Minimal Core Calculus for Java and GJ,” OOPSLA 1999, pp. 132–146, DOI [10.1145/320384.320395](https://doi.org/10.1145/320384.320395); [ACM publisher record](https://dl.acm.org/doi/10.1145/320384.320395), retrieved 2026-11-03 | B (peer-reviewed research paper; publisher abstract checked; PDF not parsed) |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-03 | 1.0 | Audit created: 22 findings, counterexamples, count corrections, Gate 1 readiness table. |
| 2026-11-03 | 1.1 | Verified the Featherweight Java bibliographic citation against the ACM publisher abstract and narrowed the methodological claim; updated the source manifest. |
| 2026-11-03 | 1.2 | Added UTS #55 chunk-diagnostic analysis, exact versioned Unicode data hashes, and the v0.2.3 conformance-budget correction (26 findings total). |
| 2026-11-03 | 1.3 | Independently checked UTS #55/UTS #39 direction and joining clauses, version alignment, and the 16-file source inventory; added SA-27–SA-29, A-45–A-47, Decision 0012, and evidence #097–#100. 29 findings total. |
