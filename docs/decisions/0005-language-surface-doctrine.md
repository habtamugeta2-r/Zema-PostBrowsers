# Decision Record 0005 — Plain's surface doctrine: one notation per concept, blocks by `:`, no method calls, no tuples

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — the specification is a draft; syntax freezes only at Gate 1, after the conformance suite passes |
| **Evidence label** | **Proposed** |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); owner sign-off pending (Gate 0 C1, `PlainP` ruling C5) |
| **Implements** | [`../plain/00-lexical-and-layout.md`](../plain/00-lexical-and-layout.md), [`../plain/03-ambiguities.md`](../plain/03-ambiguities.md) |

## Context

Phase 1 asks for the smallest language that can express the target app
class safely and readably, with "one notation for each feature before
syntactic sugar" and readable diagnostics with error spans. Every
language that tries this faces the same three temptations: convenience
syntax that creates a second way to say one thing; a large stylistic
surface that makes code review expensive; and diagnostics written for
compiler authors instead of users.

Plain also has a constraint most languages do not: layout, state, and
logic live in one file, so the surface has to stay readable when the
same construct appears next to a UI tree (Phase 6).

## Options considered

### Option A — Braces and semicolons (C/Rust/JS-shaped)

- What it is: explicit delimiters; layout is free-form.
- Security cost: none.
- Performance cost: none.
- Fit: **weaker.** The formatter stops being authoritative, and a
  UI-heavy file accumulates three nesting characters per level.

### Option B — Indentation-delimited, expression-oriented blocks

- What it is: blocks introduced by a line ending in `:`; dedent ends a
  block; a block's value is its tail expression.
- Security cost: none.
- Performance cost: none.
- Fit: **strongest.** One visual rule for structure; the formatter's
  output is canonical; the reader's eye tracks one column instead of
  matching braces. Prior art (Elm, Python-shaped layouts) shows the
  model is teachable, and Elm's error-message culture is a cited model
  for L-30…L-34.

### Option C — Both (optional braces, Scala-3 style)

- Fit: **rejected.** Two spellings for one concept is precisely the
  doctrine violation this decision exists to prevent; it also doubles
  the parser's diagnostic surface.

## Decision

**Choose Option B**, with these specific consequences, all normative in
the specification:

1. **One block introducer, `:`** — for function bodies, `if`/`else`,
   `when` arms, and `defer`. There is no `{}` block, no arrow-block, and
   no semicolon.
2. **One pattern introducer, `pattern:`** — `->` is reserved for return
   types only. Matching therefore has no arrow soup and no
   statement/expression asymmetry (the Kotlin trap).
3. **No method-call syntax.** `.` is field access; calls are `f(x)`. The
   compiler rejects `x.f(y)` with a message naming the canonical form.
4. **No tuples.** A product is a record; positional payloads are
   rejected (T-09). One product notation, one sum notation.
5. **No user-defined operators**, no compound assignment, no `elif`, no
   ternary, no index syntax. All are rejected **by name**, with the
   canonical alternative in the diagnostic.
6. **Sugar is legal only with a printed desugaring** (S-0…S-4). If the
   compiler cannot show the desugared form, the sugar does not exist.
7. **Diagnostics are part of the surface**: stable codes, spans, quoted
   source with carets, causes, machine-applicable fixes, no cascades
   (L-30…L-34), each asserted by a fixture.

## Consequences

- **Positive:** the syntax is small enough to specify completely in one
  document; the formatter can be canonical; errors can be written once
  and tested; a reviewer reads structure from indentation alone.
- **Negative / accepted costs:**
  - Copy-paste from brace languages will often be a syntax error — by
    design, but it is friction for newcomers.
  - No method chaining means data pipelines read as `x |> f |> g`;
    authors who prefer `x.f().g()` will find it awkward.
  - Indentation errors are catastrophic-looking (a whole block can move);
    L-19…L-24 and the formatter mitigate, but not eliminate, this.
  - No tuples makes some ad-hoc pairs verbose: `{ first: a, second: b }`.
- **New obligations created:**
  - A **diagnostics conformance section** (L-34) and a fixture per error
    code.
  - A **formatter** with canonical output is now load-bearing for
    readability, not cosmetic (Phase 13).
  - Any future sugar must include its desugaring printer in the same
    change.
- **What would make us revisit this decision:** the Phase 13 task-log
  study showing the surface itself (not tooling) causes measured
  rework — for example, chronic indentation mistakes or unreadable
  pipelines. A syntax change after Gate 1 requires a new decision, a
  dated revision, and a gate.

## Evidence

- Citations: [`../../research/phase-01-01-language-prior-art.md`](../../research/phase-01-01-language-prior-art.md) (Elm's no-runtime-exceptions culture and Kotlin's statement/expression exhaustiveness gap [S1][S4]; UAX #31 / UTS #39 for identifiers and confusables [S7][S8]).
- Experiments: none — Gate 1's conformance suite is the first test of this decision, and Phase 13 is the first measurement of its developer cost.
- Related records: [`0006-type-and-evaluation-core.md`](./0006-type-and-evaluation-core.md), [`0007-deferred-features.md`](./0007-deferred-features.md), [`../plain/03-ambiguities.md`](../plain/03-ambiguities.md).
