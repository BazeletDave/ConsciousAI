import unittest
from integrity import *

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.policy=AssessmentPolicy("exam-1",AIPolicy.PERMITTED,True,True,"v1",True)
        self.event=ExamTelemetryEvent(True,True,0,False,0,0.95)
    def test_no_activity(self):
        self.assertEqual(evaluate_academic_integrity(self.event,self.policy).level,FlagLevel.NO_INTERVENTION)
    def test_authorized_large_paste(self):
        e=ExamTelemetryEvent(True,True,0,True,3000,0.99)
        self.assertEqual(evaluate_academic_integrity(e,self.policy).level,FlagLevel.NO_INTERVENTION)
    def test_authorized_many_switches(self):
        e=ExamTelemetryEvent(True,False,20,False,0,0.99)
        self.assertEqual(evaluate_academic_integrity(e,self.policy).level,FlagLevel.NO_INTERVENTION)
    def test_restricted_paste_is_review_only(self):
        p=AssessmentPolicy("exam-1",AIPolicy.PROHIBITED,False,False,"v1",True)
        e=ExamTelemetryEvent(True,True,0,True,200,0.95)
        d=evaluate_academic_integrity(e,p)
        self.assertEqual(d.level,FlagLevel.LOG_FOR_REVIEW)
        self.assertFalse(d.misconduct_determined)
        self.assertFalse(d.adverse_action_authorized)
    def test_restricted_switch_is_review_only(self):
        p=AssessmentPolicy("exam-1",AIPolicy.RESTRICTED,False,False,"v1",True)
        e=ExamTelemetryEvent(True,False,5,False,0,0.95)
        self.assertEqual(evaluate_academic_integrity(e,p).level,FlagLevel.LOG_FOR_REVIEW)
    def test_unspecified_policy(self):
        self.assertEqual(evaluate_academic_integrity(self.event,AssessmentPolicy("exam-1",student_notice_provided=True)).level,FlagLevel.NO_INTERVENTION)
        e=ExamTelemetryEvent(True,True,1,False,0,0.95)
        self.assertEqual(evaluate_academic_integrity(e,AssessmentPolicy("exam-1",student_notice_provided=True)).level,FlagLevel.INSUFFICIENT_EVIDENCE)
    def test_notice_missing(self):
        self.assertEqual(evaluate_academic_integrity(self.event,AssessmentPolicy("exam-1")).level,FlagLevel.INSUFFICIENT_EVIDENCE)
    def test_inactive(self):
        e=ExamTelemetryEvent(False,True,0,False,0,0.95)
        self.assertEqual(evaluate_academic_integrity(e,self.policy).level,FlagLevel.NO_INTERVENTION)
    def test_low_confidence(self):
        e=ExamTelemetryEvent(True,False,4,False,0,0.2)
        self.assertEqual(evaluate_academic_integrity(e,self.policy).level,FlagLevel.INSUFFICIENT_EVIDENCE)
    def test_bad_counts(self):
        with self.assertRaises(ValueError):
            evaluate_academic_integrity(ExamTelemetryEvent(True,True,-1,False,0,0.9),self.policy)
    def test_bad_confidence(self):
        with self.assertRaises(ValueError):
            evaluate_academic_integrity(ExamTelemetryEvent(True,True,0,False,0,1.5),self.policy)

if __name__=="__main__": unittest.main()
