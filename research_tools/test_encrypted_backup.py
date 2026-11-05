import tempfile
import unittest
from pathlib import Path
from encrypted_backup import encrypt, decrypt

class EncryptionTests(unittest.TestCase):
    def test_roundtrip_wrong_key_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            plain=root/"plain"; plain.write_bytes(b"restricted GRI evidence")
            cipher=root/"backup.enc"; restored=root/"restored"
            key=b"k"*32
            encrypt(plain,cipher,key)
            self.assertNotIn(b"restricted GRI evidence",cipher.read_bytes())
            with self.assertRaises(Exception):
                decrypt(cipher,root/"wrong",b"x"*32)
            decrypt(cipher,restored,key)
            self.assertEqual(restored.read_bytes(),plain.read_bytes())
            with self.assertRaises(ValueError):
                encrypt(plain,cipher,key)
            tampered=root/"tampered.enc"
            tampered.write_bytes(cipher.read_bytes()[:-1]+bytes([cipher.read_bytes()[-1]^1]))
            with self.assertRaises(Exception):
                decrypt(tampered,root/"tampered_out",key)

if __name__=="__main__":
    unittest.main()
