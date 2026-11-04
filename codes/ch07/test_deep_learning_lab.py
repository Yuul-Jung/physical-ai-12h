import tempfile
import unittest
import torch
from deep_learning_lab import (make_dataset, split_dataset, build_mlp,
                               seed_all, train, evaluate, run)


class TestLab(unittest.TestCase):
    def test_shapes(self):
        x, y = make_dataset()
        self.assertEqual(tuple(x.shape), (160, 1))
        self.assertEqual(tuple(y.shape), (160, 1))

    def test_reproducible(self):
        x1, y1 = make_dataset()
        x2, y2 = make_dataset()
        self.assertTrue(torch.equal(x1, x2))
        self.assertTrue(torch.equal(y1, y2))

    def test_split(self):
        x, y = make_dataset()
        tr, te = split_dataset(x, y)
        self.assertEqual((len(tr[0]), len(te[0])), (128, 32))

    def test_invalid_n(self):
        with self.assertRaises(ValueError):
            make_dataset(8)

    def test_mlp_shape(self):
        self.assertEqual(tuple(build_mlp()(torch.ones(3, 1)).shape), (3, 1))

    def test_loss_decreases(self):
        seed_all()
        x, y = make_dataset()
        model = torch.nn.Linear(1, 1)
        hist = train(model, (x, y), epochs=200)
        self.assertLess(hist[-1], hist[0])

    def test_metric_nonnegative(self):
        x, y = make_dataset()
        result = evaluate(build_mlp(), (x, y))
        self.assertGreaterEqual(result['mse'], 0)
        self.assertGreaterEqual(result['mae'], 0)

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            metrics = run(d)
            from pathlib import Path
            self.assertTrue((Path(d) / 'metrics.json').exists())
            self.assertTrue((Path(d) / 'predictions.csv').exists())
            self.assertLess(metrics['linear']['mae'], 0.12)
            self.assertLess(metrics['mlp']['mae'], 0.12)


if __name__ == '__main__':
    unittest.main()
