import sqlite3
import tempfile
import unittest
from pathlib import Path
from staging_backup import backup, verify

class BackupTests(unittest.TestCase):
    def test_roundtrip_and_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            source, target=Path(d)/"source.sqlite",Path(d)/"copy.sqlite"
            with sqlite3.connect(source) as db:
                db.execute("CREATE TABLE evidence (id INTEGER PRIMARY KEY, value TEXT)")
                db.execute("INSERT INTO evidence(value) VALUES ('candidate')")
            manifest=backup(source,target)
            self.assertEqual(manifest["integrity_check"],"ok")
            self.assertTrue(verify(target))
            with sqlite3.connect(target) as db:
                self.assertEqual(db.execute("SELECT value FROM evidence").fetchone()[0],"candidate")
            with self.assertRaises(FileExistsError):
                backup(source,target)
            with target.open("ab") as f:
                f.write(b"tamper")
            with self.assertRaises(ValueError):
                verify(target)

if __name__=="__main__":
    unittest.main()
