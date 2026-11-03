# AUTONOMOUS LOOP — how to run this project without writing prompts

| Field | Detail |
|---|---|
| **Document** | The loop contract: how an agent continues this project incrementally without a new prompt each time |
| **Version** | 1.0.0 |
| **Date** | 2026-11-04 |
| **Status** | Active |
| **Supersedes** | Nothing. It is subordinate to the [Master Prompt](./ZEMA-Master-Research-and-Build-Prompt.md), [Gate 0 conditions](../gates/gate-00.md), and every decision record |
| **Location** | `docs/zema-master-prompt/AUTONOMOUS-LOOP.md` |

> **The problem this solves.** Every increment so far needed a human to write
> a prompt: "continue", "research deeper", "merge it". The work is
> well-structured enough that the prompt can be *stored* instead of
> *written*. This document is that stored prompt. The owner's entire input
> becomes one word: **`continue`**.

---

## 1. The one-word contract

When the owner says **`continue`**, the agent runs exactly one *iteration*
(§3) and stops. It does not ask what to do next, because §4 says what is
next. It does not do three increments in one turn, because an increment
that cannot be reviewed is not an increment.

| Owner says | Agent does |
|---|---|
| `continue` | Run §3 for the next eligible item in [`BACKLOG.md`](./BACKLOG.md). One item. Then report. |
| `continue N` | Run up to N items, still stopping early on any **STOP** condition (§5) |
| `status` | Print the backlog table and what is blocked, without changing anything |
| anything else | Treat as a normal instruction and do not consult this loop |

If the owner says nothing at all, nothing happens. The loop is never
self-starting; `continue` is the only ignition.

## 2. Where the prompts live

| Artifact | Role |
|---|---|
| [`BACKLOG.md`](./BACKLOG.md) | **The queue.** Ordered, sized, each item with its own acceptance test. This is the prompt for the *next* time |
| This document | The **procedure** every item follows, and the invariants that must survive it |
| [`PHASE-01-EXECUTION-PROMPT.md`](./PHASE-01-EXECUTION-PROMPT.md) | The **authoritative work order** for Phase 1 build tasks. The backlog never overrides it |
| [`PHASE-TRACKER.md`](./PHASE-TRACKER.md) | The **record** of what was actually done |

The backlog is *derived from* the execution prompt, never a substitute for it.
If the two disagree, the execution prompt wins and the backlog row is wrong.

## 3. One iteration, in order

Every `continue` runs these steps. Steps marked **[gate]** are checks that can
abort the iteration.

1. **[gate] Preflight.** Run `python3 tools/audit_phase01.py --check` and
   `python3 -m unittest discover -s tests`. If either is red, the iteration's
   job is to turn it green — nothing else. A project with a red check does not
   take on new work.
2. **Select.** Read `BACKLOG.md`. Take the first row whose `Status` is `ready`
   and whose `Blocked by` column is empty or satisfied. If every row is
   blocked, the iteration produces a *blocked report* and stops (§5).
3. **[gate] Authorize.** If the item touches something an owner must authorize
   (see §6), do not do it. Mark it `blocked: owner` and take the next item.
4. **Do the work** for that one item, to its own `Done when` column.
5. **Prove it.** Every check added must be **mutation-tested**: deliberately
   break the thing and observe the check fail. A check that cannot fail is
   decoration and is itself a defect.
6. **Record.** Evidence rows if a claim was made; a dated tracker row; a
   version bump for any controlled document; an `IMPROVEMENTS.md` entry if a
   process rule changed. Then update the backlog row's `Status`.
7. **Commit and push** to the Arena branch with a message that states the
   finding, not the activity. Open or update the PR only when the owner asks.
8. **Report** in the reply: what moved, what was measured, what surprised the
   agent, what is now blocked. Never report an activity list without a result.

## 4. Selection rules

- **One item per `continue`.** If an item turns out to be larger than one
  iteration, the agent splits it *in the backlog* and does the smaller first
  piece. It does not silently overrun.
- **Smallest useful increment first**, not the most interesting one.
- **Never two items that touch the same file in one iteration** if either is
  a controlled document, because the review becomes ambiguous.
- **Measure before repairing.** If an item says "fix X", the iteration first
  records the measurement that proves X is broken. A repair with no
  before-number cannot be shown to have worked.

