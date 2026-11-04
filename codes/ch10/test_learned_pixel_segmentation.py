import unittest
import numpy as np
from learned_pixel_segmentation import PixelClassifier, make_dataset, train_model, instance_masks

class LearnedPixelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.model,cls.acc=train_model()
    def test_shape(self):
        x,y=make_dataset(count=2)
        self.assertEqual(tuple(x.shape),(2,3,48,64))
        self.assertEqual(tuple(y.shape),(2,48,64))
        self.assertEqual(tuple(PixelClassifier()(x).shape),(2,4,48,64))
    def test_validation_accuracy(self):self.assertGreater(self.acc,0.95)
    def test_instance_count(self):
        x,_=make_dataset(seed=290,count=1)
        frame=(x[0].numpy().transpose(1,2,0)*255).astype('uint8')
        mask,objs=instance_masks(self.model,frame)
        self.assertEqual(len(objs),3)
        self.assertEqual(set(np.unique(mask)),{0,1,2,3})
    def test_bad_input(self):
        with self.assertRaises(ValueError):instance_masks(self.model,np.zeros((4,4)))

if __name__=='__main__':unittest.main()
