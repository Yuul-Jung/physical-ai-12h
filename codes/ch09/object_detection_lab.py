"""교육용 합성 이미지의 색상 기반 객체 검출. 실제 로봇 제어 없음."""
from pathlib import Path
import json
import cv2
import numpy as np

LABELS = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0)}


def make_scene():
    """BGR 320x480 영상과 정답 바운딩 박스를 만든다."""
    image = np.full((320, 480, 3), 32, dtype=np.uint8)
    objects = [('red', (45, 60, 125, 145)), ('green', (190, 80, 275, 160)),
               ('blue', (325, 190, 435, 285))]
    for name, (x1, y1, x2, y2) in objects:
        cv2.rectangle(image, (x1, y1), (x2-1, y2-1), LABELS[name], -1)
    return image, [{'label': n, 'box': list(b)} for n, b in objects]


def detect_colors(image, min_area=200):
    """색상별 마스크→연결영역→좌표를 반환한다. AI 모델이 아님."""
    if image is None or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError('BGR 3채널 이미지가 필요합니다')
    found = []
    for label, bgr in LABELS.items():
        color = np.array(bgr, dtype=np.int16)
        delta = np.abs(image.astype(np.int16) - color)
        mask = (np.max(delta, axis=2) <= 12).astype(np.uint8)
        count, _, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        for i in range(1, count):
            x, y, w, h, area = [int(v) for v in stats[i]]
            if area >= min_area:
                found.append({'label': label, 'box': [x, y, x+w, y+h],
                              'area': area, 'score': None})
    return sorted(found, key=lambda d: d['box'][0])


def iou(a, b):
    """두 XYXY 박스의 Intersection over Union 계산."""
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2-x1) * max(0, y2-y1)
    area_a = max(0, a[2]-a[0]) * max(0, a[3]-a[1])
    area_b = max(0, b[2]-b[0]) * max(0, b[3]-b[1])
    union = area_a + area_b - inter
    return inter / union if union else 0.0


def evaluate(predictions, ground_truth, threshold=0.5):
    """동일 클래스, IoU 임계값 기준 일대일 매칭."""
    matched = set()
    tp = 0
    for pred in predictions:
        candidates = [(iou(pred['box'], gt['box']), j) for j, gt in enumerate(ground_truth)
                      if j not in matched and pred['label'] == gt['label']]
        if candidates:
            overlap, idx = max(candidates)
            if overlap >= threshold:
                matched.add(idx)
                tp += 1
    fp = len(predictions)-tp
    fn = len(ground_truth)-tp
    return {'TP': tp, 'FP': fp, 'FN': fn,
            'precision': tp/(tp+fp) if tp+fp else 0.0,
            'recall': tp/(tp+fn) if tp+fn else 0.0}


def annotate(image, detections):
    result = image.copy()
    for obj in detections:
        x1, y1, x2, y2 = obj['box']
        cv2.rectangle(result, (x1, y1), (x2-1, y2-1), (255, 255, 255), 2)
        cv2.putText(result, obj['label'], (x1, max(20, y1-8)),
                    cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255), 2)
    return result


def main():
    out = Path(__file__).resolve().parent / 'output'
    out.mkdir(exist_ok=True)
    image, truth = make_scene()
    predictions = detect_colors(image)
    metrics = evaluate(predictions, truth)
    cv2.imwrite(str(out/'scene.png'), image)
    cv2.imwrite(str(out/'detections.png'), annotate(image, predictions))
    (out/'results.json').write_text(json.dumps({'predictions': predictions,
          'truth': truth, 'metrics': metrics}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(metrics, ensure_ascii=False))


if __name__ == '__main__':
    main()
