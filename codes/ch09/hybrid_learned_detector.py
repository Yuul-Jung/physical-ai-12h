"""09차시 선택 심화: 결정적 후보 박스 + PyTorch 학습형 색상 클래스 분류.
실제 객체 검출 신경망/YOLO가 아니며, 알티노 AI 제어 명령이 없다.
"""
import json
from pathlib import Path
import cv2
import numpy as np
import torch
from torch import nn
from object_detection_lab import make_scene, iou

NAMES = ('background', 'red', 'green', 'blue')


class PatchClassifier(nn.Module):
    """평균 BGR 세 수치를 입력받아 4개 클래스의 logit을 예측."""
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(nn.Linear(3, 16), nn.ReLU(), nn.Linear(16, 4))

    def forward(self, x):
        return self.network(x)


def make_training_set(seed=29, samples_per_class=80):
    """학습용 합성 BGR 특징. 고정 시연 장면과 별도로 생성한다."""
    rng = np.random.default_rng(seed)
    x, y = [], []
    for label in range(4):
        for _ in range(samples_per_class):
            feature = rng.uniform(0.05, 0.25, size=3)
            if label:
                feature[[2, 1, 0][label-1]] = rng.uniform(0.68, 1.0)  # BGR 우세 채널
            x.append(feature.astype('float32'))
            y.append(label)
    idx = rng.permutation(len(y))
    return torch.tensor(np.array(x)[idx]), torch.tensor(np.array(y, dtype='int64')[idx])


def train_model(epochs=120):
    """고정 난수와 독립 생성 평가 데이터 사용. GPU/인터넷 불필요."""
    torch.manual_seed(29)
    model = PatchClassifier()
    x, y = make_training_set(29)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.06)
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = nn.functional.cross_entropy(model(x), y)
        loss.backward()
        optimizer.step()
    model.eval()
    vx, vy = make_training_set(301, samples_per_class=20)
    with torch.no_grad():
        accuracy = (model(vx).argmax(dim=1) == vy).float().mean().item()
    return model, accuracy


def detect_hybrid(image, model, min_area=200):
    """밝기 마스크로 후보 박스, 학습 모델로 후보 색상 클래스를 추정한다."""
    if image is None or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError('BGR 이미지가 필요합니다')
    foreground = (np.max(image, axis=2) > 150).astype('uint8')
    n, ids, stats, _ = cv2.connectedComponentsWithStats(foreground, 8)
    boxes = []
    with torch.no_grad():
        for k in range(1, n):
            left, top, width, height, area = [int(v) for v in stats[k]]
            if area < min_area:
                continue
            patch = image[top:top+height, left:left+width]
            mask = ids[top:top+height, left:left+width] == k
            feature = patch[mask].astype('float32').mean(axis=0) / 255.0
            probs = model(torch.tensor(feature)[None]).softmax(dim=1)[0]
            label = int(probs.argmax())
            if label != 0:
                boxes.append({'label': NAMES[label],
                              'box': [left, top, left+width, top+height],
                              'score': float(probs[label])})
    return sorted(boxes, key=lambda box: box['box'][0])


def run_demo():
    model, validation_acc = train_model()
    image, truth = make_scene()
    predictions = detect_hybrid(image, model)
    print('독립 합성 특징 검증 정확도:', f'{validation_acc:.1%}')
    print('학습형 클래스 분류가 결합된 후보:', [(d['label'],d['box']) for d in predictions])
    output = {'validation_accuracy': validation_acc,
              'predictions': predictions, 'ground_truth': truth}
    path = Path(__file__).parent/'output'/'hybrid_result.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    return output


if __name__ == '__main__':
    run_demo()
