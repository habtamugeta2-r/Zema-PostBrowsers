"""Smoke tests for Unicode 17 source parsers; run after fetch_unicode17.py."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plain.unicode17_properties import Unicode17Properties  # noqa: E402

CACHE = ROOT / "research/data/.cache/unicode17"


@unittest.skipUnless(CACHE.exists(), "run python3 tools/fetch_unicode17.py first")
class Unicode17PropertyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.properties = Unicode17Properties.from_cache(CACHE)

    def test_xid_properties(self) -> None:
        p = self.properties
        self.assertTrue(p.xid_start.contains(ord("A")))
        self.assertTrue(p.xid_continue.contains(ord("7")))
        self.assertTrue(p.xid_continue.contains(0x0301))
        self.assertFalse(p.xid_start.contains(0x0301))

    def test_script_and_category_properties(self) -> None:
        p = self.properties
        self.assertEqual(p.script(ord("A")), "Latin")
        self.assertEqual(p.script(0x05D0), "Hebrew")
        self.assertEqual(p.general_category(0x093E), "Mc")
        self.assertEqual(p.general_category(0x0378), "Cn")
        self.assertEqual(p.combining_class(0x0301), 230)

    def test_bidi_and_security_properties(self) -> None:
        p = self.properties
        self.assertEqual(p.bidi_class(ord("A")), "L")
        self.assertEqual(p.bidi_class(0x05D0), "R")
        self.assertEqual(p.bidi_class(0x0627), "AL")
        self.assertEqual(p.identifier_status.get(ord("A")), "Allowed")
        self.assertIn("Recommended", p.identifier_type(ord("A")))
        self.assertIn("Default_Ignorable", p.identifier_type(0x200C))
        self.assertTrue(p.default_ignorable.contains(0x200C))

    def test_joining_and_indic_properties(self) -> None:
        p = self.properties
        self.assertEqual(p.joining_type(0x0627), "R")
        self.assertEqual(p.joining_type(0x200C), "U")
        self.assertEqual(p.isc(0x093E), "Vowel_Dependent")
        self.assertEqual(p.isc(0x0915), "Consonant")

    def test_script_extensions_are_guarded_without_value_alias_table(self) -> None:
        # ScriptExtensions.txt uses ISO short aliases while Scripts.txt uses
        # long values. Do not allow mixed-representation set comparisons.
        with self.assertRaisesRegex(RuntimeError, "PropertyValueAliases.txt"):
            self.properties.script_extensions_for(0x30FC)

    def test_script_aliases_normalize_both_file_representations(self) -> None:
        alias_rows = "sc ; Hira ; Hiragana\nsc ; Kana ; Katakana\nsc ; Latn ; Latin\n"
        with tempfile.TemporaryDirectory() as temporary:
            aliases = Path(temporary) / "PropertyValueAliases.txt"
            aliases.write_text(alias_rows, encoding="utf-8")
            p = Unicode17Properties.from_cache(CACHE, aliases)
        self.assertEqual(p.script_code(ord("A")), "Latn")
        self.assertEqual(p.script_extensions_for(0x30FC), ("Hira", "Kana"))


if __name__ == "__main__":
    unittest.main()
