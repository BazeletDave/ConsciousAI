"""Synthetic-only lifecycle tests. Run: python -m unittest test_synthetic_ledger_lifecycle -v"""
import json
import tempfile
import unittest
from pathlib import Path
from synthetic_ledger_lifecycle import read_ledger, write_ledger, run

FIXTURE = Path(__file__).with_name("synthetic_ledger.json")

class LedgerLifecycleTests(unittest.TestCase):
    def test_json_csv_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            records = read_ledger(FIXTURE)
            csv_path = Path(d) / "out.csv"
            write_ledger(csv_path, records)
            self.assertEqual(read_ledger(csv_path), records)
    def test_export(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "out.json"
            result = run(["export", str(FIXTURE), str(out)])
            self.assertEqual(result["exported_records"], 1)
            self.assertEqual(len(read_ledger(out)), 1)
    def test_filtered_withdrawal_copy(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "filtered.json"
            result = run(["delete", str(FIXTURE), str(out), "--record-id", "synthetic-1"])
            self.assertEqual(result["exported_records"], 0)
            self.assertEqual(read_ledger(out), [])
            self.assertEqual(len(read_ledger(FIXTURE)), 1)
    def test_reject_real_data(self):
        with tempfile.TemporaryDirectory() as d:
            record = dict(read_ledger(FIXTURE)[0], synthetic=False)
            path = Path(d) / "real.json"
            path.write_text(json.dumps([record]))
            with self.assertRaises(ValueError):
                read_ledger(path)
    def test_reject_duplicate_id(self):
        with tempfile.TemporaryDirectory() as d:
            record = read_ledger(FIXTURE)[0]
            path = Path(d) / "duplicate.json"
            path.write_text(json.dumps([record, record]))
            with self.assertRaises(ValueError):
                read_ledger(path)
    def test_reject_overwrite(self):
        with self.assertRaises(FileExistsError):
            write_ledger(FIXTURE, [])
    def test_reject_unknown_field(self):
        with tempfile.TemporaryDirectory() as d:
            record = dict(read_ledger(FIXTURE)[0], passenger_name="private")
            path = Path(d) / "pii.json"
            path.write_text(json.dumps([record]))
            with self.assertRaises(ValueError):
                read_ledger(path)

if __name__ == "__main__":
    unittest.main()
