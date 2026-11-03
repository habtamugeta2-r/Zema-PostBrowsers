#!/usr/bin/env python3
"""The autonomous-loop driver.

The owner should never have to write a prompt or guess a command. This
tool reads the queue, verifies the project is healthy, and prints the
single next thing to do -- with the acceptance test that decides whether
it is finished.

    python3 tools/loop.py            # what to do next
    python3 tools/loop.py --status   # the whole queue
    python3 tools/loop.py --check    # health gate only
    python3 tools/loop.py --done B1  # mark an item finished

Deliberately small: it reads the backlog that humans and agents both edit,
and it refuses to pick anything while a check is red. It does not call a
model and does not edit source -- the agent does the work, this decides
what the work is.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "docs" / "zema-master-prompt" / "BACKLOG.md"

READY = "ready"
DONE = "done"


def backlog_rows() -> list[dict]:
    """Parse the backlog's tables into rows.

    A row is a work item only if its first cell matches an item ID such as
    `B1`. Everything else in the table (headers, the selection-trace
    rationale) is skipped, so prose cannot be mistaken for a task.
    """
    if not BACKLOG.exists():
        return []
    rows: list[dict] = []
    section = ""
    for line in BACKLOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"[A-Z]\d{1,2}", cells[0]):
            continue
        rows.append(
            {
                "id": cells[0],
                "item": cells[1],
                "done_when": cells[2],
                "blocked_by": cells[3],
                "status": cells[4].replace("*", "").replace("`", "").strip(),
                "section": section,
            }
        )
    return rows


def gate() -> dict:
    """The health gate. Nothing new starts while this is red."""
    checks: list[dict] = []

    audit = subprocess.run(
        [sys.executable, "tools/audit_phase01.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    try:
        report = json.loads(audit.stdout)
        problems = report["check"]["problems"]
        ok = report["check"]["ok"]
    except (json.JSONDecodeError, KeyError):
        ok, problems = False, ["audit tool did not emit parseable JSON"]
    checks.append({"name": "audit_phase01 --check", "ok": ok, "detail": problems})

    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    checks.append(
        {
            "name": "unittest discover -s tests",
            "ok": tests.returncode == 0,
            "detail": (tests.stderr or "").strip().splitlines()[-1:] or ["no output"],
        }
    )

    tree = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True
    )
    dirty = [l for l in tree.stdout.splitlines() if l.strip()]
    checks.append(
        {
            "name": "working tree clean",
            "ok": not dirty,
            "detail": dirty[:5],
        }
    )

    return {"ok": all(c["ok"] for c in checks), "checks": checks}


def next_item(rows: list[dict]) -> dict | None:
    """First ready row whose blockers are satisfied.

    A blocker is satisfied when it names no item, or when every item ID it
    names is `done`. This is the whole selection algorithm -- deterministic,
    so the agent never has to ask which item is next.
    """
    by_id = {r["id"]: r for r in rows}
    for row in rows:
        if row["status"] != READY:
            continue
        deps = re.findall(r"\b([A-Z]\d{1,2})\b", row["blocked_by"])
        if deps and any(by_id.get(d, {}).get("status") != DONE for d in deps):
            continue
        return row
    return None


def cmd_next() -> int:
    health = gate()
    rows = backlog_rows()

    if not rows:
        print("BACKLOG.md is missing or has no rows. Nothing to select.")
        return 1

    if not health["ok"]:
        print("STOP (loop stop condition S-1): a check is red.\n")
        for check in health["checks"]:
            mark = "PASS" if check["ok"] else "FAIL"
            print(f"  [{mark}] {check['name']}")
            if not check["ok"]:
                for line in check["detail"]:
                    print(f"         {line}")
        print("\nThis iteration's job is to turn the check green. Nothing else.")
        return 0

    item = next_item(rows)
    if item is None:
        counts = {}
        for row in rows:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        print("STOP (loop stop condition S-4): no ready item.\n")
        print(f"  queue: {counts}")
        blocked = [r for r in rows if r["status"].startswith("blocked")]
        if blocked:
            print("\n  Waiting on the owner or a dependency:")
            for row in blocked[:10]:
                print(f"    {row['id']:<3} {row['item'][:64]:<64} [{row['blocked_by']}]")
        print("\nNothing here is inventable. Report the blockage.")
        return 0

    print(f"NEXT: {item['id']} — {item['item']}\n")
    print(f"  section   {item['section']}")
    print(f"  done when {item['done_when']}")
    print(f"  blocked   {item['blocked_by'] or 'nothing'}")
    print(f"  status    {item['status']}")
    print(
        "\nProcedure: see docs/zema-master-prompt/AUTONOMOUS-LOOP.md §3.\n"
        "Do this one item, mutation-test any check it adds, record it, commit, report."
    )
    return 0


def cmd_status() -> int:
    rows = backlog_rows()
    health = gate()
    print(f"health: {'GREEN' if health['ok'] else 'RED'}\n")
    if not health["ok"]:
        for check in health["checks"]:
            if not check["ok"]:
                print(f"  FAIL {check['name']}")
                for line in check["detail"]:
                    print(f"       {line}")
        print()

    width = max((len(r["item"]) for r in rows), default=10)
    print(f"  {'id':<4} {'status':<14} {'blocked by':<12} item")
    for row in rows:
        print(
            f"  {row['id']:<4} {row['status']:<14} "
            f"{(row['blocked_by'] or '-'):<12} {row['item'][:width + 40]}"
        )

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(f"\n  {counts}")
    return 0


def cmd_done(item_id: str) -> int:
    """Mark an item done, but only if its work is actually verifiable."""
    rows = backlog_rows()
    target = next((r for r in rows if r["id"] == item_id), None)
    if target is None:
        print(f"no item {item_id} in BACKLOG.md")
        return 1
    if target["status"] == DONE:
        print(f"{item_id} is already done")
        return 0

    health = gate()
    if not health["ok"]:
        print("refusing to mark done: a check is red. PR-09 says every")
        print("iteration ends green.")
        for check in health["checks"]:
            if not check["ok"]:
                print(f"  FAIL {check['name']}")
        return 1

    lines = BACKLOG.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.startswith("|") or not cells or cells[0] != item_id:
            continue
        cells[-1] = f"**{DONE}**"
        lines[index] = "| " + " | ".join(cells) + " |"
        BACKLOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{item_id} marked done.")
        return 0
    print(f"could not rewrite the row for {item_id}")
    return 1
    print(f"{item_id} marked done.")
    return 0


def cmd_check() -> int:
    health = gate()
    for check in health["checks"]:
        mark = "PASS" if check["ok"] else "FAIL"
        print(f"[{mark}] {check['name']}")
        if not check["ok"]:
            for line in check["detail"]:
                print(f"       {line}")
    return 0 if health["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Drive the incremental loop.")
    parser.add_argument("--status", action="store_true", help="print the whole queue")
    parser.add_argument("--check", action="store_true", help="health gate only")
    parser.add_argument("--done", metavar="ID", help="mark an item finished")
    args = parser.parse_args()

    if args.check:
        return cmd_check()
    if args.status:
        return cmd_status()
    if args.done:
        return cmd_done(args.done)
    return cmd_next()


if __name__ == "__main__":
    raise SystemExit(main())
