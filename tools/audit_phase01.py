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


def evidence_summary(text: str) -> dict:
    """Read the declared counts so any legitimate evidence-register growth can be checked."""
    total = re.search(r"^\|\s*Total rows\s*\|\s*(\d+)", text, re.MULTILINE)
    counts = {}
    for label, name in (("E", "Established"), ("P", "Proposed"), ("H", "Hypothesis")):
        match = re.search(rf"^\|\s*{re.escape(name)}\s*\({label}\)\s*\|\s*(\d+)\s*\|", text, re.MULTILINE)
        if match:
            counts[label] = int(match.group(1))
    return {"total": int(total.group(1)) if total else None, "labels": counts}


def traceability_matrix() -> dict:
    """Check docs/plain/07-traceability.md covers every normative rule.

    This closes the gap where an area-level fixture budget could be met while
    individual rules went unowned. Allocation is not coverage: this check only
    proves that every rule has a named verification method and area.
    """
    path = PLAIN / "07-traceability.md"
    if not path.exists():
        return {"ok": False, "covered": 0, "missing": ["07-traceability.md not found"], "unknown": [], "methods": {}}
    text = path.read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = table_cells(line)
        if len(cells) < 3:
            continue
        ref = cells[0].replace("*", "").strip()
        if not re.fullmatch(r"(?:[LTE]-\d{2}|S-\d)", ref):
            continue
        rows.append({"rule": ref, "method": cells[1].replace("*", "").strip(), "area": cells[2].strip()})
    covered = {row["rule"] for row in rows}
    defined = set()
    defined |= set(rule_ids(read(RULE_DOC_RELS[0]), "L"))
    defined |= set(rule_ids(read(RULE_DOC_RELS[1]), "T"))
    defined |= set(rule_ids(read(RULE_DOC_RELS[2]), "E"))
    defined |= set(sugar_ids(read(RULE_DOC_RELS[0])))
    missing = sorted(defined - covered)
    unknown = sorted(covered - defined)
    methods = Counter()
    for row in rows:
        for token in re.split(r"[+,]", row["method"]):
            token = token.strip()
            if token:
                methods[token] += 1
    return {
        "ok": not missing and not unknown,
        "rows": len(rows),
        "covered": len(covered & defined),
        "defined": len(defined),
        "missing": missing,
        "unknown": unknown,
        "methods": dict(sorted(methods.items())),
    }


def conformance_area_coverage() -> dict:
    """Check every normative rule is attributed to a conformance-plan area.

    The plan's area table names rule ranges per area. Before this check, 14
    rules fell between the named ranges and had no area at all.
    """
    plan = read("docs/plain/05-conformance-plan.md")
    areas = []
    covered: set[str] = set()
    for line in plan.splitlines():
        cells = table_cells(line)
        if len(cells) < 3 or not re.match(r"^\d+", cells[2] or ""):
            continue
        col = cells[1]
        areas.append(cells[0])
        for match in re.finditer(r"([LTE])-(\d{2})\s*…\s*(?:([LTE])-)?(\d{2})", col):
            prefix, low, high = match.group(1), int(match.group(2)), int(match.group(4))
            covered.update(f"{prefix}-{i:02d}" for i in range(low, high + 1))
        for match in re.finditer(r"S-(\d)\s*…\s*(?:S-)?(\d)", col):
            covered.update(f"S-{i}" for i in range(int(match.group(1)), int(match.group(2)) + 1))
        for match in re.finditer(r"(?<![\w-])([LTE]S?-\d{2}|S-\d)(?![\d…])", col):
            token = match.group(1)
            covered.add(token)
    defined = set()
    for rel, prefix in zip(RULE_DOC_RELS, ("L", "T", "E")):
        defined |= set(rule_ids(read(rel), prefix))
    defined |= set(sugar_ids(read(RULE_DOC_RELS[0])))
    # Section 4 of the traceability matrix owns the rules this suite cannot
    # verify. That table is the single source; the plan links to it.
    trace = read("docs/plain/07-traceability.md").split("## 4.", 1)
    if len(trace) == 2:
        for match in re.finditer(r"^\|\s*(E-\d{2}|L-\d{2}|T-\d{2}|S-\d)\b", trace[1].split("## 5.", 1)[0], re.MULTILINE):
            covered.add(match.group(1))
    unattributed = sorted(defined - covered)
    return {
        "ok": not unattributed,
        "areas": len(areas),
        "attributed": len(covered & defined),
        "defined": len(defined),
        "unattributed": unattributed,
    }


