# Experiment EN — <short title> — TEMPLATE

> **How to use:** Create `experiments/EN-<slug>/README.md` from this
> template and keep the raw data beside it in the same folder. This is
> the **MEASURE** step of the five-step loop. Summary numbers without
> raw data do not pass a gate.

| Field | Detail |
|---|---|
| **Date(s)** | YYYY-MM-DD |
| **Phase / gate** | Phase N / Gate N |
| **Researcher(s)** | Names |
| **Status** | Designed · Running · Complete · Invalidated (say why) |

## Hypothesis

_The single claim being tested, copied word-for-word from the evidence
register (#NNN). State in advance what result would confirm it and
what result would retract it._

- **Confirms the hypothesis if:**
- **Retracts the hypothesis if:**

## Method

- **Workload:** (must be an *equivalent workload* — same features,
  tests, migrations, accessibility, error handling, schema, and config
  across all contenders)
- **Baseline(s):** (e.g., web/PWA build, native/Flutter build — with
  versions)
- **Metrics:** (per-metric only; **no composite scores**)
- **Environment:** hardware, OS, versions, power/thermal conditions
- **Repetitions & statistics:** runs, warmup, how variance is reported
- **Threats to validity:** what could make this measurement lie?

## Raw data

_Link or path to the raw data files in this folder. Never paste only
averages._

## Results

_Per-metric table: ZEMA vs. each baseline. Include spread, not just
central tendency._

| Metric | ZEMA | Baseline 1 | Baseline 2 | Unit |
|---|---|---|---|---|
| | | | | |

## Conclusion

- [ ] Hypothesis **confirmed** → evidence register #NNN updated
- [ ] Hypothesis **retracted** → evidence register #NNN updated, and
      the claim removed from all documents
- [ ] **Inconclusive** → what experiment comes next, and why

## Reproduction

_Exact commands / steps for a stranger to re-run this experiment and
get comparable numbers._
