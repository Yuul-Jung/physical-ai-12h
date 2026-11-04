"""외부 장비 없이 실행되는 06차시 회귀 테스트."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
from opencv_vision_lab import (make_scene, extract_roi, color_mask_bgr,
                               contours_from_mask, annotate, run)

class VisionTests(unittest.TestCase):
    def setUp(self):
        self.frame = make_scene()

    def test_shape(self): self.assertEqual(self.frame.shape, (360, 640, 3))
    def test_dtype(self): self.assertEqual(self.frame.dtype, np.uint8)
    def test_invalid_scene(self):
        with self.assertRaises(ValueError): make_scene(10, 10)
    def test_roi_shape(self): self.assertEqual(extract_roi(self.frame, 0, 180, 640, 180).shape, (180, 640, 3))
    def test_roi_copy(self):
        roi = extract_roi(self.frame, 0, 180, 100, 100)
        roi[:] = 0
        self.assertFalse(np.all(self.frame[180:280, :100] == 0))
    def test_roi_bounds(self):
        with self.assertRaises(ValueError): extract_roi(self.frame, 620, 200, 30, 30)
    def test_roi_negative(self):
        with self.assertRaises(ValueError): extract_roi(self.frame, -1, 0, 30, 30)
    def test_mask_dtype(self): self.assertEqual(color_mask_bgr(self.frame).dtype, np.uint8)
    def test_mask_binary(self): self.assertTrue(set(np.unique(color_mask_bgr(self.frame))).issubset({0, 255}))
    def test_mask_has_yellow(self): self.assertGreater(np.count_nonzero(color_mask_bgr(self.frame)), 100)
    def test_invalid_mask(self):
        with self.assertRaises(ValueError): contours_from_mask(self.frame)
    def test_negative_area(self):
        with self.assertRaises(ValueError): contours_from_mask(color_mask_bgr(self.frame), -1)
    def test_contour_detect(self): self.assertGreaterEqual(len(contours_from_mask(color_mask_bgr(self.frame))), 2)
    def test_annotate_shape(self): self.assertEqual(annotate(self.frame, []).shape, self.frame.shape)
    def test_save(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertGreaterEqual(run(d), 2)
            self.assertEqual(len(list(Path(d).glob('*.png'))), 4)

if __name__ == '__main__': unittest.main()
