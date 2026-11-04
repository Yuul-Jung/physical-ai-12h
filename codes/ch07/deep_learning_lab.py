"""CH07: deterministic CPU-only linear regression and neural network practice."""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
from torch import nn


def seed_all(seed=7):
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_dataset(n=160, seed=7):
    """Synthetic target: stop distance (m) = 0.4 + 0.08 * speed (m/s)."""
    if n < 16:
        raise ValueError('n must be >= 16')
    rng = np.random.default_rng(seed)
    speed = rng.uniform(0.0, 8.0, size=(n, 1)).astype(np.float32)
    noise = rng.normal(0, 0.025, size=(n, 1)).astype(np.float32)
    target = 0.4 + 0.08 * speed + noise
    return torch.from_numpy(speed), torch.from_numpy(target)


def split_dataset(x, y, train_ratio=0.8):
    """Preserve a reproducible shuffled hold-out; no overlap."""
    g = torch.Generator().manual_seed(11)
    idx = torch.randperm(len(x), generator=g)
    cut = int(len(x) * train_ratio)
    return (x[idx[:cut]], y[idx[:cut]]), (x[idx[cut:]], y[idx[cut:]])


def train(model, train_set, epochs=300, lr=0.03):
    x, y = train_set
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    for _ in range(epochs):
        model.train()
        pred = model(x)
        loss = loss_fn(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        history.append(float(loss.detach()))
    return history


def evaluate(model, data):
    model.eval()
    with torch.no_grad():
        x, y = data
        pred = model(x)
        mse = torch.mean((pred - y) ** 2).item()
        mae = torch.mean(torch.abs(pred - y)).item()
    return {'mse': round(mse, 6), 'mae': round(mae, 6)}


def build_mlp():
    return nn.Sequential(nn.Linear(1, 8), nn.ReLU(), nn.Linear(8, 1))


def run(outdir='outputs'):
    seed_all()
    x, y = make_dataset()
    train_set, test_set = split_dataset(x, y)
    linear = nn.Linear(1, 1)
    linear_history = train(linear, train_set, epochs=400, lr=0.025)
    seed_all()
    mlp = build_mlp()
    mlp_history = train(mlp, train_set, epochs=400, lr=0.025)
    metrics = {
        'train_count': len(train_set[0]), 'test_count': len(test_set[0]),
        'linear': evaluate(linear, test_set), 'mlp': evaluate(mlp, test_set),
        'linear_first_last_loss': [round(linear_history[0], 6), round(linear_history[-1], 6)],
        'mlp_first_last_loss': [round(mlp_history[0], 6), round(mlp_history[-1], 6)],
    }
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / 'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    with torch.no_grad():
        speeds = torch.tensor([[0.0], [4.0], [8.0]])
        rows = ['speed_mps,linear_m,mlp_m']
        for speed, a, b in zip(speeds, linear(speeds), mlp(speeds)):
            rows.append(f'{speed.item():.1f},{a.item():.4f},{b.item():.4f}')
    (outdir / 'predictions.csv').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return metrics


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', default='outputs')
    args = parser.parse_args()
    run(args.outdir)
