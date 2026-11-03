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
CATALOG_REL = "docs/plain/08-diagnostics-and-faults.md"


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


def uncoded_rejection_rules() -> list[str]:
    """Rules that demand a refusal but name no code.

    This is the measure of 'unbuildable as specified': the plan says a fault
    fixture asserts an exact code, so an obligation without a code cannot be
    fixtured without inventing one.
    """
    refuse = re.compile(
        r"MUST NOT|\bis an error\b|\bare errors\b|MUST be (?:an )?error"
        r"|\brejected\b|\bforbidden\b"
    )
    found = []
    for rel in RULE_DOC_RELS:
        for line in read(rel).splitlines():
            match = re.match(r"^- \*\*([LTE]-\d{2})\*\*(.*)", line)
            if not match:
                continue
            rule_id, body = match.group(1), match.group(2)
            if re.search(r"PL(?:FL)?\d{2,4}", body):
                continue
            if refuse.search(body):
                found.append(rule_id)
    return found


def duplicated_fact_check() -> dict:
    """Detect two documents owning the *same* table about the same rules.

    The earlier version compared rule-ID sets and produced a false positive:
    the traceability matrix and the diagnostic catalog both list rule IDs, but
    they state different facts about them (method/area vs. why-no-code). Two
    tables are the same fact only when their **header rows match** and their
    rule sets overlap.

    The defect this catches is the real one: a table copied into a second file
    with the same columns, which then drifts when one copy gains a row. That
    happened twice here (the conformance areas, the Gate 1 exclusion list).
    """
    targets = sorted(PLAIN.glob("*.md"))
    tables: list[dict] = []
    for path in targets:
        lines = path.read_text(encoding="utf-8").splitlines()
        index = 0
        while index < len(lines) - 2:
            header = lines[index]
            separator = lines[index + 1]
            if header.startswith("|") and re.fullmatch(r"\|[\s:|-]+\|", separator.strip()):
                rules: set[str] = set()
                cursor = index + 2
                while cursor < len(lines) and lines[cursor].startswith("|"):
                    match = re.match(r"\|\s*`?([LTE]-\d{2}|S-\d)\b", lines[cursor])
                    if match:
                        rules.add(match.group(1))
                    # range cells like "L-01…L-04"
                    for span in re.finditer(r"([LTE])-(\d{2})\s*…\s*(?:[LTE]-)?(\d{2})", lines[cursor]):
                        pre, low, high = span.group(1), int(span.group(2)), int(span.group(3))
                        rules.update(f"{pre}-{i:02d}" for i in range(low, high + 1))
                    cursor += 1
                if len(rules) >= 3:
                    tables.append(
                        {
                            "file": str(path.relative_to(ROOT)),
                            "header": header.strip(),
                            "rules": rules,
                            "line": index + 1,
                        }
                    )
                index = cursor
            else:
                index += 1

    clashes = []
    for i, left in enumerate(tables):
        for right in tables[i + 1:]:
            if left["header"] != right["header"]:
                continue
            shared = left["rules"] & right["rules"]
            if len(shared) >= 3:
                clashes.append(
                    {
                        "header": left["header"],
                        "files": [f'{left["file"]}:{left["line"]}', f'{right["file"]}:{right["line"]}'],
                        "shared_rules": sorted(shared),
                        "owner": left["file"],
                        "duplicate": right["file"],
                    }
                )
    return {"ok": not clashes, "clashes": clashes, "tables_scanned": len(tables)}


def uncoded_obligation_check() -> dict:
    """Every rule that demands a refusal must name a code or be explained.

    A rule that refuses a construct without an identifier cannot be fixtured by
    a runner that asserts exact codes (conformance plan 3.3). Section 6 of the
    catalog is the explicit allowlist for rules that correctly need no code.
    """
    catalog = ROOT / CATALOG_REL
    explained: set[str] = set()
    if catalog.exists():
        text = catalog.read_text(encoding="utf-8")
        section = text.split("## 6.", 1)
        if len(section) == 2:
            body = section[1].split("## 7.", 1)[0]
            for line in body.splitlines():
                if not line.startswith("|"):
                    continue
                first_cell = line.split("|")[1]
                for match in re.finditer(r"\b([LTE]-\d{2})\b", first_cell):
                    explained.add(match.group(1))
                for match in re.finditer(r"([LTE])-(\d{2})\s*…\s*([LTE])?-(\d{2})", line):
                    prefix, low, high = match.group(1), int(match.group(2)), int(match.group(4))
                    explained.update(f"{prefix}-{i:02d}" for i in range(low, high + 1))
    unresolved = [r for r in uncoded_rejection_rules() if r not in explained]
    return {"ok": not unresolved, "unexplained": unresolved, "explained_count": len(explained)}


