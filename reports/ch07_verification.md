# 07차시 기술·적대적 검증 보고서

- 작성일: 2026-11-04
- 대상: `chapters/ch07.md`, `chapters/ch07.html`, `codes/ch07/deep_learning_lab.py`
- MD A4 인쇄: **12쪽** (Pandoc HTML 변환 후 WeasyPrint A4 인쇄)
- HTML A4 인쇄: **12쪽** (WeasyPrint)
- 자동 테스트: **8개 통과** (`unittest`)
- Python 구문 검사: 통과 (`py_compile`)
- 실행: PyTorch CPU / NumPy 합성 데이터 160개, 학습 128개, 평가 32개
- 선형회귀 평가: MAE 0.01876m, MSE 0.000535m²
- MLP 평가: MAE 0.01893m, MSE 0.000538m²
- 결과 파일: `codes/ch07/outputs/metrics.json`, `predictions.csv`
- 도식: `assets/svg/ch07_learning.svg` 생성 및 HTML에 인라인 포함
- HTML 목차·상대경로: 앞 차시 링크는 존재, 다음 08차시 링크는 후속 제작 전이므로 미완성
- 적대적 검증: 교육용 선형 거리식을 실차 제동거리로 사용하지 않도록 경고; 선형 문제에서 MLP 우월 주장 금지; 평가 데이터 누출·외삽·단위 혼용 주의 반영.
- **미검증:** 제조사 알티노 AI SDK, Jetson 실행, 실물 카메라/라이다, 실차 제어 및 안전 성능.
- 개인정보: 공개 문서에 사용자명·토큰·비밀번호·로컬 홈 경로 없음(텍스트 패턴 점검).
- 결론: **교재/CPU 실습 검증 완료, 하드웨어 미검증**. 다음 차시 연결은 ch08 제작 후 재검증.
