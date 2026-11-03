"""Invariants that keep the Phase 1 documents from drifting.

These do not test Plain, because Plain does not exist yet. They test the
document set: that the audit tool is green, that every normative rule is
traceable to a verification method, that nothing is duplicated, and that the
published counts match the files. Each assertion corresponds to a failure mode
that had actually occurred in this repository before the check existed.

Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from collections import Counter
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import audit_phase01 as audit  # noqa: E402

read = audit.read
registry = audit.diagnostic_registry
uncoded_obligation_check = audit.uncoded_obligation_check
conformance_area_coverage = audit.conformance_area_coverage
fault_namespace_check = audit.fault_namespace_check


class DocumentInvariantTests(unittest.TestCase):
    def test_audit_reports_no_problems(self) -> None:
        # The single umbrella check: counts, links, xrefs, grammar, manifest,
        # traceability, area coverage, duplicate artifacts.
        traceability = audit.traceability_matrix()
        areas = audit.conformance_area_coverage()
        duplicates = audit.duplicate_artifact_check()
        self.assertTrue(traceability["ok"], traceability)
        self.assertTrue(areas["ok"], areas)
        self.assertTrue(duplicates["ok"], duplicates)
        self.assertEqual(audit.broken_links(), [])
        self.assertEqual(audit.cross_reference_check()["undefined"], {})

    def test_every_rule_has_a_verification_method(self) -> None:
        matrix = audit.traceability_matrix()
        self.assertEqual(matrix["missing"], [], "rules with no traceability row")
        self.assertEqual(matrix["unknown"], [], "traceability rows for rules that do not exist")
        self.assertEqual(matrix["covered"], matrix["defined"])
        self.assertEqual(matrix["defined"], 106, "34 L + 30 T + 36 E + 6 S expected")

    def test_every_rule_has_a_conformance_area(self) -> None:
        areas = audit.conformance_area_coverage()
        self.assertEqual(areas["attributed"], areas["defined"])
        self.assertEqual(areas["unattributed"], [])

    def test_results_are_not_stored_twice(self) -> None:
        self.assertTrue(audit.duplicate_artifact_check()["ok"])

    def test_no_rule_set_is_tabulated_in_two_documents(self) -> None:
        # A partially copied table drifts: one copy gains a row, the other does
        # not. This happened three times here (conformance areas, the Gate 1
        # exclusion list, the decision index) before the check existed.
        result = audit.duplicated_fact_check()
        self.assertTrue(result["ok"], result["clashes"])

    def test_gate_one_exclusions_have_exactly_one_owner(self) -> None:
        # Section 4 of the traceability matrix owns this table; the conformance
        # plan must link to it rather than restate it.
        plan = audit.read("docs/plain/05-conformance-plan.md")
        self.assertIn("07-traceability.md#4-rules-gate-1-cannot-fully-verify", plan)
        self.assertNotIn("| `E-31` (task-survival clause) | No scheduler", plan)

    def test_declared_fixture_total_equals_summed_areas(self) -> None:
        plan = audit.read("docs/plain/05-conformance-plan.md")
        rows = audit.fixture_targets(plan)
        self.assertGreater(len(rows), 0)
        total = sum(row["target"] for row in rows)
        declared = re.search(
            r"\|\s*\*\*Currently allocated\*\*\s*\|[^|]*\|\s*\*\*(\d+)\s*fixtures?\*\*", plan
        )
        self.assertIsNotNone(declared, "plan no longer declares a fixture total")
        self.assertEqual(int(declared.group(1)), total)
        self.assertGreaterEqual(total, 307, "fixture budget must not shrink below the recorded floor")

    def test_evidence_register_summary_matches_rows(self) -> None:
        register = audit.read("docs/evidence-register.md")
        rows = audit.evidence_rows(register)
        declared = audit.evidence_summary(register)
        self.assertEqual(declared["total"], len(rows))

        actual = Counter(row["label"] for row in rows)
        self.assertEqual(declared["labels"], {k: actual.get(k, 0) for k in ("E", "P", "H")})

    def test_no_markdown_table_is_split_by_a_blank_line(self) -> None:
        # Three tables were split this way before; a split table silently drops
        # rows from any tool that parses it.
        offenders = []
        for path in sorted(ROOT.rglob("*.md")):
            if ".git" in path.parts:
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            for index in range(1, len(lines) - 1):
                if not lines[index].strip():
                    if lines[index - 1].startswith("|") and lines[index + 1].startswith("|"):
                        offenders.append(f"{path.relative_to(ROOT)}:{index + 1}")
        self.assertEqual(offenders, [])

    def test_numbered_markdown_headings_are_unique_per_file(self) -> None:
        # gate-00.md had two "## 8." headings, so every "§8" reference in the
        # file was ambiguous. Repeated prose subheadings inside a phase are
        # normal and are not checked.
        offenders = []
        for path in sorted(ROOT.rglob("*.md")):
            if ".git" in path.parts:
                continue
            seen = set()
            for line in path.read_text(encoding="utf-8").splitlines():
                match = re.match(r"^#{2,3}\s+(\d+(?:\.\d+)*)\.\s", line)
                if not match:
                    continue
                number = match.group(1)
                if number in seen:
                    offenders.append(f"{path.relative_to(ROOT)}: heading {number}")
                seen.add(number)
        self.assertEqual(offenders, [])

    def test_gate_zero_internal_section_references_resolve(self) -> None:
        # References that explicitly point into this file must resolve. Other
        # "§N" strings cite the problem statement, the research book, or a
        # decision record and are out of scope for this check.
        gate0 = audit.read("docs/gates/gate-00.md")
        headings = {m.group(1) for m in re.finditer(r"^## (\d+)\.", gate0, re.MULTILINE)}
        internal = re.findall(
            r"(?:see|in|ruled in|recorded in)\s+§(\d+)", gate0
        ) + re.findall(r"§(\d+)\s+(?:below|above)", gate0)
        self.assertTrue(internal, "expected at least one internal section reference")
        for target in internal:
            self.assertIn(target, headings, f"gate-00.md cites §{target}, which does not exist")


if __name__ == "__main__":
    unittest.main()


class FaultNamespaceTest(unittest.TestCase):
    """A fault must never be reportable as an ordinary diagnostic.

    E-30 makes faults terminating and T-12 makes them uncatchable. If a fault
    code looked like an error code, implementers would write a `catch` for it.
    """

    def test_faults_have_their_own_namespace(self):
        faults = [e for e in registry() if e["severity"] == "fault"]
        self.assertTrue(faults, "no fault codes exist: fault fixtures are unnameable")
        for entry in faults:
            self.assertTrue(
                entry["code"].startswith("PLFL"),
                f"{entry['code']} is a fault but is not in the PLFL namespace",
            )

    def test_every_gate_one_fault_rule_names_a_fault(self):
        for rule in ("E-05", "E-06", "E-33"):
            codes = [e["code"] for e in registry() if rule in e["rules"]]
            self.assertTrue(
                any(code.startswith("PLFL") for code in codes),
                f"{rule} produces a fault but names no PLFL code",
            )


class UncodedObligationTest(unittest.TestCase):
    """A rule that refuses a construct must be fixturable.

    Conformance plan 3.3 asserts exact codes, so an uncoded refusal cannot be
    tested without inventing an identifier during implementation.
    """

    def test_no_refusal_rule_is_left_without_a_code_or_an_explanation(self):
        result = uncoded_obligation_check()
        self.assertTrue(
            result["ok"],
            f"rules demand refusal with no code and no §6 entry: {result['unexplained']}",
        )

    def test_a_code_named_as_the_fault_is_in_the_fault_namespace(self):
        """Regression: renaming PLFL03 to PL0399 passed every other test.

        The registry still held a fault (PLFL04 on the same rule) and the
        namespace test still passed, so only reading the sentence caught it.
        """
        result = fault_namespace_check()
        self.assertEqual(
            result["offenders"], [], "a code is named as a fault outside the PLFL namespace"
        )

    def test_every_registry_code_has_an_owning_rule(self):
        orphans = [e["code"] for e in registry() if not e["rules"]]
        self.assertEqual(orphans, [], "codes exist that no rule owns")


class DiagnosticCatalogTest(unittest.TestCase):
    """The catalog is the artifact that makes 71 codes fixturable."""

    def test_catalog_quotes_the_measured_registry_size(self):
        text = read("docs/plain/08-diagnostics-and-faults.md")
        self.assertIn(str(len(registry())), text, "catalog does not quote the registry size")

    def test_conformance_budget_matches_area_rows(self):
        coverage = conformance_area_coverage()
        self.assertTrue(coverage["ok"], coverage)
