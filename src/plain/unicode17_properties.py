"""Unicode 17.0.0 property lookups from the pinned UCD/security files.

These are data accessors, not a complete UTS #39 profile or UAX #9
implementation. No host ``unicodedata`` tables are consulted.
"""
from __future__ import annotations

import bisect
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

from .unicode17 import _code_range

T = TypeVar("T")


@dataclass
class RangeMap(Generic[T]):
    ranges: list[tuple[int, int, T]]
    default: T
    missing: list[tuple[int, int, T]]

    def __post_init__(self) -> None:
        self.ranges.sort(key=lambda row: row[0])
        self.starts = [row[0] for row in self.ranges]
        # Narrower @missing ranges override broader defaults.
        self.missing.sort(key=lambda row: (row[1] - row[0], row[0]))

    def get(self, cp: int) -> T:
        index = bisect.bisect_right(self.starts, cp) - 1
        if index >= 0:
            first, last, value = self.ranges[index]
            if cp <= last:
                return value
        for first, last, value in self.missing:
            if first <= cp <= last:
                return value
        return self.default


@dataclass
class RangeSet:
    ranges: list[tuple[int, int]]

    def __post_init__(self) -> None:
        self.ranges.sort()
        self.starts = [row[0] for row in self.ranges]

    def contains(self, cp: int) -> bool:
        index = bisect.bisect_right(self.starts, cp) - 1
        return index >= 0 and cp <= self.ranges[index][1]


def _merge_value_ranges(rows: list[tuple[int, int, T]]) -> list[tuple[int, int, T]]:
    merged: list[tuple[int, int, T]] = []
    for first, last, value in sorted(rows, key=lambda row: row[0]):
        if merged and merged[-1][1] + 1 == first and merged[-1][2] == value:
            prev_first, _, prev_value = merged[-1]
            merged[-1] = (prev_first, last, prev_value)
        else:
            merged.append((first, last, value))
    return merged


