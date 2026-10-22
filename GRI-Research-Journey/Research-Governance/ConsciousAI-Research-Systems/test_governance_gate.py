import unittest
from governance_gate import authorize
class GovernanceGateTests(unittest.TestCase):
    def test_approved_public_read(self):
        self.assertTrue(authorize("read_approved_public_source",source_approved=True)["allowed"])
    def test_unknown_source_denied(self):
        self.assertFalse(authorize("read_approved_public_source")["allowed"])
    def test_training_requires_external_approval(self):
        self.assertFalse(authorize("train_model",human_approval=True)["allowed"])
    def test_policy_self_modification_denied(self):
        self.assertFalse(authorize("modify_policy",human_approval=True)["allowed"])
    def test_no_sensitive_internal_processing(self):
        self.assertFalse(authorize("internal_draft",contains_personal_data=True)["allowed"])
    def test_no_publication_without_workflow(self):
        self.assertFalse(authorize("internal_draft",externally_visible=True)["allowed"])
    def test_disallowed_actions(self):
        for a in ("bypass_access_controls","intrusive_scan_without_authorization","self_authorize"):
            self.assertFalse(authorize(a)["allowed"])
    def test_unknown_actions_fail_closed(self):
        self.assertFalse(authorize("invent_new_permission")["allowed"])
if __name__=="__main__": unittest.main()
