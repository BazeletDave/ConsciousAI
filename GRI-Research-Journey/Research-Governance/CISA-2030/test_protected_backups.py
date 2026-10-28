import hashlib
import tempfile
import unittest
from pathlib import Path
from evidence_ledger import EvidenceLedger
from protected_backups import encrypted_backup, restore_encrypted

KEYS={"collector":("collector",b"a"*32),"reviewer":("reviewer",b"b"*32),"auditor":("auditor",b"c"*32)}
ENC=b"e"*32
SIGN=b"s"*32
ART=b"non-sensitive lab evidence"

class ProtectedBackupTests(unittest.TestCase):
    def setUp(self):
        try:
            import cryptography
        except ImportError:
            self.skipTest("cryptography optional dependency unavailable")
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.ledger=EvidenceLedger(self.root/"live.db",KEYS)
        self.ledger.collect("collector",{"record_id":"r1","scenario_type":"real","consent_or_authority":"lab","source_sha256":hashlib.sha256(ART).hexdigest()},ART)
    def tearDown(self):
        if hasattr(self,"ledger"): self.ledger.close()
        if hasattr(self,"tmp"): self.tmp.cleanup()
    def test_encrypted_restore(self):
        manifest=encrypted_backup(self.ledger,self.root/"backup.enc",ENC,SIGN)
        self.assertNotIn(b"SQLite format 3", (self.root/"backup.enc").read_bytes())
        restored=restore_encrypted(self.root/"backup.enc",self.root/"restore.db",ENC,SIGN,KEYS)
        self.assertEqual(restored["head_sha256"],manifest["ledger_head"])
    def test_wrong_encryption_key(self):
        encrypted_backup(self.ledger,self.root/"backup.enc",ENC,SIGN)
        with self.assertRaises(Exception): restore_encrypted(self.root/"backup.enc",self.root/"restore.db",b"x"*32,SIGN,KEYS)
    def test_wrong_signing_key(self):
        encrypted_backup(self.ledger,self.root/"backup.enc",ENC,SIGN)
        with self.assertRaises(ValueError): restore_encrypted(self.root/"backup.enc",self.root/"restore.db",ENC,b"x"*32,KEYS)
    def test_corruption(self):
        encrypted_backup(self.ledger,self.root/"backup.enc",ENC,SIGN)
        path=self.root/"backup.enc"
        path.write_bytes(path.read_bytes()+b"tampered")
        with self.assertRaises(ValueError): restore_encrypted(path,self.root/"restore.db",ENC,SIGN,KEYS)
    def test_no_overwrite(self):
        encrypted_backup(self.ledger,self.root/"backup.enc",ENC,SIGN)
        with self.assertRaises(FileExistsError): encrypted_backup(self.ledger,self.root/"backup.enc",ENC,SIGN)
    def test_distinct_keys(self):
        with self.assertRaises(ValueError): encrypted_backup(self.ledger,self.root/"backup.enc",ENC,ENC)

if __name__=="__main__":
    unittest.main()
