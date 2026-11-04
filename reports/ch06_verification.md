# 06차시 기술·적대적 검증 보고서

- 주제: OpenCV 관심 영역, 도형, 문자, 색 마스크, 윤곽선
- Python 실행: OpenCV 4.13.0 / NumPy 2.3.5
- 자동 테스트: 15개 통과 (`python -m unittest -v test_opencv_vision_lab.py`)
- 출력 확인: 360×640×3 원본, 180×640×3 ROI, 윤곽선 2개, PNG 4개 저장
- Markdown A4 인쇄: 17페이지 (Pandoc HTML 변환 → WeasyPrint PDF)
- HTML A4 인쇄: 17페이지 (WeasyPrint PDF)
- 기술 검증: BGR/HSV, ROI 배열 인덱싱, 마스크 자료형, findContours 반환값, 윤곽선 면적 및 경계 상자 코드 점검
- 적대적 검증: 제조사 전용 API를 사용하지 않음. 차선 검출과 색상 연결영역 검출을 구분. 조명 민감도와 ROI 누락 위험 표기. GUI 없는 환경에서 PNG 저장 방식 사용.
- 미검증: 알티노 AI SDK, 실제 카메라 영상 수집, 실제 로봇 주행, 현장 조명 성능.
- 출처: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html / https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html / https://numpy.org/doc/stable/user/basics.indexing.html
- 보안: 생성한 교재·코드의 계정/토큰 문자열 검색 및 상대경로 링크 확인. 실제 장비 화면 캡처 없음.
- 판정: 교육용 합성 데이터 기반 PASS; 실물 장비 연동 UNVERIFIED.
