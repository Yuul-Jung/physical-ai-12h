import unittest
import numpy as np
from hybrid_learned_detector import PatchClassifier, make_training_set, train_model, detect_hybrid
from object_detection_lab import make_scene

class HybridDetectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.model, cls.acc = train_model(epochs=120)
    def test_dataset(self):
        x,y=make_training_set()
        self.assertEqual(tuple(x.shape),(320,3))
        self.assertEqual(len(y),320)
    def test_shape(self):
        self.assertEqual(tuple(PatchClassifier()(make_training_set()[0][:2]).shape),(2,4))
    def test_independent_synthetic_data(self):
        self.assertGreater(self.acc, 0.95)
    def test_hybrid_boxes(self):
        frame, truth=make_scene(); boxes=detect_hybrid(frame,self.model)
        self.assertEqual([b['label'] for b in boxes], ['red','green','blue'])
        self.assertEqual([b['box'] for b in boxes], [b['box'] for b in truth])
    def test_reject_malformed(self):
        with self.assertRaises(ValueError):detect_hybrid(np.zeros((3,3)),self.model)

if __name__=='__main__':unittest.main()
