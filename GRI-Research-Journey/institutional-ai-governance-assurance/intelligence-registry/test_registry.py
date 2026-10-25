import unittest
from pathlib import Path
from registry import load, validate

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.example = dict(load(Path(__file__).with_name("signals.json"))[0])

    def test_seed_records_valid(self):
        self.assertGreaterEqual(len(load(Path(__file__).with_name("signals.json"))), 4)

    def test_missing_field_rejected(self):
        self.example.pop("source_url")
        with self.assertRaises(ValueError):
            validate(self.example)

    def test_non_https_rejected(self):
        self.example["source_url"] = "http://example.com"
        with self.assertRaises(ValueError):
            validate(self.example)

    def test_unverified_cannot_be_confirmed(self):
        self.example["verification"] = "UNVERIFIED"
        self.example["review_status"] = "INDEPENDENTLY_CORROBORATED"
        with self.assertRaises(ValueError):
            validate(self.example)

if __name__ == "__main__":
    unittest.main()
