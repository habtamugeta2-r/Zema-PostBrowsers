# Decision Record 0002 — The first-release desktop OS is Linux (Ubuntu 24.04 LTS)

| Field | Detail |
|---|---|
| **Date** | 2026-11-02 |
| **Phase / gate** | Phase 0 / Gate 0 (recorded now because the choice constrains Phases 5, 6, 8, 11) |
| **Status** | **Proposed** — requires owner confirmation (Gate 0 condition C3, which is still open; C1 was the unrelated sign-off condition and was resolved 2026-11-03) |
| **Owner ratification** | **pending — Gate 0 condition C3** — the target OS is unconfirmed |
| **Evidence label** | **Proposed** |
| **Deciders** | ZEMA research agent (Arena.ai Agent Mode); project owner (Better-back) to confirm |

## Context

Master Prompt v1.1 says *"One desktop OS: pick one; ship one"* (Phase 14)
but never names it; `IMPROVEMENTS.md` §5 records that the choice affects
Phases 5, 6, and 8 and should be made at Gate 0. It cannot be deferred,
because three later decisions are already downstream of it:

1. **Which accessibility API** ZEMA bridges to (Phase 8, the release gate).
2. **Which OS sandbox primitives** the capability host composes (Phase 5).
3. **Which signing/distribution path** the release uses (Phase 11).

Leaving it open until Phase 14 would mean writing the accessibility
bridge, the sandbox policy, and the updater against three targets and
shipping none well — the exact scope failure Core Concerns Concern 19
forbids.

## Options considered

### Option A — Reuse: Linux desktop (Ubuntu 24.04 LTS) as the first-release OS

- What it is: a mainstream GNU/Linux desktop with a stable LTS kernel.
- **Accessibility:** the platform's AT stack (AT-SPI) is open, inspectable,
  and drivable in automation; screen readers such as Orca are open source
  and scriptable in CI [S1]. WCAG 2.2 exists as the reference [S2].
  *This matters most:* Gate 8 needs reproducibility, and closed AT
  programs are hard to license, automate, or even install in CI.
- **Sandboxing:** seccomp-bpf and **Landlock** are in the mainline kernel
  and usable by unprivileged processes [S3]; both are documented, which
  a security review can cite.
- **OS integration:** desktop services arrive through **XDG Desktop
  Portals** (file chooser, print, notifications, OpenURI, proxy
  resolver), which grant access per user action rather than ambiently
  [S6] — a natural match for a capability model.
- **Distribution:** no store gatekeeper, no notarization service, no
  annual developer program; a signed tarball/`.deb`/Flatpak is publishable
  by one person — and the signing toolchain can be added later.
- **CI:** free hosted Linux runners make every gate's evidence
  reproducible by a stranger.
- Security cost: no platform-supplied notarization; the project owns more
  of the trust chain (mitigated by TUF-style design, Phase 11 [S4]).
- Performance cost: GPL/compositor variance and GPU driver quality vary;
  *must be measured*, not assumed — Phase 6 covers it.
- Fit for ZEMA's defined app class: good for developer and internal tools
  (the most plausible early adopters), weak for mass-market consumers.

### Option B — Build on existing foundations: Windows

- Accessibility: **UI Automation** is the documented framework [S5];
  NVDA is open source.
- Sandboxing: AppContainer/job objects exist but are less directly
  documented for this use than Landlock/seccomp.
- Distribution: Authenticode signing plus an installer is workable, but
  the trust chain is certificate-purchase-dependent and SmartScreen
  reputation starts at zero.
- Fit: the largest desktop user base and the best adoption story.
- Why not first: AT automation and CI are heavier to reproduce, and
  certificate/notarization friction arrives before the first gate.

### Option C — Invent: macOS first

- Accessibility: NSAccessibility is capable.
- Distribution: notarization and a paid developer program are hard
  prerequisites (Phase 11 friction, before any evidence exists).
- Hardware: every CI run needs Apple hardware; reproducibility cost is
  highest of the three.
