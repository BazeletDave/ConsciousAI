"""Synthetic Tiger Legacy bridge and HTTP route integration tests."""
import hashlib
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

import server
from tiger_legacy_bridge import MANIFEST, SNAPSHOT, snapshot

class TigerLegacyBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        source = Path(server.ROOT)
        for name in (MANIFEST, SNAPSHOT):
            (self.root / name).write_bytes((source / name).read_bytes())

    def tearDown(self):
        self.temp.cleanup()

    def test_snapshot_integrity_and_no_operational_authority(self):
        result = snapshot(self.root)
        self.assertEqual(result["fixture_checks_passed"], 4)
        self.assertEqual(result["production_security"], "unmeasured")
        self.assertFalse(result["model_promoted"])
        self.assertEqual(result["operational_actions_authorized"], 0)
        self.assertNotIn("fixture_checks", result)

    def test_snapshot_tampering_fails_closed(self):
        p = self.root / SNAPSHOT
        p.write_bytes(p.read_bytes().replace(b'"fixture_checks_passed": 4', b'"fixture_checks_passed": 9'))
        with self.assertRaises(ValueError):
            snapshot(self.root)

    def test_missing_snapshot_fails_closed(self):
        (self.root / SNAPSHOT).unlink()
        with self.assertRaises(OSError):
            snapshot(self.root)

    def test_swapped_report_and_rehashed_internal_digest_fails_pinned_manifest(self):
        p = self.root / SNAPSHOT
        data = json.loads(p.read_text())
        data["fixture_checks_passed"] = 99
        payload = {k: v for k, v in data.items() if k != "content_sha256"}
        data["content_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        p.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")
        with self.assertRaises(ValueError):
            snapshot(self.root)

    def test_read_only(self):
        before = [(self.root / n).read_bytes() for n in (MANIFEST, SNAPSHOT)]
        snapshot(self.root)
        self.assertEqual(before, [(self.root / n).read_bytes() for n in (MANIFEST, SNAPSHOT)])

    def test_http_success_and_fail_closed(self):
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{httpd.server_port}/institutional/tiger-legacy"
        try:
            with patch.object(server, "ROOT", self.root):
                with urlopen(url, timeout=3) as res:
                    self.assertEqual(res.status, 200)
                    self.assertEqual(json.load(res)["classification"], "synthetic_research_only")
                (self.root / SNAPSHOT).unlink()
                with self.assertRaises(HTTPError) as exc:
                    urlopen(url, timeout=3)
                self.assertEqual(exc.exception.code, 503)
                self.assertFalse(json.load(exc.exception)["model_promoted"])
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=3)

if __name__ == "__main__":
    unittest.main()
