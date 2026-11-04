import unittest
from robot_python_lab import clamp, decide, run_scenario

class RobotPythonTests(unittest.TestCase):
    def test_clamp(self): self.assertEqual(clamp(50, 0, 30), 30)
    def test_clamp_low(self): self.assertEqual(clamp(-5, 0, 30), 0)
    def test_clamp_bad_range(self):
        with self.assertRaises(ValueError): clamp(1, 5, 0)
    def test_clamp_nan(self):
        with self.assertRaises(ValueError): clamp(float('nan'), 0, 1)
    def test_stop_near(self): self.assertEqual(decide(0.2, 'left').speed_pct, 0)
    def test_stop_none(self): self.assertEqual(decide(None, 'left').speed_pct, 0)
    def test_stop_negative(self): self.assertEqual(decide(-1, 'left').speed_pct, 0)
    def test_stop_bad_direction(self): self.assertEqual(decide(2, 'up').speed_pct, 0)
    def test_left(self): self.assertEqual(decide(2, 'left').steering_deg, -15)
    def test_right(self): self.assertEqual(decide(2, 'right').steering_deg, 15)
    def test_slow(self): self.assertEqual(decide(.8, 'straight').speed_pct, 20)
    def test_loop(self): self.assertEqual(len(run_scenario([1,2,None], 'left')), 3)

if __name__ == '__main__': unittest.main()
