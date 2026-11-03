"""Minimal Unicode 17 canonical normalization from manifest-pinned data.

This module intentionally does not import Python's ``unicodedata``.
It implements canonical decomposition, canonical ordering, and canonical
composition, including algorithmic Hangul decomposition/composition.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


S_BASE = 0xAC00
L_BASE = 0x1100
V_BASE = 0x1161
T_BASE = 0x11A7
L_COUNT = 19
V_COUNT = 21
T_COUNT = 28
N_COUNT = V_COUNT * T_COUNT
S_COUNT = L_COUNT * N_COUNT


def _code_range(text: str) -> tuple[int, int]:
    text = text.strip()
    if ".." in text:
        first, last = text.split("..", 1)
        return int(first, 16), int(last, 16)
    point = int(text, 16)
    return point, point


def _ranges(path: Path, property_name: str) -> set[int]:
    result: set[int] = set()
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            fields = [field.strip() for field in line.split(";")]
            if len(fields) < 2 or fields[1] != property_name:
                continue
            first, last = _code_range(fields[0])
            result.update(range(first, last + 1))
    return result


@dataclass
class Unicode17Normalizer:
    canonical_decomposition: dict[int, tuple[int, ...]]
    combining_class: dict[int, int]
    composition: dict[tuple[int, int], int]
    full_composition_exclusion: set[int]

    @classmethod
    def from_directory(cls, data_dir: Path) -> "Unicode17Normalizer":
        def source_file(name: str) -> Path:
            matches = list(data_dir.glob(f"*/{name}"))
            if len(matches) != 1:
                raise FileNotFoundError(f"Expected exactly one {name} under {data_dir}; found {matches}")
            return matches[0]

        unicode_data = source_file("UnicodeData.txt")
        derived = source_file("DerivedNormalizationProps.txt")
        exclusions = _ranges(derived, "Full_Composition_Exclusion")
        decomposition: dict[int, tuple[int, ...]] = {}
        combining: dict[int, int] = {}
        with unicode_data.open(encoding="utf-8") as handle:
            for raw in handle:
                fields = raw.rstrip("\n").split(";")
                if len(fields) < 6:
                    raise ValueError(f"Malformed UnicodeData row: {raw!r}")
                cp = int(fields[0], 16)
                ccc = int(fields[3])
                if ccc:
                    combining[cp] = ccc
                mapping = fields[5].strip()
                if mapping and not mapping.startswith("<"):
                    decomposition[cp] = tuple(int(item, 16) for item in mapping.split())

        composition: dict[tuple[int, int], int] = {}
        for cp, mapping in decomposition.items():
            if len(mapping) == 2 and cp not in exclusions:
                composition[mapping] = cp
        return cls(decomposition, combining, composition, exclusions)

    def ccc(self, cp: int) -> int:
        return self.combining_class.get(cp, 0)

    @staticmethod
    def _hangul_decompose(cp: int) -> tuple[int, ...] | None:
        index = cp - S_BASE
        if not 0 <= index < S_COUNT:
            return None
        lead = L_BASE + index // N_COUNT
        vowel = V_BASE + (index % N_COUNT) // T_COUNT
        trail_index = index % T_COUNT
        if trail_index:
            return lead, vowel, T_BASE + trail_index
        return lead, vowel

    @staticmethod
    def _hangul_compose(first: int, second: int) -> int | None:
        lead_index = first - L_BASE
        if 0 <= lead_index < L_COUNT:
            vowel_index = second - V_BASE
            if 0 <= vowel_index < V_COUNT:
                return S_BASE + (lead_index * V_COUNT + vowel_index) * T_COUNT
        syllable_index = first - S_BASE
        if 0 <= syllable_index < S_COUNT and syllable_index % T_COUNT == 0:
            trail_index = second - T_BASE
            if 1 <= trail_index < T_COUNT:
                return first + trail_index
        return None

    def _decompose_one(self, cp: int, output: list[int]) -> None:
        hangul = self._hangul_decompose(cp)
        if hangul is not None:
            for part in hangul:
                self._decompose_one(part, output)
            return
        mapping = self.canonical_decomposition.get(cp)
        if mapping is None:
            output.append(cp)
            return
        for part in mapping:
            self._decompose_one(part, output)

    def _canonical_order(self, points: list[int]) -> list[int]:
        ordered: list[int] = []
        for cp in points:
            ccc = self.ccc(cp)
            if ccc == 0:
                ordered.append(cp)
                continue
            index = len(ordered)
            while index > 0:
                previous_ccc = self.ccc(ordered[index - 1])
                if previous_ccc == 0 or previous_ccc <= ccc:
                    break
                index -= 1
            ordered.insert(index, cp)
        return ordered

    def nfd(self, text: str) -> str:
        points: list[int] = []
        for char in text:
            self._decompose_one(ord(char), points)
        return "".join(chr(cp) for cp in self._canonical_order(points))

    def _compose_pair(self, first: int, second: int) -> int | None:
        hangul = self._hangul_compose(first, second)
        if hangul is not None:
            return hangul
        return self.composition.get((first, second))

    def nfc(self, text: str) -> str:
        decomposed = [ord(char) for char in self.nfd(text)]
        if not decomposed:
            return ""
        result = [decomposed[0]]
        starter_pos: int | None = 0 if self.ccc(decomposed[0]) == 0 else None
        starter = decomposed[0] if starter_pos is not None else None
        last_ccc = 0

        for cp in decomposed[1:]:
            ccc = self.ccc(cp)
            composite = None
            if starter is not None and (last_ccc < ccc or last_ccc == 0):
                composite = self._compose_pair(starter, cp)
            if composite is not None:
                assert starter_pos is not None
                result[starter_pos] = composite
                starter = composite
                continue

            if ccc == 0:
                starter_pos = len(result)
                starter = cp
            last_ccc = ccc
            result.append(cp)
        return "".join(chr(cp) for cp in result)


def cached_unicode17_directory(repo_root: Path) -> Path:
    return repo_root / "research/data/.cache/unicode17"
