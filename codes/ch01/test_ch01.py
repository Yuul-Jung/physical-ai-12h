"""장비 없는 환경에서 수행하는 자동 회귀 테스트."""
import unittest
from safety_gate import SafetyInputs, may_enable_motion
from system_probe import collect_environment


class Chapter01Tests(unittest.TestCase):
    def test_environment_keys(self):
        self.assertIn("python", collect_environment())
        self.assertNotIn("hostname", collect_environment())

    def test_all_safe(self):
        self.assertTrue(may_enable_motion(SafetyInputs(True, True, True, True, True)))

    def test_each_blocker(self):
        for idx in range(5):
            flags = [True] * 5
            flags[idx] = False
            with self.subTest(blocker=idx):
                self.assertFalse(may_enable_motion(SafetyInputs(*flags)))

    def test_no_hardware_side_effect(self):
        self.assertEqual(may_enable_motion(SafetyInputs(False, False, False, False, False)), False)


if __name__ == "__main__":
    unittest.main()
