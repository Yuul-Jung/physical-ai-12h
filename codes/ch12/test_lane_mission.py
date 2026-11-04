import unittest
import numpy as np
from lane_mission import scene,detect,decide,W,H
class TestLane(unittest.TestCase):
    def test_dimensions(self): self.assertEqual(scene().shape,(H,W,3))
    def test_nominal(self):
        c,s,_=detect(scene());self.assertEqual(s,'OK');self.assertAlmostEqual(c,320,delta=15)
    def test_offset(self):
        c,s,_=detect(scene(35));self.assertEqual(s,'OK');self.assertGreater(c,330)
    def test_missing(self):self.assertEqual(detect(scene(missing=True))[1],'NO_LANES')
    def test_invalid(self):self.assertEqual(detect(np.zeros((10,10,3),np.uint8))[1],'INVALID_FRAME')
    def test_straight(self):self.assertEqual(decide(320,'OK',1.5),'PLAN_STRAIGHT')
    def test_left(self):self.assertEqual(decide(280,'OK',1.5),'PLAN_LEFT')
    def test_right(self):self.assertEqual(decide(350,'OK',1.5),'PLAN_RIGHT')
    def test_obstacle(self):self.assertEqual(decide(320,'OK',0.3),'STOP_OBSTACLE')
    def test_missing_sensor(self):self.assertEqual(decide(320,'OK',None),'STOP_SENSOR')
    def test_red(self):self.assertEqual(decide(320,'OK',1.5,False),'STOP_SIGNAL')
    def test_vision(self):self.assertEqual(decide(None,'NO_LANES',1.5),'STOP_VISION')
    def test_negative_distance_sensor_error(self):
        self.assertEqual(decide(320, 'OK', -1), 'STOP_SENSOR')
    def test_unconfirmed_signal_stops(self):
        self.assertEqual(decide(320, 'OK', 1.5, None), 'STOP_SIGNAL')
    def test_nan(self):self.assertEqual(decide(320,'OK',float('nan')),'STOP_SENSOR')
if __name__=='__main__':unittest.main()
