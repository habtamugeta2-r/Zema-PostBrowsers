#!/usr/bin/env python3
"""Record UTS #39 internalSkeleton outputs; bidiSkeleton remains unimplemented."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plain.unicode17_security import Unicode17SecurityData  # noqa: E402
OUTPUT = ROOT / "research/data/phase-01-internal-skeleton-examples.json"
EXAMPLES = ["aא1", "a1א", "Строкa", "Δt", "HTTPसर्वर"]


def main() -> int:
    security = Unicode17SecurityData.from_cache(ROOT / "research/data/.cache/unicode17")
    results = []
    for text in EXAMPLES:
        skeleton = security.internal_skeleton(text)
        results.append({
            "input": text,
            "input_codepoints": [f"U+{ord(ch):04X}" for ch in text],
            "internal_skeleton": skeleton,
            "internal_skeleton_codepoints": [f"U+{ord(ch):04X}" for ch in skeleton],
        })
    report = {
        "computed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "unicode_version": "17.0.0",
        "algorithm": "UTS #39 rev32 internalSkeleton only: NFD, remove Default_Ignorable_Code_Point, map confusables.txt, NFD",
        "not_implemented": "UAX #9 bidi processing; outputs are not skeleton(X) or bidiSkeleton(d, X) results",
        "results": results,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(results)} internalSkeleton results)")
    for row in results:
        print(f"{row['input']!r} -> {row['internal_skeleton']!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
