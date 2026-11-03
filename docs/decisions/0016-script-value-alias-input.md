# Decision Record 0016 — Unicode Script-Value Alias Input for Script_Extensions

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — owner revision/ratification required; the manifest and A-46 text are unchanged |
| **Evidence label** | Established for the source-file format and immutable GitHub object identity; Proposed for adding it to Plain's input lock |
| **Deciders** | ZEMA research agent; Better-back selected revision of the A-* group but has not specified/approved this amendment |

## Context

A-46 / decision 0012 proposes a complete pinned Unicode input lock of 16 files. The implementation work exposed a representation mismatch needed by L-11: `Scripts.txt` expresses `Script` values with long names (for example, `Latin`), while `ScriptExtensions.txt` expresses values with ISO 15924 short aliases (for example, `Latn`). Directly comparing these strings would make Script_Extensions subset/intersection calculations incorrect. Unicode's `PropertyValueAliases.txt` is the authoritative mapping from the short to long Script value aliases. It is not one of the current 16 inputs.

This is a concrete dependency gap in the current proposed lock. The current property accessor explicitly refuses Script_Extensions comparisons without an alias map; no C4/restriction-level/security diagnostic is implemented using mixed aliases.

## Options considered

### Option A — Reuse: retrieve PropertyValueAliases.txt without pinning it

- **What it is, who maintains it, license:** Fetch the file opportunistically from Unicode/GitHub without recording its immutable identity in the project manifest.
- **Security cost / attack surface:** Unacceptable silent version drift; alias changes could alter the security diagnostic.
- **Performance cost:** Not measured or material to the issue.
- **Fit for ZEMA's defined app class:** Rejected because it breaks the non-silent Unicode input lock.

### Option B — Build on existing foundations: add a manifest-pinned alias file

- **What it is, who maintains it, license:** Add Unicode 17.0.0 `PropertyValueAliases.txt` from the same `unicode-org/unicodetools` commit and use it to canonicalize all `Scripts.txt` and `ScriptExtensions.txt` values to one alias representation.
- **Security cost / attack surface:** Keeps comparison inputs versioned and fail-closed; adds one Unicode source file and one generated lookup table. Raw file remains in ignored cache unless license decision C4 permits otherwise.
- **Performance cost:** Not measured; the lookup table is small by design, but no speed claim is made.
- **Fit for ZEMA's defined app class:** Directly resolves the representation mismatch for UTS #39 resolved-script/C4 logic and is consistent with the existing pinning approach.

### Option C — Invent: hard-code an alias table in Plain code

- **What it is, who maintains it, license:** Embed a hand-maintained short/long mapping in source.
- **Security cost / attack surface:** Duplicates Unicode data, risks omissions and version skew, and makes the data lock less auditable.
- **Performance cost:** Not measured.
- **Fit for ZEMA's defined app class:** Rejected absent evidence that a manual duplicate table is safer or more maintainable than the Unicode-provided alias data.

## Decision

**Proposed selection: Option B.** Amend the Unicode input set from 16 to 17 files by adding `PropertyValueAliases.txt`, then canonicalize Script and Script_Extensions values through its `sc` rows before any script-set comparison. Do not amend the source manifest or normative A-46 resolution until Better-back provides the requested revision wording or explicitly approves this proposal. Until then, Script_Extensions comparison is a stop condition for the relevant security work package; XID, normalization, and other independent work may continue.

## Candidate source identity (Established; not added to manifest)

- Repository: `unicode-org/unicodetools`
- Commit: `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c`
- Path: `unicodetools/data/ucd/17.0.0/PropertyValueAliases.txt`
- Git blob: `b92662eda2867baed56e55440e5187d52c1cb341`
- Byte length: `81,858`
- SHA-256: `64e9a5f76f7a1e8b5a47d6a1f9a26522a251208f5276bdfa1559dac7cf2e827a`
- Evidence: GitHub API contents/blob endpoints returned this identity; bytes were decoded from the immutable blob and locally re-hashed on 2026-11-03. The file was not saved into the repository or cache.

## Consequences

- **Positive:** Script aliases become comparable through the standard's own alias table; missing property data is called out instead of silently miscomputing security sets.
- **Negative / accepted costs:** The current 16-file proposal is incomplete for a normalized Script_Extensions implementation; source manifest counts and validation must change if the owner approves this amendment.
- **New obligations created:** If approved, add the file to the source manifest with URL, blob SHA-1, SHA-256, size, license note, and section; update the fetch verifier's expected count, data-audit checks, readiness response, A-46 wording, and evidence register; test all aliases used by Scripts/ScriptExtensions resolve.
- **What would make us revisit this decision:** A primary-source mapping already pinned in the repo that covers every value exactly; a Unicode 17 source correction; or owner/reviewer rejection of the extra input.

## Evidence

- Citations: Unicode 17.0.0 `Scripts.txt`, `ScriptExtensions.txt`, and candidate `PropertyValueAliases.txt`, all at the pinned unicodetools commit; source contents inspected 2026-11-03.
- Experiments: none; no C4/restriction-level calculation run.
- Related records: decisions 0012, 0014; readiness packet A-46; `src/plain/unicode17_properties.py` refuses Script_Extensions comparisons without a supplied alias map.
