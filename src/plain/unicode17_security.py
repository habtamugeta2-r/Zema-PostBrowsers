"""Unicode 17.0.0 UTS #39 internal skeleton primitives.

This module implements internalSkeleton only. It does not implement
UAX #9 bidi reordering or the external skeleton/bidiSkeleton wrappers;
callers must not treat this as full identifier-confusability checking.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .unicode17 import Unicode17Normalizer, _code_range


@dataclass
class Unicode17SecurityData:
    normalizer: Unicode17Normalizer
    default_ignorables: set[int]
    confusables: dict[int, tuple[int, ...]]

    @classmethod
    def from_cache(cls, cache_dir: Path) -> "Unicode17SecurityData":
        core_files = list(cache_dir.glob("*/DerivedCoreProperties.txt"))
        confusable_files = list(cache_dir.glob("*/confusables.txt"))
        if len(core_files) != 1 or len(confusable_files) != 1:
            raise FileNotFoundError("Need one DerivedCoreProperties.txt and confusables.txt in Unicode cache")

        default_ignorables: set[int] = set()
        with core_files[0].open(encoding="utf-8") as handle:
            for raw in handle:
                content = raw.split("#", 1)[0].strip()
                if not content:
                    continue
                fields = [part.strip() for part in content.split(";")]
                if len(fields) < 2 or fields[1] != "Default_Ignorable_Code_Point":
                    continue
                first, last = _code_range(fields[0])
                default_ignorables.update(range(first, last + 1))

        confusables: dict[int, tuple[int, ...]] = {}
        with confusable_files[0].open(encoding="utf-8") as handle:
            for line_number, raw in enumerate(handle, start=1):
                content = raw.split("#", 1)[0].strip()
                if not content:
                    continue
                fields = [part.strip() for part in content.split(";")]
                if len(fields) < 2:
                    raise ValueError(f"Malformed confusables row at line {line_number}")
                source = tuple(int(item, 16) for item in fields[0].split())
                target = tuple(int(item, 16) for item in fields[1].split())
                if len(source) != 1:
                    raise ValueError(f"Expected single-code-point source at line {line_number}")
                confusables[source[0]] = target

        normalizer = Unicode17Normalizer.from_directory(cache_dir)
        return cls(normalizer, default_ignorables, confusables)

    def internal_skeleton(self, text: str) -> str:
        decomposed = self.normalizer.nfd(text)
        mapped: list[int] = []
        for char in decomposed:
            cp = ord(char)
            if cp in self.default_ignorables:
                continue
            mapped.extend(self.confusables.get(cp, (cp,)))
        return self.normalizer.nfd("".join(chr(cp) for cp in mapped))
