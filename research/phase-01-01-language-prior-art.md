# Phase 1 · Record 01 — Language Prior Art: What "Easy" Already Costs Somebody Else

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-01-01-language-prior-art.md` |
| **Version** | 1.0 |
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Author** | ZEMA research agent (Arena.ai Agent Mode) on behalf of the project owner |
| **Status** | Complete for the research half of Phase 1; build half blocked on Gate 0 conditions C1/C5 |
| **Evidence label** | Mixed — labeled per row; grades per [`README.md` §3](./README.md#3-source-grades-annotation-not-an-extra-label) |

> Phase 1's research task is to study the "easy" specification — small
> core, one notation per feature, readable diagnostics with spans,
> predictable behavior, local inference at boundaries — and the type
> system that supports it. This record surveys the languages that already
> made those choices, so Plain copies what is proven and refuses what is
> not.

---

## 1. Survey

| # | Language | What it proves | What it costs | What ZEMA takes | Label | Src |
|---|---|---|---|---|---|---|
| L1 | **Elm** | A small, purely functional core with no exception primitives can ship production apps: failure is carried by `Maybe`/`Result` in the type, and the compiler refuses to build until both branches are handled | A deliberately slow release cadence and a small hiring pool; interop with the host is a separate, untyped seam ("ports") | The no-exceptions posture, exhaustive `case`, and compiler errors written for humans | E | [S1] |
| L2 | **Rust** | Ownership and `Option`/`Result` make absence and failure explicit; `?` propagation keeps the happy path readable | Overflow semantics depend on the **build profile** (checked with debug assertions, wrapping otherwise), so the same program can behave differently in debug and release unless the author opts into `checked_*`/`wrapping_*` explicitly | `?`, `Result`, no null; **rejects** mode-dependent overflow semantics | E | [S2], [S3] |
| L3 | **Kotlin** | Sealed hierarchies + `when` give closed-world exhaustiveness and a compiler error when a case is missing when the result is used | `when` exists as **both** a statement and an expression, so whether a missing case is an error depends on form and language version — the guarantee is real but conditional, and a reader must know which form they are looking at (the statement-form gap is reported by a secondary source; **verify against Kotlin docs before Gate 1**) | Sealed-union exhaustiveness, but matching is **expression-only** in Plain, so the conditional cannot arise | E (expression form) / H (statement-form gap) | [S4], [S9] |
| L4 | **Swift** | Enums with associated values make illegal states unrepresentable, and `switch` over an enum is exhaustive by default | The language carries a large surface (protocols, extensions, property wrappers, result builders) that a beginner must learn before reading real code | Associated-value unions and exhaustive matching; **not** the surface area | E | [S5] |
| L5 | **Unison** | Content-addressed definitions make renames and dependency conflicts structurally impossible, with perfect incremental compilation | Code lives in a database, not files; a new mental model and a new toolchain for every user | Nothing in v1 — recorded as a **deferred** idea with a stated trigger | E | [S6] |
| L6 | **Unicode UAX #31 / UTS #39** | Identifier syntax can be specified rather than improvised (`XID_Start`/`XID_Continue`), and spoofing can be bounded with skeleton comparison and mixed-script restrictions | Confusable detection is a **floor, not a ceiling**: it maps characters, not sequences, and its coverage depends on the shipped data version | The default identifier syntax, plus a scope-level skeleton-collision check | E | [S7], [S8] |

## 2. The four lessons that shape Plain

### Lesson 1 — "Easy" is a specification, not a vibe

Every language above that feels easy made **specific, enforceable**
choices: one way to declare a value, one way to branch on a sum, one way
to propagate failure. Languages that feel hard let the same concept be
expressed five ways and leave the reader to decode intent.

> **Applied:** Plain's core has exactly one notation per concept, and
> syntactic sugar is admitted only when its desugaring is defined in the
> specification. *Label: P; see decision [0005](../docs/decisions/0005-language-surface-doctrine.md).*

### Lesson 2 — Mode-dependent semantics are a design smell

Rust's overflow RFC is an honest compromise: check in debug, wrap in
release, and hope authors use `checked_*` when it matters [S2][S3]. For
an **application** language whose users are not systems programmers, a
program that behaves differently in two builds is a defect generator.

> **Applied:** integer overflow is checked in **all** build profiles;
> wrapping and saturating are explicit, named operations. *Label: P.*

### Lesson 3 — Exhaustiveness only counts where the compiler enforces it

Kotlin has two forms of the same construct [S4], so whether a missing
case is an error depends on how `when` is used and on the language
version (the statement-form gap itself is C-grade, `[S9]`, and must be
re-verified before Gate 1). The lesson does not depend on which version
is current: **a guarantee whose strength varies by context is hard to
teach and hard to trust.**

> **Applied:** matching is always an expression, always checked — one
> form, one rule. *Label: P.*

### Lesson 4 — Unicode identifiers need a rule and a defense

UAX #31 gives a default syntax [S7]; UTS #39 gives skeleton comparison
and restriction levels, while admitting the mechanism is a pragmatic
floor [S8]. ZEMA's app class includes names in Ethiopic, Arabic, Hebrew,
and Indic scripts, so "ASCII identifiers only" is not acceptable — and
"any Unicode" without a confusable rule is a spoofing vector inside a
code review.

> **Applied:** default identifier syntax, NFC required, declaration-level
> skeleton collisions rejected, mixed-script identifiers warned. *Label: P.*

## 3. What Plain deliberately does **not** copy

| Not copied | From | Why |
|---|---|---|
| Build-profile-dependent overflow | Rust | Same program, two behaviors — unacceptable for the target class |
| Statement-form matching | Kotlin | Removes the exhaustiveness guarantee exactly where bugs hide |
| Untyped host-interop seams | Elm ports | ZEMA's authority model is capability handles (Phase 5); the seam must be typed |
| Content-addressed modules | Unison | Powerful, but it replaces files and tooling before the project has either |
| Large surface (extensions, macros, operators) | Swift, Haskell-lineage languages | Directly contradicts "small core"; all are deferred with stated triggers |
| A per-language package registry | npm/Cargo-shaped ecosystems | A public registry is an explicit non-goal (Phase 14) |

## 4. What the survey did *not* establish

- **It did not measure** whether Plain will be easier to learn or faster
  to write. That is Phase 13's task-log study, and a survey cannot
  substitute for it (register #049, #050).
- **It did not evaluate** compiler implementation strategies in depth;
  that is Phase 3 (Decision A) and the interpreter work.
- **It did not resolve** the language's relationship to the owner's
  `PlainP`/PL work (Open Question OQ-1 / condition C5). Until C5 is
  ruled, this specification must be treated as a **candidate** that may
  be merged into, or superseded by, that line of work.

## 5. Sources

| # | Source | Grade | Retrieved |
|---|---|---|---|
| S1 | Elm, *Syntax* reference ("a delightful language with friendly error messages … and no runtime exceptions") — <https://elm-lang.org/docs/syntax> | A | 2026-11-02 |
| S2 | Rust RFC 560, *integer overflow* (checked with `debug_assert!`, wrapping otherwise; `WrappingOps`) — <https://rust-lang.github.io/rfcs/0560-integer-overflow.html> | A | 2026-11-02 |
| S3 | Huon Wilson, *Myths and Legends about Integer Overflow in Rust* (behavior across profiles; `checked_*`, `wrapping_*`, `saturating_*`) — <https://huonw.github.io/blog/2016/04/myths-and-legends-about-integer-overflow-in-rust/> | B | 2026-11-02 |
| S4 | Kotlin, *Sealed classes and interfaces* (exhaustive `when` over sealed hierarchies) — <https://kotlinlang.org/docs/sealed-classes.html> | A | 2026-11-02 |
| S5 | Swift language reference material on enumerations, associated values, and exhaustive `switch` — <https://swiftgit.com/enumeration-syntax-in-swift/> (secondary; primary Swift book to be cited before Gate 1) | C | 2026-11-02 |
| S6 | Unison repository (content-addressed definitions; names separate from hashes) — <https://github.com/unisonweb/unison> | A | 2026-11-02 |
| S7 | Unicode Standard Annex #31, *Unicode Identifier and Pattern Syntax*, §2 Default Identifiers (UAX31-R1, XID_Start/XID_Continue) — <https://www.unicode.org/reports/tr31/> | A | 2026-11-02 |
| S9 | Secondary write-up on Kotlin `when` exhaustiveness in statement vs expression position — <https://learn.programmingline.com/learn/kotlin/kotlin-sealed-classes> (C-grade; A-grade verification owed before Gate 1) | C | 2026-11-02 |
| S8 | Unicode Technical Standard #39, *Unicode Security Mechanisms* (confusable skeletons, mixed-script detection, restriction levels) — <https://www.unicode.org/reports/tr39/> | A | 2026-11-02 |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: six-language survey, four applied lessons, six non-copies, three explicit non-findings. |