def duplicate_artifact_check() -> dict:
    """Report committed result files duplicated under research/data and experiments.

    The same measurement must live in one place. Two copies that differ only by
    a timestamp is how a reader ends up quoting the wrong number.
    """
    canonical = ROOT / "research" / "data" / "phase-01-normalization-report.json"
    experiment = ROOT / "research" / "experiments" / "EN-unicode17-normalization" / "normalization-report.json"
    duplicates = []
    if canonical.exists() and experiment.exists():
        duplicates.append(
            {
                "canonical": str(canonical.relative_to(ROOT)),
                "experiment": str(experiment.relative_to(ROOT)),
                "reason": "normalization result stored twice; the experiment record owns it",
            }
        )
    return {"ok": not duplicates, "duplicates": duplicates}


def duplicated_fact_check() -> dict:
    """Detect two documents tabulating the same rule set.

    A fact must have one owning table (process rule PR-04). The failure mode is
    not a byte-identical copy -- it is a *partial* copy that then drifts: one
    table gains a row, the other keeps the old list. This defect occurred three
    times in this repository (conformance areas, the Gate 1 exclusion list, and
    the decision-status table). Identical-set detection misses it, so overlap is
    measured instead.

    Threshold: two files clash when they share at least 3 rule rows and those
    rows are at least 60% of the smaller table.
    """
    rule_re = re.compile(r"^\|\s*`?([LTE]-\d{2}|S-\d)\b")
    per_file: dict[str, set[str]] = {}
    for path in sorted(PLAIN.glob("*.md")):
        rows = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            match = rule_re.match(line)
            if match:
                rows.add(match.group(1))
        if len(rows) >= 3:
            per_file[str(path.relative_to(ROOT))] = rows

    clashes = []
    names = sorted(per_file)
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            shared = per_file[left] & per_file[right]
            smaller = min(len(per_file[left]), len(per_file[right]))
            if len(shared) >= 3 and len(shared) >= 0.6 * smaller:
                clashes.append(
                    {
                        "files": [left, right],
                        "shared_rules": sorted(shared),
                        "shared_count": len(shared),
                        "smaller_table": smaller,
                        "owner": left,
                        "duplicate": right,
                    }
                )
    return {"ok": not clashes, "clashes": clashes}


