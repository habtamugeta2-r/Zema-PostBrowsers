# Phase 1 · Record 01 — Language Prior Art: What "Easy" Already Costs Somebody Else

| Field | Detail |
|---|---|
| **Document** | Research record `research/phase-01-01-language-prior-art.md` |
| **Version** | 1.1 |
| **Date** | 2026-11-03 |
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
| L1 | **Elm** | A small, purely functional core with no exception primitives can ship production apps: failure is carried by `Maybe`/`Result` in the type, and the official homepage advertises “No Runtime Exceptions” | Ports are typed in Elm as `Cmd msg` / `Sub msg`; the JavaScript implementation outside Elm is not checked by Elm’s type system. The seam is typed at the boundary, not “untyped” | The no-exceptions posture, exhaustive `case`, human-readable errors; capability-mediated authority remains ZEMA’s separate design | E | [S1], [S10], [S11] |
| L2 | **Rust** | Ownership and `Option`/`Result` make absence and failure explicit; `?` propagation keeps the happy path readable | Overflow checks follow `debug-assertions`/`overflow-checks`; `MIN / -1` and `MIN % -1` are checked even when overflow checks are disabled. Profile-dependent wrapping remains a real difference | `?`, `Result`, no null; checked-in-all-profiles remains Plain’s choice, stated precisely | E | [S2], [S3], [S12] |
| L3 | **Kotlin** | Sealed hierarchies + `when` give closed-world exhaustiveness | Since Kotlin 1.7, non-exhaustive `when` **statements** over enum, sealed, and Boolean subjects are errors. The old statement-form gap is historical for those subjects; other subject types still differ by form | Expression-only matching as a simplicity choice, not as a fix for a current sealed-union hole | E | [S4], [S13] |
| L4 | **Swift** | Enums with associated values make illegal states unrepresentable; the official book says every `switch` statement must be exhaustive | The language carries a large surface (protocols, extensions, property wrappers, result builders) that a beginner must learn before reading real code | Associated-value unions and exhaustive matching; **not** the surface area | E | [S5], [S14] |
| L5 | **Unison** | Content-addressed definitions separate names from hashes and remove some name/order conflicts; abilities provide algebraic-effect handlers | Code lives in a database, not files; handlers are not host capabilities; content addressing does not prove semantic compatibility | Nothing in v1 — deferred with a stated trigger; correct the handler/capability conflation | E | [S6], [S15] |
| L6 | **Unicode UAX #31 / UTS #39 / UTS #55** | Identifier syntax can be specified and versioned; UTS #55 gives programming-language-specific source-handling guidance | Skeletons are sequence-aware but versioned/incomplete; mixed-script checks need identifier chunks; text literals should not be silently normalized | Declared identifier profile, NFC identifiers, preserved text data, chunk-based warnings, safe diagnostic quoting | E | [S7], [S8], [S16] |

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

Kotlin has two forms of the same construct [S4]. Since 1.7, enum,
sealed, and Boolean `when` statements are exhaustive too [S13], so the
old “statement-form gap” is not a current defect for those subjects.
The durable lesson is narrower: **one form with one rule is easier to
specify and teach than a context-dependent surface.**

> **Applied:** matching is always an expression, always checked — one
> form, one rule. *Label: P.*

### Lesson 4 — Unicode identifiers need a rule and a defense

UAX #31 gives a default syntax [S7]; UTS #39 gives skeleton comparison
and restriction levels, while admitting the mechanism is a pragmatic
floor [S8]. ZEMA's app class includes names in Ethiopic, Arabic, Hebrew,
and Indic scripts, so "ASCII identifiers only" is not acceptable — and
"any Unicode" without a confusable rule is a spoofing vector inside a
code review.

> **Applied:** declared identifier profile, NFC identifiers, text data
> preserved, versioned skeleton collisions rejected, chunk-based
> mixed-script warnings, and case conventions that do not exclude
> unicameral scripts. *Label: P; see record 03.*

## 3. What Plain deliberately does **not** copy

| Not copied | From | Why |
|---|---|---|
| Build-profile-dependent overflow | Rust | Same program, two behaviors — unacceptable for the target class |
| Statement-form matching | Kotlin | One expression form is simpler to specify; current Kotlin already closes the sealed/enum/Boolean statement gap |
| Authority-by-convention at host seams | Elm ports | Elm ports are typed, but ZEMA additionally wants opaque host-issued capability handles (Phase 5) |
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
| S1 | Elm, *Syntax* reference — <https://elm-lang.org/docs/syntax> | A | 2026-11-02; rechecked 2026-11-03 |
| S2 | Rust RFC 560, *integer overflow* (checked with `debug_assert!`, wrapping otherwise; `WrappingOps`) — <https://rust-lang.github.io/rfcs/0560-integer-overflow.html> | A | 2026-11-02 |
| S3 | Huon Wilson, *Myths and Legends about Integer Overflow in Rust* (behavior across profiles; `checked_*`, `wrapping_*`, `saturating_*`) — <https://huonw.github.io/blog/2016/04/myths-and-legends-about-integer-overflow-in-rust/> | B | 2026-11-02 |
| S4 | Kotlin, *Sealed classes and interfaces* (exhaustive `when` over sealed hierarchies) — <https://kotlinlang.org/docs/sealed-classes.html> | A | 2026-11-02 |
| S5 | Swift.org, *The Swift Programming Language: Enumerations* — pinned `swift-book` commit; see source manifest | A | 2026-11-03 (replaces C-grade secondary) |
| S6 | Unison repository (content-addressed definitions; names separate from hashes) — <https://github.com/unisonweb/unison> | A | 2026-11-02 |
| S7 | Unicode Standard Annex #31, *Unicode Identifier and Pattern Syntax*, §2 Default Identifiers (UAX31-R1, XID_Start/XID_Continue) — <https://www.unicode.org/reports/tr31/> | A | 2026-11-02 |
| S9 | Secondary write-up on Kotlin `when` exhaustiveness — **retired**, superseded by S13 | C (historical) | 2026-11-02 |
| S8 | Unicode Technical Standard #39, *Unicode Security Mechanisms* (confusable skeletons, mixed-script detection, restriction levels) — <https://www.unicode.org/reports/tr39/> | A | 2026-11-02 |
| S10 | Elm homepage, “No Runtime Exceptions” — <https://elm-lang.org/> | A (official claim) | 2026-11-03 |
| S11 | Elm, *Ports* — <https://guide.elm-lang.org/interop/ports> | A | 2026-11-03 |
| S12 | Rust Reference, *Operator expressions — Overflow*, pinned commit | A | 2026-11-03 |
| S13 | JetBrains, *Compatibility guide for Kotlin 1.7.0*, pinned commit | A | 2026-11-03 |
| S14 | Swift.org, *Control Flow*, pinned commit | A | 2026-11-03 |
| S15 | Unison, *Introduction to Abilities* — <https://www.unison-lang.org/docs/fundamentals/abilities/> | A | 2026-11-03 |
| S16 | Unicode, UTS #55 revision 5, *Unicode Source Code Handling* | A | 2026-11-03 |

## 6. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-02 | 1.0 | Record created: six-language survey, four applied lessons, six non-copies, three explicit non-findings. |
| 2026-11-03 | 1.1 | Primary-source corrections: Elm typed ports/homepage claim, Rust overflow edge cases, Kotlin 1.7 statement exhaustiveness, Swift primary book, Unison abilities, UTS #55. Details in record 03. |
