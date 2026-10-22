import unittest
from dataclasses import asdict
from evidence import EvidenceRecorder, verify_export

class EvidenceTests(unittest.TestCase):
    def test_export_and_external_verification(self):
        recorder=EvidenceRecorder()
        recorder.generate_proof("a1","agent",{"amount":"25.00"},"AUTHORIZED_SIMULATION")
        recorder.generate_proof("a2","agent",{"amount":"500.00"},"REJECTED_LIMIT","CAP")
        bundle=recorder.export()
        checkpoint={"head":bundle["head"],"count":bundle["count"]}
        self.assertTrue(verify_export(bundle, trusted_checkpoint=checkpoint))
        bundle["records"][0]["decision_status"]="REJECTED"
        self.assertFalse(verify_export(bundle, trusted_checkpoint=checkpoint))

    def test_truncation_detected_against_checkpoint(self):
        recorder=EvidenceRecorder()
        recorder.generate_proof("a1","agent",{"a":1},"APPROVED")
        first=recorder.export()
        recorder.generate_proof("a2","agent",{"a":2},"REJECTED")
        checkpoint={"head":recorder.head,"count":2}
        self.assertTrue(verify_export(recorder.export(),trusted_checkpoint=checkpoint))
        self.assertFalse(verify_export(first,trusted_checkpoint=checkpoint))

    def test_index_and_head(self):
        recorder=EvidenceRecorder()
        recorder.generate_proof("a1","agent",{"x":1},"APPROVED")
        b=recorder.export()
        b["records"][0]["record_index"]=2
        self.assertFalse(verify_export(b))
        b=recorder.export()
        b["head"]="0"*64
        self.assertFalse(verify_export(b))

if __name__=="__main__": unittest.main()
