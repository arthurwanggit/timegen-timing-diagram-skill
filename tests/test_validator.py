import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.validate_timegen_xml import EXPECTED_LENGTH, validate


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def validate_xml(self, signals, extra_children=None):
        root = ET.Element("waveform")
        for name, value in signals:
            signal = ET.SubElement(root, "signal", {"name": name})
            ET.SubElement(signal, "data", {"value": value})
            if extra_children:
                for tag, attrs in extra_children:
                    ET.SubElement(signal, tag, attrs)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "waveform.xml"
            ET.ElementTree(root).write(path, encoding="utf-8")
            return validate(path)

    def test_minimal_template_is_valid(self):
        self.assertEqual(validate(ROOT / "templates" / "minimal.xml"), [])

    def test_verified_example_is_valid(self):
        self.assertEqual(validate(ROOT / "examples" / "example.xml"), [])

    def test_rejects_non_600_length(self):
        errors = self.validate_xml([("signal", "0" * (EXPECTED_LENGTH - 1))])
        self.assertTrue(any("data length must be 600" in error for error in errors))

    def test_rejects_empty_data(self):
        errors = self.validate_xml([("signal", "")])
        self.assertTrue(any("must be nonempty" in error for error in errors))

    def test_rejects_duplicate_signal_names(self):
        errors = self.validate_xml(
            [("ready", "0" * EXPECTED_LENGTH), ("ready", "1" * EXPECTED_LENGTH)]
        )
        self.assertIn("duplicate signal name: ready", errors)

    def test_rejects_unverified_data_characters(self):
        for character in "256789":
            with self.subTest(character=character):
                errors = self.validate_xml(
                    [("signal", character * EXPECTED_LENGTH)]
                )
                self.assertTrue(
                    any("invalid data characters" in error for error in errors)
                )

    def test_allows_text_with_valid_cycle(self):
        errors = self.validate_xml(
            [("signal", "0" * EXPECTED_LENGTH)],
            extra_children=[("text", {"cycle": "4", "value": "label"})],
        )
        self.assertEqual(errors, [])

    def test_rejects_text_cycle_out_of_range(self):
        errors = self.validate_xml(
            [("signal", "0" * EXPECTED_LENGTH)],
            extra_children=[("text", {"cycle": str(EXPECTED_LENGTH), "value": "late"})],
        )
        self.assertTrue(any("exceeds data length" in e for e in errors))

    def test_rejects_text_without_value(self):
        errors = self.validate_xml(
            [("signal", "0" * EXPECTED_LENGTH)],
            extra_children=[("text", {"cycle": "0"})],
        )
        self.assertTrue(any("must have exactly cycle and value" in e for e in errors))

    def test_rejects_text_with_empty_value(self):
        errors = self.validate_xml(
            [("signal", "0" * EXPECTED_LENGTH)],
            extra_children=[("text", {"cycle": "0", "value": ""})],
        )
        self.assertTrue(any("value must be nonempty" in e for e in errors))

    def test_rejects_text_with_negative_cycle(self):
        errors = self.validate_xml(
            [("signal", "0" * EXPECTED_LENGTH)],
            extra_children=[("text", {"cycle": "-1", "value": "bad"})],
        )
        self.assertTrue(any("nonnegative" in e for e in errors))

    def test_allows_multiple_texts_on_one_signal(self):
        errors = self.validate_xml(
            [("signal", "0" * EXPECTED_LENGTH)],
            extra_children=[
                ("text", {"cycle": "0", "value": "first"}),
                ("text", {"cycle": "4", "value": "second"}),
            ],
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
