"""표준 라이브러리만 사용하는 자동 검증."""
import unittest
from math import isclose
from steering_sim import Command, Pose, VehicleSpec, clamp, sanitize, simulate, update

class SteeringTests(unittest.TestCase):
    def setUp(self):
        self.spec = VehicleSpec()

    def test_clamp(self):
        self.assertEqual(clamp(30, -20, 20), 20)
        self.assertEqual(clamp(-30, -20, 20), -20)

    def test_stop_priority(self):
        self.assertEqual(sanitize(Command(18, .3, False), self.spec), Command(0, 0, False))

    def test_limit(self):
        self.assertEqual(sanitize(Command(50, 2, True), self.spec), Command(20, .35, True))

    def test_straight(self):
        p = update(Pose(), Command(0, .2, True), .1, self.spec)
        self.assertGreater(p.x_m, 0)
        self.assertAlmostEqual(p.y_m, 0)

    def test_turn(self):
        p = update(Pose(speed_mps=.2), Command(15, .2, True), .1, self.spec)
        self.assertGreater(p.heading_rad, 0)
        self.assertGreater(p.y_m, 0)

    def test_acceleration(self):
        p = update(Pose(), Command(0, .35, True), .1, self.spec)
        self.assertAlmostEqual(p.speed_mps, .04)

    def test_invalid_dt(self):
        with self.assertRaises(ValueError):
            update(Pose(), Command(0, 0, False), 0, self.spec)

    def test_invalid_wheelbase(self):
        with self.assertRaises(ValueError):
            update(Pose(), Command(0, 0, False), .1, VehicleSpec(wheelbase_m=0))

    def test_sequence(self):
        poses = simulate([Command(0, .2, True)] * 5)
        self.assertEqual(len(poses), 6)
        self.assertTrue(isclose(poses[0].x_m, 0))

    # (추가) 비정상 수치가 유효한 구동 명령으로 바뀌는 안전 결함 재발 방지
    def test_nan_steering_fails_closed(self):
        self.assertEqual(sanitize(Command(float('nan'), 0.2, True), self.spec), Command(0, 0, False))

    def test_infinite_speed_fails_closed(self):
        self.assertEqual(sanitize(Command(0, float('inf'), True), self.spec), Command(0, 0, False))

    def test_nan_dt_is_invalid(self):
        with self.assertRaises(ValueError):
            update(Pose(), Command(0, 0, False), float('nan'), self.spec)

    def test_stop_is_not_instant(self):
        p = update(Pose(speed_mps=.2), Command(0, 0, False), .1, self.spec)
        self.assertGreater(p.speed_mps, 0)  # 모의 감속 한계; 실제 긴급정지 성능 아님

if __name__ == '__main__':
    unittest.main(verbosity=2)