def measured_facts() -> dict:
    """Quantities that prose is allowed to quote (process rule PR-01).

    Prose may restate these; it may not originate them. Run with --verify to
    print them, then compare against the documents. This is deliberately a
    small, explicit list rather than a general number scraper: a scraper
    produces false positives, and a check nobody trusts gets switched off.
    """
    def prose_words(rel: str) -> int:
        text = read(rel)
        body = text.split("---", 1)[1] if "---" in text else text
        words = []
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("|", "#", "```", ">")):
                continue
            stripped = re.sub(r"\[[EPT]\]|\*\(.*?\)\*", "", stripped)
            words += stripped.split()
        return len(words)

    def total_words(rel: str) -> int:
        return len(re.findall(r"\b[\w'’-]+\b", read(rel)))

    plain_docs = sorted(PLAIN.glob("*.md"))
    return {
        "markdown_files": len(list(ROOT.rglob("*.md"))),
        "python_files": len(list(ROOT.rglob("*.py"))),
        "normative_rules_L_T_E": len(rule_ids(read(RULE_DOC_RELS[0]), "L"))
        + len(rule_ids(read(RULE_DOC_RELS[1]), "T"))
        + len(rule_ids(read(RULE_DOC_RELS[2]), "E")),
        "sugar_ids": len(sugar_ids(read(RULE_DOC_RELS[0]))),
        "ambiguities": len(ambiguity_rows(read("docs/plain/03-ambiguities.md"))),
        "deferrals": len(re.findall(r"^### (D-\d{2})", read("docs/plain/04-deferred-features.md"), re.MULTILINE)),
        "evidence_rows": len(evidence_rows(read("docs/evidence-register.md"))),
        "decision_records": len(list((ROOT / "docs" / "decisions").glob("0*.md"))),
        "plain_documents": len(plain_docs),
        "problem_statement_prose_words": prose_words("docs/problem-statement.md"),
        "problem_statement_total_words": total_words("docs/problem-statement.md"),
        "conformance_fixtures_written": len(list(ROOT.rglob("conformance/**/*.plain"))),
    }


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
    scan += sorted((ROOT / "docs" / "decisions").glob("*.md"))
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
    parser.add_argument("--verify", action="store_true", help="print the numbers prose may quote")
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
    declared_evidence = evidence_summary(evidence)
    deferral_ids = sorted(set(re.findall(r"^### (D-\d{2})", deferrals, re.MULTILINE)))
    registry = diagnostic_registry()
    traceability = traceability_matrix()
    areas = conformance_area_coverage()
    duplicates = duplicate_artifact_check()
    fact_clashes = duplicated_fact_check()
    xref = cross_reference_check()
    grammar = grammar_check()
    manifest = source_manifest_check()

    report = {
        "date": "2026-11-03",
        "scope": "Document audit; no Plain parser/evaluator or conformance fixtures",
        "rules": {k: {"count": len(v), "ids": v} for k, v in rules.items()},
        "normative_rule_count_L_T_E": sum(len(rules[k]) for k in ("L", "T", "E")),
        "ambiguities": {"count": len(amb), "status": {k: amb_status.get(k, 0) for k in ("resolved", "deferred", "open", "unknown")}, "rows": amb},
        "deferrals": {"count": len(deferral_ids), "ids": deferral_ids},
        "conformance_fixture_targets": {"rows": fixtures, "sum": sum(r["target"] for r in fixtures)},
        "evidence": {"count": len(ev), "labels": dict(labels), "declared_summary": declared_evidence, "retracted": [r["id"] for r in ev if r["status"].lower().startswith("retracted")]},
        "diagnostic_registry": registry,
        "traceability": traceability,
        "conformance_area_coverage": areas,
        "duplicate_artifacts": duplicates,
        "duplicated_facts": fact_clashes,
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
    fixture_sum = report["conformance_fixture_targets"]["sum"]
    declared_total = re.search(
        r"\|\s*\*\*Currently allocated\*\*\s*\|[^|]*\|\s*\*\*(\d+)\s*fixtures?\*\*",
        conformance,
    )
    if not declared_total:
        problems.append("conformance plan has no declared fixture total")
    elif int(declared_total.group(1)) != fixture_sum:
        problems.append(
            f"conformance plan declares {declared_total.group(1)} fixtures but its areas sum to {fixture_sum}"
        )
    if fixture_sum < 307:
        problems.append(f"fixture budget shrank below the recorded 307 floor: {fixture_sum}")
    if (
        declared_evidence["total"] != len(ev)
        or declared_evidence["labels"] != {key: labels.get(key, 0) for key in ("E", "P", "H")}
    ):
        problems.append(
            f"evidence register summary drift: actual={len(ev)} rows / {dict(labels)}, "
            f"declared={declared_evidence}"
        )
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
    if not traceability["ok"]:
        problems.append(
            f"traceability matrix incomplete: missing={traceability['missing']} "
            f"unknown={traceability['unknown']}"
        )
    if not areas["ok"]:
        problems.append(f"rules with no conformance-plan area: {areas['unattributed']}")
    if not duplicates["ok"]:
        problems.append(f"duplicated result artifacts: {duplicates['duplicates']}")
    if not fact_clashes["ok"]:
        problems.append(f"the same rule set is tabulated in more than one file: {fact_clashes['clashes']}")
    report["measured_facts"] = measured_facts()
    report["check"] = {"ok": not problems, "problems": problems}
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "check": report["check"],
        "normative_rule_count_L_T_E": report["normative_rule_count_L_T_E"],
        "ambiguities": report["ambiguities"]["status"],
        "deferrals": report["deferrals"]["count"],
        "evidence": report["evidence"]["labels"],
        "diagnostic_codes": len(registry),
        "traceability": {
            "rows": traceability["rows"],
            "covered": traceability["covered"],
            "defined": traceability["defined"],
            "missing": traceability["missing"],
        },
        "conformance_area_coverage": areas,
        "duplicate_artifacts": duplicates["duplicates"],
        "duplicated_facts": fact_clashes["clashes"],
        "cross_reference_check": xref,
        "grammar_check": grammar,
        "source_manifest_check": manifest,
    }, indent=2, ensure_ascii=False))
    if args.verify:
        print(json.dumps(report["measured_facts"], indent=2))
    return 1 if args.check and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
