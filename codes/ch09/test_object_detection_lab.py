import unittest
import numpy as np
from object_detection_lab import make_scene, detect_colors, iou, evaluate, annotate

class TestDetector(unittest.TestCase):
    def setUp(self):
        self.image, self.truth = make_scene()
    def test_shape(self): self.assertEqual(self.image.shape, (320, 480, 3))
    def test_ground_truth(self): self.assertEqual(len(self.truth), 3)
    def test_detection_count(self): self.assertEqual(len(detect_colors(self.image)), 3)
    def test_labels(self): self.assertEqual([x['label'] for x in detect_colors(self.image)], ['red', 'green', 'blue'])
    def test_exact_iou(self): self.assertEqual(iou([0,0,10,10], [0,0,10,10]), 1)
    def test_disjoint_iou(self): self.assertEqual(iou([0,0,10,10], [20,20,30,30]), 0)
    def test_zero_iou(self): self.assertEqual(iou([0,0,0,0], [0,0,0,0]), 0)
    def test_metrics(self): self.assertEqual(evaluate(detect_colors(self.image), self.truth)['TP'], 3)
    def test_false_positive(self): self.assertEqual(evaluate([{'label':'red','box':[0,0,10,10]}], self.truth)['FP'], 1)
    def test_false_negative(self): self.assertEqual(evaluate([], self.truth)['FN'], 3)
    def test_annotation(self): self.assertEqual(annotate(self.image, detect_colors(self.image)).shape, self.image.shape)
    def test_bad_input(self):
        with self.assertRaises(ValueError): detect_colors(np.zeros((3,3)))
    def test_min_area(self): self.assertEqual(len(detect_colors(self.image, 100000)), 0)

if __name__ == '__main__': unittest.main()
