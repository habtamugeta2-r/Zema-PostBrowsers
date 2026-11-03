#!/usr/bin/env python3
"""Read-only Phase 1 document audit and registry generator.

This script does not implement Plain and does not write conformance
fixtures. It recomputes counts, checks specification cross-references and
grammar production closure, validates the source-manifest structure, and
generates a diagnostic-code registry from the normative rules so the
tracker/register cannot drift silently.

Usage:
    python3 tools/audit_phase01.py
    python3 tools/audit_phase01.py --check   # exit 1 on internal inconsistencies
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAIN = ROOT / "docs" / "plain"
RULE_DOC_RELS = [
    "docs/plain/00-lexical-and-layout.md",
    "docs/plain/01-types.md",
    "docs/plain/02-evaluation.md",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def rule_ids(text: str, prefix: str) -> list[str]:
    return sorted(set(re.findall(rf"\*\*({prefix}-\d{{2}})\*\*", text)))


def sugar_ids(text: str) -> list[str]:
    ids = set(re.findall(r"\*\*(S-\d)\*\*", text))
    ids |= set(re.findall(r"\*\*(S-\d)\s", text))
    ids |= set(re.findall(r"\|\s*\*\*(S-\d)\*\*\s*\|", text))
    return sorted(ids)


def table_cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def ambiguity_rows(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*A-\d{2}\s*\|", line):
            continue
        cells = [c.replace("*", "") for c in table_cells(line)]
        if len(cells) < 5:
            continue
        rows.append({"id": cells[0], "status": cells[3], "spec_ref": cells[4]})
    return rows


def fixture_targets(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "Fixture count" in line or "Currently allocated" in line:
            continue
        cells = table_cells(line)
        if len(cells) >= 3 and re.match(r"^\d+", cells[2]):
            rows.append({"area": cells[0], "target": int(re.match(r"^\d+", cells[2]).group(0))})
    return rows


def evidence_rows(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*\d{3}\s*\|", line):
            continue
        cells = table_cells(line)
        if len(cells) >= 7:
            label = cells[2].replace("*", "").split("→")[0].strip()
            status = cells[6].replace("*", "").strip()
            rows.append({"id": cells[0], "label": label, "status": status})
    return rows


def broken_links() -> list[dict]:
    broken = []
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = match.group(1).split("#", 1)[0].strip()
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            dest = (path.parent / target).resolve()
            if not dest.exists():
                broken.append({"file": str(path.relative_to(ROOT)), "target": target})
    return broken


def defined_ids() -> set[str]:
    lexical = read(RULE_DOC_RELS[0])
    types = read(RULE_DOC_RELS[1])
    evaluation = read(RULE_DOC_RELS[2])
    ids = set(rule_ids(lexical, "L")) | set(rule_ids(types, "T")) | set(rule_ids(evaluation, "E"))
    ids |= set(sugar_ids(lexical))
    ids |= {r["id"] for r in ambiguity_rows(read("docs/plain/03-ambiguities.md"))}
    ids |= set(re.findall(r"^### (D-\d{2})", read("docs/plain/04-deferred-features.md"), re.MULTILINE))
    return ids


def cross_reference_check() -> dict:
    defined = defined_ids()
    scan = [ROOT / rel for rel in RULE_DOC_RELS]
    scan += sorted(PLAIN.glob("*.md"))
    scan += sorted((ROOT / "research").glob("phase-01-*.md"))
    scan += sorted((ROOT / "docs" / "decisions").glob("000[5-9]-*.md"))
    missing = defaultdict(set)
    ref_re = re.compile(r"\b([LTE]-\d{2}|S-\d|A-\d{2}|D-\d{2})\b")
    for path in sorted(set(scan)):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for match in ref_re.finditer(text):
            ref = match.group(1)
            if ref not in defined:
                missing[ref].add(str(path.relative_to(ROOT)))
    return {
        "defined_count": len(defined),
        "undefined": {k: sorted(v) for k, v in sorted(missing.items())},
    }


def grammar_check() -> dict:
    lexical = read(RULE_DOC_RELS[0])
    match = re.search(r"```ebnf\n(.*?)```", lexical, re.DOTALL)
    if not match:
        return {"ok": False, "error": "no ebnf block"}
    grammar = match.group(1)
    productions = set(re.findall(r"^([a-z_]+)\s*=", grammar, re.MULTILINE))
    rhs_names = []
    for line in grammar.splitlines():
        if "=" not in line:
            continue
        rhs = line.split("=", 1)[1]
        rhs = re.sub(r'"[^"]*"', "", rhs)
        rhs = re.sub(r"\(\*.*?\*\)", "", rhs)
        rhs_names += re.findall(r"\b([a-z_]+)\b", rhs)
    terminals = {"EOF", "NEWLINE", "INDENT", "DEDENT"}
    undefined = sorted(set(rhs_names) - productions - terminals)
    return {"ok": not undefined, "production_count": len(productions), "undefined_nonterminals": undefined}


def source_manifest_check() -> dict:
    path = ROOT / "research" / "data" / "phase-01-source-manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "count": 0, "duplicate_ids": [], "invalid_entries": [str(exc)]}
    sources = data.get("sources", [])
    ids = [s.get("id") for s in sources]
    duplicates = sorted(k for k, count in Counter(ids).items() if count != 1)
    invalid = []
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            invalid.append(f"source[{i}] is not an object")
            continue
        for field in ("id", "kind", "url", "retrieved"):
            if not source.get(field):
                invalid.append(f"source[{i}] missing {field}")
        if not re.match(r"^https://", str(source.get("url", ""))):
            invalid.append(f"source[{i}] URL is not HTTPS")
        digest = source.get("sha256")
        if digest is not None and not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            invalid.append(f"source[{i}] has invalid sha256")
    unicode17_files = [
        s for s in sources
        if s.get("repo") == "unicode-org/unicodetools"
        and s.get("version") == "Unicode 17.0.0"
        and s.get("git_blob_sha")
    ]
    return {"ok": not duplicates and not invalid, "count": len(sources), "unicode17_data_files": len(unicode17_files), "duplicate_ids": duplicates, "invalid_entries": invalid}


def diagnostic_registry() -> list[dict]:
    """Extract diagnostic codes from normative rule text.

    This is an index, not a message catalog. A future compiler must still
    define exact messages/spans/fixes and prove fixture coverage.
    """
    codes = defaultdict(lambda: {"rules": set(), "documents": set(), "historical": False})
    rule_re = re.compile(r"\*\*([LTE]-\d{2}|S-\d)(?:\s|\*)")
    for rel in RULE_DOC_RELS:
        text = read(rel)
        current = None
        for line in text.splitlines():
            m = rule_re.search(line)
            if m:
                current = m.group(1)
            if line.startswith("#"):
                current = None
            for code in re.findall(r"PL\d{4}", line):
                entry = codes[code]
                if current:
                    entry["rules"].add(current)
                entry["documents"].add(rel)
                if "retired" in line.lower() and code in line:
                    entry["historical"] = True
    registry = []
    for code, entry in sorted(codes.items()):
        registry.append({
            "code": code,
            "severity": "warning" if code.startswith("PL1") else "error",
            "historical": entry["historical"],
            "rules": sorted(entry["rules"]),
            "documents": sorted(entry["documents"]),
        })
    return registry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    lexical = read(RULE_DOC_RELS[0])
    types = read(RULE_DOC_RELS[1])
    evaluation = read(RULE_DOC_RELS[2])
    ambiguities = read("docs/plain/03-ambiguities.md")
    deferrals = read("docs/plain/04-deferred-features.md")
    conformance = read("docs/plain/05-conformance-plan.md")
    evidence = read("docs/evidence-register.md")

    rules = {
        "L": rule_ids(lexical, "L"),
        "T": rule_ids(types, "T"),
        "E": rule_ids(evaluation, "E"),
        "S": sugar_ids(lexical),
    }
    amb = ambiguity_rows(ambiguities)
    amb_status = Counter()
    for row in amb:
        st = row["status"].lower().replace("*", "")
        if st.startswith("resolved"):
            amb_status["resolved"] += 1
        elif st.startswith("deferred"):
            amb_status["deferred"] += 1
        elif st.startswith("open"):
            amb_status["open"] += 1
        else:
            amb_status["unknown"] += 1
    fixtures = fixture_targets(conformance)
    ev = evidence_rows(evidence)
    labels = Counter(r["label"] for r in ev)
    deferral_ids = sorted(set(re.findall(r"^### (D-\d{2})", deferrals, re.MULTILINE)))
    registry = diagnostic_registry()
    xref = cross_reference_check()
    grammar = grammar_check()
    manifest = source_manifest_check()

    report = {
        "date": "2026-11-03",
        "scope": "Read-only document audit; no Plain implementation or fixtures",
        "rules": {k: {"count": len(v), "ids": v} for k, v in rules.items()},
        "normative_rule_count_L_T_E": sum(len(rules[k]) for k in ("L", "T", "E")),
        "ambiguities": {"count": len(amb), "status": {k: amb_status.get(k, 0) for k in ("resolved", "deferred", "open", "unknown")}, "rows": amb},
        "deferrals": {"count": len(deferral_ids), "ids": deferral_ids},
        "conformance_fixture_targets": {"rows": fixtures, "sum": sum(r["target"] for r in fixtures)},
        "evidence": {"count": len(ev), "labels": dict(labels), "retracted": [r["id"] for r in ev if r["status"].lower().startswith("retracted")]},
        "diagnostic_registry": registry,
        "cross_reference_check": xref,
        "grammar_check": grammar,
        "source_manifest_check": manifest,
        "broken_relative_links": broken_links(),
    }
    out = ROOT / "research" / "data" / "phase-01-document-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    problems = []
    if report["normative_rule_count_L_T_E"] != 100:
        problems.append(f"expected 100 L/T/E rules, found {report['normative_rule_count_L_T_E']}")
    if len(amb) != 47 or amb_status.get("resolved") != 42 or amb_status.get("deferred") != 5 or amb_status.get("open", 0) != 0:
        problems.append(f"expected 47 ambiguities (42 resolved, 5 deferred, 0 open), found {len(amb)} / {amb_status}")
    if len(deferral_ids) != 20:
        problems.append(f"expected 20 deferrals, found {len(deferral_ids)}")
    if report["conformance_fixture_targets"]["sum"] != 307:
        problems.append("fixture target sum is not 307")
    if len(ev) != 100 or labels.get("E") != 49 or labels.get("P") != 22 or labels.get("H") != 29:
        problems.append(f"evidence counts drift: {len(ev)} rows, labels={dict(labels)}")
    if report["broken_relative_links"]:
        problems.append(f"broken links: {report['broken_relative_links']}")
    if xref["undefined"]:
        problems.append(f"undefined specification references: {xref['undefined']}")
    if not grammar["ok"]:
        problems.append(f"grammar closure failure: {grammar}")
    if not manifest["ok"] or manifest["count"] != 58 or manifest["unicode17_data_files"] != 16:
        problems.append(f"source manifest check failed or entry counts drifted: {manifest}")
    if any(not entry["rules"] and not entry["historical"] for entry in registry):
        problems.append("diagnostic code without an owning rule")
    report["check"] = {"ok": not problems, "problems": problems}
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "check": report["check"],
        "normative_rule_count_L_T_E": report["normative_rule_count_L_T_E"],
        "ambiguities": report["ambiguities"]["status"],
        "deferrals": report["deferrals"]["count"],
        "evidence": report["evidence"]["labels"],
        "diagnostic_codes": len(registry),
        "cross_reference_check": xref,
        "grammar_check": grammar,
        "source_manifest_check": manifest,
    }, indent=2, ensure_ascii=False))
    return 1 if args.check and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
