"""교육용 합성 교통 표지 인식: 실차 제어 API가 아닙니다."""
from dataclasses import dataclass
import cv2
import numpy as np

@dataclass(frozen=True)
class Observation:
    signal: str
    arrow: str
    parking: bool
    confidence: float

def make_scene(signal='red', arrow='left', parking=True):
    """재현 가능한 합성 장면과 정답을 생성합니다."""
    assert signal in ('red', 'yellow', 'green', 'off')
    assert arrow in ('left', 'right', 'none')
    img = np.full((360, 640, 3), (230, 230, 230), np.uint8)
    cv2.rectangle(img, (45, 30), (155, 225), (35, 35, 35), -1)
    positions = {'red': (100, 75), 'yellow': (100, 125), 'green': (100, 175)}
    colors = {'red': (0, 0, 255), 'yellow': (0, 255, 255), 'green': (0, 255, 0)}
    for key, pos in positions.items():
        cv2.circle(img, pos, 23, colors[key] if signal == key else (75, 75, 75), -1)
    cv2.rectangle(img, (240, 45), (400, 165), (40, 40, 40), -1)
    if arrow != 'none':
        if arrow == 'left':
            pts = np.array([[265, 105], [310, 65], [310, 90], [375, 90], [375, 120], [310, 120], [310, 145]])
        else:
            pts = np.array([[375, 105], [330, 65], [330, 90], [265, 90], [265, 120], [330, 120], [330, 145]])
        cv2.fillPoly(img, [pts], (255, 255, 255))
    if parking:
        cv2.rectangle(img, (460, 200), (600, 335), (255, 0, 0), -1)
        cv2.putText(img, 'P', (490, 305), cv2.FONT_HERSHEY_SIMPLEX, 2.8, (255, 255, 255), 7)
    return img

def recognize(img):
    """고정 ROI의 색상/형태 규칙. 학습형 객체 검출기가 아닙니다."""
    if img is None or img.shape != (360, 640, 3):
        return Observation('unknown', 'unknown', False, 0.0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    signal_scores = {}
    for name, (x, y) in {'red': (100, 75), 'yellow': (100, 125), 'green': (100, 175)}.items():
        b, g, r = [int(v) for v in img[y, x]]
        signal_scores[name] = (r > 180 and r > g * 1.5) if name == 'red' else ((r > 180 and g > 180 and b < 100) if name == 'yellow' else (g > 180 and g > r * 1.5))
    active = [name for name, yes in signal_scores.items() if yes]
    signal = active[0] if len(active) == 1 else 'unknown'
    # 화살표의 좌우 끝 영역 흰 픽셀 면적을 비교하여 방향 판정
    mask = cv2.inRange(img[60:155, 255:390], (220, 220, 220), (255, 255, 255))
    left = bool(mask[20, 45])  # 좌측 화살촉 위치 (원본 x=265, y=105)
    right = bool(mask[20, 90])  # 우측 화살촉 위치 (원본 x=375, y=105)
    arrow = 'left' if left and not right else 'right' if right and not left else 'unknown'
    blue = img[210:330, 470:590]
    parking = bool(np.count_nonzero((blue[:, :, 0] > 180) & (blue[:, :, 1] < 100)) > 500)
    return Observation(signal, arrow, parking, 1.0 if signal != 'unknown' and arrow != 'unknown' else 0.0)

def decide(obs, distance_m):
    """실차 명령이 아닌 모의 상태 출력. 불확실하면 정지."""
    if distance_m is None or not np.isfinite(distance_m) or distance_m < 0.0:
        return 'STOP_SENSOR_ERROR'
    if distance_m < 0.5:
        return 'STOP_OBSTACLE'
    # (변경) 허용 목록 외의 모든 신호, 비정상 확신도는 무조건 정지
    if obs.signal != 'green' or not np.isfinite(obs.confidence) or obs.confidence < 0.8:
        return 'STOP_SIGNAL_UNCERTAIN'
    if obs.arrow not in ('left', 'right'):
        return 'STOP_ARROW_UNCERTAIN'
    return 'PLAN_' + obs.arrow.upper() + ('_PARKING_VISIBLE' if obs.parking else '')

def main():
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='outputs')
    args = p.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    for s, a in [('red', 'left'), ('yellow', 'right'), ('green', 'left'), ('green', 'right')]:
        frame = make_scene(s, a)
        obs = recognize(frame)
        cv2.imwrite(str(out / f'{s}_{a}.png'), frame)
        print(s, a, obs, decide(obs, 1.2))
if __name__ == '__main__':
    main()
