"""06차시: 합성 영상 기반 OpenCV 영상처리 실습. 카메라·로봇 API 사용 없음."""
from pathlib import Path
import argparse
import cv2
import numpy as np


def make_scene(width=640, height=360):
    """BGR 영상에 관심 영역, 노란 도형, 빨간 표지판을 생성한다."""
    if width < 100 or height < 100:
        raise ValueError('영상 크기는 가로·세로 각각 100 이상이어야 합니다.')
    image = np.full((height, width, 3), (40, 40, 40), dtype=np.uint8)
    cv2.rectangle(image, (0, height // 2), (width - 1, height - 1), (65, 65, 65), -1)
    cv2.line(image, (width // 3, height - 1), (width // 2 - 40, height // 2), (0, 220, 220), 8)
    cv2.line(image, (width * 2 // 3, height - 1), (width // 2 + 40, height // 2), (0, 220, 220), 8)
    cv2.rectangle(image, (width // 2 - 35, height // 2 + 30), (width // 2 + 35, height // 2 + 95), (0, 0, 255), -1)
    return image


def extract_roi(image, x, y, width, height):
    """배열의 [y:y+h, x:x+w] 영역을 복사한다. 영상 경계를 검사한다."""
    if image is None or image.ndim not in (2, 3):
        raise ValueError('2차원 또는 3차원 영상 배열이 필요합니다.')
    ih, iw = image.shape[:2]
    if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > iw or y + height > ih:
        raise ValueError('관심 영역이 영상 범위를 벗어났습니다.')
    return image[y:y + height, x:x + width].copy()


def color_mask_bgr(image):
    """BGR을 HSV로 변환하고 노란색 영역을 이진 마스크로 분리한다."""
    if image is None or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError('3채널 BGR 영상이 필요합니다.')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([18, 80, 80], dtype=np.uint8)
    upper = np.array([38, 255, 255], dtype=np.uint8)
    return cv2.inRange(hsv, lower, upper)


def contours_from_mask(mask, min_area=80.0):
    """외곽 윤곽선을 찾고 면적이 작은 잡음을 제외한다."""
    if mask is None or mask.ndim != 2 or mask.dtype != np.uint8:
        raise ValueError('uint8 단일 채널 마스크가 필요합니다.')
    if min_area < 0:
        raise ValueError('최소 면적은 0 이상이어야 합니다.')
    found, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return sorted((c for c in found if cv2.contourArea(c) >= min_area),
                  key=cv2.contourArea, reverse=True)


def annotate(image, contours):
    """윤곽선, 경계 사각형, 영어 안내 문자를 원본의 복사본에 표시한다."""
    output = image.copy()
    cv2.drawContours(output, contours, -1, (255, 255, 0), 2)
    for index, contour in enumerate(contours, start=1):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(output, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.putText(output, f'ROI {index}', (x, max(18, y - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return output


def run(out_dir):
    """GUI 없이 결과 PNG를 저장하므로 서버·원격 터미널에서도 실행 가능하다."""
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    frame = make_scene()
    roi = extract_roi(frame, 0, 180, 640, 180)
    mask = color_mask_bgr(roi)
    contours = contours_from_mask(mask)
    overlay = annotate(roi, contours)
    outputs = {'scene.png': frame, 'roi.png': roi,
               'yellow_mask.png': mask, 'contours.png': overlay}
    for name, image in outputs.items():
        if not cv2.imwrite(str(target / name), image):
            raise OSError(f'이미지 저장 실패: {name}')
    print(f'frame={frame.shape}, roi={roi.shape}, contours={len(contours)}')
    print('saved=' + ', '.join(outputs))
    return len(contours)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='06차시 OpenCV 영상처리 실습')
    parser.add_argument('--out', default='outputs', help='결과 이미지 저장 폴더')
    args = parser.parse_args()
    run(args.out)
