import unittest
import numpy as np
from instance_segmentation_lab import make_scene, segment_instances, mask_iou, evaluate

class SegmentationTests(unittest.TestCase):
    def setUp(self):
        self.img, self.gt = make_scene()
        self.pred = segment_instances(self.img)

    def test_shape(self): self.assertEqual(self.img.shape, (320, 480, 3))
    def test_truth_count(self): self.assertEqual(len(self.gt), 4)
    def test_count(self): self.assertEqual(len(self.pred), 4)
    def test_red_separated(self): self.assertEqual(sum(x['label']=='red' for x in self.pred), 2)
    def test_green(self): self.assertEqual(sum(x['label']=='green' for x in self.pred), 1)
    def test_blue(self): self.assertEqual(sum(x['label']=='blue' for x in self.pred), 1)
    def test_mask_binary(self): self.assertTrue(all(set(np.unique(x['mask'])) <= {0,1} for x in self.pred))
    def test_mask_size(self): self.assertTrue(all(x['mask'].shape == self.img.shape[:2] for x in self.pred))
    def test_area(self): self.assertTrue(all(x['area'] > 100 for x in self.pred))
    def test_perfect_iou(self): self.assertEqual(mask_iou(self.gt[0]['mask'], self.gt[0]['mask']), 1)
    def test_empty_iou(self): self.assertEqual(mask_iou(np.zeros((3,3)), np.zeros((3,3))), 0)
    def test_bad_shape(self):
        with self.assertRaises(ValueError): mask_iou(np.zeros((2,2)), np.zeros((3,3)))
    def test_bad_image(self):
        with self.assertRaises(ValueError): segment_instances(np.zeros((3,3)))
    def test_bad_area(self):
        with self.assertRaises(ValueError): segment_instances(self.img, 0)
    def test_precision(self): self.assertEqual(evaluate(self.pred, self.gt)['precision'], 1)
    def test_recall(self): self.assertEqual(evaluate(self.pred, self.gt)['recall'], 1)
    def test_no_detection(self): self.assertEqual(evaluate([], self.gt)['fn'], 4)
    def test_no_truth(self): self.assertEqual(evaluate(self.pred, [])['fp'], 4)

if __name__ == '__main__': unittest.main()