- Fit: worst cost-to-evidence ratio for a first release.

### Option D — Defer the choice to Phase 14

- Explicitly rejected: it maximizes the cost of every earlier phase and
  breaks the "one OS" scope rule in spirit while keeping it in letter.

## Decision

**Choose Option A: Linux (Ubuntu 24.04 LTS) for the first release**, with
Windows recorded as the **first** candidate for a second release and the
most likely pivot target if adoption evidence at Gate 11 is unfavourable.

The decision is deliberately about *where the evidence can be produced
cheaply and honestly*, not about where the market is. The market argument
is real, and it is exactly why this decision carries a revisit trigger
rather than an assumption.

## Consequences

- **Positive:** Gate 8 testing is reproducible and mostly unlicensed;
  Phase 5's sandbox can cite documented kernel mechanisms; Phase 11 can
  ship a signed package without a gatekeeper; CI evidence is free and
  public.
- **Negative / accepted costs:** smallest consumer reach of the three;
  distro variance (compositor, font stacks, GPU drivers) is now a
  first-class test matrix; "works on my Ubuntu" is not a portability
  claim.
- **New obligations created:**
  - Phase 5 must evaluate **seccomp-bpf + Landlock** together and record
    which kernel versions are supported [S3].
  - Phase 6 must record the **compositor/GPU/CPU-fallback matrix** on
    Ubuntu LTS, including a software-rendering path.
  - Phase 7 must test **fonts and IME on Linux**, including Ethiopic,
    Arabic, Hebrew, Indic, and CJK fallback.
  - Phase 8 must name the **screen reader(s)** and AT versions actually
    used, and include AT users as testers.
  - Phase 11 must document the **signing trust bootstrap** and what a
    user is actually trusting when they install.
  - Phase 5/6 must route file, print, notification, and open-URI access
    through **portals** and record the per-desktop-environment behaviour
    matrix (GNOME, KDE, wlroots) — portal availability is itself a
    Linux-specific risk.
- **What would make us revisit this decision (revisit triggers):**
  1. Gate 8 cannot source AT-SPI tooling reliable enough for reproducible testing.
  2. Gate 11 measures install/adoption friction so high on Linux that the
     only viable path is Windows or browser-hosted Wasm.
  3. Phase 6 finds the Linux GPU/driver matrix makes per-metric
     comparison meaningless.
  Any of these produces a **new dated decision record**; this one is not
  edited.

## Evidence

- Citations:
  - [S1] GNOME accessibility documentation (AT-SPI/ATK model; role, state, relations on accessible objects) — <https://wiki.gnome.org/Accessibility(2f)Documentation(2f)GNOME2(2f)AtkGuide.html> — grade B.
  - [S2] W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, Recommendation 5 October 2023 — <https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/> — grade A.
  - [S3] Linux kernel documentation, *Landlock LSM* and *Landlock: unprivileged access control* (stackable LSM; unprivileged sandboxing; seccomp-bpf distinction) — <https://docs.kernel.org/security/landlock.html>, <https://docs.kernel.org/userspace-api/landlock.html> — grade A.
  - [S4] The Update Framework, *Security* (rollback, freeze, mix-and-match, key-compromise defenses) — <https://theupdateframework.io/docs/security/> — grade A.
  - [S5] Microsoft Learn, *UI Automation Overview* — <https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-uiautomationoverview> — grade A.
  - [S6] XDG Desktop Portal (portal-mediated file chooser, print, notification, OpenURI; per-file document portal grants) — <https://github.com/flatpak/xdg-desktop-portal> — grade A.
- Experiments: none yet. Phase 6 and Phase 12 supply the measurements that would test the "performance cost" of this choice.
- Related records: [`0003-browser-service-strategy.md`](./0003-browser-service-strategy.md) (BSC-09/BSC-15/BSC-16 depend on this), [`../gates/gate-00.md`](../gates/gate-00.md) condition C3.
