import unittest
import numpy as np
from numpy_sensor_lab import (clean_ranges, front_sector_min, obstacle_decision,
                              moving_average, image_roi_mean)

class TestSensorLab(unittest.TestCase):
    def test_invalid_nan(self): self.assertTrue(np.isnan(clean_ranges([np.inf])[0]))
    def test_out_of_range(self): self.assertTrue(np.isnan(clean_ranges([0.0])[0]))
    def test_valid(self): self.assertEqual(clean_ranges([0.5])[0], 0.5)
    def test_front(self): self.assertEqual(front_sector_min([0, 90], [0.4, 0.2]), 0.4)
    def test_wrap(self): self.assertEqual(front_sector_min([355, 90], [0.7, 0.2]), 0.7)
    def test_no_front(self): self.assertIsNone(front_sector_min([90], [1.0]))
    def test_shape(self):
        with self.assertRaises(ValueError): front_sector_min([0, 1], [1])
    def test_stop_invalid(self): self.assertEqual(obstacle_decision(None), 'STOP_SENSOR_INVALID')
    def test_negative_distance_is_invalid(self):
        self.assertEqual(obstacle_decision(-1.0), 'STOP_SENSOR_INVALID')
    def test_bad_thresholds(self):
        with self.assertRaises(ValueError):
            obstacle_decision(1.0, stop_m=2.0, slow_m=1.0)
    def test_stop(self): self.assertEqual(obstacle_decision(0.3), 'STOP_OBSTACLE')
    def test_slow(self): self.assertEqual(obstacle_decision(0.7), 'SLOW')
    def test_go(self): self.assertEqual(obstacle_decision(1.2), 'GO')
    def test_moving(self): np.testing.assert_allclose(moving_average([1, 2, 3]), [1, 1.5, 2])
    def test_moving_bad(self):
        with self.assertRaises(ValueError): moving_average([1], 0)
    def test_roi(self):
        im=np.ones((4, 4, 3), dtype=np.uint8)*20
        np.testing.assert_array_equal(image_roi_mean(im, 1, 1, 3, 3), [20,20,20])
    def test_roi_bounds(self):
        with self.assertRaises(ValueError): image_roi_mean(np.zeros((2,2,3)),0,0,3,2)

if __name__ == '__main__': unittest.main()
