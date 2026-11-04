# 12차시 제작 검증 및 12차시 통합 감사 — 2026-11-04

## 이번 실행
- ch12 MD 14쪽 / HTML 12쪽: WeasyPrint A4 인쇄 렌더링으로 측정.
- unittest 13개 통과, 합성 장면 5종 출력 확인.
- Python 구문·로컬 상대경로·민감 문자열 점검: 12차시 자료에서 발견 ['sk-'].
- 실제 알티노 AI SDK/카메라/모터 연동: **미검증**. SDK API를 추측해 구현하지 않음.
- 제조사 SDK의 정확한 문서 및 실물 호환성: **미확인**.
- 참고: https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html ; https://docs.python.org/3/library/unittest.html

## 통합 감사 범위와 제한
- ch01~ch12 MD/HTML 존재: 아래 manifest에 기록.
- 이번 실행에서 01~11차시의 인쇄 페이지 수, 테스트, 기술 타당성을 재검증하지 않았으므로 **12차시 전체 최종 검증 완료로 판정하지 않음**.
- 통합 상대 자산 경로 누락 18건. 아래 상세 참조.
- 차시 간 링크의 실제 존재 여부는 기존 HTML 구조에 따라 추가 감사 필요.

## 누락 목록
- ch01: HTML 없음
- ch05: missing asset ../assets/svg/ch05_pipeline.svg
- ch06: missing asset ../assets/css/ch06.css
- ch06: missing asset ../assets/svg/ch06_pipeline.svg
- ch06: missing asset ../assets/data/ch06/scene.png
- ch06: missing asset ../assets/data/ch06/roi.png
- ch06: missing asset ../assets/data/ch06/yellow_mask.png
- ch06: missing asset ../assets/data/ch06/contours.png
- ch07: missing asset ../assets/css/ch07.css
- ch08: missing asset ../assets/svg/ch08_pipeline.svg
- ch09: missing asset ../assets/svg/ch09_pipeline.svg
- ch09: missing asset ../codes/ch09/output/scene.png
- ch09: missing asset ../codes/ch09/output/detections.png
- ch10: missing asset ../assets/ch10.css
- ch10: missing asset ../assets/svg/ch10_pipeline.svg
- ch10: missing asset ../codes/ch10/outputs/scene.png
- ch10: missing asset ../codes/ch10/outputs/instances.png
- ch11: missing asset ../assets/svg/ch11_pipeline.svg