## 5. STOP conditions

The agent stops immediately and reports — regardless of what the backlog says
— when any of these is true:

| # | Condition | Why |
|---|---|---|
| S-1 | A check is red and the fix is not obvious | Guessing at a red check is how the last eight defects started |
| S-2 | The work needs an **owner decision** (§6) | Silence is not approval. This is the established project rule |
| S-3 | The work would make a claim the evidence does not support | Evidence discipline, Concern 16 |
| S-4 | The next backlog row is blocked and no row is ready | That is a genuine queue exhaustion, not a reason to invent work |
| S-5 | A repair would require deleting a concern, phase, exit criterion, or evidence row | Never. Record a dated correction instead |
| S-6 | Two documents would both need editing to stay consistent, and the iteration can only do one | Prevents the split-brain that PR-02 exists to stop |

## 6. What the agent may never decide alone

These are the owner's. The agent may *prepare* them and must ask:

1. Ratifying or rejecting any **proposal** — including the 20 diagnostic
   identifiers in [`08-diagnostics-and-faults.md`](../plain/08-diagnostics-and-faults.md) §9
   and the three gate-review fields in [`VERTICAL-TRACE.md`](./VERTICAL-TRACE.md) §4.
2. Importing or retiring the **research book** (decision 0004, condition C2).
3. The **license** (condition C4).
4. Making an **evidence register label** retrospective — the labels on
   existing rows stay as recorded.
5. Declaring a **gate passed**.
6. Changing the **19 concerns**, the phase list, or any gate exit criterion.
7. Choosing a term where two exist (`Prompt Gate` vs `Phase Gate`) — that is
   a vocabulary decision, and it is asked once in the backlog, not guessed.

## 7. Invariants that must survive every iteration

Carried from [`IMPROVEMENTS.md`](./IMPROVEMENTS.md), restated because they are
the acceptance test for the *loop itself*:

| # | Invariant |
|---|---|
| PR-01 | No count is typed into prose; it is printed by `--verify` |
| PR-02 | One authoritative location per fact; others link |
| PR-03 | No check is trusted until a mutation makes it fail |
| PR-04 | Every identifier has exactly one owning rule |
| PR-05 | Deleting an artifact means deleting every reference to it in the same commit |
| PR-06 | Decision status is two fields: `Status` and `Owner ratification` |
| PR-07 | A rule that refuses a construct names its code, or is listed as needing none |
| PR-08 | A fault is never in a recoverable diagnostic's namespace |
| PR-09 | Every iteration ends with a green audit, green tests, and a clean tree |
| PR-10 | The agent's own errors are recorded in the audit record, not quietly fixed |

## 8. Anti-patterns this loop is designed to prevent

Each of these has actually happened in this repository:

| Anti-pattern | What it looks like | The rule that stops it |
|---|---|---|
| Prompt inflation | Each turn adds prose to a document instead of doing one thing | One item, with a `Done when` test |
| Measuring by reading | "I checked the docs" with no command run | §3 step 1 and step 5 |
| The optimistic count | A number typed from memory | PR-01 |
| Decoration checks | A check that passes against a known defect | PR-03 |
| Silent scope creep | An item grows mid-iteration | §4, split in the backlog |
| Repairing the map, not the territory | Editing the audit *record* so it reads well | §3 step 5; S-3 |
| Asking the owner what to do | Endless clarification instead of work | §4 selection is deterministic |

## 9. How to change this loop

The loop is itself a controlled artifact:

1. Propose the change in the iteration report.
2. If the owner agrees, bump this document's version and add a change-log row.
3. Add or amend a `PR-nn` invariant in `IMPROVEMENTS.md` if the change is
   a process rule.

The backlog may be reordered by the agent at any time. **The invariants in §7
may not be weakened by the agent.** That asymmetry is deliberate: it lets the
agent choose *what* to do next while preventing it from choosing *how careful*
to be.

## 10. Change log

| Date | Version | Change |
|---|---|---|
| 2026-11-04 | 1.0.0 | Created. Defines the one-word contract, the eight-step iteration, deterministic selection, six stop conditions, seven owner-only decisions, and ten invariants. Adds PR-09 and PR-10. |