def measured_facts() -> dict:
    """Quantities that prose is allowed to quote (process rule PR-01).

    Prose may restate these; it may not originate them. Run with --verify to
    print them, then compare against the documents.
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
        """Every word except the leading control block's own Length row.

        The Length cell quotes this number, so counting it makes the figure
        depend on itself: correcting 866 to 868 changed the total to 868 and
        the "corrected" value was wrong again. Excluding the row it lives in
        makes the measurement a stable fixed point.
        """
        lines = [
            line
            for line in read(rel).splitlines()
            if not line.startswith("| **Length**")
        ]
        return len(re.findall(r"\b[\w'’-]+\b", "\n".join(lines)))

    def code_accounting() -> dict:
        """Codes cited by rule text, plus faults defined only in the catalog."""
        registry = diagnostic_registry()
        active = {e["code"] for e in registry if not e["historical"]}
        historical = {e["code"] for e in registry if e["historical"]}
        faults = {e["code"] for e in registry if e["severity"] == "fault"}
        return {
            "codes_cited_by_rules": len(active),
            "historical_codes": len(historical),
            "fault_codes_defined": len(faults),
            "all_active_codes": len(active) + len(faults),
        }

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
        "plain_documents": len(list(PLAIN.glob("*.md"))),
        "problem_statement_prose_words": prose_words("docs/problem-statement.md"),
        "problem_statement_total_words": total_words("docs/problem-statement.md"),
        "conformance_fixtures_written": len(list(ROOT.rglob("conformance/**/*.plain"))),
        "code_accounting": code_accounting(),
        "rules_requiring_rejection_without_a_code": uncoded_rejection_rules(),
    }


def fault_namespace_check() -> dict:
    """A code introduced as *the fault* must be in the fault namespace.

    A sentence-level search is too coarse: these rule lines are long, and
    "fault" often appears in a different clause from the code ("Faults are not
    recoverable failures ... (`PL0204`)"), which produced five false positives.
    The real signal is the appositive — "the fault `X`", "a fault `X`" — where a
    code is *named as* a fault. Only that construction is checked.
    """
    pattern = re.compile(r"\b(?:the|a|an)\s+fault\s+`?(PL[\w]+)`?", re.IGNORECASE)
    offenders = []
    for rel in RULE_DOC_RELS:
        for line in read(rel).splitlines():
            for match in pattern.finditer(line):
                code = match.group(1)
                if not code.startswith("PLFL"):
                    offenders.append({"file": rel, "code": code, "text": match.group(0)})
    return {"ok": not offenders, "offenders": offenders}


def codeless_claim_check() -> dict:
    """A rule listed as needing no code must not silently own one.

    Section 6 lists rules whose correct fixture is behavior, not a diagnostic.
    A rule can legitimately appear there *and* own a code when only part of it
    is a rejection — `?` evaluates once (behavior) but `?` inside `defer` is
    rejected (PL0228). That partial case is allowed only if the §6 row names the
    code, so the catalog acknowledges it instead of contradicting itself.

    Found by audit: five rules were listed as codeless while the registry
    recorded them as owning a code, because the registry attributes a code to
    every rule mentioned on its line, including enumerations.
    """
    catalog = ROOT / CATALOG_REL
    if not catalog.exists():
        return {"ok": False, "silent": [{"rule": "*", "why": "catalog missing"}]}
    text = catalog.read_text(encoding="utf-8")
    section = text.split("## 6.", 1)
    if len(section) != 2:
        return {"ok": False, "silent": [{"rule": "*", "why": "no §6"}]}
    body = section[1].split("## 7.", 1)[0]

    rows: dict[str, str] = {}
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cell = line.split("|")[1]
        ids = set(re.findall(r"[LTE]-\d{2}", cell))
        for span in re.finditer(r"([LTE])-(\d{2})\s*…\s*(?:[LTE]-)?(\d{2})", cell):
            ids.update(f"{span.group(1)}-{i:02d}" for i in range(int(span.group(2)), int(span.group(3)) + 1))
        for rule in ids:
            rows[rule] = rows.get(rule, "") + " " + line

    silent = []
    for entry in diagnostic_registry():
        for rule in entry["rules"]:
            if rule not in rows:
                continue
            if entry["code"] in rows[rule]:
                continue
            silent.append({"rule": rule, "owns": entry["code"]})
    return {"ok": not silent, "silent": silent, "listed": len(rows)}


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


def fault_severity(code: str) -> str:
    """Severity is part of a code's identity (catalog 1, rule 4).

    A fault terminates the task and cannot be caught, so it must never be
    reported as an ordinary error: that would invite a `catch` for it, which
    T-12 forbids.
    """
    if code.startswith("PLFL"):
        return "fault"
    if code.startswith("PL1"):
        return "warning"
    return "error"


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
            for code in re.findall(r"PL(?:FL)?\d{2,4}", line):
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
            "severity": fault_severity(code),
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
    uncoded = uncoded_obligation_check()
    fault_ns = fault_namespace_check()
    codeless = codeless_claim_check()
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
        "uncoded_obligations": uncoded,
        "fault_namespace": fault_ns,
        "codeless_claims": codeless,
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
    if not codeless["ok"]:
        problems.append(
            "rules are listed in the catalog as needing no code but the registry records "
            f"them as owning one, and the row does not say so: {codeless['silent']}"
        )
    if not fault_ns["ok"]:
        problems.append(
            "a code is introduced as a fault but is not in the PLFL namespace: "
            f"{[o['file'] + ' -> ' + o['code'] for o in fault_ns['offenders']]}"
        )
    if not uncoded["ok"]:
        problems.append(
            "rules demand a refusal but name no diagnostic code and are not explained "
            f"in {CATALOG_REL} §6: {uncoded['unexplained']}"
        )
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
        "diagnostic_codes_by_severity": dict(
            sorted(Counter(e["severity"] for e in registry).items())
        ),
        "codes_without_owning_rule": sorted(e["code"] for e in registry if not e["rules"]),
        "fault_namespace": report["fault_namespace"],
        "codeless_claims": report["codeless_claims"],
        "traceability": {
            "rows": traceability["rows"],
            "covered": traceability["covered"],
            "defined": traceability["defined"],
            "missing": traceability["missing"],
        },
        "conformance_area_coverage": areas,
        "duplicate_artifacts": duplicates["duplicates"],
        "duplicated_facts": fact_clashes["clashes"],
        "uncoded_obligations": uncoded['unexplained'],
        "cross_reference_check": xref,
        "grammar_check": grammar,
        "source_manifest_check": manifest,
    }, indent=2, ensure_ascii=False))
    if args.verify:
        print(json.dumps(report["measured_facts"], indent=2))
    return 1 if args.check and problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
