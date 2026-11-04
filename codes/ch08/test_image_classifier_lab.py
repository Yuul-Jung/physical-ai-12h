import unittest
import torch
from image_classifier_lab import LABELS, make_image, dataset, TinyCNN, split_indices, confusion_matrix, train_demo
from tempfile import TemporaryDirectory
from pathlib import Path

class TestImageClassification(unittest.TestCase):
    def test_classes(self): self.assertEqual(len(LABELS),3)
    def test_image_size(self): self.assertEqual(make_image(0,1).size,(32,32))
    def test_invalid_label(self):
        with self.assertRaises(ValueError): make_image(9,1)
    def test_dataset_shape(self):
        x,y=dataset(5);self.assertEqual(tuple(x.shape),(15,3,32,32));self.assertEqual(tuple(y.shape),(15,))
    def test_value_range(self):
        x,_=dataset(2);self.assertGreaterEqual(x.min().item(),0);self.assertLessEqual(x.max().item(),1)
    def test_model_shape(self): self.assertEqual(tuple(TinyCNN()(torch.zeros(2,3,32,32)).shape),(2,3))
    def test_split_disjoint(self):
        _,y=dataset(10);tr,te=split_indices(y);self.assertEqual(len(tr),24);self.assertEqual(len(te),6);self.assertFalse(set(tr)&set(te))
    def test_split_stratified(self):
        _,y=dataset(10);tr,te=split_indices(y);self.assertEqual([int((y[te]==i).sum()) for i in range(3)],[2,2,2])
    def test_confusion(self): self.assertEqual(confusion_matrix([0,1,2],[0,2,2]).tolist(),[[1,0,0],[0,0,1],[0,0,1]])
    def test_deterministic_images(self): self.assertEqual(make_image(0,1).tobytes(),make_image(0,1).tobytes())
    def test_train_outputs(self):
        with TemporaryDirectory() as d:
            r=train_demo(d,epochs=3,n_per_class=10)
            self.assertEqual(r['test_count'],6)
            self.assertTrue((Path(d)/'metrics.json').exists())
            self.assertTrue((Path(d)/'tinycnn_weights.pt').exists())
            self.assertTrue((Path(d)/'sample_circle.png').exists())
if __name__=='__main__': unittest.main()
