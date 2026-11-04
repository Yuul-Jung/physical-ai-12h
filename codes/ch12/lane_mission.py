"""Synthetic lane mission: no hardware output, no robot SDK."""
from pathlib import Path
import cv2
import numpy as np

W, H = 640, 360

def scene(shift=0, missing=False):
    """Generate reproducible road with two white lane markings."""
    frame = np.full((H, W, 3), (65, 65, 65), dtype=np.uint8)
    if not missing:
        cv2.line(frame, (190 + shift, 350), (290 + shift, 190), (255,255,255), 8)
        cv2.line(frame, (450 + shift, 350), (350 + shift, 190), (255,255,255), 8)
    return frame

def detect(frame):
    """Detect two lanes in a lower trapezoid; reject ambiguous geometry."""
    if frame is None or frame.shape != (H,W,3):
        return None, 'INVALID_FRAME', None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 70, 150)
    roi = np.zeros_like(edges)
    poly = np.array([[(90,359),(550,359),(400,170),(240,170)]], np.int32)
    cv2.fillPoly(roi, poly, 255)
    edges = cv2.bitwise_and(edges, roi)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, minLineLength=55, maxLineGap=30)
    if lines is None:
        return None, 'NO_LANES', edges
    left, right = [], []
    for x1,y1,x2,y2 in lines[:,0]:
        if abs(x2-x1) < 5: continue
        slope = (y2-y1)/(x2-x1)
        if not 0.5 < abs(slope) < 5: continue
        # Extrapolate to a common y=320, robustly separated by slope.
        x_at = x1 + (320-y1)/slope
        if slope < 0 and x_at < 320: left.append(x_at)
        elif slope > 0 and x_at > 320: right.append(x_at)
    if not left or not right:
        return None, 'ONE_SIDE_OR_AMBIGUOUS', edges
    center = (float(np.median(left)) + float(np.median(right))) / 2
    if not 220 < center < 420:
        return None, 'GEOMETRY_OUT_OF_RANGE', edges
    return center, 'OK', edges

def decide(center, status, distance_m, green=True):
    """Safety gate; produces a simulation label, NEVER motor commands."""
    if status != 'OK' or center is None: return 'STOP_VISION'
    # (변경) 비정상 거리는 장애물 상태가 아닌 센서 오류로 안전 정지
    if distance_m is None or not np.isfinite(distance_m) or distance_m < 0: return 'STOP_SENSOR'
    if distance_m < 0.7: return 'STOP_OBSTACLE'
    # (변경) 신호의 True가 확정된 경우만 계획 생성 허용
    if green is not True: return 'STOP_SIGNAL'
    error = center - W/2
    if abs(error) <= 12: return 'PLAN_STRAIGHT'
    return 'PLAN_RIGHT' if error > 0 else 'PLAN_LEFT'

def main(output=None):
    out = Path(output or 'outputs')
    out.mkdir(parents=True, exist_ok=True)
    for name, shift, missing, dist, green in [
        ('straight',0,False,1.5,True), ('offset',35,False,1.5,True),
        ('missing',0,True,1.5,True), ('obstacle',0,False,0.3,True),
        ('red',0,False,1.5,False)]:
        frame = scene(shift, missing)
        center, status, edges = detect(frame)
        action = decide(center,status,dist,green)
        cv2.imwrite(str(out / f'{name}.png'), frame)
        if edges is not None: cv2.imwrite(str(out / f'{name}_edges.png'), edges)
        print(f'{name}: {status}, center={center}, decision={action}')

if __name__ == '__main__': main()
