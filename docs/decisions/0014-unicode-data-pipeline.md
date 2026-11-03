# Decision Record 0014 — Unicode 17.0.0 Data Pipeline for Phase 1

| Field | Detail |
|---|---|
| **Date** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 |
| **Status** | **Proposed** — owner/reviewer acceptance not recorded; no Unicode implementation is claimed |
| **Evidence label** | Established for version and manifest observations; Proposed for pipeline selection |
| **Deciders** | ZEMA research agent; owner Better-back has not ratified this decision |

## Context

The Plain draft proposes a Unicode 17.0.0 profile. The repository manifest pins 16 source/test files to `unicode-org/unicodetools` commit `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c`, with Git blob IDs, sizes, and SHA-256 values. The Python 3.11 host Unicode database is 14.0.0; it cannot be used as normative input. `unicode.org` is outside this sandbox's network allowlist, while the pinned GitHub API blob endpoint was verified reachable. The project license condition C4 is not yet resolved; do not vendor data or adopt third-party code into Git pending license review.

## Options considered

### Option A — Reuse: host runtime Unicode APIs

- **What it is, who maintains it, license:** Python `unicodedata` or another host's built-in Unicode functions.
- **Security cost / attack surface:** Low package surface, but version drift and undocumented property coverage can silently alter identifier security behavior.
- **Performance cost:** Not measured; irrelevant to Gate 1 acceptance.
- **Fit for ZEMA's defined app class:** Rejected for normative Unicode 17 behavior because Python's current UCD is 14.0.0 and does not satisfy the pin.

### Option B — Build on existing foundations: manifest-verified generated tables

- **What it is, who maintains it, license:** Fetch exact bytes from immutable GitHub blobs named in the project manifest; verify Git blob SHA-1, exact byte length, and SHA-256 before use; generate compact internal tables and algorithms with project-owned standard-library tooling.
- **Security cost / attack surface:** Fail-closed identity checking, no unpinned fallback, no host Unicode APIs for normative behavior. Downloaded data remains in a gitignored cache unless C4 and provenance review authorize vendoring.
- **Performance cost:** Not measured; optimize only after correctness and with no performance claims at Gate 1.
- **Fit for ZEMA's defined app class:** Directly follows the proposed source lock and can support the full set of identifier, normalization, bidi, and security rules.

### Option C — Invent: manually encode Unicode properties or copy an unpinned third-party table

- **What it is, who maintains it, license:** Hand-coded property exceptions, or tables copied from an unpinned library.
- **Security cost / attack surface:** High risk of omissions, version mismatch, and unclear provenance; difficult to review or reproduce.
- **Performance cost:** Not measured.
- **Fit for ZEMA's defined app class:** Poor; no evidence supports replacing the pinned authoritative data with hand-maintained guesses.

## Decision

**Proposed selection: Option B.** Implement a fetch-and-verify tool driven solely by `research/data/phase-01-source-manifest.json`. Fail closed on any missing/mismatched file. Keep data under a gitignored cache until C4 is decided and any license/provenance review is complete. Generate property tables from those exact bytes. Implement normalization without Python's host Unicode database and require every test row in the pinned `NormalizationTest.txt` to pass before the implementation is used by the lexer. Implement the exact UTS #39 rev32 skeleton and bidiSkeleton transformations, UAX #9 L2/L3/L4 operations, UTS #55 rev5 chunk/C4 logic, and join-control contexts against the locked files. This is a proposal; no data has yet been fetched or algorithm tested as part of execution.

## Consequences

- **Positive:** Reproducible inputs; explicit Unicode-version boundary; host Unicode version cannot silently change Plain behavior. The fetch verifier and NFC/NFD conformance checker have been implemented; all 16 inputs passed identity checks and all 20,034 NormalizationTest rows passed 200,340 assertions (evidence #106).
- **Negative / accepted costs:** Table generation, bidi, skeleton, and security-profile implementation remain significant work; GitHub availability is needed for clean acquisition in this sandbox; no offline build is possible until data has been cached under an approved distribution policy.
- **New obligations created:** Keep a machine-readable verification log; hash-check before parsing; preserve the normalization report; implement and test remaining properties/algorithms; disclose any Unicode-version upgrade through a new decision and regenerated tests.
- **What would make us revisit this decision:** A manifest error, a missing normative property source, an official Unicode correction, a license restriction, or an independent review showing the selected input set is insufficient.

## Evidence

- Citations: project source manifest `research/data/phase-01-source-manifest.json`; Unicode 17.0.0 data; Python 3.11 `unicodedata` docs at https://docs.python.org/3.11/library/unicodedata.html; GitHub API reachability check (2026-11-03).
- Experiments: [`EN-unicode17-normalization`](../../research/experiments/EN-unicode17-normalization/README.md) — all 16 source files verified; 20,034 normalization rows / 200,340 assertions passed; bidi/skeleton/profile algorithms remain untested.
- Related records: decisions 0009, 0011, 0012; research `phase-01-06-implementation-feasibility.md`.
