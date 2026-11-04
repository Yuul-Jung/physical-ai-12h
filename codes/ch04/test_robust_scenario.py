import tempfile
import unittest
from pathlib import Path
from robust_scenario import parse_distance, make_log, save_csv


class RobustScenarioTest(unittest.TestCase):
    def test_convert(self): self.assertEqual(parse_distance('0.8'), 0.8)
    def test_missing(self): self.assertIsNone(parse_distance('bad'))
    def test_negative(self): self.assertIsNone(parse_distance('-1.0'))
    def test_nan(self): self.assertIsNone(parse_distance('nan'))
    def test_inf(self): self.assertIsNone(parse_distance('inf'))
    def test_fail_stop(self):
        log = make_log(['bad', 'nan', '-1', '0.2'])
        self.assertEqual([r['speed_pct'] for r in log], [0, 0, 0, 0])
    def test_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = save_csv(make_log(['1.0', None]), Path(tmp)/'out.csv')
            self.assertEqual(len(p.read_text(encoding='utf-8-sig').splitlines()), 3)

if __name__ == '__main__':
    unittest.main()
