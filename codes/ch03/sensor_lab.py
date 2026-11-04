"""03차시: 실제 로봇 제어가 없는 카메라·라이다 학습용 예제."""
from dataclasses import dataclass
from math import cos, sin, isfinite, radians
from pathlib import Path
import argparse
import csv

@dataclass(frozen=True)
class Scan:
    angle_min_deg: float
    angle_step_deg: float
    ranges_m: tuple[float, ...]
    min_m: float = 0.05
    max_m: float = 8.0

    def points(self):
        """유효한 측정값을 (각도, 거리, x, y)로 반환."""
        if (not all(isfinite(v) for v in (self.angle_min_deg, self.angle_step_deg, self.min_m, self.max_m))
                or self.angle_step_deg <= 0 or self.min_m <= 0 or self.max_m <= self.min_m):
            raise ValueError('스캔 메타데이터가 올바르지 않습니다')
        for i, distance in enumerate(self.ranges_m):
            if not isfinite(distance) or not self.min_m <= distance <= self.max_m:
                continue
            angle = self.angle_min_deg + i * self.angle_step_deg
            theta = radians(angle)
            yield (angle, distance, distance * cos(theta), distance * sin(theta))

    def nearest_front(self, half_angle_deg=20):
        """전방 부채꼴 유효 거리의 최솟값. 유효 측정이 없으면 None."""
        if not isfinite(half_angle_deg) or not 0 <= half_angle_deg <= 180:
            raise ValueError('전방 각도 범위 오류')
        # (변경) 350도와 -10도를 동일한 전방 방향으로 취급
        front = [d for a, d, _, _ in self.points()
                 if abs((a + 180) % 360 - 180) <= half_angle_deg]
        return min(front) if front else None


def sample_scan():
    """-90°부터 +90°까지 10° 간격의 모의 스캔."""
    values = [2.8] * 19
    values[8], values[9], values[10] = 0.9, 0.6, 0.8
    values[2], values[17] = float('inf'), float('nan')
    return Scan(-90, 10, tuple(values))


def save_scan_csv(scan, path):
    """좌표 변환 결과를 CSV로 기록."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['angle_deg', 'range_m', 'x_m', 'y_m'])
        for row in scan.points():
            writer.writerow([f'{v:.4f}' for v in row])
    return path


def create_demo_frame(path, width=640, height=360):
    """카메라 없이 생성 가능한 테스트 영상 한 장."""
    import cv2
    import numpy as np
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (40, 40, 40)  # OpenCV BGR 순서
    cv2.rectangle(image, (100, 90), (260, 260), (0, 180, 255), -1)
    cv2.circle(image, (440, 170), 75, (50, 220, 50), -1)
    cv2.putText(image, 'CAMERA DEMO', (120, 45), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise OSError('이미지 저장 실패')
    return path, image.shape


def capture_one_frame(source, path):
    """실제 연결된 일반 카메라 또는 영상 파일에서 한 프레임 저장."""
    import cv2
    source = int(source) if str(source).isdigit() else source
    cap = cv2.VideoCapture(source)
    try:
        if not cap.isOpened():
            raise RuntimeError('영상 입력을 열 수 없습니다')
        ok, frame = cap.read()
        if not ok or frame is None:
            raise RuntimeError('프레임을 읽을 수 없습니다')
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(path), frame):
            raise OSError('프레임 저장 실패')
        return path, frame.shape
    finally:
        cap.release()


def main():
    parser = argparse.ArgumentParser(description='03차시 카메라·라이다 데이터 실습')
    parser.add_argument('--out', default='outputs/ch03')
    parser.add_argument('--camera', help='실제 카메라 번호(0) 또는 영상 파일 경로')
    args = parser.parse_args()
    out = Path(args.out)
    scan = sample_scan()
    print('전방 최소 유효 거리(m):', scan.nearest_front())
    print('유효 라이다 점 수:', len(list(scan.points())))
    print('라이다 CSV:', save_scan_csv(scan, out / 'scan.csv'))
    if args.camera is None:
        path, shape = create_demo_frame(out / 'demo_camera.png')
    else:
        path, shape = capture_one_frame(args.camera, out / 'camera_frame.png')
    print('카메라 이미지:', path, '배열 형상:', shape)

if __name__ == '__main__':
    main()
