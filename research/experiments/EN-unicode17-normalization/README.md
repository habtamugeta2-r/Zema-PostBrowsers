# Experiment EN — Unicode 17.0.0 NFC/NFD Conformance Corpus

| Field | Detail |
|---|---|
| **Date(s)** | 2026-11-03 |
| **Phase / gate** | Phase 1 / Gate 1 preparation |
| **Researcher(s)** | ZEMA research agent |
| **Status** | **Complete** for the pinned NormalizationTest corpus; broader security profile remains untested |

## Hypothesis

Copied word-for-word from evidence register #106:

> "The project-owned Unicode 17.0.0 NFC/NFD implementation matched every row in the pinned NormalizationTest.txt corpus: 20,034 rows, 200,340 assertions, zero failures."

- **Confirms the hypothesis if:** the pinned source bytes match the manifest; the custom implementation (with no `unicodedata` import) checks all data rows and satisfies all five NFC and five NFD expected relations on each row with zero failures.
- **Retracts the hypothesis if:** any checked row differs, any row is skipped/malformed, or the corpus hash does not match the source manifest.

## Method

- **Workload:** every non-comment, non-directive row in Unicode 17.0.0 `NormalizationTest.txt` (all five columns, NFC and NFD).
- **Baseline(s):** The standard's expected output columns; no host Unicode implementation used as the oracle.
- **Metrics:** Row count, assertion count, failure count; no speed metric.
- **Environment:** Python 3.11.2 in the Arena sandbox; project-owned implementation at `src/plain/unicode17.py`; pinned files fetched from `unicode-org/unicodetools` commit `3ff0e2bb2ff8253831cb243d2d8e26a7f9534b1c` and verified before use.
- **Repetitions & statistics:** One full deterministic corpus run. This is conformance checking, not performance measurement.
- **Threats to validity:** The expected table and implementation could share an interpretation error; corpus completeness is a standard test obligation, not a proof for all possible strings; the test does not exercise bidiSkeleton, confusables, identifier profiles, or Plain lexer integration.

## Raw data

- [`normalization-report.json`](./normalization-report.json) — complete machine-readable result.
- [`phase-01-unicode-verification.json`](../../data/phase-01-unicode-verification.json) — identities for all 16 fetched inputs.

## Results

| Metric | Result | Expected |
|---|---:|---:|
| Data rows checked | 20,034 | All non-comment/non-directive rows |
| Normalization assertions | 200,340 | 10 per row (NFC and NFD for each of five columns) |
| Failures | 0 | 0 |

**Conclusion:** Hypothesis #106 is confirmed for this pinned published corpus. This does not establish complete Unicode conformance for arbitrary strings, UAX #9 bidi processing, UTS #39 skeletons, UTS #55 chunking, or the Plain language implementation.

## Reproduction

From repository root, after fetching/validating the pinned source files:

```sh
python3 tools/fetch_unicode17.py
python3 tools/check_unicode17_normalization.py
```

Environment used: Python 3.11.2. The commands use only the Python standard library. The first command writes raw source files only beneath ignored `research/data/.cache/unicode17/` and writes a compact verification log under `research/data/`.
