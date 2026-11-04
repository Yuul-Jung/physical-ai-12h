import unittest
import numpy as np
from traffic_scene_lab import make_scene, recognize, decide, Observation
class TestTraffic(unittest.TestCase):
    def test_signal(self):
        for signal in ('red','yellow','green'):
            self.assertEqual(recognize(make_scene(signal)).signal, signal)
    def test_arrow(self):
        for arrow in ('left','right'):
            self.assertEqual(recognize(make_scene('green',arrow)).arrow, arrow)
    def test_parking(self):
        self.assertTrue(recognize(make_scene(parking=True)).parking)
        self.assertFalse(recognize(make_scene(parking=False)).parking)
    def test_fail_safe(self):
        obs=recognize(make_scene('green','left'))
        for d in (None, float('nan'), -1):
            self.assertEqual(decide(obs,d),'STOP_SENSOR_ERROR')
        self.assertEqual(decide(obs,.3),'STOP_OBSTACLE')
    def test_red_yellow_stop(self):
        for s in ('red','yellow'):
            self.assertEqual(decide(recognize(make_scene(s)),2),'STOP_SIGNAL_UNCERTAIN')
    def test_green_plan(self):
        self.assertEqual(decide(recognize(make_scene('green','right')),2),'PLAN_RIGHT_PARKING_VISIBLE')
    # (추가) 임의 문자열이 유효한 주행 계획으로 변환되는 결함 회귀 테스트
    def test_unknown_signal_fails_closed(self):
        self.assertEqual(decide(Observation('blue','left',False,1.0), 2), 'STOP_SIGNAL_UNCERTAIN')
    def test_unknown_arrow_fails_closed(self):
        self.assertEqual(decide(Observation('green','spin',False,1.0), 2), 'STOP_ARROW_UNCERTAIN')
    def test_nan_confidence_fails_closed(self):
        self.assertEqual(decide(Observation('green','left',False,float('nan')), 2), 'STOP_SIGNAL_UNCERTAIN')
    def test_bad_image(self):
        self.assertEqual(recognize(np.zeros((10,10,3),dtype=np.uint8)).signal,'unknown')
if __name__=='__main__': unittest.main()
