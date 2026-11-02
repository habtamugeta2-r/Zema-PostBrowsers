# Plain 0 — Lexical Structure, Layout, and Grammar

| Field | Detail |
|---|---|
| **Version** | 0.1 (draft) |
| **Phase / gate** | Phase 1 → Gate 1 |
| **Status** | Proposed — normative text, not frozen |
| **Rules** | `L-nn` (lexical/layout), `S-nn` (sanctioned sugar) |

---

## 1. Source and encoding

- **L-01** A source file **MUST** be valid UTF-8. A byte-order mark **MUST** be rejected (`PL0101`).
- **L-02** Line endings **MUST** be accepted as LF or CRLF and **MUST** be normalized to LF before parsing.
- **L-03** The only permitted indentation characters are the space (U+0020). A tab in indentation **MUST** be an error with a fix suggestion (`PL0102`).
- **L-04** Identifiers and text literals **MUST** be Unicode **NFC**. A non-NFC identifier **MUST** be an error that shows the NFC form and offers it as a fix (`PL0103`). Rationale: two visually identical names that differ in normalization are undeclared aliasing.

## 2. Comments

- **L-05** `--` starts a line comment that ends at the newline.
- **L-06** `{-` … `-}` is a block comment and **MUST** nest.
- **L-07** `---` starts a **doc comment** attached to the next declaration; it is preserved for tooling and documentation. A doc comment with no following declaration **MUST** be an error (`PL0104`).

## 3. Identifiers

