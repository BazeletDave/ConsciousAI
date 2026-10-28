from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from curriculum_experiment_bridge import snapshot,REPORT,FILES


class ExperimentBridgeTests(unittest.TestCase):
    def test_hash_checks_and_no_promotion(self):
        with TemporaryDirectory() as directory:
            repo=Path(directory);root=repo/'service';(root/'learning_ledger').mkdir(parents=True)
            folder=repo/REPORT;folder.mkdir(parents=True)
            hashes={}
            for name in FILES:
                (folder/name).write_text('fixture');hashes[name]=sha256(b'fixture').hexdigest()
            data={'artifact_hashes':hashes,'model_promoted':False,'status':'synthetic_fixture'}
            (root/'learning_ledger/putting_experiment_summary.json').write_text(json.dumps(data))
            self.assertEqual(snapshot(root,repo)['status'],'synthetic_fixture')
            (folder/'results.json').write_text('tampered')
            with self.assertRaises(ValueError):snapshot(root,repo)


if __name__=='__main__':unittest.main()
