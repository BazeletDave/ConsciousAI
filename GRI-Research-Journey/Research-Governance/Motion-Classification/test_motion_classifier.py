import unittest
import numpy as np
from motion_classifier import generate_synthetic_data,extract_features,PhoneHandlingClassifier,MotionWindow

class MotionTests(unittest.TestCase):
    def test_deterministic_generator(self):
        a,y,_=generate_synthetic_data(2,7)
        b,z,_=generate_synthetic_data(2,7)
        self.assertTrue(np.array_equal(y,z))
        self.assertTrue(np.array_equal(a[0].accel_x,b[0].accel_x))
    def test_feature_shape_and_finite(self):
        w,_,_=generate_synthetic_data(1)
        f=extract_features(w[0])
        self.assertEqual(f.shape,(11,))
        self.assertTrue(np.isfinite(f).all())
    def test_reject_bad_window(self):
        w,_,_=generate_synthetic_data(1)
        bad=MotionWindow(np.zeros(4),w[0].accel_y,w[0].accel_z,w[0].gyro_x,w[0].gyro_y,w[0].gyro_z)
        with self.assertRaises(ValueError): extract_features(bad)
    def test_train_and_predict(self):
        w,y,_=generate_synthetic_data(12)
        clf=PhoneHandlingClassifier()
        with self.assertRaises(RuntimeError): clf.classify_event(w[0])
        clf.train(w,y)
        label,p=clf.classify_event(w[0])
        self.assertIsInstance(label,str)
        self.assertTrue(0<=p<=1)
if __name__=="__main__": unittest.main()