- **L-08** An identifier **MUST** match `(_ | XID_Start) XID_Continue*` using the Unicode properties defined by [UAX #31](https://www.unicode.org/reports/tr31/) (UAX31-R1 default identifiers), with `_` additionally permitted as a start character. A lone `_` is the wildcard pattern, not an identifier.
- **L-09** Reserved words **MUST NOT** be identifiers. The set is closed for v0.1:
  `alias and as defer distinct else fn for if impl import in interface let mut not or return then type when with`
  (`return` is reserved even though `return` is not used in expressions — early exit is written with `?` for `Result` and by block structure otherwise; see A-14.)
- **L-10** **Confusable declarations are an error.** Two names declared in the same scope **MUST NOT** have equal UTS #39 skeletons ([UTS #39](https://www.unicode.org/reports/tr39/)) (`PL0105`). Example: Latin `pаypal` and Cyrillic `paypal`-shaped names in one scope is rejected, mirroring the classic homoglyph attack inside a code review.
- **L-11** **Mixed-script identifiers produce a warning** (`PL1101`) when a single identifier mixes Latin with Cyrillic or Greek. This is a floor, not a guarantee: the confusable mechanism maps characters, not sequences (see the research note's limits).
- **L-12** Naming conventions **MUST** be enforced as *errors* (they are syntax, not style, because the formatter and pattern syntax depend on the distinction):
  - types, interfaces, constructors, variants, modules: `UpperCamel` (`TaskList`, `Ok`);
  - values, parameters, fields, functions: `lower_snake` (`task_id`, `is_done`);
  - type parameters: `lower_snake` in angle brackets (`<a>`, `<item, error>`).
  A violation is `PL0106` with the corrected name as a fix.

## 4. Literals

- **L-13** Integer literals: decimal `0`, `1_000_000`; hexadecimal `0xFF`; binary `0b1011`. Underscores **MAY** separate digits but **MUST NOT** lead or trail.
- **L-14** Float literals **MUST** contain a decimal point with digits on both sides (`1.5`, `0.25`) and **MAY** carry an exponent (`1.5e3`). `1.` and `.5` are errors. A literal without a decimal point is an `Int`.
- **L-15** Text literals are `"..."` on one line with escapes `\n \t \" \\ \u{1F600}`. Multi-line strings are **deferred** (D-18); their absence is deliberate v0.1 scope.
- **L-16** The unit value is `()`. There is **no empty record literal**: `{}` is an error pointing at `()` (`PL0107`). One notation per concept.
- **L-17** List literals use `[a, b, c]` and **MAY** be empty (`[]`). Trailing commas are permitted in lists, records, argument lists, and parameter lists; the formatter removes them (S-0).
- **L-18** Integer literals that do not fit in `Int` **MUST** be a compile-time error (`PL0108`), never a wrapped value.

## 5. Layout

Plain is indentation-delimited. There are no semicolons and no braces for blocks.

- **L-19** A **block** is introduced by a line ending in `:`. The following lines that are indented deeper belong to it; the block ends at the first line at the same or lower indentation (a virtual `DEDENT`).
- **L-20** All statements in one block **MUST** start at the same column. That column **MUST** be greater than the column of the line that introduced the block. Widths are free (the formatter canonicalizes to two spaces per level).
- **L-21** A **case arm** is introduced by `pattern:` and owns a block. There is no `->` in patterns: `->` appears **only** in function return types. One notation per concept.
- **L-22** An expression **MAY** continue on the next line if, and only if, one of the following holds:
  1. the next line begins with a binary operator (`.`, `|>`, `and`, `or`, `==`, `!=`, `<`, `<=`, `>`, `>=`, `+`, `-`, `*`, `/`, `%`);
  2. the previous line ends with a binary operator, `,`, `(`, `[`, or `{`;
  3. the previous line ends with `:` (which introduces a block, not a continuation).

  Such continuation lines **MUST** be indented deeper than the first token of the statement. Any other newline ends the expression. This rule is the *only* line-continuation mechanism.
- **L-23** Blank lines and comment-only lines **MUST NOT** affect indentation analysis.
- **L-24** Empty blocks are forbidden (`PL0109`). A block's last line is either a statement or the block's tail expression.
- **L-25** One declaration per line; declarations **MUST NOT** be nested inside function bodies (local declarations are deferred, D-17).
- **L-26** A block's value is the value of its **tail expression**; if the block ends in a statement, its value is `()`.
- **L-27** A non-final expression statement **MUST** have type `()`. Discarding a non-`()` value silently is an error (`PL0110`) — the value must be bound to a name or consumed by a function.

## 6. Grammar (v0.1, compact EBNF)

```ebnf
program        = { declaration } EOF ;
declaration    = type_decl | alias_decl | distinct_decl | interface_decl
               | impl_decl | fn_decl | const_decl ;

type_decl      = "type" TYPE_NAME [ type_params ] "=" variant { "|" variant } ;
variant        = VARIANT_NAME [ "(" type ")" ] ;        (* at most one payload value *)
alias_decl     = "alias" TYPE_NAME "=" type ;
distinct_decl  = "distinct" TYPE_NAME "=" type ;

interface_decl = "interface" TYPE_NAME [ type_params ] ":" NEWLINE INDENT { sig } DEDENT ;
sig            = "fn" VALUE_NAME "(" [ params ] ")" [ "->" type ] ;
impl_decl      = "impl" TYPE_NAME "for" type ":" NEWLINE INDENT { fn_decl } DEDENT ;

fn_decl        = "fn" VALUE_NAME [ type_params ] "(" [ params ] ")" [ "->" type ] block ;
const_decl     = "let" VALUE_NAME ":" type "=" expr NEWLINE ;
params         = param { "," param } [ "," ] ;
param          = VALUE_NAME ":" type ;
type_params    = "<" TYPE_PARAM { "," TYPE_PARAM } ">" ;

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
primary        = literal | VALUE_NAME | record | list
               | "(" expr ")" | if_expr | when_expr | lambda ;

record         = "{" field { "," field } [ "," ] "}" ;
field          = VALUE_NAME ":" expr ;
list           = "[" [ expr { "," expr } [ "," ] ] "]" ;
if_expr        = "if" expr block [ "else" block ] ;
when_expr      = "when" expr ":" NEWLINE INDENT { arm } DEDENT ;
arm            = pattern ":" block ;
lambda         = "fn" "(" [ params ] ")" [ "->" type ] block ;

pattern        = "_" | INT | TEXT | "()"
               | VARIANT_NAME [ "(" pattern ")" ]
               | VALUE_NAME | record_pattern ;
record_pattern = "{" VALUE_NAME ":" pattern { "," VALUE_NAME ":" pattern } [ "," ] "}" ;

type           = TYPE_NAME [ "<" type { "," type } ">" ]
               | "fn" "(" [ type { "," type } ] ")" "->" type
               | record_type ;
record_type    = "{" VALUE_NAME ":" type { "," VALUE_NAME ":" type } [ "," ] "}" ;
literal        = INT | FLOAT | TEXT | "()" ;
```

Notes that the grammar alone does not express, and which **MUST** be checked by the compiler rather than the parser: exhaustiveness of `when` (E-14), the `else`-required rule for non-`()` `if` (E-15), `mut`-capture rejection (E-11), interface coherence (T-16), and inference limits (T-20).

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
| **S-3** | `"Count: {count}"` | `Text.concat([Text.from("Count: "), Display.display(count)])` | Requires `Display` for the interpolated type (T-15); unknown type is `PL0113` |
| **S-4** | `as` between a `distinct` type and its representation | identity at runtime; no allocation | `as` is **not** a general cast: any other use is `PL0114` (T-17) |

**S-5 (forbidden sugar).** Compound assignment (`+=`), `elif`, ternaries, `do`-notation, list comprehensions, index syntax `xs[i]`, and method calls are **not** sugar and **MUST** be rejected with a message naming the canonical form (`PL0115`). Indexing is rejected outright because bounds-safe access is `List.get(xs, i) -> Option<a>` (T-04).

## 9. Diagnostics (normative)

Phase 1 requires "readable diagnostics with error spans". These rules make that testable.

- **L-30** Every diagnostic **MUST** carry: a stable code (`PLnnnn` / `PL1nnn` for warnings), a severity, a primary span with `line:column` start and end, a one-line message, a cause paragraph, and — where a fix is mechanical — one or more machine-applicable fixes.
- **L-31** Every diagnostic **MUST** quote the offending source line with a caret underline.
- **L-32** The compiler **MUST NOT** cascade: after an unrecoverable parse or type error in a declaration, subsequent errors in that declaration **MUST** be suppressed and summarized (`PL0199`).
- **L-33** Diagnostic wording **MUST** use the language's own terms ("a block", "a case arm", "a record field"), never internal AST or IR names.
- **L-34** The conformance suite **MUST** include a diagnostics section: for each of `PL0101`–`PL0116`, `PL1101`, `PL1102`, and `PL0199`, a fixture asserting code, span, and the presence of a fix where required.

## 10. Open questions owned by this document

| ID | Question | Status |
|---|---|---|
| A-03 | Tuples? | **Resolved: none.** A product is a record; a tuple would be a second notation for it |
| A-04 | Tuple/record destructuring in `let`? | **Deferred** (D-05); pattern matching in `when` is the only destructuring |
| A-15 | `return` / early exit? | **Resolved: no `return` in v0.1.** `?` exits a `Result` function with an error; otherwise blocks are expressions. The keyword is reserved to keep the door open |
| A-20 | Line continuation | **Resolved: L-22**, the only mechanism |

See [`03-ambiguities.md`](./03-ambiguities.md) for the full register.
