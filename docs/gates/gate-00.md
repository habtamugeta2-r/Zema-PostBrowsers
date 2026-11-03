# Gate 0 Review — Phase 0: Historical Foundations & Problem Definition

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase** | 0 — Historical Foundations & Problem Definition |
| **Reviewers** | Prepared by the ZEMA research agent (Arena.ai Agent Mode). **Independent review by the project owner (Better-back) is required and has not yet been performed** — condition C1 |
| **Result** | 🔁 **Pass with recorded conditions** (C1–C5) |
| **Template** | [`../zema-master-prompt/templates/gate-review.md`](../zema-master-prompt/templates/gate-review.md) |

> A gate that cannot say "stop" is not a review. This one says: **do not
> begin Phase 1's build tasks until C1 is signed.** Research tasks for
> Phase 1 may start immediately.

---

## 1. Exit criteria checklist (verbatim from Master Prompt Phase 0)

- [x] **"Problem statement is reviewed and frozen."**
  - Evidence: [`../problem-statement.md`](../problem-statement.md) v1.0, "Frozen at Gate 0", dated 2026-11-02.
  - **Caveat:** *frozen by the author, not yet reviewed independently.* Condition **C1**.
- [x] **"Target app class is defined with concrete examples, starting with the task list app."**
  - Evidence: problem statement §3 — five admission tests and six concrete examples, the task list first.
- [x] **"Non-goals are documented and agreed."**
  - Evidence: problem statement §4 — eight non-goals; also catalog §7 (scheduled give-ups).
  - **Caveat:** "agreed" requires the owner. Condition **C1**.

**Gate verdict against its own wording:** all three criteria have
artifacts; two carry an outstanding human sign-off. Hence "pass with
conditions", not a clean pass.

## 2. Records produced by this phase

| Record | Location |
|---|---|
| Research index, method, source grades | [`../../research/README.md`](../../research/README.md) |
| Lineage: hypertext → accidental app platform | [`../../research/phase-00-01-lineage.md`](../../research/phase-00-01-lineage.md) |
| **Browser-services catalog** (BSC-01…BSC-21) | [`../../research/phase-00-02-browser-services-catalog.md`](../../research/phase-00-02-browser-services-catalog.md) |
| Coordination-cost research (CC-1…CC-12) | [`../../research/phase-00-03-coordination-cost.md`](../../research/phase-00-03-coordination-cost.md) |
| Prior art + headline-claim audit (PA-1…PA-8) | [`../../research/phase-00-04-prior-art.md`](../../research/phase-00-04-prior-art.md) |
| Research-book import audit (negative finding) | [`../../research/phase-00-05-book-import-audit.md`](../../research/phase-00-05-book-import-audit.md) |
| **Problem statement (frozen)** | [`../problem-statement.md`](../problem-statement.md) |
| **Evidence register** (63 rows) | [`../evidence-register.md`](../evidence-register.md) |
| Decision 0001 — source grading | [`../decisions/0001-source-grading.md`](../decisions/0001-source-grading.md) |
| Decision 0002 — target OS = Linux (Ubuntu 24.04 LTS) | [`../decisions/0002-target-os-linux.md`](../decisions/0002-target-os-linux.md) |
| Decision 0003 — browser-service strategy | [`../decisions/0003-browser-service-strategy.md`](../decisions/0003-browser-service-strategy.md) |
| Decision 0004 — missing book / E3 / Decision C | [`../decisions/0004-research-book-missing.md`](../decisions/0004-research-book-missing.md) |
| Tracker and README updates | [`../zema-master-prompt/PHASE-TRACKER.md`](../zema-master-prompt/PHASE-TRACKER.md), [`../../README.md`](../../README.md) |

## 3. Claims audit

**Retracted this phase (2):**

| # | Claim | Reason |
|---|---|---|
| 001 | "ZEMA is the world's first post-browser platform." | Other post-browser application platforms exist and ship (Electron, Tauri, Flutter, React Native, PWAs); "first" is a universal negative this survey cannot establish. Replaced by #048 |
| 062 | "Decision C exists." | No source in this repository or the owner's public repositories names it. Closed as unattested |

**Confirmed or established this phase:** 27 rows (register §B and §E),
including the browser's dual role as distribution/security platform, the
measured weight of the modern stack (2,652 KB median desktop page; 613 KB
JavaScript), the 56% Core Web Vitals pass rate, six billion people
online, and the platform constraints of Android and iOS.

**Still open, with an owner experiment (headline only):**

| # | Claim | Owned by |
|---|---|---|
| 002 | The central "measurably better" hypothesis | E1–E5, Phase 12 |
| 003 | "100× faster" | Phase 12 — restate per metric or retract |
| 006, 007, 008 | Battery, 70/25/5 split, million-item lists | Phase 12 (007/008 also Phase 6) |
| 023 | Electron/Tauri size and memory figures | Phase 12 measurement |
| 045 | Capability broker meets the frame budget | Phase 5 + 12 |
| 047 | Capability model beats browser privacy controls | Phase 12 |
| 057 | No existing system occupies the same intersection | Phase 1 deep review |

**Blocked (3):** #060 (book exists), #061 (E3 exists/its definition),
#063 (70/25/5 definition). All three are consequences of the missing
book; none blocks a gate.

