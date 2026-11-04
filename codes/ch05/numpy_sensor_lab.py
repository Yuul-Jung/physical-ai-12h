"""05차시: 모의 센서 데이터 NumPy 분석. 실제 로봇 연결은 수행하지 않는다."""
import numpy as np


def clean_ranges(values, min_m=0.05, max_m=4.0):
    """NaN, inf, 측정 범위 밖 값은 NaN으로 통일한다."""
    data = np.asarray(values, dtype=np.float64).copy()
    valid = np.isfinite(data) & (data >= min_m) & (data <= max_m)
    data[~valid] = np.nan
    return data


def front_sector_min(angles_deg, ranges_m, half_width=25):
    """전방 0도 기준 ±half_width 내 유효 거리의 최소값을 반환한다."""
    angles = np.asarray(angles_deg, dtype=float)
    distances = clean_ranges(ranges_m)
    if angles.shape != distances.shape:
        raise ValueError('각도와 거리 배열의 크기가 다릅니다.')
    wrapped = (angles + 180) % 360 - 180
    mask = (np.abs(wrapped) <= half_width) & np.isfinite(distances)
    return float(np.min(distances[mask])) if np.any(mask) else None


def obstacle_decision(distance_m, stop_m=0.45, slow_m=1.0):
    """결측 시 안전 정지, 가까운 장애물 시 정지, 그 외 감속/진행."""
    # (변경) 음수 거리·잘못된 임계값은 장애물 감지가 아닌 측정/설정 오류
    if not (np.isfinite(stop_m) and np.isfinite(slow_m) and 0 < stop_m <= slow_m):
        raise ValueError('invalid distance thresholds')
    if distance_m is None or not np.isfinite(distance_m) or distance_m < 0:
        return 'STOP_SENSOR_INVALID'
    if distance_m < stop_m:
        return 'STOP_OBSTACLE'
    if distance_m < slow_m:
        return 'SLOW'
    return 'GO'


def moving_average(values, window=3):
    """1차원 데이터의 유효 값만 평균; 빈 구간은 NaN으로 둔다."""
    if window < 1:
        raise ValueError('window는 1 이상이어야 합니다.')
    arr = clean_ranges(values)
    out = np.empty(arr.size, dtype=float)
    for i in range(arr.size):
        segment = arr[max(0, i-window+1):i+1]
        valid = segment[np.isfinite(segment)]
        out[i] = np.mean(valid) if valid.size else np.nan
    return out


def image_roi_mean(image, x1, y1, x2, y2):
    """H×W×3 영상에서 관심영역 RGB 채널별 평균을 계산한다."""
    img = np.asarray(image)
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError('영상 형식은 H×W×3이어야 합니다.')
    h, w, _ = img.shape
    if not (0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
        raise ValueError('관심영역 좌표가 잘못되었습니다.')
    return img[y1:y2, x1:x2].mean(axis=(0, 1))


def run_demo():
    angles = np.array([-60, -30, -15, 0, 15, 30, 60])
    ranges = np.array([2.0, 1.5, 0.8, 0.4, np.nan, 1.2, np.inf])
    cleaned = clean_ranges(ranges)
    front = front_sector_min(angles, ranges)
    print('유효 측정:', np.isfinite(cleaned).sum(), '/', cleaned.size)
    print('전방 최소거리(m):', front)
    print('판단:', obstacle_decision(front))
    print('이동평균:', np.round(moving_average(ranges), 2))
    image = np.zeros((6, 8, 3), dtype=np.uint8)
    image[2:5, 3:7] = [200, 40, 20]
    print('ROI RGB 평균:', image_roi_mean(image, 3, 2, 7, 5))


if __name__ == '__main__':
    run_demo()
