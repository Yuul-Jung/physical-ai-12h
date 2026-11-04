import math
import tempfile
import unittest
from pathlib import Path
from sensor_lab import Scan, sample_scan, save_scan_csv, create_demo_frame

class TestSensorLab(unittest.TestCase):
    def test_angle_count(self):
        self.assertEqual(len(sample_scan().ranges_m), 19)
    def test_front_distance(self):
        self.assertAlmostEqual(sample_scan().nearest_front(), 0.6)
    def test_nonfinite_filtered(self):
        self.assertEqual(len(list(sample_scan().points())), 17)
    def test_empty_front(self):
        self.assertIsNone(Scan(90, 10, (1.0, 2.0)).nearest_front(10))
    def test_invalid_step(self):
        with self.assertRaises(ValueError):
            list(Scan(0, 0, (1.0,)).points())
    def test_invalid_range(self):
        self.assertEqual(list(Scan(0, 10, (0.01, 99, math.inf, math.nan)).points()), [])
    def test_cartesian(self):
        a, d, x, y = next(Scan(90, 1, (2.0,)).points())
        self.assertAlmostEqual(x, 0, places=6)
        self.assertAlmostEqual(y, 2, places=6)
    # (추가) 0~360도 라이다 스캔의 경계값 회귀 테스트
    def test_wrapped_front_angles(self):
        self.assertAlmostEqual(Scan(350, 5, (0.4, 0.2, 1.0)).nearest_front(), 0.2)

    def test_nonfinite_start_angle(self):
        with self.assertRaises(ValueError):
            list(Scan(float('nan'), 1, (1.0,)).points())

    def test_nonfinite_front_width(self):
        with self.assertRaises(ValueError):
            sample_scan().nearest_front(float('nan'))

    def test_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p = save_scan_csv(sample_scan(), Path(d) / 'a.csv')
            self.assertEqual(len(p.read_text().splitlines()), 18)
    def test_image(self):
        with tempfile.TemporaryDirectory() as d:
            p, shape = create_demo_frame(Path(d) / 'a.png')
            self.assertTrue(p.exists())
            self.assertEqual(shape, (360, 640, 3))

if __name__ == '__main__':
    unittest.main()