## 4. Stopping-condition check (Master Prompt Phase 14 risks)

| Risk | Does a stopping condition apply **now**? | Reasoning |
|---|---|---|
| Adoption / install friction too high | **Not yet measurable — highest known risk** | Zero-install reach is a deliberate give-up (BSC-02). Phase 11 must measure it; the pre-agreed pivot is browser-hosted Wasm |
| Security-maintenance capacity insufficient | **Unknown — must be answered by Gate 5** | Catalog BSC-03 makes the duty explicit: a runtime needing weekly security refreshes needs a response process. If it does not exist, the project's own rule is **stop** |
| Accessibility gaps remain | **No data yet** | Phase 8 owns it; nothing in Phase 0 substitutes for AT-user testing |
| Performance hypotheses fail | **No data yet** | No ZEMA measurement exists by design; Phase 12 decides |
| Language scope explodes | **Watch during Phase 1** | Syntax frozen at Gate 1; deferred-feature list already recorded |
| Offline data loss observed | N/A | No data layer yet |
| Platform / app-store restrictions apply | **Partially — recorded, not triggered** | Android forbids downloaded executable code except interpreted code; Apple permits only HTML5/JS mini apps and forbids exposing native APIs. These constrain any later mobile or store-distributed plan, and are why the first release targets Linux (decision 0002) |
| An existing solution is better | **Plausible, not established** | PWAs and Tauri already answer part of the problem (PA-5, PA-2). Phase 1's deep prior-art review and Phase 12's comparison are the tests. No stop today |

**No stopping condition is triggered at Gate 0.** Two are escalated:
security-maintenance capacity (Gate 5) and install friction (Gate 11).

## 5. Conditions attached to this pass

| ID | Condition | Owner | Due | Consequence if unmet |
|---|---|---|---|---|
| **C1** | Read and sign the frozen problem statement, target app class, and non-goals; record sign-off in this file | Project owner (Better-back) | Before any Phase 1 **build** task | Phase 1 research may proceed; build is blocked |
| **C2** | Import the research book (Ch. 1–13) **or** authorize retiring the chapter cross-references, per decision 0004 | Project owner | **Before Gate 1** | Phase 1 proceeds on derived specifications; Gate 1 must record the retirement |
| **C3** | Confirm or overrule the target OS (Linux, Ubuntu 24.04 LTS — decision 0002) | Project owner | Before Phase 5 begins | Phases 5/6/8 cannot start |
| **C4** | State a license for the project and its documents (open item inherited from `IMPROVEMENTS.md` §5 item 5) | Project owner | Before any public release or third-party code adoption | Gate 11/14 cannot pass; external contributions are legally ambiguous |
| **C5** | Rule on the relationship to the adjacent `PlainP` project (supersede / donor / eventual home — OQ-1, register #059) | Project owner | Before Phase 1 build begins | Phase 1's starting point is undefined |

**Why these are conditions and not blockers:** every one is an owner
decision or a document supply task, not missing engineering. None of
them invalidates the Phase 0 research, and all five are recorded so they
cannot be discovered late.

## 6. What Gate 0 changed in the project's own words

1. **"World's first" is retracted.** The project will describe itself by
   what it is (#048), not by a superlative it cannot prove.
2. **The browser is no longer a monolith to be replaced.** It is 21
   services, 11 of which ZEMA gives up or delegates, with the cost of each
   written down (catalog).
3. **The evidence bar is now operational:** 63 numbered claims, three
   labels, three source grades, and two retractions already on the books.
4. **The missing book is a recorded gap, not a hidden one.** E3 remains
   blocked and is not invented.
5. **The project now has a first-release OS and a reason for it** —
   reproducibility and unlicensed accessibility tooling, with the market
   cost stated.

## 7. Decision

**Pass with recorded conditions.** Phase 0 produced every deliverable the
Master Prompt names — a frozen problem statement with explicit non-goals,
a full browser-services catalog with rebuild/interoperate/give-up
decisions and their costs, a populated evidence register, and a
reproducible negative finding about the research book. The gate does not
pass *cleanly* because the review has no independent human reviewer yet
(C1) and four owner decisions remain outstanding (C2–C5).

Phase 1 — *The Unified Language: "Plain"* — may begin its **research**
tasks now. Its **build** tasks start when C1 and C5 are signed.

## 8. Sign-off

- [x] `PHASE-TRACKER.md` updated in the same commit as this review
- [x] Evidence register updated in the same commit as this review
- [ ] **Owner sign-off (C1)** — name and date: ______________________
- [ ] **Owner confirmation of target OS (C3)** — name and date: ______________________
- [ ] **Owner license decision (C4)** — license: ______________________

## 8. Dated post-gate note (2026-11-03)

Phase 1 research added evidence relevant to the open conditions, without
changing the Gate 0 result or signing any condition:

- **C5:** a read-only `PlainP` audit now exists
  ([record 04](../../research/phase-01-04-integrated-systems-and-plainp.md)).
  It establishes bounded prototype facts, not a relationship decision.
- **C2:** the research book is still not imported; the derived ambiguity
  register remains a substitute, not the book’s §12.1.
- **C1/C3/C4:** unchanged. No owner sign-off is implied by this note.

Gate 1 remains unattempted. Phase 1 build tasks remain blocked on C1/C5.
