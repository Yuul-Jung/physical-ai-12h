# 03차시 기술·적대적 검증 보고서

- 제작 범위: 카메라 프레임 데이터, 모의 라이다 스캔, 유효성 필터, 극좌표 변환, 전방 거리, CSV/PNG 저장.
- 실행: `python -m unittest -v test_sensor_lab` → **9개 통과**; `python sensor_lab.py --out ...` → 전방 0.6m, 유효 점 17개, PNG 360×640×3 생성.
- HTML 인쇄: WeasyPrint A4 **16쪽** (`reports/ch03.pdf`).
- Markdown 인쇄: Markdown 원문을 HTML로 변환 후 동일한 A4 CSS로 인쇄 **10쪽** (`reports/ch03_md_print.pdf`).
- 내용 일치: 같은 12개 주제와 원본 전체 Python 코드를 HTML·Markdown 양쪽에 포함.
- 오류/보완: OpenCV는 BGR 채널 순서, ROS LaserScan 각도는 라디안, 교재 Scan은 도 단위라는 차이를 명시. `None`을 장애물 없음으로 오인하지 않도록 명시.
- 실제 알티노 AI 센서 모델, SDK/API, 장치 연결, 타임스탬프, 카메라 인덱스, 라이다 드라이버: **미검증**.
- 안전: 실제 로봇 구동 코드 없음. 테스트 통과는 실물 하드웨어 검증이 아님.
- 출처: https://opencv.org/reading-and-writing-videos-using-opencv/ ; https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs/msg/LaserScan.msg ; https://docs.python.org/3/library/math.html ; https://shop.saeon.co.kr/
- 확인 범위: 코드 실행 및 PDF 렌더링. 수동 GUI 시각 점검은 수행하지 않음.
- 01~02차시 파일은 존재하나 이번 실행에서 해당 차시의 품질을 재검증하지 않았음.
