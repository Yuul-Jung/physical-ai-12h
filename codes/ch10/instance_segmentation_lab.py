"""교육용 합성 객체 인스턴스 분할: 학습된 AI 모델이 아님."""
import json
from pathlib import Path
import cv2
import numpy as np

COLORS = {'red': (0, 0, 220), 'green': (0, 180, 0), 'blue': (220, 0, 0)}


def make_scene():
    """분리된 원형 객체 4개와 참조 마스크를 생성한다."""
    img = np.full((320, 480, 3), 235, dtype=np.uint8)
    objects = [('red', (85, 100), 34), ('red', (195, 100), 28),
               ('green', (315, 95), 38), ('blue', (260, 235), 42)]
    masks = []
    for name, center, radius in objects:
        mask = np.zeros(img.shape[:2], np.uint8)
        cv2.circle(mask, center, radius, 255, -1)
        cv2.circle(img, center, radius, COLORS[name], -1)
        masks.append({'label': name, 'mask': mask})
    return img, masks


def segment_instances(image, min_area=100):
    """색상별 이진 마스크에서 연결된 객체를 개별 인스턴스로 분리한다."""
    if image is None or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError('BGR 3채널 영상이 필요합니다')
    if min_area < 1:
        raise ValueError('min_area는 1 이상이어야 합니다')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ranges = {
        'red': [((0, 100, 80), (10, 255, 255)), ((170, 100, 80), (179, 255, 255))],
        'green': [((35, 80, 60), (85, 255, 255))],
        'blue': [((95, 80, 60), (135, 255, 255))]
    }
    found = []
    for label, bands in ranges.items():
        binary = np.zeros(image.shape[:2], dtype=np.uint8)
        for lo, hi in bands:
            binary = cv2.bitwise_or(binary, cv2.inRange(hsv, np.array(lo), np.array(hi)))
        n, ids, stats, _ = cv2.connectedComponentsWithStats(binary, 8)
        for i in range(1, n):
            x, y, w, h, area = map(int, stats[i])
            if area < min_area:
                continue
            found.append({'label': label, 'box': [x, y, x+w, y+h],
                          'area': area, 'mask': (ids == i).astype(np.uint8)})
    return sorted(found, key=lambda item: (item['label'], item['box'][0]))


def mask_iou(a, b):
    """픽셀 단위 IoU. 공집합 두 개의 IoU는 0으로 정의한다."""
    a, b = np.asarray(a, dtype=bool), np.asarray(b, dtype=bool)
    if a.shape != b.shape:
        raise ValueError('마스크 크기가 서로 다릅니다')
    union = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / union) if union else 0.0


def evaluate(predictions, truth, threshold=0.5):
    """클래스 일치 + mask IoU 임계값으로 일대일 매칭한다."""
    candidates = []
    for p, pred in enumerate(predictions):
        for t, gt in enumerate(truth):
            if pred['label'] == gt['label']:
                score = mask_iou(pred['mask'], gt['mask'])
                if score >= threshold:
                    candidates.append((score, p, t))
    matched_p, matched_t = set(), set()
    for _, p, t in sorted(candidates, reverse=True):
        if p not in matched_p and t not in matched_t:
            matched_p.add(p)
            matched_t.add(t)
    tp = len(matched_p)
    fp = len(predictions) - tp
    fn = len(truth) - tp
    return {'tp': tp, 'fp': fp, 'fn': fn,
            'precision': tp / (tp + fp) if tp + fp else 0.0,
            'recall': tp / (tp + fn) if tp + fn else 0.0}


def visualize(image, instances):
    overlay = image.copy()
    for i, item in enumerate(instances, 1):
        color = COLORS[item['label']]
        mask = item['mask'].astype(bool)
        overlay[mask] = (0.4 * overlay[mask] + 0.6 * np.array(color)).astype(np.uint8)
        x1, y1, x2, y2 = item['box']
        cv2.rectangle(overlay, (x1, y1), (x2-1, y2-1), color, 2)
        cv2.putText(overlay, f"{i}:{item['label']}", (x1, max(16, y1-6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 20, 20), 2)
    return overlay


def main(output_dir='outputs'):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    image, truth = make_scene()
    pred = segment_instances(image)
    report = evaluate(pred, truth)
    report['count'] = len(pred)
    report['objects'] = [{'label': p['label'], 'box': p['box'], 'area': p['area']}
                         for p in pred]
    cv2.imwrite(str(folder / 'scene.png'), image)
    cv2.imwrite(str(folder / 'instances.png'), visualize(image, pred))
    for i, item in enumerate(pred, 1):
        cv2.imwrite(str(folder / f'mask_{i:02d}.png'), item['mask'] * 255)
    (folder / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == '__main__':
    main()
