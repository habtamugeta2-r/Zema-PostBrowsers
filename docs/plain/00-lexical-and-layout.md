# Plain 0 — Lexical Structure, Layout, and Grammar

| Field | Detail |
|---|---|
| **Version** | 0.2.5 (draft) — v0.2.5 adds diagnostic codes to rules that named none; no rule's meaning changed |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Proposed — normative text, not frozen |
| **Rules** | `L-nn` (lexical/layout), `S-nn` (sanctioned sugar) |

---

## 1. Source and encoding

- **L-01** A source file **MUST** be valid UTF-8. A byte-order mark **MUST** be rejected (`PL0101`).
- **L-02** Line endings **MUST** be accepted as LF or CRLF and **MUST** be normalized to LF before parsing. Other Unicode line/paragraph separators (U+0085, U+2028, U+2029) **MUST NOT** act as source line terminators outside text literals (`PL0126`); they are data or invalid source, not hidden layout ([UTS #55 revision 5](https://www.unicode.org/reports/tr55/tr55-5.html#Whitespace-Syntax) §3.2).
- **L-03** The only permitted indentation characters are the space (U+0020). A tab in indentation **MUST** be an error with a fix suggestion (`PL0102`).
- **L-04** Identifiers **MUST** be treated as their Unicode **NFC** form. A non-NFC identifier **MUST** be an error that shows the NFC form and offers it as a fix (`PL0103`). Text literals **MUST NOT** be silently normalized: their scalar-value contents are data, including non-NFC sequences. Tooling **MAY** show a “normalize this text” fix only when the user explicitly requests it ([UTS #55 revision 5](https://www.unicode.org/reports/tr55/tr55-5.html#Normalization-and-Case) §3.1.1; [UAX #15 revision 57](https://www.unicode.org/reports/tr15/tr15-57.html) states normalization forms are not closed under concatenation).

## 2. Comments

- **L-05** `--` starts a line comment that ends at the newline.
- **L-06** `{-` … `-}` is a block comment and **MUST** nest. An unterminated block comment is `PL0125`, with its span opening at `{-`.
- **L-07** `---` starts a **doc comment** attached to the next declaration; it is preserved for tooling and documentation. A doc comment with no following declaration **MUST** be an error (`PL0104`).

## 3. Identifiers

- **L-08** An identifier **MUST** match the declared profile `(_ | XID_Start) XID_Continue*` (`PL0118`), using XID_Start/XID_Continue from **Unicode 17.0.0** (Unicode 17.0.0; UAX #31 rev43/C1/C2; UAX #15 rev57; UAX #9 rev51; UTS #39 rev32; UTS #55 rev5), the initial pinned profile (A-27, decision 0009). This is a UAX #31 R1-2 profile that adds `_` to Start; it is not unmodified R1-1. A lone `_` is the wildcard pattern, not an identifier. The implementation **MUST** report the Unicode data release and all algorithm revisions in the adopted profile: UAX #31, #15, and #9, plus UTS #39 and #55. Exact data-file hashes are in the source manifest. A data upgrade requires a decision record, data diff, regenerated fixtures, and a conformance rerun; no silent bump.
- **L-09** Reserved words **MUST NOT** be identifiers (`PL0119`). The set is closed for v0.1:
  `alias and as defer distinct else fn for if impl import in interface let mut not or return then type when with`
  (`return` is reserved even though `return` is not used in expressions — early exit is written with `?` for `Result` and by block structure otherwise; see A-15.)
- **L-10** **Confusable declarations are an error.** Two distinct, simultaneously visible names are directionally confusable if `bidiSkeleton(d, X) == bidiSkeleton(d, Y)` for any `d ∈ {LTR, RTL, FS}` under UTS #39 rev32 (decision 0012); a matching direction produces the proposed `PL0105` error. The standard’s compatibility `skeleton(X)` is only `bidiSkeleton(LTR, X)`, so Plain’s proposed relation is broader than that default. Compare names that resolve to distinct declarations in the same scope or that are both visible at a use site; repeated references resolving to the same declaration are not collisions. Reserved/prelude names participate where visible. Directional skeletons are internal comparison data only, not normalized source text or display text (UTS #39 rev32 §4; UTS #55 rev5 §5.1.1; decisions 0011/0012). This is a proposed mitigation, not an anti-spoofing guarantee; owner ratification and conformance are pending.
- **L-11** Unicode security diagnostics follow UTS #55 rev5 §§5.1.2–5.1.3, with the proposed all-direction identifier relation from decision 0012:
  - Identifier chunks use the exact CamelBoundary, HATBoundary, and snake-boundary rules in UTS #55 §5.1.2.1, including `Mn`/`Me` mark handling and the Greek `Lt` exception; no other boundaries are introduced.
  - A chunk **MUST** receive a proposed `PL1101` warning when it meets UTS #55 §5.1.2.2 C4: restriction level above Highly Restrictive, plus a qualifying `Y` whose resolved script set is neither empty nor `ALL`, is a subset of the union of the chunk’s `Script_Extensions`, and is in the UTS #39 rev32 General Security Profile. For Plain identifiers, `Y` is directionally confusable with the chunk if any LTR/RTL/FS `bidiSkeleton` values match (decision 0012). This is an explicit proposed extension of the C4 confusable relation, informed by UTS #39 §4; it is not presented as wording in UTS #55. A chunk above the restriction level with no qualifying `Y` under the adopted relation is visibly mixed-script and **MUST NOT** receive `PL1101`.
  - An identifier outside the UTS #39 rev32 General Security Profile **MUST** receive a separate proposed `PL1104` warning. U+200C/U+200D are profile exceptions only when the complete UTS #39 §3.1.1.1 A1/A2/B context succeeds, including its single-script restriction (ignoring Common/Inherited) and NFC condition. L-04 already requires NFC identifiers. The warning does not reject an otherwise syntactically valid identifier and is a separate diagnostic from `PL1101`. Per UTS #55 §5.1.3, Plain proposes that `PL1104` also be independently suppressible from `PL0105`/`PL1101`; the exact tool configuration mechanism is deferred (decision 0012, A-47).
  - These checks **MUST NOT** be replaced by a blanket “Latin plus Cyrillic/Greek” heuristic. This is bounded mitigation, not a guarantee against spoofing; all-direction outcomes remain unimplemented and untested.
- **L-12** Name roles are determined by declaration context and name resolution, **not** by case alone. The grammar’s `TYPE_NAME`, `VALUE_NAME`, and `VARIANT_NAME` are resolved categories, not case-sensitive token classes.
  - recommended style: types/interfaces/constructors/variants/modules `UpperCamel`; values/parameters/fields/functions `lower_snake`; type parameters `lower_snake`.
  - For bicameral scripts, a style violation is a warning (`PL1103`) with a suggested fix, not a parse error. For unicameral scripts, case-based style checks are not applied. This keeps Ethiopic, Arabic, Hebrew, CJK, and other scripts usable ([UTS #55 revision 5](https://www.unicode.org/reports/tr55/tr55-5.html#Computer-Language-Specifications) §3.1.2).
  - `PL0106` is retired as an error code; the conformance registry records it as historical, not active.

## 4. Literals

- **L-13** Integer literals: decimal `0`, `1_000_000`; hexadecimal `0xFF`; binary `0b1011`. Underscores **MAY** separate digits but **MUST NOT** lead or trail (`PL0120`).
- **L-14** Float literals **MUST** contain a decimal point with digits on both sides (`1.5`, `0.25`) and **MAY** carry an exponent (`1.5e3`). `1.` and `.5` are errors (`PL0121`). A literal without a decimal point is an `Int`.
- **L-15** Text literals are `"..."` on one line with escapes `\n \t \" \\ \u{1F600}`. Escape values **MUST** be Unicode scalar values: surrogate code points U+D800–U+DFFF and values above U+10FFFF are errors (`PL0117`). Literal contents are not normalized (L-04). Multi-line strings are **deferred** (D-18); their absence is deliberate v0.1 scope.
- **L-16** The unit value is `()`. There is **no empty record literal**: `{}` is an error pointing at `()` (`PL0107`). One notation per concept.
- **L-17** List literals use `[a, b, c]` and **MAY** be empty (`[]`). Trailing commas are permitted in lists, records, argument lists, and parameter lists; the formatter removes them (S-0).
- **L-18** Integer literals that do not fit in `Int` **MUST** be a compile-time error (`PL0108`), never a wrapped value.

## 5. Layout

Plain is indentation-delimited. There are no semicolons and no braces for blocks.

- **L-19** A **block** is introduced by a line ending in `:`. The following lines that are indented deeper belong to it; the block ends at the first line at the same or lower indentation (a virtual `DEDENT`).
- **L-20** All statements in one block **MUST** start at the same column. That column **MUST** be greater than the column of the line that introduced the block. Either violation is `PL0122`. Widths are free (the formatter canonicalizes to two spaces per level).
- **L-21** A **case arm** is introduced by `pattern:` and owns a block. There is no `->` in patterns: `->` appears **only** in function return types. One notation per concept.
- **L-22** An expression **MAY** continue on the next line if, and only if, one of the following holds:
  1. the next line begins with a binary operator (`.`, `|>`, `and`, `or`, `==`, `!=`, `<`, `<=`, `>`, `>=`, `+`, `-`, `*`, `/`, `%`);
  2. the previous line ends with a binary operator, `,`, `(`, `[`, or `{`.
  A trailing `:` introduces a block under L-19; it is not an expression continuation. A block opener and a continuation are mutually exclusive.

  Such continuation lines **MUST** be indented deeper than the first token of the statement (`PL0123`). Any other newline ends the expression. This rule is the *only* line-continuation mechanism.
- **L-23** Blank lines and comment-only lines **MUST NOT** affect indentation analysis.
- **L-24** Empty blocks are forbidden (`PL0109`). A block's last line is either a statement or the block's tail expression.
- **L-25** One declaration per line; declarations **MUST NOT** be nested inside function bodies (`PL0124`; local declarations are deferred, D-17).
- **L-26** A block's value is the value of its **tail expression**; if the block ends in a statement, its value is `()`.
- **L-27** A non-final expression statement **MUST** have type `()`. Discarding a non-`()` value silently is an error (`PL0110`) — the value must be bound to a name or consumed by a function.

## 6. Grammar (v0.2.4, compact EBNF)

```ebnf
program        = { declaration } EOF ;
declaration    = type_decl | alias_decl | distinct_decl | interface_decl
               | impl_decl | fn_decl | const_decl ;

type_decl      = "type" TYPE_NAME [ type_params ] "=" variant { "|" variant } ;
variant        = VARIANT_NAME [ "(" type ")" ] ;       (* at most one payload value *)
alias_decl     = "alias" TYPE_NAME [ type_params ] "=" type ;
distinct_decl  = "distinct" TYPE_NAME [ type_params ] "=" type ;

interface_decl = "interface" TYPE_NAME [ type_params ] ":" NEWLINE INDENT { sig } DEDENT ;
sig            = "fn" VALUE_NAME [ type_params ] "(" [ params ] ")" "->" type ;
impl_decl      = "impl" [ type_params ] TYPE_NAME [ type_args ] "for" type ":" NEWLINE INDENT { fn_decl } DEDENT ;

fn_decl        = "fn" VALUE_NAME [ type_params ] "(" [ params ] ")" "->" type block ;
const_decl     = "let" VALUE_NAME ":" type "=" const_expr NEWLINE ;
params         = param { "," param } [ "," ] ;
param          = VALUE_NAME ":" type ;
type_params    = "<" type_param { "," type_param } ">" ;
type_param     = TYPE_PARAM [ ":" TYPE_NAME { "+" TYPE_NAME } ] ;
type_args      = "<" type { "," type } ">" ;

block          = ":" NEWLINE INDENT { statement } [ expr NEWLINE ] DEDENT ;
statement      = let_stmt | mut_stmt | assign_stmt | defer_stmt ;
let_stmt       = "let" VALUE_NAME [ ":" type ] "=" expr NEWLINE ;
mut_stmt       = "mut" VALUE_NAME [ ":" type ] "=" expr NEWLINE ;
assign_stmt    = placeable "=" expr NEWLINE ;
defer_stmt     = "defer" block ;
placeable      = VALUE_NAME { "." VALUE_NAME } ;

expr           = pipe_expr ;
pipe_expr      = or_expr { "|>" or_expr } ;
or_expr        = and_expr { "or" and_expr } ;
and_expr       = cmp_expr { "and" cmp_expr } ;
cmp_expr       = add_expr [ cmp_op add_expr ] ;
cmp_op         = "==" | "!=" | "<" | "<=" | ">" | ">=" ;
add_expr       = mul_expr { ( "+" | "-" ) mul_expr } ;
mul_expr       = unary { ( "*" | "/" | "%" ) unary } ;
unary          = [ "not" | "-" ] postfix ;
postfix        = primary { "." VALUE_NAME | "(" [ args ] ")" | "?" | "as" type } ;
args           = expr { "," expr } [ "," ] ;
primary        = literal | name_expr | constructor | record | list
               | "(" expr ")" | if_expr | when_expr | lambda ;
name_expr      = VALUE_NAME { "." VALUE_NAME } ;     (* resolved path or field projection *)
constructor    = VARIANT_NAME | TYPE_NAME "." VARIANT_NAME ; (* e.g. True, Option.None *)

record         = "{" field { "," field } [ "," ] "}"
               | "{" expr "with" field { "," field } [ "," ] "}" ;
field          = VALUE_NAME ":" expr ;
list           = "[" [ expr { "," expr } [ "," ] ] "]" ;
if_expr        = "if" expr block [ "else" block ] ;
when_expr      = "when" expr ":" NEWLINE INDENT { arm } DEDENT ;
arm            = pattern ":" block ;
lambda         = "fn" "(" [ lambda_params ] ")" [ "->" type ] block ;
lambda_params  = lambda_param { "," lambda_param } [ "," ] ;
lambda_param   = VALUE_NAME [ ":" type ] ;

pattern        = "_" | INT | TEXT | "()"
               | "-" INT
               | VARIANT_NAME [ "(" pattern ")" ]
               | VALUE_NAME | record_pattern ;
record_pattern = "{" VALUE_NAME ":" pattern { "," VALUE_NAME ":" pattern } [ "," ] "}" ;

type           = TYPE_NAME [ type_args ]
               | TYPE_PARAM
               | "fn" "(" [ type { "," type } ] ")" "->" type
               | record_type ;
record_type    = "{" VALUE_NAME ":" type { "," VALUE_NAME ":" type } [ "," ] "}" ;
literal        = INT | FLOAT | TEXT | "()" ;
const_expr     = literal | const_variant | const_record | const_list | distinct_cast ;
const_variant  = constructor [ "(" const_expr ")" ] ;
const_record   = "{" VALUE_NAME ":" const_expr { "," VALUE_NAME ":" const_expr } [ "," ] "}" ;
const_list     = "[" [ const_expr { "," const_expr } [ "," ] ] "]" ;
distinct_cast  = const_expr "as" type ;
```

The parser produces names; the resolver assigns the `TYPE_NAME`,
`VALUE_NAME`, and `VARIANT_NAME` roles from declaration context. This is
why case conventions can be warnings without making the grammar
ambiguous (L-12). `constructor` in expressions resolves to a value in
the variant namespace; `Bool`’s `True`/`False`, `Option`’s `None`, and
`Result`’s `Ok`/`Err` are ordinary prelude constructors.

Notes that the grammar alone does not express, and which **MUST** be checked by the compiler rather than the parser: exhaustiveness of `when` (E-14), the `else`-required rule for non-`()` `if` (E-28), `mut`-capture rejection (E-17), interface coherence (T-18), and inference limits (T-21).

## 7. Operator precedence and associativity

Highest to lowest; all binary operators are left-associative except `<`, `<=`, `>`, `>=`, `==`, `!=`, which are **non-associative** (a chained comparison is a syntax error rather than a silent boolean).

| Level | Operators | Associativity |
|---|---|---|
| 1 | `.` (field access), `(…)` (call), `?`, `as` | postfix, left |
| 2 | unary `not`, unary `-` | prefix |
| 3 | `*` `/` `%` | left |
| 4 | `+` `-` | left |
| 5 | `==` `!=` `<` `<=` `>` `>=` | **none** |
| 6 | `and` | left (short-circuit) |
| 7 | `or` | left (short-circuit) |
| 8 | `\|>` | left |
| 9 | `if`, `when`, `fn` (block forms) | lowest; delimited by layout |

- **L-28** There are **no user-defined operators** and no operator sections (D-16). The table above is closed.
- **L-29** `.` **only** performs field access. `x.f(y)` is a type error explaining that calls are written `f(x)` (`PL0111`). Method-call syntax is deliberately absent.

## 8. Sanctioned sugar

Sugar exists only where the desugaring is total and mechanical. Each is listed here with its expansion; the compiler **MUST** be able to print the desugared form.

| ID | Sugar | Desugaring | Notes |
|---|---|---|---|
| **S-0** | Trailing commas | removed by the parser | Canonical form has none |
| **S-1** | `{ r with done = True }` | a record literal listing every field of `r`, with `done` replaced. Requires deducible record type: if the record type of `r` is not known from the surrounding annotation, `PL0112` | Preserves "one way to build a record" |
| **S-2** | `x \|> f` | `f(x)` | `x \|> f(y)` is `f(y, x)` — piping appends as the **last** argument. This is the only meaning; there is no subject-first variant |
| **S-3** | `"Count: {count}"` | `Text.concat(["Count: ", Display.display(count)])` | Requires `Display` for the interpolated type (T-15); unknown type is `PL0113` |
| **S-4** | `as` between a `distinct` type and its representation | identity at runtime; no allocation | `as` is **not** a general cast: any other use is `PL0114` (T-17) |

**S-5 (forbidden sugar).** Compound assignment (`+=`), `elif`, ternaries, `do`-notation, list comprehensions, index syntax `xs[i]`, and method calls are **not** sugar and **MUST** be rejected with a message naming the canonical form (`PL0115`). Indexing is rejected outright because bounds-safe access is `List.get(xs, i) -> Option<a>` (T-04).

## 9. Diagnostics (normative)

Phase 1 requires "readable diagnostics with error spans". These rules make that testable.

- **L-30** Every diagnostic **MUST** carry: a stable code (`PLnnnn` / `PL1nnn` for warnings), a severity, a primary span with `line:column` start and end, a one-line message, a cause paragraph, and — where a fix is mechanical — one or more machine-applicable fixes.
- **L-31** Every diagnostic **MUST** quote the offending source line with a caret underline. Directional/bidi control characters and other invisible format controls in quoted source **MUST** be escaped or visibly marked so diagnostic output cannot reorder executable code misleadingly ([UTS #55 revision 5](https://www.unicode.org/reports/tr55/tr55-5.html) §§4–5).
- **L-32** The compiler **MUST NOT** cascade: after an unrecoverable parse or type error in a declaration, subsequent errors in that declaration **MUST** be suppressed and summarized (`PL0199`).
- **L-33** Diagnostic wording **MUST** use the language's own terms ("a block", "a case arm", "a record field"), never internal AST or IR names.
- **L-34** The conformance suite **MUST** include a diagnostics section: for every active diagnostic code in the generated registry, a fixture asserting code, span, and the presence of a fix where required. The registry is derived from the rules, not a hand-maintained range; retired codes are marked historical.

## 10. Questions owned by this document

| ID | Question | Status |
|---|---|---|
| A-03 | Tuples? | **Resolved: none.** A product is a record; a tuple would be a second notation for it |
| A-04 | Tuple/record destructuring in `let`? | **Deferred** (D-15); pattern matching in `when` is the only destructuring |
| A-15 | `return` / early exit? | **Resolved: no `return` in v0.1.** `?` exits a `Result` function with an error; otherwise blocks are expressions. The keyword is reserved to keep the door open |
| A-20 | Line continuation | **Resolved: L-22**, the only mechanism |
| A-27 | Unicode/UTS #39 version pin | **Resolved (proposed):** Unicode 17.0.0 / UAX #31 rev43 / UAX #15 rev57 / UAX #9 rev51 / UTS #39 rev32 / UTS #55 rev5; upgrade policy in L-08 and decision 0009 |
| A-29/A-30 | Case-based naming and name roles | **Resolved:** contextual roles; style warnings do not exclude unicameral scripts |
| A-31 | Trailing `:` vs continuation | **Resolved:** block opener, not continuation |
| A-41 | Bidi/invisible controls in diagnostics | **Resolved (partial):** safe quoting now; full editor rendering Phase 13 |

See [`03-ambiguities.md`](./03-ambiguities.md) for the full register.
