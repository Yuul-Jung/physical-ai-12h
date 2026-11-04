# 04차시 기술·적대적 검증 보고서

- 대상: Python 변수·제어문·반복문·함수·라이브러리, 60분 필수 실습 + 선택 심화
- MD 인쇄 검증: Markdown을 HTML로 변환 후 A4 PDF로 렌더링, **14쪽**.
- HTML 인쇄 검증: HTML A4 PDF 렌더링, **14쪽**.
- HTML 구성: 주요 절 12개, SVG 1개, 코드 블록 11개.
- 코드 검증: `python -m unittest discover -s codes/ch04 -v` → **12/12 통과**.
- 구문 검증: `python -m compileall -q codes/ch04` → 통과.
- 실행 출력: 1.8m→35%, 0.8m→20%, 0.3m→정지, None→정지.
- 경계 테스트: 0.5m는 감속, 1.0m는 정상 속도(교육용 정책).
- 기술 검토: 센서 값 없음/음수/NaN/무한대/잘못된 방향은 정지하도록 설계.
- 문서 링크: 03차시 및 목차 링크 유효; 05차시는 아직 미생성으로 링크를 비활성화.
- 공개 검토: 제조사 비공개 API, 계정, 토큰, 사용자 절대 경로를 본문에 포함하지 않음.
- **미검증**: 실제 알티노 AI SDK, 카메라·라이다, 모터 제어, 주행 안전성. 표준 Python 모의 코드 테스트는 실제 로봇 안전성을 보증하지 않음.
- 참고: https://docs.python.org/3/tutorial/ , https://docs.python.org/3/library/unittest.html , https://docs.python.org/3/library/venv.html
- 검증 제한: PDF는 자동 렌더링 및 페이지 수를 확인했으나 실제 종이 인쇄나 장비 시연은 하지 않음.
