#!/usr/bin/env python3
"""Validate the project-owned Unicode 17 normalizer against all test rows."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plain.unicode17 import Unicode17Normalizer  # noqa: E402

CACHE = ROOT / "research/data/.cache/unicode17"
OUTPUT = ROOT / "research/data/phase-01-normalization-report.json"


def data_file(source_id: str) -> Path:
    matches = list((CACHE / source_id).glob("*"))
    if len(matches) != 1 or not matches[0].is_file():
        raise RuntimeError(f"Expected exactly one cached file for {source_id}; found {matches}")
    return matches[0]


def parse_points(field: str) -> str:
    return "".join(chr(int(point, 16)) for point in field.split())


def check() -> dict:
    normalizer = Unicode17Normalizer.from_directory(CACHE)
    test_path = data_file("unicode17-normalizationtest")
    rows = 0
    assertions = 0
    failures: list[dict] = []
    failure_count = 0
    with test_path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            content = raw.split("#", 1)[0].strip()
            if not content or content.startswith("@"):
                continue
            fields = [item.strip() for item in content.split(";")]
            if len(fields) < 5:
                raise RuntimeError(f"Malformed NormalizationTest row at line {line_number}")
            c1, c2, c3, c4, c5 = map(parse_points, fields[:5])
            rows += 1
            expected_nfc = (c2, c2, c2, c4, c4)
            expected_nfd = (c3, c3, c3, c5, c5)
            for column, source in enumerate((c1, c2, c3, c4, c5), start=1):
                got_nfc = normalizer.nfc(source)
                got_nfd = normalizer.nfd(source)
                assertions += 2
                if got_nfc != expected_nfc[column - 1]:
                    failure_count += 1
                    if len(failures) < 100:
                        failures.append({
                            "line": line_number,
                            "form": "NFC",
                            "column": column,
                            "input": [f"U+{ord(ch):04X}" for ch in source],
                            "expected": [f"U+{ord(ch):04X}" for ch in expected_nfc[column - 1]],
                            "actual": [f"U+{ord(ch):04X}" for ch in got_nfc],
                        })
                if got_nfd != expected_nfd[column - 1]:
                    failure_count += 1
                    if len(failures) < 100:
                        failures.append({
                            "line": line_number,
                            "form": "NFD",
                            "column": column,
                            "input": [f"U+{ord(ch):04X}" for ch in source],
                            "expected": [f"U+{ord(ch):04X}" for ch in expected_nfd[column - 1]],
                            "actual": [f"U+{ord(ch):04X}" for ch in got_nfd],
                        })
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input": "Unicode 17.0.0 NormalizationTest.txt",
        "implementation": "src/plain/unicode17.py; no Python unicodedata import",
        "rows_checked": rows,
        "assertions_checked": assertions,
        "failure_count": failure_count,
        "passed": failure_count == 0,
        "failures_first_100": failures,
    }


def main() -> int:
    report = check()
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rows={report['rows_checked']} assertions={report['assertions_checked']} failures={report['failure_count']}")
    print(f"report: {OUTPUT.relative_to(ROOT)}")
    if not report["passed"]:
        for failure in report["failures_first_100"][:10]:
            print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