def _find(cache: Path, basename: str) -> Path:
    matches = list(cache.glob(f"*/{basename}"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one {basename} under {cache}; found {matches}")
    return matches[0]


def _script_aliases(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    aliases: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            content = raw.split("#", 1)[0].strip()
            if not content:
                continue
            fields = [part.strip() for part in content.split(";")]
            if len(fields) < 3 or fields[0] != "sc":
                continue
            canonical = fields[1]
            for value in fields[1:]:
                if value:
                    aliases[value] = canonical
    return aliases


def _property_file(path: Path, default: T) -> RangeMap[T]:
    rows: list[tuple[int, int, T]] = []
    missing: list[tuple[int, int, T]] = []
    missing_re = re.compile(r"@missing:\s*([0-9A-F.]+);\s*([^#]+)")
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            # @missing declarations are comments by file syntax but define defaults.
            if "@missing:" in raw:
                match = missing_re.search(raw)
                if match:
                    value = match.group(2).strip()
                    first, last = _code_range(match.group(1))
                    missing.append((first, last, value))  # type: ignore[arg-type]
                continue
            content = raw.split("#", 1)[0].strip()
            if not content:
                continue
            fields = [part.strip() for part in content.split(";")]
            if len(fields) < 2:
                continue
            first, last = _code_range(fields[0])
            rows.append((first, last, fields[1]))
    return RangeMap(_merge_value_ranges(rows), default, missing)


def _set_property(path: Path, wanted: str) -> RangeSet:
    rows: list[tuple[int, int]] = []
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            content = raw.split("#", 1)[0].strip()
            if not content:
                continue
            fields = [part.strip() for part in content.split(";")]
            if len(fields) < 2 or fields[1] != wanted:
                continue
            rows.append(_code_range(fields[0]))
    return RangeSet(rows)


def _unicode_data_ranges(path: Path) -> tuple[RangeMap[str], RangeMap[int]]:
    categories: list[tuple[int, int, str]] = []
    cccs: list[tuple[int, int, int]] = []
    pending: tuple[int, str, int] | None = None
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            fields = raw.rstrip("\n").split(";")
            if len(fields) < 6:
                raise ValueError(f"Malformed UnicodeData row {line_no}")
            cp = int(fields[0], 16)
            name = fields[1]
            category = fields[2]
            ccc = int(fields[3])
            if name.endswith(", First>"):
                pending = (cp, category, ccc)
                continue
            if name.endswith(", Last>"):
                if pending is None:
                    raise ValueError(f"UnicodeData Last row without First at line {line_no}")
                first, first_category, first_ccc = pending
                if category != first_category or ccc != first_ccc:
                    raise ValueError(f"UnicodeData First/Last mismatch at line {line_no}")
                categories.append((first, cp, category))
                if ccc:
                    cccs.append((first, cp, ccc))
                pending = None
                continue
            categories.append((cp, cp, category))
            if ccc:
                cccs.append((cp, cp, ccc))
    if pending is not None:
        raise ValueError("UnicodeData ended with unmatched First row")
    return RangeMap(_merge_value_ranges(categories), "Cn", []), RangeMap(_merge_value_ranges(cccs), 0, [])


_BIDI_LONG_TO_SHORT = {
    "Left_To_Right": "L",
    "Right_To_Left": "R",
    "Arabic_Letter": "AL",
    "European_Number": "EN",
    "European_Separator": "ES",
    "European_Terminator": "ET",
    "Arabic_Number": "AN",
    "Common_Separator": "CS",
    "Paragraph_Separator": "B",
    "Segment_Separator": "S",
    "White_Space": "WS",
    "Other_Neutral": "ON",
    "Left_To_Right_Embedding": "LRE",
    "Left_To_Right_Override": "LRO",
    "Right_To_Left_Embedding": "RLE",
    "Right_To_Left_Override": "RLO",
    "Pop_Directional_Format": "PDF",
    "Nonspacing_Mark": "NSM",
    "Boundary_Neutral": "BN",
    "First_Strong_Isolate": "FSI",
    "Left_To_Right_Isolate": "LRI",
    "Right_To_Left_Isolate": "RLI",
    "Pop_Directional_Isolate": "PDI",
}


@dataclass
class Unicode17Properties:
    xid_start: RangeSet
    xid_continue: RangeSet
    default_ignorable: RangeSet
    scripts: RangeMap[str]
    script_extensions: RangeMap[tuple[str, ...]]
    categories: RangeMap[str]
    combining_classes: RangeMap[int]
    bidi_classes: RangeMap[str]
    identifier_status: RangeMap[str]
    identifier_type_sets: dict[str, RangeSet]
    joining_types: dict[int, str]
    indic_syllabic_category: RangeMap[str]
    script_aliases: dict[str, str]

    @classmethod
    def from_cache(cls, cache: Path, property_value_aliases: Path | None = None) -> "Unicode17Properties":
        core = _find(cache, "DerivedCoreProperties.txt")
        scripts_path = _find(cache, "Scripts.txt")
        scx_path = _find(cache, "ScriptExtensions.txt")
        unicode_data = _find(cache, "UnicodeData.txt")
        bidi_path = _find(cache, "DerivedBidiClass.txt")
        status_path = _find(cache, "IdentifierStatus.txt")
        type_path = _find(cache, "IdentifierType.txt")
        shaping_path = _find(cache, "ArabicShaping.txt")
        isc_path = _find(cache, "IndicSyllabicCategory.txt")

        scripts = _property_file(scripts_path, "Unknown")
        scx_rows: list[tuple[int, int, tuple[str, ...]]] = []
        with scx_path.open(encoding="utf-8") as handle:
            for raw in handle:
                content = raw.split("#", 1)[0].strip()
                if not content:
                    continue
                fields = [part.strip() for part in content.split(";")]
                if len(fields) < 2:
                    raise ValueError(f"Malformed ScriptExtensions row: {raw!r}")
                first, last = _code_range(fields[0])
                scx_rows.append((first, last, tuple(fields[1].split())))
        script_extensions = RangeMap(_merge_value_ranges(scx_rows), (), [])

        categories, combining = _unicode_data_ranges(unicode_data)
        bidi = _property_file(bidi_path, "L")
        bidi.ranges = [
            (first, last, _BIDI_LONG_TO_SHORT.get(value, value))
            for first, last, value in bidi.ranges
        ]
        bidi.missing = [
            (first, last, _BIDI_LONG_TO_SHORT.get(value, value))
            for first, last, value in bidi.missing
        ]
        status = _property_file(status_path, "Restricted")

        type_ranges: dict[str, list[tuple[int, int]]] = {}
        with type_path.open(encoding="utf-8") as handle:
            for raw in handle:
                content = raw.split("#", 1)[0].strip()
                if not content:
                    continue
                fields = [part.strip() for part in content.split(";")]
                if len(fields) < 2:
                    raise ValueError(f"Malformed IdentifierType row: {raw!r}")
                interval = _code_range(fields[0])
                for value in fields[1].split():
                    type_ranges.setdefault(value, []).append(interval)
        type_sets = {name: RangeSet(ranges) for name, ranges in type_ranges.items()}

        joining: dict[int, str] = {}
        with shaping_path.open(encoding="utf-8") as handle:
            for line_no, raw in enumerate(handle, start=1):
                content = raw.split("#", 1)[0].strip()
                if not content:
                    continue
                fields = [part.strip() for part in content.split(";")]
                if len(fields) < 3:
                    raise ValueError(f"Malformed ArabicShaping row at line {line_no}")
                joining[int(fields[0], 16)] = fields[2]

        isc = _property_file(isc_path, "Other")
        return cls(
            xid_start=_set_property(core, "XID_Start"),
            xid_continue=_set_property(core, "XID_Continue"),
            default_ignorable=_set_property(core, "Default_Ignorable_Code_Point"),
            scripts=scripts,
            script_extensions=script_extensions,
            categories=categories,
            combining_classes=combining,
            bidi_classes=bidi,
            identifier_status=status,
            identifier_type_sets=type_sets,
            joining_types=joining,
            indic_syllabic_category=isc,
            script_aliases=_script_aliases(property_value_aliases),
        )

    def script(self, cp: int) -> str:
        return self.scripts.get(cp)

    def script_code(self, cp: int) -> str:
        if not self.script_aliases:
            raise RuntimeError("PropertyValueAliases.txt is required to normalize Script/Script_Extensions names")
        value = self.script(cp)
        try:
            return self.script_aliases[value]
        except KeyError as exc:
            raise ValueError(f"Unmapped Unicode Script value {value!r}") from exc

    def script_extensions_for(self, cp: int) -> tuple[str, ...]:
        if not self.script_aliases:
            raise RuntimeError("PropertyValueAliases.txt is required before Script_Extensions comparisons")
        explicit = self.script_extensions.get(cp)
        values = explicit if explicit else (self.script(cp),)
        try:
            return tuple(sorted({self.script_aliases[value] for value in values}))
        except KeyError as exc:
            raise ValueError(f"Unmapped Script_Extensions value {exc.args[0]!r}") from exc

    def bidi_class(self, cp: int) -> str:
        return self.bidi_classes.get(cp)

    def general_category(self, cp: int) -> str:
        return self.categories.get(cp)

    def combining_class(self, cp: int) -> int:
        return self.combining_classes.get(cp)

    def identifier_type(self, cp: int) -> frozenset[str]:
        return frozenset(name for name, ranges in self.identifier_type_sets.items() if ranges.contains(cp))

    def joining_type(self, cp: int) -> str:
        return self.joining_types.get(cp, "U")

    def isc(self, cp: int) -> str:
        return self.indic_syllabic_category.get(cp)
